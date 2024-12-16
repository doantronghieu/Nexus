conda activate dev

pip install aider-install
aider-install
export PATH="/Users/thung/.local/bin:$PATH" #

playwright install --with-deps chromium

pip install -U google-generativeai

aider --env-file devops/tools/aider/.env

aider --list-models gemini/