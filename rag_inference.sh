#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Define the query
QUERY="What is the capital of France?"

# Run the inference script with the query parameter
python rag_inference.py --query "$QUERY"
