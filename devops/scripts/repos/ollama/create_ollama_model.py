import argparse
import ollama
import os

# https://github.com/ollama/ollama-python

def get_modelfile(model_name):
  return ollama.show(model_name)["modelfile"]

def create_ollama_model(modelfile_path, model_name):
    if not os.path.exists(modelfile_path):
        print(f"Error: Modelfile not found at {modelfile_path}")
        return

    try:
        with open(modelfile_path, "rb") as f:
            modelfile = f.read().decode()

        ollama.create(
            model=model_name,
            modelfile=modelfile,
        )
        print(f"Successfully created Ollama model: {model_name}")
    except Exception as e:
        print(f"Error creating Ollama model: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create an Ollama model from a Modelfile")
    parser.add_argument("modelfile_path", help="Path to the Modelfile")
    parser.add_argument("model_name", help="Name of the model to create")
    
    args = parser.parse_args()
    
    create_ollama_model(args.modelfile_path, args.model_name)