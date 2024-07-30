## Overview

This project involves building and deploying a Retrieval-Augmented Generation (RAG) inference pipeline using Docker, Kubernetes, and Azure Pipelines. The pipeline integrates Elasticsearch for document retrieval and TensorFlow Serving for model inference. The setup includes both a manual process and an automated pipeline for deployment.

## Key Components

1. Elasticsearch: A search and analytics engine used to retrieve relevant documents based on user queries.
2. TensorFlow Serving: A system for serving machine learning models, used here to generate responses based on retrieved documents.
3. Azure Pipelines: Automates the build, push, and deployment processes.


## File Structure - 

<ul>
<li>
Dockerfile.tf-serving: Dockerfile to build the TensorFlow Serving image.
</li>
<li>
elasticsearch_deployment.yaml: Kubernetes deployment manifest for Elasticsearch.
</li>
<li>
load_data.py: Script to load data into Elasticsearch.
</li>
<li>
rag_inference.py: Script to perform RAG inference.
</li>
<li>
save_model.py: Script to save the TensorFlow model.
</li>
<li>
model/1/variables/model.pb: Saved TensorFlow model file.
</li>
<li>
azure-pipelines.yml: Azure Pipeline configuration file for CI/CD.
</li>
</ul>

## Manual Setup

### 1. **Build and Push Docker Images**

**TensorFlow Serving Docker Image:**

1. Create a Dockerfile (`Dockerfile.tf-serving`) with the following content:

    ```dockerfile
    FROM tensorflow/serving:latest
    COPY model /models/model
    ENV MODEL_NAME=model
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
