import packages
from context.utils import consts as c

from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from loguru import logger
import redis
import json
import os
import pickle
import datetime
from redis.client import Pipeline
from redis.exceptions import RedisError


@dataclass
class RedisConfig:
    """Configuration for Redis connection.
    
    Attributes:
        host: Redis server hostname
        port: Redis server port
        db: Redis database number
        password: Authentication password
        socket_timeout: Socket timeout in seconds
        max_connections: Maximum number of connections in the pool
        retry_on_timeout: Whether to retry on timeout
        health_check_interval: Interval for health checks in seconds
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries in seconds
        encoding: Character encoding for string operations
    """
    # host: str = 'localhost'
    host: str = 'localhost' if not os.environ.get("IN_PROD", None) else 'redis'
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    socket_timeout: int = 5
    max_connections: int = 10
    retry_on_timeout: bool = True
    health_check_interval: int = 30
    max_retries: int = 3
    retry_delay: int = 1
    encoding: str = 'utf-8'


class RedisNamespaceManager:
    """Manager for a specific Redis namespace (key prefix)."""
    
    def __init__(self, redis_client: redis.Redis, namespace: str):
        """Initialize namespace manager.
        
        Args:
            redis_client: Redis client instance
            namespace: Namespace prefix for keys
        """
        self.redis = redis_client
        self.namespace = namespace
        self.binary_redis = redis.Redis(
            connection_pool=redis_client.connection_pool,
            decode_responses=False
        )

    def _make_key(self, key: str) -> str:
        """Create namespaced key."""
        return f"{self.namespace}:{key}"

    async def set_value(self, key: str, value: Any, expiry: Optional[int] = None) -> Dict[str, Any]:
        """Set a key-value pair with optional expiry."""
        try:
            full_key = self._make_key(key)
            logger.info(f"Setting {c.CLR_TERM.ORANGE}{value}{c.CLR_TERM.RESET} for key: "
                        f"{c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET}")
            
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            
            self.redis.set(full_key, value, ex=expiry)
            logger.info(f"Successfully set {c.CLR_TERM.ORANGE}{value}{c.CLR_TERM.RESET} for key: "
                        f"{c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET}")
            return {"success": True, "message": f"Set value for key: {key}"}
        except Exception as e:
            logger.error(f"Failed to set {c.CLR_TERM.ORANGE}{value}{c.CLR_TERM.RESET}: {str(e)}")
            return {"success": False, "message": f"Failed to set value: {str(e)}"}

    async def get_value(self, key: str) -> Dict[str, Any]:
        """Get value for a key."""
        try:
            full_key = self._make_key(key)
            logger.info(f"Getting value for key: {c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET}")
            
            value = self.redis.get(full_key)
            if value is None:
                logger.warning(f"Key not found: {c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET}")
                return {"success": False, "message": f"Key not found: {key}"}
            
            try:
                value = json.loads(value)
            except (json.JSONDecodeError, TypeError):
                pass
                
            logger.info(f"Successfully retrieved value for key: {c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET}")
            return {
                "success": True,
                "value": value,
                "message": f"Retrieved value for key: {key}"
            }
        except Exception as e:
            logger.error(f"Failed to get value: {str(e)}")
            return {"success": False, "message": f"Failed to get value: {str(e)}"}

    async def delete_key(self, key: str) -> Dict[str, Any]:
        """Delete a key."""
        try:
            full_key = self._make_key(key)
            logger.info(f"Deleting key: {c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET}")
            
            result = self.redis.delete(full_key)
            if result == 0:
                logger.warning(f"Key not found: {c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET}")
                return {"success": False, "message": f"Key not found: {key}"}
                
            logger.info(f"Successfully deleted key: {c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET}")
            return {"success": True, "message": f"Deleted key: {key}"}
        except Exception as e:
            logger.error(f"Failed to delete key: {str(e)}")
            return {"success": False, "message": f"Failed to delete key: {str(e)}"}

    async def set_hash(self, key: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Set multiple hash fields."""
        try:
            full_key = self._make_key(key)
            logger.info(f"Setting hash fields for key: {c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET}")
            
            # Convert complex values to JSON
            processed_fields = {}
            for k, v in fields.items():
                try:
                    processed_fields[k] = json.dumps(v) if isinstance(v, (dict, list)) else str(v)
                except (TypeError, ValueError) as e:
                    logger.error(f"Failed to process field {k}: {str(e)}")
                    return {"success": False, "message": f"Failed to process field {k}: {str(e)}"}
            
            # Use hset instead of deprecated hmset
            self.redis.hset(full_key, mapping=processed_fields)
            logger.info(f"Successfully set hash fields for key: {c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET}")
            return {
                "success": True,
                "message": f"Set {len(fields)} hash fields for key: {key}"
            }
        except Exception as e:
            logger.error(f"Failed to set hash fields: {str(e)}")
            return {"success": False, "message": f"Failed to set hash fields: {str(e)}"}

    async def get_hash_fields(self, key: str, fields: List[str]) -> Dict[str, Any]:
        """Get multiple hash fields."""
        try:
            full_key = self._make_key(key)
            logger.info(f"Getting hash fields for key: {c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET}")
            
            values = self.redis.hmget(full_key, fields)
            if all(v is None for v in values):
                logger.warning(f"Hash key not found: {c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET}")
                return {"success": False, "message": f"Hash key not found: {key}"}
            
            # Process values, attempting JSON decoding
            result = {}
            for field, value in zip(fields, values):
                if value is not None:
                    try:
                        result[field] = json.loads(value)
                    except (json.JSONDecodeError, TypeError):
                        result[field] = value
                else:
                    result[field] = None
            
            logger.info(f"Successfully retrieved hash fields for key: {c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET}")
            return {
                "success": True,
                "fields": result,
                "message": f"Retrieved hash fields for key: {key}"
            }
        except Exception as e:
            logger.error(f"Failed to get hash fields: {str(e)}")
            return {"success": False, "message": f"Failed to get hash fields: {str(e)}"}

    async def increment(self, key: str, amount: int = 1) -> Dict[str, Any]:
        """Increment a numeric value."""
        try:
            full_key = self._make_key(key)
            logger.info(f"Incrementing key: {c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET} by {amount}")
            
            result = self.redis.incrby(full_key, amount)
            logger.info(f"Successfully incremented key: {c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET}")
            return {
                "success": True,
                "value": result,
                "message": f"Incremented key: {key} by {amount}"
            }
        except Exception as e:
            logger.error(f"Failed to increment value: {str(e)}")
            return {"success": False, "message": f"Failed to increment value: {str(e)}"}

    async def add_to_set(self, key: str, *members: Any) -> Dict[str, Any]:
        """Add members to a set."""
        try:
            full_key = self._make_key(key)
            logger.info(f"Adding members to set: {c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET}")
            
            # Convert complex objects to JSON
            processed_members = [
                json.dumps(m) if isinstance(m, (dict, list)) else str(m)
                for m in members
            ]
            
            added_count = self.redis.sadd(full_key, *processed_members)
            logger.info(f"Successfully added {added_count} members to set: {c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET}")
            return {
                "success": True,
                "added_count": added_count,
                "message": f"Added {added_count} members to set: {key}"
            }
        except Exception as e:
            logger.error(f"Failed to add to set: {str(e)}")
            return {"success": False, "message": f"Failed to add to set: {str(e)}"}

    async def get_set_members(self, key: str) -> Dict[str, Any]:
        """Get all members of a set."""
        try:
            full_key = self._make_key(key)
            logger.info(f"Getting set members for: {c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET}")
            
            members = self.redis.smembers(full_key)
            if not members:
                logger.warning(f"Set not found or empty: {c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET}")
                return {
                    "success": False,
                    "message": f"Set not found or empty: {key}"
                }
            
            # Process members, attempting JSON decoding
            processed_members = []
            for member in members:
                try:
                    processed_members.append(json.loads(member))
                except (json.JSONDecodeError, TypeError):
                    processed_members.append(member)
            
            logger.info(f"Successfully retrieved {len(processed_members)} set members")
            return {
                "success": True,
                "members": processed_members,
                "message": f"Retrieved {len(processed_members)} set members"
            }
        except Exception as e:
            logger.error(f"Failed to get set members: {str(e)}")
            return {"success": False, "message": f"Failed to get set members: {str(e)}"}

    async def add_to_sorted_set(
        self,
        key: str,
        member_scores: Dict[Any, float]
    ) -> Dict[str, Any]:
        """Add members with scores to a sorted set."""
        try:
            full_key = self._make_key(key)
            logger.info(f"Adding scored members to: {c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET}")
            
            # Process members with error handling
            mapping = {}
            processed_count = 0
            for member, score in member_scores.items():
                try:
                    # Handle member serialization
                    if isinstance(member, str):
                        try:
                            json.loads(member)  # Validate if it's already JSON
                            key = member
                        except json.JSONDecodeError:
                            key = json.dumps(member)
                    else:
                        key = json.dumps(member) if isinstance(member, (dict, list)) else str(member)
                    
                    # Validate score
                    if not isinstance(score, (int, float)):
                        raise ValueError(f"Score must be a number, got {type(score)}")
                    
                    mapping[key] = float(score)
                    processed_count += 1
                except (TypeError, ValueError) as e:
                    logger.error(f"Failed to process member {member}: {str(e)}")
                    return {"success": False, "message": f"Failed to process member: {str(e)}"}
            
            added_count = self.redis.zadd(full_key, mapping)
            logger.info(f"Successfully added {added_count} members to sorted set")
            return {
                "success": True,
                "added_count": added_count,
                "message": f"Added {added_count} members to sorted set: {key}"
            }
        except Exception as e:
            logger.error(f"Failed to add to sorted set: {str(e)}")
            return {"success": False, "message": f"Failed to add to sorted set: {str(e)}"}

    async def get_sorted_set_range(
        self,
        key: str,
        start: int = 0,
        end: int = -1,
        desc: bool = False,
        withscores: bool = True
    ) -> Dict[str, Any]:
        """Get range of members from sorted set."""
        try:
            full_key = self._make_key(key)
            logger.info(f"Getting range from sorted set: {c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET}")
            
            if desc:
                results = self.redis.zrevrange(full_key, start, end, withscores=withscores)
            else:
                results = self.redis.zrange(full_key, start, end, withscores=withscores)
                
            if not results:
                logger.warning(f"Sorted set not found or empty: {c.CLR_TERM.GREEN}{full_key}{c.CLR_TERM.RESET}")
                return {
                    "success": False,
                    "message": f"Sorted set not found or empty: {key}"
                }
            
            # Get results with proper type handling
            if desc:
                raw_results = self.redis.zrevrange(full_key, start, end, withscores=withscores, score_cast_func=float)
            else:
                raw_results = self.redis.zrange(full_key, start, end, withscores=withscores, score_cast_func=float)
                
            processed_results = []
            if withscores:
                for member, score in raw_results:
                    try:
                        processed_member = json.loads(member)
                    except (json.JSONDecodeError, TypeError):
                        processed_member = member
                    processed_results.append({
                        "member": processed_member,
                        "score": score
                    })
            else:
                for member in raw_results:
                    try:
                        processed_results.append(json.loads(member))
                    except (json.JSONDecodeError, TypeError):
                        processed_results.append(member)
            
            logger.info(f"Successfully retrieved {len(processed_results)} members")
            return {
                "success": True,
                "members": processed_results,
                "message": f"Retrieved {len(processed_results)} members from sorted set: {key}"
            }
        except Exception as e:
            logger.error(f"Failed to get sorted set range: {str(e)}")
            return {"success": False, "message": f"Failed to get sorted set range: {str(e)}"}

    async def bulk_set(self, items: Dict[str, Any]) -> Dict[str, Any]:
        """Set multiple key-value pairs in a single operation."""
        try:
            logger.info(f"Performing bulk set for {len(items)} items")
            pipe: Pipeline = self.redis.pipeline()
            
            for key, value in items.items():
                full_key = self._make_key(key)
                try:
                    if isinstance(value, (dict, list)):
                        value = json.dumps(value)
                    pipe.set(full_key, value)
                except (TypeError, ValueError) as e:
                    logger.error(f"Failed to process item {key}: {str(e)}")
                    return {"success": False, "message": f"Failed to process item {key}: {str(e)}"}
            
            pipe.execute()
            logger.info(f"Successfully performed bulk set")
            return {
                "success": True,
                "message": f"Set {len(items)} items"
            }
        except Exception as e:
            logger.error(f"Failed to perform bulk set: {str(e)}")
            return {"success": False, "message": f"Failed to perform bulk set: {str(e)}"}


class RedisDatabaseManager:
    """Manager for the entire Redis database."""
    
    def __init__(self, config: Optional[RedisConfig] = None):
        """Initialize the database manager."""
        self.config = config or RedisConfig()
        self._namespace_managers: Dict[str, RedisNamespaceManager] = {}
        self.client = None
        self.connection_pool = None
        
        self.connect()

    def connect(self) -> None:
        """Establish connection to Redis."""
        try:
            self.connection_pool = redis.ConnectionPool(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                decode_responses=True,
                socket_timeout=self.config.socket_timeout,
                max_connections=self.config.max_connections,
                retry_on_timeout=self.config.retry_on_timeout,
                encoding=self.config.encoding
            )
            
            self.client = redis.Redis(connection_pool=self.connection_pool)
            
            cyan = "\033[36m"
            reset = "\033[0m"
            logger.info(f"Successfully connected to Redis database: {cyan}{self.config.db}{reset}")
            
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            raise

    def get_namespace(self, namespace: str) -> RedisNamespaceManager:
        """Get or create a namespace manager."""
        if namespace not in self._namespace_managers:
            green = "\033[32m"
            reset = "\033[0m"
            logger.info(f"Creating manager for namespace: {green}{namespace}{reset}")
            self._namespace_managers[namespace] = RedisNamespaceManager(self.client, namespace)
        return self._namespace_managers[namespace]

    async def flush_database(self) -> Dict[str, Any]:
        """Clear the entire database."""
        try:
            logger.warning(f"Flushing database: {self.config.db}")
            self.client.flushdb()
            self._namespace_managers.clear()
            logger.info(f"Successfully flushed database: {self.config.db}")
            return {
                "success": True,
                "message": f"Flushed database: {self.config.db}"
            }
        except Exception as e:
            logger.error(f"Failed to flush database: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to flush database: {str(e)}"
            }

    def close(self) -> None:
        """Close the Redis connection."""
        if self.client:
            self.connection_pool.disconnect()
            logger.info("Redis connection closed")


async def main():
    """Test cases for Redis manager methods."""
    print("\n=== Redis Manager Tests ===")
    
    config = RedisConfig(
        host="localhost",
        port=6379,
        password="mypassword",
        db=0
    )
    
    db = RedisDatabaseManager(config)
    
    try:
        # Clean up before tests
        print("\n0. Cleaning up test environment:")
        flush_result = await db.flush_database()
        print(f"Flush database result: {flush_result}")
        
        test_namespace = db.get_namespace("test")
        
        # Test simple key-value operations
        print("\n1. Testing key-value operations:")
        set_result = await test_namespace.set_value(
            "user:1",
            {
                "name": "Test User",
                "email": "test@example.com",
                "created_at": datetime.datetime.now().isoformat()
            }
        )
        print(f"Set value result: {set_result}")
        
        get_result = await test_namespace.get_value("user:1")
        print(f"Get value result: {get_result}")
        
        # Test hash operations
        print("\n2. Testing hash operations:")
        hash_fields = {
            "theme": "light",
            "notifications": True,
            "preferences": {"language": "en", "timezone": "UTC"}
        }
        hash_set_result = await test_namespace.set_hash("settings:1", hash_fields)
        print(f"Set hash result: {hash_set_result}")
        
        hash_get_result = await test_namespace.get_hash_fields(
            "settings:1",
            ["theme", "notifications", "preferences"]
        )
        print(f"Get hash result: {hash_get_result}")
        
        # Test bulk operations
        print("\n3. Testing bulk operations:")
        bulk_data = {
            "bulk:1": {"name": "Bulk User 1", "score": 85},
            "bulk:2": {"name": "Bulk User 2", "score": 92},
            "bulk:3": {"name": "Bulk User 3", "score": 78}
        }
        bulk_set_result = await test_namespace.bulk_set(bulk_data)
        print(f"Bulk set result: {bulk_set_result}")
        
        # Verify bulk set results
        for key in bulk_data.keys():
            verify_result = await test_namespace.get_value(key)
            print(f"Verify bulk set for {key}: {verify_result}")

        # Test expiration
        print("\n4. Testing key expiration:")
        expire_result = await test_namespace.set_value(
            "temp:1",
            "temporary value",
            expiry=2  # 2 seconds
        )
        print(f"Set with expiry result: {expire_result}")
        
        # Verify before expiration
        verify_before = await test_namespace.get_value("temp:1")
        print(f"Value before expiration: {verify_before}")
        
        # Wait for expiration
        import asyncio
        await asyncio.sleep(3)
        
        # Verify after expiration
        verify_after = await test_namespace.get_value("temp:1")
        print(f"Value after expiration: {verify_after}")

        # Test deletion
        print("\n5. Testing key deletion:")
        delete_result = await test_namespace.delete_key("bulk:1")
        print(f"Delete result: {delete_result}")
        
        # Verify deletion
        verify_delete = await test_namespace.get_value("bulk:1")
        print(f"Verify deletion: {verify_delete}")

        # Test error cases
        # Test Redis-specific features
        print("\n6. Testing Redis-specific features:")
        
        # Test increment
        incr_result = await test_namespace.increment("counter:1", 5)
        print(f"Increment result: {incr_result}")
        incr_verify = await test_namespace.get_value("counter:1")
        print(f"Verify increment: {incr_verify}")
        
        # Test sets
        print("\nTesting sets:")
        set_add_result = await test_namespace.add_to_set(
            "users:active",
            {"id": 1, "name": "User 1"},
            {"id": 2, "name": "User 2"},
            {"id": 3, "name": "User 3"}
        )
        print(f"Add to set result: {set_add_result}")
        
        set_members = await test_namespace.get_set_members("users:active")
        print(f"Get set members result: {set_members}")
        
        # Test sorted sets
        print("\nTesting sorted sets:")
        # Create scores using string keys for the dictionary
        scores = {
            json.dumps({"id": 1, "name": "Player 1"}): 100.0,
            json.dumps({"id": 2, "name": "Player 2"}): 85.5,
            json.dumps({"id": 3, "name": "Player 3"}): 95.0
        }
        sorted_set_result = await test_namespace.add_to_sorted_set("leaderboard", scores)
        print(f"Add to sorted set result: {sorted_set_result}")
        
        # Get top 2 scores
        top_scores = await test_namespace.get_sorted_set_range(
            "leaderboard",
            start=0,
            end=1,
            desc=True
        )
        print(f"Top scores result: {top_scores}")

        print("\n7. Testing error cases:")
        # Test non-existent key
        error_result1 = await test_namespace.get_value("nonexistent:1")
        print(f"Error result (key not found): {error_result1}")
        
        # Test invalid JSON in hash field
        invalid_hash = {
            "valid_field": "valid_value",
            "invalid_field": lambda x: x  # Un-serializable object
        }
        error_result2 = await test_namespace.set_hash("error:1", invalid_hash)
        print(f"Error result (invalid JSON): {error_result2}")
        
        # Final cleanup
        print("\n7. Final cleanup:")
        final_flush = await db.flush_database()
        print(f"Final database flush result: {final_flush}")

    finally:
        db.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())