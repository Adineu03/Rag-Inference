import requests
import json

def load_data():
    documents = [
        {"text": "This is a sample document for testing purposes."},
        {"text": "Another document to showcase retrieval capabalities."}
    ]

    for doc in documents:
        response = requests.post("http://localhost:9200/documents/_doc/", headers={"Content-Type": "application/json"}, data=json.dumps(doc))
        print(f"Document ID:{response.json()['_id']} - Status:{response.status_code}")

if __name__ == "__main__":
    load_data()