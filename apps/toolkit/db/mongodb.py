from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo import UpdateOne
from bson import ObjectId
from typing import Any, Dict, List, Optional, Tuple, Union
import datetime
import json
from loguru import logger


class MongoDBCollectionManager:
    """Manager for a specific MongoDB collection."""
    
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def drop_collection(self) -> Dict[str, Any]:
        """Drop the entire collection."""
        try:
            logger.warning(f"Dropping collection: {self.collection.name}")
            await self.collection.drop()
            logger.info(f"Successfully dropped collection: {self.collection.name}")
            return {
                "success": True,
                "message": f"Dropped collection: {self.collection.name}"
            }
        except Exception as e:
            logger.error(f"Failed to drop collection: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to drop collection: {str(e)}"
            }

    @staticmethod
    def json_encode(o: Any) -> str:
        """Custom JSON encoder to handle ObjectId and datetime."""
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        raise TypeError(f"Object of type {type(o)} is not JSON serializable")

    async def create_document(self, doc_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new document with the specified ID and data."""
        logger.info(f"Creating new document with ID {doc_id} in collection {self.collection.name}")
        data['_id'] = doc_id
        try:
            await self.collection.insert_one(data)
            logger.info(f"Successfully created document {doc_id}")
            return {"success": True, "message": f"Created document {doc_id}"}
        except Exception as e:
            logger.error(f"Failed to create document: {str(e)}")
            return {"success": False, "message": f"Failed to create document: {str(e)}"}

    async def bulk_create(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create multiple documents in one operation."""
        logger.info(f"Creating {len(documents)} documents")
        try:
            result = await self.collection.insert_many(documents)
            inserted_ids = [str(id) for id in result.inserted_ids]
            logger.info(f"Successfully created {len(inserted_ids)} documents")
            return {
                "success": True,
                "inserted_ids": inserted_ids,
                "message": f"Created {len(inserted_ids)} documents"
            }
        except Exception as e:
            logger.error(f"Bulk create failed: {str(e)}")
            return {"success": False, "message": f"Bulk create failed: {str(e)}"}

    async def bulk_update(self, updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform multiple document updates in one operation.
        updates format: [{"filter": {}, "update": {}, "upsert": bool}, ...]
        """
        try:
            operations = [UpdateOne(
                update["filter"],
                {"$set": update["update"]},
                upsert=update.get("upsert", False)
            ) for update in updates]
            
            logger.info(f"Performing bulk update with {len(operations)} operations")
            result = await self.collection.bulk_write(operations)
            
            return {
                "success": True,
                "modified_count": result.modified_count,
                "upserted_count": result.upserted_count,
                "message": f"Updated {result.modified_count} documents"
            }
        except Exception as e:
            logger.error(f"Bulk update failed: {str(e)}")
            return {"success": False, "message": f"Bulk update failed: {str(e)}"}

    async def update_field(self, doc_id: str, field_path: str, new_value: Any) -> Dict[str, Any]:
        """Update a specific field in a document."""
        logger.info(f"Updating field {field_path} for document {doc_id}")
        
        document = await self.collection.find_one({"_id": doc_id})
        if not document:
            logger.warning(f"Document with ID {doc_id} not found")
            return {"success": False, "message": f"Document with ID {doc_id} not found"}

        result = await self.collection.update_one(
            {"_id": doc_id},
            {"$set": {field_path: new_value}}
        )
        
        if result.modified_count == 0:
            logger.info(f"Field {field_path} set to same value for document {doc_id}")
        else:
            logger.info(f"Successfully updated {field_path} for document {doc_id}")
            
        return {"success": True, "message": f"Updated {field_path} for document {doc_id}"}

    async def update_multiple_fields(self, doc_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update multiple fields in a document in a single operation."""
        logger.info(f"Updating multiple fields for document {doc_id}: {list(updates.keys())}")
        
        document = await self.collection.find_one({"_id": doc_id})
        if not document:
            logger.warning(f"Document with ID {doc_id} not found")
            return {"success": False, "message": f"Document with ID {doc_id} not found"}

        try:
            result = await self.collection.update_one(
                {"_id": doc_id},
                {"$set": updates}
            )
            
            if result.modified_count == 0:
                logger.info(f"No fields were modified for document {doc_id}")
                return {
                    "success": True,
                    "message": f"No fields were modified for document {doc_id}",
                    "modified": False
                }
            else:
                logger.info(f"Successfully updated {len(updates)} fields for document {doc_id}")
                return {
                    "success": True,
                    "message": f"Updated {len(updates)} fields for document {doc_id}",
                    "modified": True
                }
        except Exception as e:
            logger.error(f"Failed to update fields: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to update fields: {str(e)}"
            }

    async def create_index(self, keys: List[Tuple[str, int]], unique: bool = False) -> Dict[str, Any]:
        """Create an index on specified fields."""
        try:
            logger.info(f"Creating index on fields: {keys}, unique: {unique}")
            index_name = await self.collection.create_index(keys, unique=unique)
            logger.info(f"Successfully created index: {index_name}")
            return {
                "success": True, 
                "index_name": index_name,
                "message": f"Created index: {index_name}"
            }
        except Exception as e:
            logger.error(f"Failed to create index: {str(e)}")
            return {"success": False, "message": f"Failed to create index: {str(e)}"}

    async def list_indexes(self) -> Dict[str, Any]:
        """List all indexes in the collection."""
        try:
            logger.info(f"Listing indexes for collection: {self.collection.name}")
            indexes = await self.collection.list_indexes().to_list(None)
            indexes_list = [idx for idx in indexes]  # Convert CommandCursor to list
            logger.info(f"Successfully retrieved {len(indexes_list)} indexes")
            return {
                "success": True,
                "indexes": json.loads(json.dumps(indexes_list, default=self.json_encode)),
                "message": f"Retrieved {len(indexes_list)} indexes"
            }
        except Exception as e:
            logger.error(f"Failed to list indexes: {str(e)}")
            return {"success": False, "message": f"Failed to list indexes: {str(e)}"}

    async def get_field(self, doc_id: str, field_path: str) -> Dict[str, Any]:
        """Retrieve a specific field from a document."""
        logger.info(f"Retrieving field {field_path} for document {doc_id}")
        document = await self.collection.find_one({"_id": doc_id})
        
        if not document:
            logger.warning(f"Document with ID {doc_id} not found")
            return {"success": False, "message": f"Document with ID {doc_id} not found"}

        fields = field_path.split('.')
        value = document
        for field in fields:
            if isinstance(value, dict) and field in value:
                value = value[field]
            else:
                logger.warning(f"Field {field_path} not found for document {doc_id}")
                return {"success": False, "message": f"Field {field_path} not found"}

        logger.info(f"Successfully retrieved {field_path} for document {doc_id}")
        return {
            "success": True,
            "value": value,
            "message": f"Retrieved {field_path} for document {doc_id}"
        }
        
    async def get_multiple_fields(self, doc_id: str, field_paths: List[str]) -> Dict[str, Any]:
        """Retrieve multiple fields from a document in a single operation."""
        logger.info(f"Retrieving multiple fields for document {doc_id}: {field_paths}")
        document = await self.collection.find_one({"_id": doc_id})
        
        if not document:
            logger.warning(f"Document with ID {doc_id} not found")
            return {
                "success": False,
                "fields": {},
                "message": f"Document with ID {doc_id} not found"
            }

        results = {
            "success": True,
            "fields": {},
            "message": f"Retrieved fields for document {doc_id}"
        }

        for field_path in field_paths:
            current = document
            fields = field_path.split('.')
            
            try:
                for field in fields:
                    current = current[field]
                results["fields"][field_path] = current
                logger.info(f"Retrieved {field_path} for document {doc_id}")
            except (KeyError, TypeError):
                results["success"] = False
                results["fields"][field_path] = None
                logger.warning(f"Field {field_path} not found for document {doc_id}")

        return results

    async def get_full_document(self, doc_id: str) -> Dict[str, Any]:
        """Retrieve the complete document."""
        logger.info(f"Retrieving full document for {doc_id}")
        document = await self.collection.find_one({"_id": doc_id})
        
        if document:
            logger.info(f"Successfully retrieved full document for {doc_id}")
            return {
                "success": True,
                "document": json.loads(json.dumps(document, default=self.json_encode)),
                "message": f"Retrieved full document for {doc_id}"
            }
        else:
            logger.warning(f"Document with ID {doc_id} not found")
            return {"success": False, "message": f"Document with ID {doc_id} not found"}

    async def get_all_field_paths(self, doc_id: str) -> Dict[str, Any]:
        """Get all field paths in a document, maintaining parent-child relationships."""
        logger.info(f"Retrieving all field paths for document {doc_id}")
        document = await self.collection.find_one({"_id": doc_id})
        
        if not document:
            logger.warning(f"Document with ID {doc_id} not found")
            return {"success": False, "message": f"Document with ID {doc_id} not found"}

        def extract_field_paths(obj: Any, prefix: str = "") -> List[str]:
            field_paths = []
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key != "_id":
                        full_key = f"{prefix}.{key}" if prefix else key
                        field_paths.append(full_key)
                        field_paths.extend(extract_field_paths(value, full_key))
            elif isinstance(obj, list) and obj:
                field_paths.extend(extract_field_paths(obj[0], f"{prefix}[0]"))
            return field_paths

        all_field_paths = extract_field_paths(document)
        
        logger.info(f"Successfully retrieved all field paths for document {doc_id}")
        return {
            "success": True,
            "field_paths": all_field_paths,
            "message": f"Retrieved all field paths for document {doc_id}"
        }

    async def delete_document(self, doc_id: str) -> Dict[str, Any]:
        """Delete a document by ID."""
        logger.info(f"Deleting document {doc_id}")
        result = await self.collection.delete_one({"_id": doc_id})
        
        if result.deleted_count == 0:
            logger.warning(f"Document {doc_id} not found")
            return {"success": False, "message": f"Document {doc_id} not found"}
        
        logger.info(f"Successfully deleted document {doc_id}")
        return {"success": True, "message": f"Deleted document {doc_id}"}

    async def find_documents(
        self, 
        query: Dict[str, Any], 
        skip: int = 0, 
        limit: int = 10, 
        sort: List[Tuple[str, int]] = None
    ) -> Dict[str, Any]:
        """
        Find documents matching query criteria with pagination support.
        
        Args:
            query: MongoDB query dictionary
            skip: Number of documents to skip
            limit: Maximum number of documents to return
            sort: List of (field, direction) tuples for sorting
        """
        logger.info(f"Finding documents with query: {query}, skip: {skip}, limit: {limit}, sort: {sort}")
        try:
            # Build the cursor
            cursor = self.collection.find(query)
            
            # Apply sorting if specified
            if sort:
                cursor = cursor.sort(sort)
            
            # Apply pagination
            cursor = cursor.skip(skip).limit(limit)
            
            # Get the documents
            documents = await cursor.to_list(length=limit)
            
            # Get total count for pagination
            total_count = await self.collection.count_documents(query)
            
            logger.info(f"Found {len(documents)} documents, total count: {total_count}")
            return {
                "success": True,
                "documents": json.loads(json.dumps(documents, default=self.json_encode)),
                "count": len(documents),
                "total_count": total_count,
                "has_more": total_count > (skip + limit),
                "message": f"Found {len(documents)} documents"
            }
        except Exception as e:
            logger.error(f"Failed to find documents: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to find documents: {str(e)}"
            }

    async def insert_json_file(self, file_path: str, doc_id: str = None) -> Dict[str, Any]:
        """
        Read a JSON file and insert it as a document into the collection.
        
        Args:
            file_path: Path to the JSON file
            doc_id: Optional document ID. If not provided, uses _id from JSON if present
            
        Returns:
            Dict containing success status and message
        """
        logger.info(f"Reading JSON file from: {file_path}")
        try:
            # Read the file
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            # Handle document ID
            if doc_id:
                data['_id'] = doc_id
            elif '_id' not in data:
                logger.warning("No _id provided in JSON or as parameter. MongoDB will generate one.")
            
            # Insert the document
            result = await self.collection.insert_one(data)
            
            logger.info(f"Successfully inserted document with ID: {result.inserted_id}")
            return {
                "success": True,
                "inserted_id": str(result.inserted_id),
                "message": f"Successfully inserted document from {file_path}"
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON file: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to parse JSON file: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Failed to insert document: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to insert document: {str(e)}"
            }

class MongoDBDatabaseManager:
    """Manager for the entire MongoDB database."""
    
    def __init__(self, username: str, password: str, host: str, port: str, db_name: str):
        """Initialize the database manager."""
        self.mongo_uri = f"mongodb://{username}:{password}@{host}:{port}/?authSource=admin"
        self.db_name = db_name
        self.client = None
        self.db = None
        self._collection_managers: Dict[str, MongoDBCollectionManager] = {}
        
        self.connect()

    async def drop_database(self) -> Dict[str, Any]:
        """Drop the entire database."""
        try:
            logger.warning(f"Dropping database: {self.db_name}")
            await self.client.drop_database(self.db_name)
            self._collection_managers.clear()  # Clear collection managers
            logger.info(f"Successfully dropped database: {self.db_name}")
            return {
                "success": True,
                "message": f"Dropped database: {self.db_name}"
            }
        except Exception as e:
            logger.error(f"Failed to drop database: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to drop database: {str(e)}"
            }

    def connect(self) -> None:
        """Establish connection to MongoDB."""
        try:
            self.client = AsyncIOMotorClient(self.mongo_uri)
            self.db = self.client[self.db_name]
            
            cyan = "\033[36m"
            reset = "\033[0m"
            logger.info(f"Successfully connected to MongoDB database: {cyan}{self.db_name}{reset}")
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise

    def get_collection(self, collection_name: str) -> MongoDBCollectionManager:
        """Get or create a collection manager."""
        if collection_name not in self._collection_managers:
            green = "\033[32m"
            reset = "\033[0m"
            logger.info(f"Creating manager for collection: {green}{collection_name}{reset}")
            self._collection_managers[collection_name] = MongoDBCollectionManager(self.db[collection_name])
        return self._collection_managers[collection_name]

    async def close(self) -> None:
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")


async def main():
    """Test cases for MongoDB manager methods."""
    print("\n=== MongoDB Manager Tests ===")
    
    db = MongoDBDatabaseManager(
        username="root",
        password="example",
        host="localhost",
        port="27017",
        db_name="test_db"
    )

    try:
        # Clean up before tests
        print("\n0. Cleaning up test environment:")
        drop_db_result = await db.drop_database()
        print(f"Drop database result: {drop_db_result}")
        
        test_collection = db.get_collection("test_collection")
        drop_collection_result = await test_collection.drop_collection()
        print(f"Drop collection result: {drop_collection_result}")

        # Create indexes for testing
        print("\n1. Testing index creation:")
        index_result = await test_collection.create_index([("name", 1)], unique=True)
        print(f"Create index result: {index_result}")
        
        indexes_result = await test_collection.list_indexes()
        print(f"List indexes result: {indexes_result}")

        # Test document creation
        print("\n2. Testing single document creation:")
        test_data = {
            "name": "Test User",
            "email": "test@example.com",
            "settings": {
                "theme": "light",
                "notifications": True
            },
            "preferences": {
                "language": "en",
                "timezone": "UTC"
            },
            "metadata": {
                "created_at": datetime.datetime.now()
            }
        }
        create_result = await test_collection.create_document("test_doc", test_data)
        print(f"Create result: {create_result}")

        # Test bulk document creation
        print("\n3. Testing bulk document creation:")
        bulk_data = [
            {"_id": "bulk1", "name": "Bulk User 1", "score": 85},
            {"_id": "bulk2", "name": "Bulk User 2", "score": 92}
        ]
        bulk_result = await test_collection.bulk_create(bulk_data)
        print(f"Bulk create result: {bulk_result}")

        # Test bulk update
        print("\n4. Testing bulk update:")
        bulk_updates = [
            {
                "filter": {"_id": "bulk1"},
                "update": {"score": 88},
                "upsert": False
            },
            {
                "filter": {"_id": "bulk2"},
                "update": {"score": 95},
                "upsert": False
            }
        ]
        bulk_update_result = await test_collection.bulk_update(bulk_updates)
        print(f"Bulk update result: {bulk_update_result}")

        # Test get_field
        print("\n5. Testing get_field:")
        field_result = await test_collection.get_field("test_doc", "settings.theme")
        print(f"Get field result: {field_result}")

        # Test update_field
        print("\n6. Testing update_field:")
        update_result = await test_collection.update_field("test_doc", "settings.theme", "dark")
        print(f"Update result: {update_result}")

        # Test update_multiple_fields
        print("\n7. Testing update_multiple_fields:")
        multi_update_result = await test_collection.update_multiple_fields(
            "test_doc",
            {
                "settings.theme": "light",
                "settings.notifications": False,
                "preferences.language": "es"
            }
        )
        print(f"Multiple fields update result: {multi_update_result}")

        # Test get_multiple_fields
        print("\n8. Testing get_multiple_fields:")
        multi_fields_result = await test_collection.get_multiple_fields(
            "test_doc", 
            ["name", "email", "settings.theme", "settings.notifications", "preferences.language"]
        )
        print(f"Multiple fields result: {multi_fields_result}")

        # Test find_documents with pagination
        print("\n9. Testing find_documents with pagination:")
        # First page
        query_result1 = await test_collection.find_documents(
            {"score": {"$gt": 80}}, 
            skip=0, 
            limit=1,
            sort=[("score", -1)]
        )
        print(f"Query result page 1: {query_result1}")
        
        # Second page
        query_result2 = await test_collection.find_documents(
            {"score": {"$gt": 80}}, 
            skip=1, 
            limit=1,
            sort=[("score", -1)]
        )
        print(f"Query result page 2: {query_result2}")

        # Test get_full_document
        print("\n10. Testing get_full_document:")
        full_doc_result = await test_collection.get_full_document("test_doc")
        print(f"Full document result: {full_doc_result}")

        # Test get_all_field_paths
        print("\n11. Testing get_all_field_paths:")
        paths_result = await test_collection.get_all_field_paths("test_doc")
        print(f"Field paths result: {paths_result}")

        # Test error cases
        print("\n12. Testing error cases:")
        # Test non-existent document
        error_result1 = await test_collection.get_field("non_existent_doc", "field")
        print(f"Error result (doc not found): {error_result1}")
        
        # Test invalid field path
        error_result2 = await test_collection.get_field("test_doc", "invalid.field.path")
        print(f"Error result (field not found): {error_result2}")
        
        # Test update multiple fields on non-existent document
        error_result3 = await test_collection.update_multiple_fields(
            "non_existent_doc",
            {"field1": "value1", "field2": "value2"}
        )
        print(f"Error result (update multiple - doc not found): {error_result3}")
        
        # Test duplicate key error
        error_result4 = await test_collection.create_document(
            "error_doc",
            {"name": "Test User"}  # Should fail due to unique index
        )
        print(f"Error result (duplicate key): {error_result4}")

        # Test document deletion
        print("\n13. Testing document deletion:")
        delete_result = await test_collection.delete_document("bulk1")
        print(f"Delete result: {delete_result}")
        verify_delete = await test_collection.get_full_document("bulk1")
        print(f"Verify deletion: {verify_delete}")

        # Final cleanup
        print("\n14. Final cleanup:")
        final_drop_coll = await test_collection.drop_collection()
        print(f"Final collection drop result: {final_drop_coll}")
        final_drop_db = await db.drop_database()
        print(f"Final database drop result: {final_drop_db}")

    finally:
        await db.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())