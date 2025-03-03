import packages
import subprocess
import os

PATH_ROOT = packages.ROOT_PATH
PATH_REPO_PIPER = f"{PATH_ROOT}/data/assets/repos/piper"
PATH_ASSETS = f"{PATH_REPO_PIPER}"

def text_to_speech(
    text: str, 
    path_audio_output: str = f"{PATH_ASSETS}/outputs/output.wav"
):
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(path_audio_output), exist_ok=True)

    # Construct the command
    command = [
        'piper',
        '--model', os.path.join(PATH_ASSETS, 'models/en_US-ryan-high.onnx'),
        '--data-dir', os.path.join(PATH_ASSETS, 'data'),
        '--download-dir', os.path.join(PATH_ASSETS, 'download'),
        '--output_file', path_audio_output
    ]

    # Run the command
    try:
        result = subprocess.run(
            command,
            input=text,
            text=True,
            capture_output=True,
            check=True
        )
        print(f"Audio generated successfully at {path_audio_output}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        print(f"stderr: {e.stderr}")
        return False

if __name__ == "__main__":
    # Example usage - Fixed by specifying a proper WAV file path
    output_path = os.path.join(PATH_ASSETS, "outputs", "output.wav")
    text_to_speech(
        "Welcome to the world of speech synthesis!", 
        output_path
    )