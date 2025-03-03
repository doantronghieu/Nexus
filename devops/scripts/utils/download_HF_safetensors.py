import os
import shutil
import requests
import argparse
from pathlib import Path
from huggingface_hub import HfApi
from tqdm import tqdm

def get_temp_dir():
    return Path.home() / "huggingface_models_temp"

def get_final_dir():
    return Path('/') / "dist" / "models"

def check_model_exists(repo_id):
    final_dir = get_final_dir()
    provider, model = repo_id.split('/', 1)
    model_path = final_dir / provider / model
    return model_path.exists() and any(model_path.iterdir())

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        with open(local_filename, 'wb') as f, tqdm(
            desc=local_filename,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for chunk in r.iter_content(chunk_size=8192):
                size = f.write(chunk)
                progress_bar.update(size)

def download_safetensors(repo_id, temp_dir):
    api = HfApi()
    
    # Get list of files in the repository
    files = api.list_repo_files(repo_id)
    
    # Filter files with ".safetensors" in the name
    safetensor_files = [f for f in files if ".safetensors" in f]
    
    if not safetensor_files:
        print(f"No .safetensors files found in the repository: {repo_id}")
        return []
    
    # Create temporary directory if it doesn't exist
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    downloaded_files = []
    # Download each safetensor file
    for file in safetensor_files:
        file_url = f"https://huggingface.co/{repo_id}/resolve/main/{file}"
        local_path = temp_dir / Path(file).name
        
        print(f"Downloading: {file}")
        download_file(file_url, str(local_path))
        print(f"Downloaded: {local_path}")
        downloaded_files.append(local_path)
    
    return downloaded_files

def move_files(files, source_dir, dest_dir):
    dest_dir.mkdir(parents=True, exist_ok=True)
    for file in files:
        shutil.move(str(file), str(dest_dir / file.name))
        print(f"Moved {file.name} to {dest_dir}")

def main():
    temp_dir = get_temp_dir()
    final_dir = get_final_dir()
    parser = argparse.ArgumentParser(description="Download .safetensors files from a Hugging Face repository.")
    parser.add_argument("repo_id", help="The Hugging Face repository ID")
    args = parser.parse_args()

    if check_model_exists(args.repo_id):
        print(f"Model {args.repo_id} already exists in {final_dir}. Skipping download.")
        return

    temp_output_dir = temp_dir / args.repo_id
    provider, model = args.repo_id.split('/', 1)
    final_output_dir = final_dir / provider / model

    try:
        downloaded_files = download_safetensors(args.repo_id, temp_output_dir)
        if downloaded_files:
            try:
                move_files(downloaded_files, temp_output_dir, final_output_dir)
                print(f"All files successfully moved to {final_output_dir}")
            except PermissionError:
                print(f"Permission denied when trying to move files to {final_output_dir}")
                print(f"Files remain in the temporary directory: {temp_output_dir}")
                print("You may need to manually move them with sudo privileges.")
            finally:
                if temp_output_dir.exists() and not any(temp_output_dir.iterdir()):
                    temp_output_dir.rmdir()
                    print(f"Removed empty temporary directory: {temp_output_dir}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()