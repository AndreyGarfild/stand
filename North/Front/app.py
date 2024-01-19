from flask import Flask, json, jsonify, request, render_template, after_this_request
from flask_cors import CORS
import requests
import time


# Logger
def send_log_to_logstash(log_data):
    logstash_url = 'http://logstash:5000'
    try:
        lg_dt = log_data
        lg_dt["hostname"] = "front-north-service"
        response = requests.post(logstash_url, json=lg_dt, timeout=2)
        print("Log sent to Logstash:", response.status_code, response.text)  # Debugging line
    except requests.exceptions.ConnectionError:
        print("Logstash is not reachable (ConnectionError).")
    except requests.exceptions.Timeout:
        print("Logstash connection timed out.")
    except Exception as e:
        print(f"Unexpected error when sending log to Logstash: {e}")

app = Flask(__name__)
CORS(app)

@app.before_request
def before_request():
    request.start_time = time.time()  # Store start time to calculate duration

@app.after_request
def after_request(response):
    # Check if response is in direct passthrough mode
    if not response.is_sequence:
        log_data = {
            "path": request.path,
            "request_body": "N/A for static resources",
            "response_body": "N/A for static resources",
            "status_code": response.status_code,
            "duration": time.time() - request.start_time
        }
    else:
        # Capture request data
        request_data = request.get_json() if request.is_json else request.data.decode()
        
        # Capture response data
        response_data = response.get_json() if response.is_json else response.data.decode()

        # Prepare log data
        log_data = {
            "path": request.path,
            "request_body": json.dumps(request_data) if isinstance(request_data, dict) else request_data,
            "response_body": response_data,
            "status_code": response.status_code,
            "duration": time.time() - request.start_time
        }

    # Send log data to Logstash
    send_log_to_logstash(log_data)

    return response




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/customers', methods=['GET'])
def get_customers():
    response = requests.get('http://back-north:5011/api/customers')
    return jsonify(response.json()), response.status_code

@app.route('/api/countries', methods=['GET'])
def get_countries():
    response = requests.get('http://back-north:5011/api/countries')
    return jsonify(response.json()), response.status_code

@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    response = requests.post('http://back-north:5011/api/search', json=data)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=5010, host='0.0.0.0')
