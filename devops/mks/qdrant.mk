# qdrant.mk

# Qdrant service name
QDRANT_SERVICE := qdrant

# Qdrant-specific commands
.PHONY: qdrant-start qdrant-stop qdrant-logs

qdrant-start:
	$(DOCKER_COMPOSE) up -d $(QDRANT_SERVICE)

qdrant-stop:
	$(DOCKER_COMPOSE) stop $(QDRANT_SERVICE)
	$(DOCKER_COMPOSE) rm -f $(QDRANT_SERVICE)

qdrant-logs:
	$(DOCKER_COMPOSE) logs -f $(QDRANT_SERVICE)