#!/bin/bash
echo "Starting Ragume Backend and Frontend..."

# Use existing helper script logic or direct paths
if [ -f "./venv/bin/activate" ]; then
    source ./venv/bin/activate
elif [ -f "./venv/Scripts/activate" ]; then
    source ./venv/Scripts/activate
fi

# Start Backend
python -m uvicorn app.main:app --reload --port 8001 &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start Frontend
python -m streamlit run ui.py &
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Backend: http://localhost:8001"
echo "Frontend: http://localhost:8501"

# Cleanup function
cleanup() {
    echo "Stopping processes..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit
}

# Trap SIGINT (Ctrl+C)
trap cleanup SIGINT

# Wait for processes
wait
