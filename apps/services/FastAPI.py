import os
os.environ['IN_PROD'] = 'True'

import packages
import time
import asyncio
import httpx
from loguru import logger
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from starlette.background import BackgroundTask
from fastapi.middleware.cors import CORSMiddleware
import tempfile

import toolkit.utils.speech as utils_speech
from toolkit.utils import utils

import features.rag.apis as apis_rag
import features.speech.apis as apis_speech
import features.agents.car.apis as apis_car
import dev.frameworks.LlamaIndex.workflows.apis as apis_wf
from configs import components

app = FastAPI()

# Add CORS middleware with all origins allowed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=False,  # Must be False when allow_origins=["*"]
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/transcribe/")
@utils.timed_api
async def transcribe_audio(file: UploadFile = File(...)):
    logger.info(f"Received transcription request for file: {file.filename}")
    
    # Reset file pointer to the beginning
    await file.seek(0)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name
    
    try:
        # Get whisper.cpp service port
        whisper_port = int(os.getenv("PORT_SVC_STT_WHISPER_CPP", 8769))
        whisper_url = f"http://localhost:{whisper_port}/transcribe/"
        
        # Prepare the file for upload
        files = {
            'audio_file': (file.filename, open(temp_file_path, 'rb'), file.content_type)
        }
        params = {'return_timing': 'true'}
        
        # Make request to whisper.cpp service
        logger.info(f"Sending request to whisper.cpp service at port {whisper_port}")
        async with httpx.AsyncClient() as client:
            response = await client.post(whisper_url, files=files, params=params)
            response.raise_for_status()
            result = response.json()
        
        if "error" in result:
            logger.warning(f"Transcription service returned error: {result['error']}")
            return JSONResponse(
                content={"error": result['error']},
                status_code=400
            )
        
        # Format response to match existing API
        response_content = {
            "transcribed_text": result["transcription"],
            "preprocessing_time": float(result.get("preprocessing_time", "0").rstrip('s')),
            "transcription_time": float(result.get("transcription_time", "0").rstrip('s')),
        }
        
        logger.info(f"Final transcription result: {result['transcription']}")
        logger.info("Audio transcription process completed")
        return JSONResponse(content=response_content)
        
    except httpx.HTTPError as e:
        logger.error(f"HTTP error when calling whisper service: {str(e)}")
        return JSONResponse(
            content={"error": f"Whisper service error: {str(e)}"}, 
            status_code=500
        )
    except Exception as e:
        logger.error(f"Error transcribing audio: {str(e)}")
        return JSONResponse(
            content={"error": str(e)}, 
            status_code=500
        )
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)
        logger.info(f"Temporary file removed")
        
@app.post("/text_to_speech/")
async def text_to_speech(text: str = Form(...)):
    logger.info(f"Received text-to-speech request")
    
    try:
        # Generate a temporary file path for the output audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            output_audio_path = temp_file.name
        
        logger.info(f"Temporary file will be created at: {output_audio_path}")

        # Convert the text to speech
        logger.info("Starting text-to-speech conversion")
        tts_start = time.time()
        tts_success = apis_speech.text_to_speech(text, output_audio_path)
        tts_time = time.time() - tts_start
        logger.info(f"Text-to-speech conversion completed in {tts_time:.2f} seconds")

        if tts_success:
            logger.info("Text-to-speech conversion completed successfully")
            return FileResponse(
                output_audio_path, 
                media_type="audio/wav", 
                filename="response.wav",
                background=BackgroundTask(lambda: os.unlink(output_audio_path))
            )
        else:
            logger.error("Text-to-speech conversion failed")
            return JSONResponse(content={"error": "Text-to-speech conversion failed"}, status_code=500)

    except Exception as e:
        logger.error(f"Error in text-to-speech conversion: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/query/")
async def query(query: str = "Could you provide some tips or notes to consider before driving a car?"):
    async def generate():
        async for token in await apis_rag.do_querying(query, mode="astream"):
            yield token.encode('utf-8')

    return StreamingResponse(generate(), media_type="text/plain")

