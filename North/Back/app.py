from flask import Flask, json, jsonify, request, render_template, after_this_request
import psycopg2
from flask_cors import CORS
import requests
import time


# Logger
def send_log_to_logstash(log_data):
    logstash_url = 'http://logstash:5000'
    try:
        lg_dt = log_data
        lg_dt["hostname"] = "back-north-service"
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

# Function to get customers from the database
def get_customers():
    try:
        # Creating DB connection
        conn = psycopg2.connect(
        dbname="north-back",
        user="north-back",
        password="123",
        host="db-north",
        port="5012"
)
        # Create a cursor object to execute SQL queries
        cur = conn.cursor()

        # Execute the SQL query to fetch customers from the customers_view
        cur.execute("SELECT * FROM customers_view")

        # Fetch all customer records
        customers = cur.fetchall()

        # Close the cursor and connection
        cur.close()
        conn.close()

        # Convert the result to a list of dictionaries and return as JSON response
        customer_list = []
        for customer in customers:
            customer_list.append(customer[0])

        return jsonify(customer_list)

    except psycopg2.Error as e:
        # Handle database errors
        print("Error connecting to the database:", e)
        return jsonify({"error": "Database error"}), 500

def get_countries():
    try:
        
        # Creating DB connection
        conn = psycopg2.connect(
        dbname="north-back",
        user="north-back",
        password="123",
        host="db-north",
        port="5012"
)       
        # Create a cursor object to execute SQL queries
        cur = conn.cursor()

        # Execute the SQL query to fetch customers from the customers_view
        
        cur.execute("SELECT * FROM countries_view")

        # Fetch all customer records
        countries = cur.fetchall()

        # Close the cursor and connection
        cur.close()
        conn.close()

        # Convert the result to a list of dictionaries and return as JSON response
        countries_list = []
        for country in countries:
            countries_list.append(country[0])

        return jsonify(countries_list)

    except psycopg2.Error as e:
        # Handle database errors
        print("Error connecting to the database:", e)
        return jsonify({"error": "Database error"}), 500


def get_search(customer_id, ship_country):
    try:
        # Creating DB connection
        conn = psycopg2.connect(
            dbname="north-back",
            user="north-back",
            password="123",
            host="db-north",
            port="5012"
        )

        # Create a cursor object to execute SQL queries
        cur = conn.cursor()

        # Execute the SQL query to fetch data based on customer_id and ship_country
        cur.execute(f"SELECT * FROM public.orders WHERE customer_id = '{customer_id}' AND ship_country = '{ship_country}'")
        ## print(f"SELECT * FROM public.orders WHERE customer_id = '{customer_id}' AND ship_country = '{ship_country}'")
        
        # Fetch all records
        data = cur.fetchall()
        # Close the cursor and connection
        cur.close()
        conn.close()
        # Convert the result to a list of dictionaries and return as JSON response
        
        return jsonify(data)

    except psycopg2.Error as e:
        # Handle database errors
        print("Error connecting to the database:", e)
        return jsonify({"error": "Database error"}), 500

#Logger
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


# Customers endpoint
@app.route('/api/customers', methods=['GET'])
def customers():
    return get_customers()

# Countries endpoint
@app.route('/api/countries', methods=['GET'])
def countries():
    return get_countries()


# search endpoint
@app.route('/api/search', methods=['POST'])
def search():
    # Retrieve data from the request
    data = request.get_json()
    customer_id = data.get('customer', '')  # Get customer_id from the JSON data
    ship_country = data.get('country', '')  # Get ship_country from the JSON data
    # Call the get_search function with the retrieved data
    return get_search(customer_id, ship_country)

if __name__ == '__main__':
    app.run(debug=False, port=5011, host='0.0.0.0')
