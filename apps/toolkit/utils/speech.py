import os
from pydub import AudioSegment

import os
from pydub import AudioSegment
from loguru import logger

def preprocess_audio(input_file_path, output_file_path=None):
    """
    Convert any audio file to WAV format with 16 kHz sample rate.
    
    :param input_file_path: Path to the input audio file
    :param output_file_path: Path to save the processed audio file (optional)
    :return: Path to the processed audio file
    """
    logger.info(f"Preprocessing audio file: {input_file_path}")
    logger.info(f"Input file size: {os.path.getsize(input_file_path)} bytes")

    if output_file_path is None:
        output_file_path = os.path.splitext(input_file_path)[0] + "_processed.wav"
    
    try:
        audio = AudioSegment.from_file(input_file_path)
        
        logger.info(f"Original audio: {audio.channels} channels, {audio.frame_rate} Hz, {audio.sample_width} bytes/sample")
        
        if audio.channels > 1:
            audio = audio.set_channels(1)
            logger.info("Converted to mono")
        
        if audio.frame_rate != 16000:
            audio = audio.set_frame_rate(16000)
            logger.info("Set frame rate to 16000 Hz")
        
        if audio.sample_width != 2:  # 16-bit
            audio = audio.set_sample_width(2)
            logger.info("Set sample width to 16 bits")
        
        audio.export(output_file_path, format="wav")
        
        logger.info(f"Processed audio saved to: {output_file_path}")
        logger.info(f"Processed file size: {os.path.getsize(output_file_path)} bytes")
        
        return output_file_path
    except Exception as e:
        logger.error(f"Error preprocessing audio: {str(e)}")
        return None