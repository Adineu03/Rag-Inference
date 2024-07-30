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
        # print("Raw search results:", results)  # Debugging output
        if results['hits']['total']['value'] > 0:
            # Access the first hit's source
            relevant_text = results['hits']['hits'][0]['_source']['text']
            return relevant_text
        else:
            return "No relevant text found."
    except Exception as e:
        return f"Error querying Elasticsearch: {str(e)}"

# Main function to handle user queries
def main():
    query = input("Enter your query Here: ")
    retrieved_text = retrieve_relevant_text(query)
    print("Retrieved text:", retrieved_text)

if __name__ == "__main__":
    main()
