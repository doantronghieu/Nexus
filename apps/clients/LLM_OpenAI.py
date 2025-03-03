from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8767/v1",
    api_key="dummy"
)

# Non-streaming - special tokens will be removed
response = client.chat.completions.create(
    model="nano-llm",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)  # Clean response without special tokens

# Streaming - tokens are cleaned as they arrive
for chunk in client.chat.completions.create(
    model="nano-llm",
    messages=[{"role": "user", "content": "Tell me a joke!"}],
    stream=True
):
    print(chunk.choices[0].delta.content or "", end="")