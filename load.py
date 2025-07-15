import yaml
from pymongo import MongoClient
import os
import argparse

def load_yaml_to_mongodb(yaml_file_path, mongo_uri='mongodb://localhost:27017/', db_name='mydatabase', collection_name='mycollection'):
    """
    Loads YAML content from a file and inserts it into a MongoDB collection.

    :param yaml_file_path: Path to the YAML file.
    :param mongo_uri: MongoDB connection URI (default: local MongoDB).
    :param db_name: Name of the database (default: 'mydatabase').
    :param collection_name: Name of the collection (default: 'mycollection').
    """
    try:
        # Load YAML data
        with open(yaml_file_path, 'r') as file:
            data = yaml.safe_load(file)
        
        if data is None:
            print("YAML file is empty or invalid.")
            return
        
        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]
        
        # Insert data
        if isinstance(data, list):
            result = collection.insert_many(data)
            print(f"Inserted {len(result.inserted_ids)} documents.")
        elif isinstance(data, dict):
            result = collection.insert_one(data)
            print(f"Inserted document with ID: {result.inserted_id}")
        else:
            print("Unsupported data type in YAML. Expected list or dict.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load YAML content into MongoDB. MongoDB parameters can be provided via a config YAML file or environment variables.")
    parser.add_argument('yaml_file', help="Path to the YAML file to load.")
    parser.add_argument('--config', default=None, help="Path to the config YAML file containing MongoDB parameters (mongo_uri, db_name, collection_name). If not provided, falls back to environment variables (MONGO_URI, DB_NAME, COLLECTION_NAME) or defaults.")
    
    args = parser.parse_args()
    
    config = {}
    if args.config:
        try:
            with open(args.config, 'r') as f:
                config = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error loading config file: {e}")
            config = {}
    
    mongo_uri = config.get('mongo_uri', os.environ.get('MONGO_URI', 'mongodb://localhost:27017/'))
    db_name = config.get('db_name', os.environ.get('DB_NAME', 'mydatabase'))
    collection_name = config.get('collection_name', os.environ.get('COLLECTION_NAME', 'mycollection'))
    
    load_yaml_to_mongodb(args.yaml_file, mongo_uri, db_name, collection_name)