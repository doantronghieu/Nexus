#!/usr/bin/env python3
print('testing vLLM...')

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List
from huggingface_hub import hf_hub_download, HfApi, snapshot_download
from vllm import LLM, SamplingParams


@dataclass
class ModelConfig:
    repo_id: str
    filename: Optional[str] = None
    base_model_id: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    gpu_utilization: float = 0.5
    max_tokens: int = 150  # Reduced to keep responses shorter
    temperature: float = 0.3  # Reduced for more focused responses
    system_message: str = (
        "You are a straightforward AI assistant. Follow these rules strictly:\n"
        "1. Always respond directly to the user's question or prompt\n"
        "2. Keep responses brief and relevant\n"
        "3. Don't include meta-commentary or self-references\n"
        "4. Don't include instructions or examples unless specifically asked\n"
        "5. Don't apologize or use phrases like 'here's a revised version'\n"
        "6. Don't mention being an AI unless relevant to the question"
    )
    cache_dir: Path = Path("/data/models/huggingface")


class ModelManager:
    def __init__(self):
        self.api = HfApi()

    def find_model_files(self, repo_id: str) -> list:
        """List all GGUF files in the repository."""
        try:
            files = self.api.list_repo_files(repo_id)
            gguf_files = [f for f in files if f.endswith('.gguf')]
            if not gguf_files:
                raise RuntimeError(f"No GGUF files found in repository: {repo_id}")
            return gguf_files
        except Exception as e:
            raise RuntimeError(f"Failed to list repository files: {str(e)}")

    def get_model_path(self, config: ModelConfig) -> str:
        """Find or download model based on config."""
        repo_dir = config.cache_dir / f"models--{config.repo_id.replace('/', '--')}"
        filename = config.filename

        # If filename not provided, find available models
        if filename is None:
            try:
                gguf_files = self.find_model_files(config.repo_id)
                q4_files = [f for f in gguf_files if 'q4_0' in f.lower()]
                filename = q4_files[0] if q4_files else gguf_files[0]
                print(f"Selected model file: {filename}")
            except Exception as e:
                raise RuntimeError(f"Failed to find model files: {str(e)}")

        # Check if model exists in cache
        if repo_dir.exists():
            for snapshot_dir in repo_dir.glob("snapshots/*"):
                model_path = snapshot_dir / filename
                if model_path.exists():
                    print(f"Found existing model at: {model_path}")
                    return str(model_path)

        # Download if not found
        return self._download_model(config.repo_id, filename, config.cache_dir)

    def _download_model(self, repo_id: str, filename: str, cache_dir: Path) -> str:
        """Download model with fallback strategies."""
        print(f"Model not found locally. Downloading from Hugging Face Hub: {repo_id}")
        try:
            # Try direct download first
            try:
                return hf_hub_download(
                    repo_id=repo_id,
                    filename=filename,
                    cache_dir=str(cache_dir)
                )
            except Exception as e:
                print(f"Direct download failed, trying repository snapshot: {str(e)}")
                
                # Fall back to full repo download
                snapshot_path = snapshot_download(
                    repo_id=repo_id,
                    cache_dir=str(cache_dir)
                )
                
                # Find the model file
                for root, _, files in os.walk(snapshot_path):
                    if filename in files:
                        model_path = os.path.join(root, filename)
                        print(f"Found model in snapshot at: {model_path}")
                        return model_path
                        
                raise RuntimeError(f"Could not find {filename} in downloaded snapshot")
                
        except Exception as e:
            raise RuntimeError(f"Failed to download model: {str(e)}")

class ChatBot:
    def __init__(self, config: ModelConfig):
        self.config = config
        self.model_manager = ModelManager()
        self.llm = None
        self.sampling_params = None
        # Simplified prompt template
        self.prompt_template = (
            "<|system|>\n"
            "{system_message}"
            "</s>\n"
            "<|user|>\n"
            "Respond directly to this message: {prompt}"
            "</s>\n"
            "<|assistant|>\n"
        )

    def initialize(self):
        """Initialize the LLM and sampling parameters."""
        if self.llm is not None:
            return

        print("Initializing LLM...")
        model_path = self.model_manager.get_model_path(self.config)
        
        self.llm = LLM(
            model=model_path,
            tokenizer=self.config.base_model_id,
            gpu_memory_utilization=self.config.gpu_utilization
        )
        
        self.sampling_params = SamplingParams(
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            top_p=0.1,  # Reduced for more focused responses
            presence_penalty=0.1,
            frequency_penalty=0.1,  # Added to reduce repetition
            stop=["</s>", "<|user|>", "<|system|>"]  # Added stop tokens
        )
        print("LLM initialized successfully!")

    def update_system_message(self, new_message: str):
        """Update the system message."""
        self.config.system_message = new_message
        print(f"System message updated to: {new_message}")

    def generate_response(self, prompt: str) -> str:
        """Generate a response for the given prompt."""
        formatted_prompt = self.prompt_template.format(
            system_message=self.config.system_message,
            prompt=prompt
        )
        outputs = self.llm.generate([formatted_prompt], self.sampling_params)
        response = outputs[0].outputs[0].text.strip()
        
        # Clean up common issues in responses
        response = response.replace("Here's", "").replace("Sure,", "")
        response = response.replace("Let me", "I will")
        response = ' '.join(response.split())  # Normalize whitespace
        
        return response
      
    def chat_loop(self):
        """Run the interactive chat loop."""
        self.initialize()

        print("\nChat initialized! Type your messages and press Enter.")
        print("Special commands:")
        print("  /system <message> - Update system message")
        print("  quit, exit, q - Exit the chat")
        print("-" * 50)

        while True:
            try:
                user_prompt = input("\n> ")
                
                if user_prompt.lower() in ['quit', 'exit', 'q']:
                    print("Exiting the program...")
                    break
                
                if user_prompt.startswith("/system "):
                    self.update_system_message(user_prompt[8:])
                    continue
                
                print("\nGenerating response...")
                response = self.generate_response(user_prompt)
                print(f"\n{response}")
                
            except KeyboardInterrupt:
                print("\nProgram interrupted by user. Exiting...")
                break
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")
                continue


def main():
    # Example configuration with improved defaults
    config = ModelConfig(
        repo_id="TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
        filename="tinyllama-1.1b-chat-v1.0.Q4_0.gguf",
        base_model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        temperature=0.7,  # Add some randomness
        max_tokens=256    # Allow for longer responses
    )
    
    try:
        chatbot = ChatBot(config)
        chatbot.chat_loop()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
    print('vLLM OK\n')