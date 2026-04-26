from flask import Flask, jsonify
from flask_cors import CORS
from predictor import run_prediction

app = Flask(__name__)
# Enable CORS so our future frontend won't get blocked
CORS(app)

@app.route('/api/analyze', methods=['GET'])
def analyze():
    """
    Endpoint that triggers the pipeline to fetch Supabase data, 
    run the LSTM, run Llama-3, and save to ai_memories.
    """
    try:
        # Run the main prediction function
        result = run_prediction()
        
        # Return a clean JSON response containing the numbers and text
        return jsonify({
            "status": "success",
            "data": result
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    # Run the server on port 5000
    print("Starting QARC Flask Server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
