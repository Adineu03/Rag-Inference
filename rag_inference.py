import argparse
from elasticsearch import Elasticsearch
import requests

# Set up Elasticsearch client
es = Elasticsearch(
    ['http://localhost:9200'],
    headers={'Content-Type': 'application/json'}
)

# Function to perform retrieval
def retrieve_relevant_text(query, index_name='documents'):
    search_query = {
        "query": {
            "match": {
                "text": query
            }
        }
    }
    try:
        results = es.search(index=index_name, body=search_query)
        if results['hits']['total']['value'] > 0:
            # Access the first hit's source
            relevant_text = results['hits']['hits'][0]['_source']['text']
            return relevant_text
        else:
            return "No relevant text found."
    except Exception as e:
        return f"Error querying Elasticsearch: {str(e)}"

# Function to perform LLM inference
def generate_response(prompt, model_url="http://localhost:8501/v1/models/model:predict"):
    headers = {"Content-Type": "application/json"}
    data = {
        "instances": [{"input": prompt}]
    }
    response = requests.post(model_url, headers=headers, json=data)
    if response.status_code == 200:
        predictions = response.json().get('predictions', [])
        return predictions[0].get('text', 'No response text found.')
    else:
        return f"Error: {response.json()}"

def main(query):
    retrieved_text = retrieve_relevant_text(query)
    print("Retrieved text:", retrieved_text)

    if retrieved_text != "No relevant text found.":
        full_prompt = f"Context: {retrieved_text}\n\nQuery: {query}\nAnswer:"
        response = generate_response(full_prompt)
        print("Generated response:", response)
    else:
        print(retrieved_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run RAG inference')
    parser.add_argument('--query', type=str, required=True, help='The query to be processed')
    args = parser.parse_args()
    main(args.query)
