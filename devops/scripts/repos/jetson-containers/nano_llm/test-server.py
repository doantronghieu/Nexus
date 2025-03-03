# Use with OpenAI client
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="dummy"
)

# Non-streaming
response = client.chat.completions.create(
    model="nano-llm",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Streaming
for chunk in client.chat.completions.create(
    model="nano-llm",
    messages=[{"role": "user", "content": "hello"}],
    stream=True
):
    print(chunk.choices[0].delta.content or "", end="")