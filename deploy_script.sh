# Install dependencies (if any)
pip install -r requirements.txt

# Start the Flask application (assuming your app is named app.py)
nohup python app.py &

# Wait for the Flask app to start (adjust sleep time if needed)
sleep 20

# Extract Flask app URL
FLASK_URL=$(curl -s http://localhost:5000 | grep -o "http://[^\"]*")

# Open Flask app URL in default browser
xdg-open $FLASK_URL
