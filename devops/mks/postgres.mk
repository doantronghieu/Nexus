# postgres.mk

# PostgreSQL service name
POSTGRES_SERVICE := postgres

# PostgreSQL-specific commands
.PHONY: postgres-start postgres-stop postgres-logs postgres-shell

postgres-start:
	$(DOCKER_COMPOSE) up -d $(POSTGRES_SERVICE)

postgres-stop:
	$(DOCKER_COMPOSE) stop $(POSTGRES_SERVICE)
	$(DOCKER_COMPOSE) rm -f $(POSTGRES_SERVICE)

postgres-logs:
	$(DOCKER_COMPOSE) logs -f $(POSTGRES_SERVICE)

postgres-shell:
	$(DOCKER_COMPOSE) exec $(POSTGRES_SERVICE) psql -U myuser -d mydatabase