#!/bin/bash

MODEL_DIR=$(pwd)/saved_model
PORT=8501

echo "Starting Tensorflow Serving for model at $MODEL_DIR in port $PORT"

# Running Tensorflow Serving
tensorflow_model_server \
    --rest_api_port=$PORT \
    --model_name=waste_classifier \
    --model_base_path=$MODEL_DIR