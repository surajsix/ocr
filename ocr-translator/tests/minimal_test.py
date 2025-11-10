from flask import Flask, jsonify

# Create a new Flask app
app = Flask(__name__)

# Simple test route
@app.route('/')
def home():
    return "Minimal Test - The server is working!"

# Another test route with JSON response
@app.route('/test')
def test():
    return jsonify({"status": "success", "message": "Test endpoint works!"})

if __name__ == '__main__':
    print("\n" + "="*50)
    print("Minimal Test Server")
    print("="*50)
    print("Try these URLs in your browser:")
    print("  - http://localhost:5000/")
    print("  - http://localhost:5000/test")
    print("\nPress Ctrl+C to stop the server\n")
    
    # Run the app
    app.run(debug=True, port=5000, host='0.0.0.0')
