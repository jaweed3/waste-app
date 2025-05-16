#!/bin/bash

# Make Scripts Executable
chmod +x serving.py

# Checking if the model Exist or not
if [! -d "./waste_classifier" ]; then
    echo "Saving model in SavedModel Format..."
    python3 save_model.py
fi

# Starting Tensorflow Serving in the background
echo "Starting Tensorflow Serving...."
./start_tf_serving.sh
TF_SERVING_PID=$

# Wait for TF Serving to start
echo "Waiting Tensorflow Serving to Start"
sleep 5

# Start Flask App in the background
echo "Waiting for Flask API....."
sleep 5

# Starting the GUI
echo "Starting the GUI...."
python3 gui.py

# When GUI Closes, Clean Up!
echo "Shutting Down..."
kill $FLASK_PID
kill $TF_SERVING_PID
echo "Application Stopped"