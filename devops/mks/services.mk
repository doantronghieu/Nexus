# List of all services
BASE_SERVICES := qdrant postgres mongo mongo-express
JETSON_SERVICES := fastapi-tts-piper-jetson fastapi-llm-nano-jetson
SERVICES := ollama $(BASE_SERVICES)
SERVER_SERVICES := fastapi fastapi-stt-whisper-cpp

# Helper function to construct Jetson compose commands
define jetson_services_cmd
	$(DOCKER_COMPOSE_TTS_JETSON) $(1) && \
	$(DOCKER_COMPOSE_LLM_NANO_JETSON) $(1)
endef

# Docker compose commands for all services
COMPOSE_CMD = $(if $(filter jetson,$(MAKECMDGOALS)),\
	$(MAKE) -f devops/mks/ollama.mk ollama-$(1) jetson && \
	$(call jetson_services_cmd,$(2)) && \
	$(DOCKER_COMPOSE_INFRA) $(2) $(BASE_SERVICES) && \
	$(DOCKER_COMPOSE_SERVERS) $(3),\
	$(DOCKER_COMPOSE_INFRA) $(2) $(SERVICES) && \
	$(DOCKER_COMPOSE_SERVERS) $(3))

# Service-specific command handler
SERVICE_CMD = $(if $(filter ollama,$*),\
	$(if $(filter jetson,$(MAKECMDGOALS)),$(MAKE) -f devops/mks/ollama.mk ollama-$(1) jetson,$(DOCKER_COMPOSE_INFRA) $(2) $*),\
	$(if $(filter fastapi-tts-piper-jetson,$*),$(DOCKER_COMPOSE_TTS_JETSON) $(2),\
	$(if $(filter fastapi-llm-nano-jetson,$*),$(DOCKER_COMPOSE_LLM_NANO_JETSON) $(2),\
	$(if $(filter $(SERVER_SERVICES),$*),$(DOCKER_COMPOSE_SERVERS) $(3) $*,\
	$(DOCKER_COMPOSE_INFRA) $(2) $*))))

# Main targets
start: ; @echo "Starting all services..." && $(call COMPOSE_CMD,start,up -d,up -d --build)
stop:  ; @echo "Stopping all services..." && $(call COMPOSE_CMD,stop,stop,stop)
remove:; @echo "Removing all services..." && $(call COMPOSE_CMD,remove,down,down)

# Single service targets
start-%:  ; @echo "Starting service: $*"  && $(call SERVICE_CMD,start,up -d,up -d --build)
stop-%:   ; @echo "Stopping service: $*"  && $(call SERVICE_CMD,stop,stop,stop)
remove-%: ; @echo "Removing service: $*"  && $(call SERVICE_CMD,remove,down,rm -f)

# Multi-service operations
define multi_op
$(1)-multi:
	@echo "$(2) multiple services..."
	@for service in $$(filter-out $(1)-multi jetson,$$(MAKECMDGOALS)); do \
		$$(MAKE) $(1)-$$$$service $$(filter jetson,$$(MAKECMDGOALS)); \
	done
endef

$(eval $(call multi_op,start,Starting))
$(eval $(call multi_op,stop,Stopping))
$(eval $(call multi_op,remove,Removing))

# Allow arbitrary targets for multi operations
%: ; @:

.PHONY: start stop remove $(addprefix start-,$(SERVICES) $(SERVER_SERVICES)) \
	$(addprefix stop-,$(SERVICES) $(SERVER_SERVICES)) \
	$(addprefix remove-,$(SERVICES) $(SERVER_SERVICES)) \
	start-multi stop-multi remove-multi