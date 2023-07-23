from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
import os
import json
from bson import json_util
app = FastAPI()

mongo_client = MongoClient("mongodb+srv://mishrasiddharth1999:Reenter2@documents.qfctqu8.mongodb.net/?retryWrites=true&w=majority")

mongo_db = mongo_client["search_database"]
collection = mongo_db["documents"]

def index_documents():
    collection.create_index([("text", "text")])
    for root, _, files in os.walk("patent_jsons"):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as json_file:
                    try:
                        data = json.load(json_file)
                        if isinstance(data, list):
                            collection.insert_many(data)
                        elif isinstance(data, dict):
                            collection.insert_one(data)
                        else:
                            print(f"Invalid data format in file {file_path}")
                    except Exception as e:
                        print(f"Error while processing file {file_path}: {e}")



@app.get("/search/")
async def search_documents(keyword: str = Query(...)):
    import time
    time.sleep(5)

    mongo_query = { "titles": { "$elemMatch": { "text": { "$regex": keyword } } } }
    print(mongo_query)
    mongo_results = list(collection.find(mongo_query))
    json_results = json.loads(json_util.dumps(mongo_results))

    print(mongo_results)
   #  mongo_results
    return  json_results

index_documents()
