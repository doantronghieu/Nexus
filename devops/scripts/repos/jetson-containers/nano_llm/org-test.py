import termcolor
import nano_llm
from nano_llm import NanoLLM, ChatHistory

# /data/models/mlc/dist

model = NanoLLM.from_pretrained(
  #  "princeton-nlp/Sheared-LLaMA-2.7B-ShareGPT",  # HuggingFace repo/model name, or path to HF model checkpoint
  "meta-llama/Meta-Llama-3-8B-Instruct", # ✅
  api='mlc',                   # supported APIs are: mlc, awq, hf
  api_token='HF_API_KEY',    # HuggingFace API key for authenticated models ($HUGGINGFACE_TOKEN)
  quantization='q4f16_ft'      # q4f16_ft, q4f16_1, q8f16_0 for MLC, or path to AWQ weights
)

# create the chat history
chat_history = ChatHistory(model, system_prompt="You are a helpful and friendly AI assistant.")

while True:
    # enter the user query from terminal
    print('>> ', end='', flush=True)
    prompt = input().strip()

    # add user prompt and generate chat tokens/embeddings
    chat_history.append('user', prompt)
    embedding, position = chat_history.embed_chat()

    # generate bot reply
    reply = model.generate(
        embedding, 
        streaming=True, 
        kv_cache=chat_history.kv_cache,
        stop_tokens=chat_history.template.stop,
        # max_new_tokens=args.max_new_tokens,
    )
        
    # stream the output
    for token in reply:
        termcolor.cprint(token, 'blue', end='\n\n' if reply.eos else '', flush=True)

    # save the final output
    chat_history.append('bot', reply)