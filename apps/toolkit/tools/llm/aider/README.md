# Aider

## Installation

```bash
pip install -r requirements.txt
playwright install
playwright install-deps
playwright install --with-deps chromium
```

## LLM

- GPT-4o:
`aider --openai-api-key sk-xxx...`

- Claude 3 Opus:
`aider --anthropic-api-key sk-xxx... --opus`

- DeepSeek:

```bash
export DEEPSEEK_API_KEY=sk-73648ca491ce432dac9a465dc1d7ae27
aider --model deepseek/deepseek-coder
aider --model deepseek/deepseek-coder --no-git

/web URL URL ...
```
