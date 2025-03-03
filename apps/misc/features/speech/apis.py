import packages
import requests
import os
from . import whisper_cpp
from . import piper

def transcribe(path_audio: str):
  return whisper_cpp.transcribe(path_audio)

# def text_to_speech(
#     text: str, 
#     path_audio_output: str,
# ):
#   is_success = piper.text_to_speech(text, path_audio_output)
#   return is_success

def text_to_speech(text: str, path_audio_output: str):
    port = int(os.getenv("PORT_SVC_TTS_PIPER"))
    url = f"http://localhost:{port}/tts"
    
    try:
        response = requests.post(url, data={"text": text})
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        if response.headers.get('content-type') == 'audio/wav':
            with open(path_audio_output, "wb") as file:
                file.write(response.content)
            is_success = True
        else:
            error_message = response.json().get('error', 'Unknown error occurred')
            print(f"Error in text-to-speech conversion: {error_message}")
            is_success = False
    
    except requests.RequestException as e:
        print(f"Error occurred while making the request: {e}")
        is_success = False
    except IOError as e:
        print(f"Error occurred while writing the file: {e}")
        is_success = False
    
    return is_success