#!/bin/bash

conda deactivate && conda activate dev

make start jetson

conda deactivate && conda activate dev
cd apps/servers/
python FastAPI-WWD-STT-TTS.py

conda deactivate && conda activate dev
cd apps/servers/
python FastAPI.py

cd front_end/Chatbot
npm run dev

#--- Map

conda deactivate && conda activate dev
cd apps/services/map
python main.py

conda deactivate && conda activate dev
cd apps/services/map
python mapbox.py

cd front_end/dev/Mapbox-LLM
npm run dev

#--- Video Stream

conda deactivate && conda activate dev
cd apps/services/stream
python FastAPI-Video-WebRTC.py

cd front_end/dev/stream
npm run dev

---

ngrok http --url=positive-viper-presently.ngrok-free.app 80
ngrok http --url=key-amoeba-basically.ngrok-free.app 80

./devops/setup/nginx/nginx-control.sh start
./devops/setup/nginx/nginx-control.sh reload
./devops/setup/nginx/nginx-control.sh stop

conda deactivate && conda activate dev
cd apps/services/dev/stream
python server.py

cd apps/services/dev/stream/Camera
npm run dev

https://positive-viper-presently.ngrok-free.app
https://key-amoeba-basically.ngrok-free.app

positive-viper-presently.ngrok-free.app
key-amoeba-basically.ngrok-free.app
localhost:8000

---


