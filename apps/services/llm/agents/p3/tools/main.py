import requests
import urllib
import os
import logging
from typing import Dict, List, Optional, Union, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)

# Constants
ENERGYSTACKS_BASE_URL = os.getenv('ENERGY_STACKS_BASE_URL', 'https://api.energystacks.com/')

class ChargingStationTools:
    """
    Class that provides methods for interacting with charging stations through the EnergyStacks API.
    """
    
    def __init__(self, base_url: str = None):
        """
        Initialize the ChargingStationTools with the API base URL.
        
        Args:
            base_url (str, optional): The base URL for the EnergyStacks API. 
                                     Defaults to the value from environment variables.
        """
        self.base_url = base_url or ENERGYSTACKS_BASE_URL
        logger.info(f"Initialized ChargingStationTools with base URL: {self.base_url}")
    
    async def unlock_charging_connector(self, identityKey: str, connectorId: str) -> Dict[str, Any]:
        """
        Send a request to unlock the charging connector.
        
        Args:
            identityKey (str): The unique identifier for the customer
            connectorId (str): The ID of the connector to unlock.
            
        Returns:
            Dict[str, Any]: The response from the unlock connector request.
        """
        logger.info(f"Attempting to unlock connector {connectorId} on station {identityKey}")
        
        try:
            # Getting OCPP Version as this defines the endpoint we need to use
            result = requests.get(f"{self.base_url}chargingstations/{urllib.parse.quote(identityKey)}")
            result.raise_for_status()
            
            ocpp_protocol = result.json()['shadow']['ocppProtocol']
            logger.debug(f"Station uses OCPP protocol: {ocpp_protocol}")
            
            # Switch Casing about the OCPP Version and the corresponding endpoint
            if ocpp_protocol == "V_16":
                # Convert connector ID to string if it's not already
                connectorId = str(connectorId)
                
                # Make the unlock request
                unlock_url = f"{self.base_url}management/v16/chargingstations/{urllib.parse.quote(identityKey)}/unlockConnector"
                unlock_params = {"connectorId": connectorId}
                
                unlock_result = requests.post(unlock_url, json=unlock_params)
                unlock_result.raise_for_status()
                
                return {
                    "success": True,
                    "message": "Connector unlock request sent successfully",
                    "details": unlock_result.json() if unlock_result.content else {}
                }
            else:
                return {
                    "success": False, 
                    "message": f"Unsupported OCPP protocol: {ocpp_protocol}",
                    "details": {}
                }
                
        except requests.RequestException as e:
            logger.error(f"Error unlocking connector: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to unlock connector: {str(e)}",
                "details": {"error": str(e)}
            }

    async def restart_chargingstation(self, evseId: str) -> Dict[str, Any]:
        """
        Attempts to restart the charging station identified by the given evseId.

        This function is used to resolve operational issues by restarting a charging station.
        It requires an evseId, which is a unique identifier for the charging station.
        
        Args:
            evseId (str): The unique identifier for the charging station to be restarted.

        Returns:
            Dict[str, Any]: A dictionary with the status and details of the restart operation.
        """
        logger.info(f"Attempting to restart charging station with EVSE ID: {evseId}")
        
        try:
            # Prepare reset parameters
            reset_params = {"type": "Soft"}
            
            # First, get the identityKey using the EVSE ID
            connector_url = f"{self.base_url}shadow/connectors/{urllib.parse.quote(str(evseId))}"
            connector_response = requests.get(connector_url)
            connector_response.raise_for_status()
            
            identity_key = connector_response.json().get("identityKey")
            if not identity_key:
                return {
                    "success": False,
                    "message": f"Could not retrieve identity key for EVSE ID: {evseId}",
                    "details": {}
                }
            
            # Send the reset request
            reset_url = f"{self.base_url}management/v16/chargingstations/{identity_key}/reset"
            reset_response = requests.post(reset_url, json=reset_params)
            reset_response.raise_for_status()
            
            return {
                "success": True,
                "message": f"Successfully initiated restart for charging station with EVSE ID: {evseId}",
                "details": reset_response.json() if reset_response.content else {}
            }
            
        except requests.RequestException as e:
            logger.error(f"Error restarting charging station: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to restart charging station: {str(e)}",
                "details": {"error": str(e)}
            }

    async def start_charging_transaction(self, evseId: str, tokenId: str) -> Dict[str, Any]:
        """
        Initiates a charging session at the specified charging station using a user identification token.

        This function is responsible for starting a new charging transaction at a charging station identified by evseId.
        It requires a tokenId, which represents the RFID card associated with the user attempting to start the session.
        
        Args:
            evseId (str): The unique identifier for the charging station where the transaction will be initiated.
            tokenId (str): The RFID card identifier used to authenticate the user.

        Returns:
            Dict[str, Any]: A dictionary with the status and details of the transaction initiation.
        """
        logger.info(f"Attempting to start charging transaction at EVSE ID: {evseId} with token ID: {tokenId}")
        
        try:
            # First, get the identityKey using the EVSE ID
            connector_url = f"{self.base_url}shadow/connectors/{urllib.parse.quote(str(evseId))}"
            connector_response = requests.get(connector_url)
            connector_response.raise_for_status()
            
            identity_key = connector_response.json().get("identityKey")
            if not identity_key:
                return {
                    "success": False,
                    "message": f"Could not retrieve identity key for EVSE ID: {evseId}",
                    "details": {}
                }
            
            # Prepare the remote start transaction request
            start_transaction_params = {
                "idTag": tokenId,
                "connectorId": 1  # Default to connector ID 1, could be parameterized if needed
            }
            
            # Send the remote start transaction request
            start_url = f"{self.base_url}management/v16/chargingstations/{identity_key}/remoteStartTransaction"
            start_response = requests.post(start_url, json=start_transaction_params)
            start_response.raise_for_status()
            
            return {
                "success": True,
                "message": f"Successfully initiated charging transaction at EVSE ID: {evseId}",
                "details": start_response.json() if start_response.content else {}
            }
            
        except requests.RequestException as e:
            logger.error(f"Error starting charging transaction: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to start charging transaction: {str(e)}",
                "details": {"error": str(e)}
            }

    async def get_chargingstation_status(self, evseId: str) -> Dict[str, Any]:
        """
        Retrieves the current operational status of the specified charging station.

        This function is used to check the current status of a charging station identified by evseId.
        It provides information on whether the station is operational, occupied, or experiencing any issues.
        
        Args:
            evseId (str): The unique identifier for the charging station whose status is being queried.
                          The evseId is formatted like regex [A-Z]{2}*[A-Z0-9]{3}*[A-Z0-9]{1,20}

        Returns:
            Dict[str, Any]: A dictionary with the charging station information, especially focusing on
                           'online' and 'chargingStatusStatus' fields.
        """
        logger.info(f"Retrieving status for charging station with EVSE ID: {evseId}")
        
        try:
            # First, get the identityKey using the EVSE ID
            connector_url = f"{self.base_url}shadow/connectors/{urllib.parse.quote(str(evseId))}"
            connector_response = requests.get(connector_url)
            connector_response.raise_for_status()
            
            identity_key = connector_response.json().get("identityKey")
            if not identity_key:
                return {
                    "success": False,
                    "message": f"Could not retrieve identity key for EVSE ID: {evseId}",
                    "details": {}
                }
            
            # Get the charging station information
            station_url = f"{self.base_url}chargingstations/{identity_key}"
            station_response = requests.get(station_url)
            station_response.raise_for_status()
            
            station_info = station_response.json()
            
            # Extract key status information
            status_info = {
                "success": True,
                "message": "Successfully retrieved charging station status",
                "station_info": {
                    "evseId": evseId,
                    "online": station_info.get("shadow", {}).get("online", False),
                    "status": station_info.get("shadow", {}).get("chargingStatusStatus", "Unknown"),
                    "lastHeartbeat": station_info.get("shadow", {}).get("lastHeartbeat", None),
                    "connectors": station_info.get("shadow", {}).get("connectors", [])
                },
                "full_details": station_info
            }
            
            return status_info
            
        except requests.RequestException as e:
            logger.error(f"Error retrieving charging station status: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to retrieve charging station status: {str(e)}",
                "details": {"error": str(e)}
            }

    async def get_chargingstation_transactions(self, evseId: str) -> Dict[str, Any]:
        """
        Retrieves the last ten transactions of the specified charging station.
        
        This function should only be called when the user specifically asks for their last transactions.
        It provides information on charging station usage.

        Args:
            evseId (str): The unique identifier for the charging station.

        Returns:
            Dict[str, Any]: A dictionary with information about the last ten transactions,
                           including transaction IDs and start timestamps.
        """
        logger.info(f"Retrieving last 10 transactions for charging station with EVSE ID: {evseId}")
        
        try:
            # First, get the identityKey using the EVSE ID
            connector_url = f"{self.base_url}shadow/connectors/{urllib.parse.quote(str(evseId))}"
            connector_response = requests.get(connector_url)
            connector_response.raise_for_status()
            
            identity_key = connector_response.json().get("identityKey")
            if not identity_key:
                return {
                    "success": False,
                    "message": f"Could not retrieve identity key for EVSE ID: {evseId}",
                    "transactions": []
                }
            
            # Get the transactions
            transactions_url = f"{self.base_url}shadow/transactions/search?page=0&size=10&sort=string&includeMeterValues=false&includeTransactionData=false"
            transactions_response = requests.get(transactions_url)
            transactions_response.raise_for_status()
            
            transactions_data = transactions_response.json()
            
            # Extract key transaction information
            results = []
            if "content" in transactions_data:
                for item in transactions_data["content"]:
                    results.append({
                        "transactionId": item.get("transactionId"),
                        "timestampStart": item.get("timestampStart"),
                        "timestampStop": item.get("timestampStop", None),
                        "meterStart": item.get("meterStart", 0),
                        "meterStop": item.get("meterStop", 0),
                        "connectorId": item.get("connectorId", None)
                    })
            
            return {
                "success": True,
                "message": f"Successfully retrieved transactions for charging station with EVSE ID: {evseId}",
                "transactions": results,
                "total": len(results)
            }
            
        except requests.RequestException as e:
            logger.error(f"Error retrieving charging station transactions: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to retrieve charging station transactions: {str(e)}",
                "transactions": []
            }


# Create a singleton instance of the ChargingStationTools class
charging_station_tools = ChargingStationTools()
