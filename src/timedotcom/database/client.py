import pymongo
import pandas as pd
from typing import Optional, Dict, Any, List


class MongoDBClient:
    def __init__(
        self,
        database_name: str = "deep-diver-v2",
        collection_name: str = "boreport",
        host: Optional[str] = None,
        port: Optional[int] = None,
    ):
        """Initialize MongoDB client connection.

        Creates a connection to MongoDB and sets up the specified database and collection.
        If host and port are not provided, connects to the default MongoDB instance
        on localhost:27017.

        Args:
            database_name: Name of the database to connect to
            collection_name: Name of the collection to use
            host: MongoDB host address (default: localhost)
            port: MongoDB port (default: 27017)

        Raises:
            pymongo.errors.ConnectionFailure: If connection to MongoDB fails
            pymongo.errors.ConfigurationError: If there's an issue with the MongoDB configuration
        """
        connection_kwargs: Dict[str, Any] = {}
        if host:
            connection_kwargs["host"] = host
        if port:
            connection_kwargs["port"] = port

        try:
            self.client = pymongo.MongoClient(**connection_kwargs)
            # Verify connection works
            self.client.admin.command("ping")
            self.db = self.client[database_name]
            self.collection = self.db[collection_name]
        except pymongo.errors.ConnectionFailure as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")

    def find_all(self):
        """Get all documents from the collection."""
        return self.collection.find({})

    def find(self, query=None):
        """Find documents matching the query."""
        query = query or {}
        return self.collection.find(query)

    def close(self):
        """Close the MongoDB connection."""
        self.client.close()

    def to_dataframe(self, query=None, limit=None):
        """Convert MongoDB documents to a pandas DataFrame.

        Args:
            query: Optional query to filter documents
            limit: Optional limit on number of documents

        Returns:
            pandas DataFrame containing the documents
        """
        cursor = self.find(query)
        if limit:
            cursor = cursor.limit(limit)
        return pd.DataFrame(list(cursor))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == "__main__":
    # Example usage
    with MongoDBClient() as client:
        query = {}
        df = pd.DataFrame(
            list(client.collection.find(query).sort("Funnel Create Date", -1).limit(5))
        )
        print(
            df[
                ["Funnel SO No", " Channel", "Funnel Create Date", "Funnel Bandwidth"]
            ].head()
        )
