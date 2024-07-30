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
elasticsearch_deployment.yaml: Kubernetes deployment manifest for Elasticsearch.
load_data.py: Script to load data into Elasticsearch.
rag_inference.py: Script to perform RAG inference.
save_model.py: Script to save the TensorFlow model.
model/1/variables/model.pb: Saved TensorFlow model file.
azure-pipelines.yml: Azure Pipeline configuration file for CI/CD.
</li>
</ul>
