import packages

from faster_whisper import WhisperModel
from configs.consts import whisper

# Initialize the WhisperModel
model = WhisperModel(
  whisper.Model.TINY.value,
  device=whisper.Device.CPU.value,
  compute_type=whisper.ComputeType.INT8.value,
)

def transcribe(path_audio: str) -> str:
  # Transcribe the audio file
  segments, info = model.transcribe(
      path_audio,
      beam_size=5,
      vad_filter=False,
      vad_parameters=dict(min_silence_duration_ms=500),
  )

  # Combine all segments into a single text
  result = "".join(segment.text for segment in segments)

  return result