@app.post("/audio_query/")
async def audio_query(file: UploadFile = File(...)):
    logger.info(f"Received audio query request for file: {file.filename}")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name
    
    logger.info(f"Temporary file created at: {temp_file_path}")

    try:
        # Preprocess the audio file
        logger.info("Starting audio preprocessing")
        preprocessing_start = time.time()
        processed_audio_path = utils_speech.preprocess_audio(temp_file_path)
        preprocessing_time = time.time() - preprocessing_start
        logger.info(f"Audio preprocessing completed in {preprocessing_time:.2f} seconds")

        # Transcribe the processed audio file
        logger.info("Starting audio transcription")
        transcription_start = time.time()
        transcribed_text = apis_speech.transcribe(processed_audio_path)
        transcription_time = time.time() - transcription_start
        logger.info(f"Audio transcription completed in {transcription_time:.2f} seconds")

        logger.info(f"Transcribed text: {transcribed_text}")

        # Use the transcribed text as a query
        logger.info("Starting query processing")
        query_start = time.time()
        result, time_to_first_token = apis_rag.do_querying(transcribed_text)
        
        total_time_to_first_token = preprocessing_time + transcription_time + float(time_to_first_token)
        logger.info(f"[RAG Flow] Time to first token: {time_to_first_token} seconds")
        logger.info(f"[API Flow] Time to first token: {total_time_to_first_token} seconds")

        query_time = time.time() - query_start
        logger.info(f"Query processing completed in {query_time:.2f} seconds")

        response_content = {
            "transcribed_text": transcribed_text,
            "query_result": result,
            "time_to_first_token": time_to_first_token,
            "preprocessing_time": preprocessing_time,
            "transcription_time": transcription_time,
            "query_processing_time": query_time,
        }
        logger.info("Audio query processing completed successfully")
        return JSONResponse(content=response_content)
    except Exception as e:
        logger.error(f"Error processing audio query: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        # Clean up the temporary files
        os.unlink(temp_file_path)
        if 'processed_audio_path' in locals():
            os.unlink(processed_audio_path)
        logger.info(f"Temporary files removed")

@app.post("/audio_query_tts/")
async def audio_query_tts(file: UploadFile = File(...)):
    logger.info(f"Received audio query and TTS request for file: {file.filename}")
    
    temp_file_path = None
    processed_audio_path = None
    output_audio_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name
        
        logger.info(f"Temporary file created at: {temp_file_path}")

        # Preprocess the audio file
        logger.info("Starting audio preprocessing")
        preprocessing_start = time.time()
        processed_audio_path = utils_speech.preprocess_audio(temp_file_path)
        preprocessing_time = time.time() - preprocessing_start
        logger.info(f"Audio preprocessing completed in {preprocessing_time:.2f} seconds")

        # Transcribe the processed audio file
        logger.info("Starting audio transcription")
        transcription_start = time.time()
        transcribed_text = apis_speech.transcribe(processed_audio_path)
        transcription_time = time.time() - transcription_start
        logger.info(f"Audio transcription completed in {transcription_time:.2f} seconds")

        logger.info(f"Transcribed text: {transcribed_text}")

        # Use the transcribed text as a query
        logger.info("Starting query processing")
        query_start = time.time()
        result, time_to_first_token = apis_rag.do_querying(transcribed_text)
        query_time = time.time() - query_start
        logger.info(f"Query processing completed in {query_time:.2f} seconds")

        # Convert the query result to speech
        logger.info("Starting text-to-speech conversion")
        tts_start = time.time()
        output_audio_path = tempfile.mktemp(suffix=".wav")
        tts_success = apis_speech.text_to_speech(result, output_audio_path)
        tts_time = time.time() - tts_start
        logger.info(f"Text-to-speech conversion completed in {tts_time:.2f} seconds")

        if tts_success:
            logger.info("Audio query and TTS processing completed successfully")
            return FileResponse(output_audio_path, media_type="audio/wav", filename="response.wav", background=BackgroundTask(cleanup, temp_file_path, processed_audio_path, output_audio_path))
        else:
            logger.error("Text-to-speech conversion failed")
            return JSONResponse(content={"error": "Text-to-speech conversion failed"}, status_code=500)

    except Exception as e:
        logger.error(f"Error processing audio query and TTS: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        # Clean up the temporary files only if we're not returning a FileResponse
        if 'temp_file_path' in locals() and temp_file_path:
            os.unlink(temp_file_path)
        if 'processed_audio_path' in locals() and processed_audio_path:
            os.unlink(processed_audio_path)
        logger.info(f"Temporary files removed")

def cleanup(temp_file_path, processed_audio_path, output_audio_path):
    try:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        if processed_audio_path and os.path.exists(processed_audio_path):
            os.unlink(processed_audio_path)
        if output_audio_path and os.path.exists(output_audio_path):
            os.unlink(output_audio_path)
        logger.info("All temporary files cleaned up successfully")
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")

@app.get("/control/")
async def control(query: str = "Is the car locked?"):
    async def generate():
        async for token in await apis_car.do_controlling(query, mode="astream_chat"):
            yield token.encode('utf-8')

    return StreamingResponse(generate(), media_type="text/plain")

@app.get("/general/")
async def general(query: str = "What is the current temperature?"):
    async def generate():
        async for token in await apis_car.do_general(query, mode="astream_chat"):
            yield token.encode('utf-8')

    return StreamingResponse(generate(), media_type="text/plain")

@app.post("/run_workflow/")
async def run_workflow(query: str="Could you provide some tips or notes to consider before driving a car?"):
    result = await apis_wf.run_workflow(query)
    return JSONResponse(content={"result": result})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT_FAST_API")))