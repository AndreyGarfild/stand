from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/customers', methods=['GET'])
def get_customers():
    response = requests.get('http://back-north:5001/api/customers')
    return jsonify(response.json()), response.status_code

@app.route('/api/countries', methods=['GET'])
def get_countries():
    response = requests.get('http://back-north:5001/api/countries')
    return jsonify(response.json()), response.status_code

@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    response = requests.post('http://back-north:5001/api/search', json=data)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')