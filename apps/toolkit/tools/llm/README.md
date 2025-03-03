# Tools running instructions

## Ollama

- Installaion: https://github.com/ollama/ollama?tab=readme-ov-file
- Docker:
  - https://github.com/ollama/ollama/blob/main/docs/docker.md
  - https://hub.docker.com/r/ollama/ollama

### Docker

```bash
chmod +x apps/toolkit/tools/llm/scripts/*.sh
cd apps/toolkit/tools/llm
```

#### Use Makefile

```bash
make ollama-start
make ollama-start-and-run MODEL=YOUR_MODEL # default: llama3.1:8b
make ollama-stop
```

#### Run manuallly

- Run

```bash
bash run_ollama.sh

# docker exec -d ollama ollama run MODEL

docker exec -d ollama ollama run llama3.1:8b
```

- Stop

```bash
bash stop_ollama.sh
```

Notes:

- The initial run may be slow.

### Normal

- Download model: `ollama pull MODEL`
- Run: `ollama run MODEL`
- Others:
  - Remove model:
    - `ollama rm MODEL`
    - Manually: `rm ~/.ollama/models/MODEL`
