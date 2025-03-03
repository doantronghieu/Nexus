import packages # Must include this
from toolkit.utils import utils

HOST_POSTGRES = "localhost" if utils.os.getenv("IN_PROD") is None else "postgres"
HOST_QDRANT = "localhost" if utils.os.getenv("IN_PROD") is None else "qdrant"
PORT_QDRANT = utils.os.getenv("PORT_QDRANT") if  utils.os.getenv("IN_PROD") is None else 6333
HOST_MONGODB = "localhost" if utils.os.getenv("IN_PROD") is None else "mongo"
HOST_REDIS = "localhost" if utils.os.getenv("IN_PROD") is None else "redis"

HOST_SVC_MAP = "localhost" if utils.os.getenv("IN_PROD") is None else "svc-nav-main"
PORT_SVC_MAP = utils.os.getenv("PORT_SVC_MAP", "8000")
PROTOCOL_SVC_MAP = "https"
URL_SVC_MAP = f"{PROTOCOL_SVC_MAP}://{HOST_SVC_MAP}:{PORT_SVC_MAP}"

HOST_SVC_MAPBOX = "localhost" if utils.os.getenv("IN_PROD") is None else "svc-nav-mapbox"
PORT_SVC_MAPBOX = utils.os.getenv("PORT_SVC_MAPBOX", "8000")
PROTOCOL_SVC_MAPBOX = "http"
URL_SVC_MAPBOX = f"{PROTOCOL_SVC_MAPBOX}://{HOST_SVC_MAPBOX}:{PORT_SVC_MAPBOX}"

HOST_SVC_MUSIC = "localhost" if utils.os.getenv("IN_PROD") is None else "svc-music"
PORT_SVC_MUSIC = utils.os.getenv("PORT_SVC_MUSIC", "8000")
PROTOCOL_SVC_MUSIC = "http"
URL_SVC_MUSIC = f"{PROTOCOL_SVC_MUSIC}://{HOST_SVC_MUSIC}:{PORT_SVC_MUSIC}"

HOST_SVC_NEWS = "localhost" if utils.os.getenv("IN_PROD") is None else "svc-news"
PORT_SVC_NEWS = utils.os.getenv("PORT_SVC_NEWS", "8000")
PROTOCOL_SVC_NEWS = "http"
URL_SVC_NEWS = f"{PROTOCOL_SVC_NEWS}://{HOST_SVC_NEWS}:{PORT_SVC_NEWS}"

HOST_SVC_SEARCH = "localhost" if utils.os.getenv("IN_PROD") is None else "svc-search"
PORT_SVC_SEARCH = utils.os.getenv("PORT_SVC_SEARCH", "8000")
PROTOCOL_SVC_SEARCH = "http"
URL_SVC_SEARCH = f"{PROTOCOL_SVC_SEARCH}://{HOST_SVC_SEARCH}:{PORT_SVC_SEARCH}"

HOST_SVC_WEATHER = "localhost" if utils.os.getenv("IN_PROD") is None else "svc-weather"
PORT_SVC_WEATHER = utils.os.getenv("PORT_SVC_WEATHER", "8000")
PROTOCOL_SVC_WEATHER = "http"
URL_SVC_WEATHER = f"{PROTOCOL_SVC_WEATHER}://{HOST_SVC_WEATHER}:{PORT_SVC_WEATHER}"

HOST_SVC_WWD = "localhost" if utils.os.getenv("IN_PROD") is None else "svc-audio-wwd"
PORT_SVC_WWD = utils.os.getenv("PORT_SVC_WWD", "8000")
PROTOCOL_SVC_WWD = "http"
URL_SVC_WWD = f"{PROTOCOL_SVC_WWD}://{HOST_SVC_WWD}:{PORT_SVC_WWD}"

HOST_SVC_TTS = "localhost" if utils.os.getenv("IN_PROD") is None else "svc-audio-tts"
PORT_SVC_TTS = utils.os.getenv("PORT_SVC_TTS", "8000")
PROTOCOL_SVC_TTS = "http"
URL_SVC_TTS = f"{PROTOCOL_SVC_TTS}://{HOST_SVC_TTS}:{PORT_SVC_TTS}"

HOST_SVC_STT = "localhost" if utils.os.getenv("IN_PROD") is None else "svc-audio-stt"
PORT_SVC_STT = utils.os.getenv("PORT_SVC_STT", "8000")
PROTOCOL_SVC_STT = "http"
URL_SVC_STT = f"{PROTOCOL_SVC_STT}://{HOST_SVC_STT}:{PORT_SVC_STT}"

HOST_SVC_FACE = "localhost" if utils.os.getenv("IN_PROD") is None else "svc-vision-face"
PORT_SVC_FACE = utils.os.getenv("PORT_SVC_FACE", "8000")
PROTOCOL_SVC_FACE = "http"
URL_SVC_FACE = f"{PROTOCOL_SVC_FACE}://{HOST_SVC_FACE}:{PORT_SVC_FACE}"

HOST_APP_VEHICLE = "localhost" if utils.os.getenv("IN_PROD") is None else "app-llm"
PORT_APP_VEHICLE = utils.os.getenv("PORT_APP_VEHICLE", "8000")
PROTOCOL_APP_VEHICLE = "http"
URL_APP_VEHICLE = f"{PROTOCOL_APP_VEHICLE}://{HOST_APP_VEHICLE}:{PORT_APP_VEHICLE}"

HOST_APP_LLM_P3 = "localhost" if utils.os.getenv("IN_PROD") is None else "app-llm-p3"
PORT_APP_LLM_P3 = utils.os.getenv("PORT_APP_LLM_P3", "8000")
PROTOCOL_APP_LLM_P3 = "http"
URL_APP_LLM_P3 = f"{PROTOCOL_APP_LLM_P3}://{HOST_APP_LLM_P3}:{PORT_APP_LLM_P3}"
