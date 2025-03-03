import packages
from configs import components
from toolkit.llm.llama_index import utils as utils_llama_index
from toolkit.utils.llm import main as utils_llm
from toolkit.llm.llama_index import cores, messages

from typing import Any, Dict, List
from pydantic import Field
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import datetime, json, yaml, asyncio
from loguru import logger


class VehicleDBManager:
    def __init__(self, username: str, password: str, host: str, port: str, db_name: str):
        self.mongo_uri = f"mongodb://{username}:{password}@{host}:{port}/?authSource=admin"
        self.db_name = db_name
        self.client = None
        self.db = None
        self.collection_vehicles = None
        
        # Connect to the database
        self.connect()
        logger.info(f"VehicleDBManager initialized with database: {db_name}")

    def connect(self):
        """Establish a connection to MongoDB."""
        try:
            self.client = AsyncIOMotorClient(self.mongo_uri)
            self.db = self.client[self.db_name]
            self.collection_vehicles = self.db['vehicles']
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise

    async def close(self):
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

    @staticmethod
    def json_encode(o):
        """Custom JSON encoder to handle ObjectId and datetime."""
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        raise TypeError(f"Object of type {type(o)} is not JSON serializable")

    async def update_field(self, vehicle_id: str, field_path: str, new_value: Any) -> Dict[str, Any]:
        """
        Update a specific field in the vehicle document.
        Returns success=True if the document was found and the field was set, 
        regardless of whether the value actually changed.
        """
        logger.info(f"Updating field {field_path} for vehicle {vehicle_id}")
        
        # First, check if the vehicle and field exist
        vehicle = await self.collection_vehicles.find_one({"vehicleId": vehicle_id})
        if not vehicle:
            logger.warning(f"Vehicle with ID {vehicle_id} not found")
            return {
                "success": False,
                "message": f"Vehicle with ID {vehicle_id} not found"
            }
        
        # Check if the field path exists by traversing the document
        current_obj = vehicle
        field_parts = field_path.split('.')
        
        # Traverse until the second-to-last part to check if the path exists
        for i, part in enumerate(field_parts[:-1]):
            if part not in current_obj:
                logger.warning(f"Field path {'.'.join(field_parts[:i+1])} does not exist for vehicle {vehicle_id}")
                return {
                    "success": False,
                    "message": f"Field path {field_path} does not exist in vehicle document"
                }
            current_obj = current_obj[part]
            
            # Check if we've hit a non-dictionary value in the middle of the path
            if not isinstance(current_obj, dict):
                logger.warning(f"Cannot traverse field path {field_path} at {'.'.join(field_parts[:i+1])}")
                return {
                    "success": False,
                    "message": f"Invalid field path {field_path}: cannot traverse through non-object value"
                }
        
        # Perform the update
        result = await self.collection_vehicles.update_one(
            {"vehicleId": vehicle_id},
            {"$set": {field_path: new_value}},
            upsert=False
        )
        
        if result.modified_count == 0:
            # Document was found but value wasn't modified (same value)
            logger.info(f"Field {field_path} set to same value for vehicle {vehicle_id}")
            return {
                "success": True,
                "message": f"Updated {field_path} for vehicle {vehicle_id}"
            }
        else:
            logger.info(f"Successfully updated {field_path} for vehicle {vehicle_id}")
            return {
                "success": True,
                "message": f"Updated {field_path} for vehicle {vehicle_id}"
            }

    async def get_field(self, vehicle_id: str, field_path: str) -> Dict[str, Any]:
        """Retrieve a specific field from the vehicle document."""
        logger.info(f"Retrieving field {field_path} for vehicle {vehicle_id}")
        vehicle = await self.collection_vehicles.find_one({"vehicleId": vehicle_id})
        if not vehicle:
            logger.warning(f"Vehicle with ID {vehicle_id} not found")
            return {
                "success": False,
                "message": f"Vehicle with ID {vehicle_id} not found"
            }

        # Split the field path and traverse the document
        fields = field_path.split('.')
        value = vehicle
        for field in fields:
            if isinstance(value, dict) and field in value:
                value = value[field]
            else:
                logger.warning(f"Field {field_path} not found for vehicle {vehicle_id}")
                return {
                    "success": False,
                    "message": f"Field {field_path} not found for vehicle {vehicle_id}"
                }

        logger.info(f"Successfully retrieved {field_path} for vehicle {vehicle_id}")
        return {
            "success": True,
            "value": value,
            "message": f"{field_path} for vehicle {vehicle_id}: {value}"
        }

    async def get_multiple_fields(self, vehicle_id: str, field_paths: List[str]) -> Dict[str, Any]:
        """
        Retrieve multiple fields from a vehicle document in a single operation.
        """
        logger.info(f"Retrieving multiple fields for vehicle {vehicle_id}: {field_paths}")
        
        # First get the vehicle document
        vehicle = await self.collection_vehicles.find_one({"vehicleId": vehicle_id})
        if not vehicle:
            logger.warning(f"Vehicle with ID {vehicle_id} not found")
            return {
                "success": False,
                "fields": {},
                "message": f"Vehicle with ID {vehicle_id} not found"
            }
        
        # Initialize results dictionary
        results = {
            "success": True,
            "fields": {},
            "message": f"Retrieved fields for vehicle {vehicle_id}"
        }
        
        all_fields_found = True
        
        # Process each field path
        for field_path in field_paths:
            # Split the field path and traverse the document
            current = vehicle
            valid_path = True
            
            # Handle array indexing and nested fields
            parts = field_path.split('.')
            for i, part in enumerate(parts):
                # Check for array index notation
                if '[' in part and ']' in part:
                    try:
                        # Split into array name and index
                        array_name = part[:part.index('[')]
                        index = int(part[part.index('[')+1:part.index(']')])
                        
                        # Check if array exists and has enough elements
                        if (array_name in current and 
                            isinstance(current[array_name], list) and 
                            len(current[array_name]) > index):
                            current = current[array_name][index]
                        else:
                            valid_path = False
                            break
                    except (ValueError, IndexError):
                        valid_path = False
                        break
                elif part in current:
                    current = current[part]
                else:
                    valid_path = False
                    break
            
            # Add the field value to results
            if valid_path:
                # Handle special MongoDB types
                if isinstance(current, (ObjectId, datetime.datetime)):
                    current = self.json_encode(current)
                    
                results["fields"][field_path] = current
                logger.info(f"Retrieved {field_path} for vehicle {vehicle_id}: {current}")
            else:
                all_fields_found = False
                results["fields"][field_path] = None
                logger.warning(f"Field {field_path} not found for vehicle {vehicle_id}")
        
        # Update success status
        results["success"] = all_fields_found
        if not all_fields_found:
            results["message"] = f"Some fields were not found for vehicle {vehicle_id}"
            
        logger.info(f"Successfully retrieved multiple fields for vehicle {vehicle_id}")
        return results

    async def get_full_document(self, vehicle_id: str) -> Dict[str, Any]:
        """Retrieve the full document for a vehicle."""
        logger.info(f"Retrieving full document for vehicle {vehicle_id}")
        vehicle = await self.collection_vehicles.find_one({"vehicleId": vehicle_id})
        if vehicle:
            logger.info(f"Successfully retrieved full document for vehicle {vehicle_id}")
            return {
                "success": True,
                "document": json.loads(json.dumps(vehicle, default=self.json_encode)),
                "message": f"Retrieved full document for vehicle {vehicle_id}"
            }
        else:
            logger.warning(f"Vehicle with ID {vehicle_id} not found")
            return {
                "success": False,
                "message": f"Vehicle with ID {vehicle_id} not found"
            }

    async def get_all_field_paths(self, vehicle_id: str) -> Dict[str, Any]:
        """
        Retrieve all field paths of the document for a vehicle, maintaining the parent-child relationship.
        """
        logger.info(f"Retrieving all field paths for vehicle {vehicle_id}")
        vehicle = await self.collection_vehicles.find_one({"vehicleId": vehicle_id})
        
        if not vehicle:
            logger.warning(f"Vehicle with ID {vehicle_id} not found")
            return {
                "success": False,
                "message": f"Vehicle with ID {vehicle_id} not found"
            }
        
        def extract_field_paths(obj: Any, prefix: str = "") -> List[str]:
            field_paths = []
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key != "_id":  # Exclude MongoDB-specific fields
                        full_key = f"{prefix}.{key}" if prefix else key
                        field_paths.append(full_key)
                        field_paths.extend(extract_field_paths(value, full_key))
            elif isinstance(obj, list) and obj:
                # For lists, we'll just process the first item to get the structure
                field_paths.extend(extract_field_paths(obj[0], f"{prefix}[0]"))
            return field_paths

        all_field_paths = extract_field_paths(vehicle)
        
        logger.info(f"Successfully retrieved all field paths for vehicle {vehicle_id}")
        return {
            "success": True,
            "field_paths": all_field_paths,
            "message": f"Retrieved all field paths for vehicle {vehicle_id}"
        }
    
    async def add_alert(self, vehicle_id: str, alert_type: str, message: str, severity: str) -> Dict[str, Any]:
        """Add a new alert to the vehicle document."""
        logger.info(f"Adding new alert for vehicle {vehicle_id}")
        new_alert = {
            "type": alert_type,
            "message": message,
            "severity": severity,
            "timestamp": datetime.datetime.now(),
            "acknowledged": False
        }
        result = await self.collection_vehicles.update_one(
            {"vehicleId": vehicle_id},
            {"$push": {"alerts": new_alert}}
        )
        if result.matched_count == 0:
            logger.warning(f"Vehicle with ID {vehicle_id} not found")
            return {
                "success": False,
                "message": f"Vehicle with ID {vehicle_id} not found"
            }
        elif result.modified_count == 0:
            logger.warning(f"Failed to add alert for vehicle {vehicle_id}")
            return {
                "success": False,
                "message": f"Failed to add alert for vehicle {vehicle_id}. The document was not modified."
            }
        else:
            logger.info(f"Successfully added new alert for vehicle {vehicle_id}")
            return {
                "success": True,
                "message": f"Added new alert for vehicle {vehicle_id}"
            }

    async def acknowledge_alert(self, vehicle_id: str, alert_index: int) -> Dict[str, Any]:
        """Acknowledge an alert in the vehicle document."""
        logger.info(f"Acknowledging alert at index {alert_index} for vehicle {vehicle_id}")
        result = await self.collection_vehicles.update_one(
            {"vehicleId": vehicle_id},
            {"$set": {f"alerts.{alert_index}.acknowledged": True}}
        )
        if result.matched_count == 0:
            logger.warning(f"Vehicle with ID {vehicle_id} not found")
            return {
                "success": False,
                "message": f"Vehicle with ID {vehicle_id} not found"
            }
        elif result.modified_count == 0:
            logger.warning(f"Failed to acknowledge alert for vehicle {vehicle_id}")
            return {
                "success": False,
                "message": f"Failed to acknowledge alert for vehicle {vehicle_id}. The alert may not exist or is already acknowledged."
            }
        else:
            logger.info(f"Successfully acknowledged alert at index {alert_index} for vehicle {vehicle_id}")
            return {
                "success": True,
                "message": f"Acknowledged alert at index {alert_index} for vehicle {vehicle_id}"
            }

    async def parse_user_query(
        self, 
        user_query: str = Field(description="User input into the tool")
    ) -> Dict[str, Any]:
        """Parse user input to determine the intended action and extract relevant information."""

        with open(f"{packages.APP_PATH}/features/agents/car/prompts.yaml", 'r') as file:
            prompts_agent_car = yaml.safe_load(file)

        logger.info(f"Parsing user query: {user_query}")
        
        if "llama" in dict(cores.Settings.llm)["model"]:
            prompt_parse_user_input = prompts_agent_car["control"]["ParseUserInput"]["llama"]
        else: # TODO
            prompt_parse_user_input = prompts_agent_car["control"]["ParseUserInput"]["llama"]

        examples = prompts_agent_car["control"]["ParseUserInput"]["examples"]
        examples = await utils_llm.convert_examples_to_string(examples)
        
        field_paths = await utils_llama_index.extract_retriever_results(
            await components.retriever_car_info_field_paths.aretrieve(user_query)
        )
        fields_and_values = await self.get_multiple_fields("v123", field_paths)
        fields_and_values = fields_and_values["fields"]

        prompt_tpl_parse_user_input = messages.PromptTemplate(prompt_parse_user_input)

        msg_parse_user_input = messages.ChatMessage(
            role="user",
            content=prompt_tpl_parse_user_input.format(
                user_query=user_query,
                fields_and_values=fields_and_values,
                examples=examples,
            )
        )

        # Use the async chat method
        result = await cores.Settings.llm.achat([msg_parse_user_input])
        result_content = result.message.content
        result_parsed = await utils_llm.parse_json(result_content)
        
        logger.info(f"Parsed user query result: {result_parsed}")
        return result_parsed
    
    async def execute_db_operation(self, parsed_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the appropriate database operation based on the parsed user input."""
        action = parsed_input.get('action')
        vehicle_id = parsed_input.get('vehicle_id')
        logger.info(f"Executing database operation: {action} for vehicle {vehicle_id}")

        if action == 'get':
            return await self.get_field(vehicle_id, parsed_input['field_path'])
        elif action == 'update':
            return await self.update_field(vehicle_id, parsed_input['field_path'], parsed_input['new_value'])
        elif action == 'full_document':
            return await self.get_full_document(vehicle_id)
        elif action == 'add_alert':
            return await self.add_alert(vehicle_id, parsed_input['alert_type'], parsed_input['message'], parsed_input['severity'])
        elif action == 'acknowledge_alert':
            return await self.acknowledge_alert(vehicle_id, parsed_input['alert_index'])
        else:
            logger.warning(f"Unsupported action: {action}")
            return {'success': False, 'message': f"Unsupported action: {action}"}
    
    @staticmethod
    async def format_response(operation_result: Dict[str, Any]) -> str:
        """Format the database operation result into a user-friendly response."""
        if operation_result['success']:
            if 'document' in operation_result:
                return f"Operation successful. {operation_result['message']}\nFull document: {json.dumps(operation_result['document'], indent=2)}"
            elif 'value' in operation_result:
                return f"Operation successful. {operation_result['message']}\nValue: {operation_result['value']}"
            else:
                return f"Operation successful. {operation_result['message']}"
        else:
            return f"Operation failed. {operation_result['message']}"

    async def process_user_query(
        self, 
        input: str = Field(..., description="Full natural user input to be processed."),
        **kwargs,
    ):
        """Main function that processes user input, executes database operations, and returns a formatted response."""
        try:
            logger.info(f"Processing user query: {input}")
            parsed_input = await self.parse_user_query(input)
            operation_result = await self.execute_db_operation(parsed_input)
            formatted_response = await self.format_response(operation_result)
            logger.info(f"User query processed successfully: {formatted_response}")
            return parsed_input, operation_result
        except Exception as e:
            logger.exception(f"An error occurred while processing user query: {str(e)}")
            return f"An error occurred while processing your request: {str(e)}"

# Initialize the database manager
db_mongo_vehicle = VehicleDBManager(
    username="root",
    password="example",
    host="localhost",
    port="27017",
    db_name="car_control_app"
)

# Example usage:
async def main():
    # Example user inputs
    user_query = [
        "Get the driver's temperature setting for vehicle v123",
        "Update the driver's temperature to 23.5 degrees for vehicle v123",
        "Add a maintenance alert for an oil change for vehicle v123",
        "Acknowledge the first alert for vehicle v123",
        "Get the full document for vehicle v123",
    ]

    try:
        # Process each user input
        for input_text in user_query:
            print(f"User Input: {input_text}")
            result = await db_mongo_vehicle.process_user_query(input_text)
            print(f"Result: {result}\n")
    finally:
        # Close the connection
        await db_mongo_vehicle.close()

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())