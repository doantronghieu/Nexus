# mongo.mk

# MongoDB-specific commands

# List MongoDB collections
mongo-list-collections:
	@echo "Listing MongoDB collections..."
	@$(DOCKER_COMPOSE) exec mongo mongosh --username root --password example --eval "db.getCollectionNames()"

# Create a new MongoDB collection
mongo-create-collection:
	@echo "Creating a new MongoDB collection..."
	@read -p "Enter collection name: " name; \
	$(DOCKER_COMPOSE) exec mongo mongosh --username root --password example --eval "db.createCollection('$$name')"

# Drop a MongoDB collection
mongo-drop-collection:
	@echo "Dropping a MongoDB collection..."
	@read -p "Enter collection name to drop: " name; \
	$(DOCKER_COMPOSE) exec mongo mongosh --username root --password example --eval "db.$$name.drop()"

.PHONY: mongo-list-collections mongo-create-collection mongo-drop-collection