#!/bin/bash

MODEL_DIR=$(pwd)/waste_classifier
PORT=8501

echo "Starting Tensorflow Serving for model at $MODEL_DIR on port $PORT"

# Running Tensorflow serving server
docker run -t --rm -p $PORT:8501 \ 
    -v "$MODEL_DIR:/models/waste_classifier" \
    -e MODEL_NAME=waste_classifier \
    tensorflow/serving