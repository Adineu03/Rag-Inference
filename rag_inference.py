import requests
import json

def query_elasticsearch(query):
    url = "http://localhost:9200/documents/_search"
    payload = {
        "query": {
            "match": {
                "text": query
            }
        }
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url,headers=headers,data=json.dumps(payload))
    return response.json()

def query_llm(input_text):
    url = "http://localhost:8501/v1/models/model:predict"
    payload = {
        "instances": [{"input": input_text}]
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url,headers=headers,json=payload)
    return response.json()

def main():
    user_query = input("Enter your Query Here:")
    retrieval_results = query_elasticsearch(user_query)
    if retrieval_results['hits']['hits']:
        relevant_text = retrieval_results['hits']['hits'][0]['source']['text']
        print(f"Retrieved_texts: {relevant_text}")

        llm_input = [0] * 10
        llm_response = query_llm(llm_input)
        print(f"LLM Response: {llm_response}")
    else:
        print("No relevant document found")

if __name__ == "__main__":
    main()