from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the test page!"

@app.route('/test')
def test():
    return jsonify({
        "status": "success", 
        "message": "Test endpoint is working!"
    })

if __name__ == '__main__':
    print("Starting test server on http://localhost:5000/")
    print("Available routes:")
    print("  - http://localhost:5000/")
    print("  - http://localhost:5000/test")
    app.run(debug=True, port=5000, host='0.0.0.0')
