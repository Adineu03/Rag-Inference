## Overview

This project involves building and deploying a Retrieval-Augmented Generation (RAG) inference pipeline using Docker, Kubernetes, and Azure Pipelines. The pipeline integrates Elasticsearch for document retrieval and TensorFlow Serving for model inference. The setup includes both a manual process and an automated pipeline for deployment.

## Key Components

1. Elasticsearch: A search and analytics engine used to retrieve relevant documents based on user queries.
2. TensorFlow Serving: A system for serving machine learning models, used here to generate responses based on retrieved documents.
3. Azure Pipelines: Automates the build, push, and deployment processes.


## File Structure

- Dockerfile.tf-serving: Dockerfile to build the TensorFlow Serving image.
- elasticsearch_deployment.yaml: Kubernetes deployment manifest for Elasticsearch.
- load_data.py: Script to load data into Elasticsearch.
- rag_inference.py: Script to perform RAG inference.
- save_model.py: Script to save the TensorFlow model.
- model/1/variables/model.pb: Saved TensorFlow model file.
- azure-pipelines.yml: Azure Pipeline configuration file for CI/CD.

## Manual Setup
### Pre-start
#### Save TensorFlow Model

The `save_model.py` script defines and saves a simple TensorFlow model. Here is the script:

```python
import tensorflow as tf

class SimpleModel(tf.keras.Model):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.dense = tf.keras.layers.Dense(10)

    def call(self, inputs):
        return self.dense(inputs)

model = SimpleModel()
model.build(input_shape=(None, 10))

tf.saved_model.save(model, "model")
```

### 1. **Build and Push Docker Images**

**TensorFlow Serving Docker Image:**

1. Create a Dockerfile (`Dockerfile.tf-serving`) with the following content:

    ```dockerfile
    # use tensorflow serving base image
    FROM tensorflow/serving:2.7.0

    # copy model to the container
    COPY model /models/model

    # set environment variable for model name
    ENV MODEL_NAME=model

    # expose port
    EXPOSE 8501
    ```

2. Build the Docker image:

    ```bash
    docker build -f Dockerfile.tf-serving -t adi3008/tf-serving:latest .
    ```
3. Push the Docker image to DockerHub:

    ```bash
    docker push adi3008/tf-serving:latest
    ```

### 2. **Run Docker Containers**

**TensorFlow Serving Container:**

```bash
docker run -d --name tf-serving --mount type=bind,source=$(pwd)/model,target=/models/model -e MODEL_NAME=model -p 8501:8501 adi3008/tf-serving:latest
```
**Running Elasticsearch Container:**

```bash
docker run -d --name elasticsearch -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.10.1
```
## 3. Kubernetes Deployment(instead going with docker)

**1. Deploy TensorFlow Serving**
Create the Kubernetes deployment and service for TensorFlow Serving:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tf-serving-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: tf-serving
  template:
    metadata:
      labels:
        app: tf-serving
    spec:
      containers:
      - name: tf-serving-container
        image: adi3008/tf-serving:latest
        ports:
        - containerPort: 8501
---
apiVersion: v1
kind: Service
metadata:
  name: tf-serving-service
spec:
  type: LoadBalancer
  ports:
  - port: 8501
    targetPort: 8501
  selector:
    app: tf-serving
```
**2. Deploy ElasticSearch**
Create the Kubernetes deployment and service for ElasticSearch:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: elasticsearch
spec:
  replicas: 1
  selector:
    matchLabels:
      app: elasticsearch
  template:
    metadata:
      labels:
        app: elasticsearch
    spec:
      containers:
      - name: elasticsearch
        image: docker.elastic.co/elasticsearch/elasticsearch:7.10.1
        ports:
        - containerPort: 9200
        env:
        - name: discovery.type
          value: single-node
---
apiVersion: v1
kind: Service
metadata:
  name: elasticsearch-service
spec:
  ports:
  - port: 9200
  selector:
    app: elasticsearch
```
Applying and Port-Forwarding(in case of minikube)
```bash
kubectl apply -f tf-serving-deployment.yaml -n rag-inference
kubectl apply -f elasticsearch.yaml -n rag-inference

kubectl port-forward svc/elasticsearch-service 9200:9200
kubectl port-forward svc/tf-serving-service 8501:8501
```

## 4. Load Data into Elasticsearch

After setting up Elasticsearch, load data into it using the `load_data.py` script. This script is designed to populate your Elasticsearch index with the necessary data for retrieval tasks.
Here is the script:
```python
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
```
To run the script, use the following command:

```bash
python load_data.py
```

## 5. Run RAG Inference

Once the data is loaded into Elasticsearch, you can perform Retrieval-Augmented Generation (RAG) inference using the `rag_inference.py` script. This script interacts with both Elasticsearch and TensorFlow Serving to generate responses based on the user query.
Here is the script:
```python
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
```
To run the inference, use the following command:

```bash
python rag_inference.py
```
## 6. Result 
![image](https://github.com/user-attachments/assets/3e1d833a-c982-4dda-8aac-25276b455ddc)

## Pipeline Setup

The Azure Pipeline automates the process of building, pushing, and deploying Docker images and running the scripts.

### azure-pipelines.yml

```yaml
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: Docker@2
  inputs:
    command: 'buildAndPush'
    containerRegistry: 'dockerhub'
    repository: 'adi3008/tf-serving'
    Dockerfile: 'Dockerfile'
    tags: 'latest'

- script: |
    docker run -d --name tf-serving --mount type=bind,source="$(pwd)/model",target=/models/model -e MODEL_NAME=model -p 8501:8501 tf-serving
  displayName: 'Run TensorFlow Serving container'

- script: |
    docker run -d --name elasticsearch -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.10.1
  displayName: 'Run Elasticsearch container'

- task: Kubernetes@1
  inputs:
    connectionType: 'Kubernetes Service Connection'
    kubernetesServiceEndpoint: '<your-kubernetes-service-connection>'
    namespace: 'default'
    command: 'apply'
    arguments: '-f k8s/tf-serving-deployment.yaml -f k8s/elasticsearch-deployment.yaml'

- task: AzureCLI@2
  inputs:
    azureSubscription: 'adi3008'
    scriptType: 'bash'
    scriptPath: 'scripts/load_data.sh'
    arguments: ''
    workingDirectory: 'scripts'

- task: AzureCLI@2
  inputs:
    azureSubscription: 'adi3008'
    scriptType: 'bash'
    scriptPath: 'scripts/rag_inference.sh'
    arguments: ''
    workingDirectory: 'scripts'
```

## Usage

### Prepare Your Environment:

1. Ensure Docker and Kubernetes are set up.
2. Configure Azure Pipelines with your subscription and service connections.

### Configure the Pipeline:

1. Update the container-registry and repository, kubernetes-service-connection and azure-subscription in the YAML file according to your own.
2. Adjust paths and environment variables as needed.

### Run the Pipeline:

1. Commit changes to your repository to trigger the Azure Pipeline.
2. Monitor the pipeline execution through Azure DevOps to ensure all steps complete successfully.

## Troubleshooting

- **Docker Errors**: Check container logs using `docker logs <container_name>`.
- **Kubernetes Deployment Issues**: Verify deployments with `kubectl get pods` and check pod logs.
- **Pipeline Failures**: Review Azure Pipeline logs for detailed error messages.

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Azure Pipelines Documentation](https://docs.microsoft.com/en-us/azure/devops/pipelines/)
