import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import text  

app = Flask(__name__)
CORS(app)
# Enable debug logging for SQLAlchemy
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

# Configure PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://back-end:123@localhost/backend'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Payment(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255))  # Change data type to string
    amount = db.Column(db.Float)
    payment_date = db.Column(db.Date)


## API SECTION

#payment
@app.route('/api/payment', methods=['POST'])
def process_payment():
    try:
        data = request.get_json()

        # Extract data from the JSON request
        name = data.get('name')
        first_payment_day = data.get('firstPaymentDay')
        second_payment_day = data.get('secondPaymentDay')
        amount = data.get('amount')

        # Get user from the request (assuming you have it in your frontend data)
        user = name

        # Generate and insert two records for each month from the current month for the next two years
        current_date = datetime.now().date()
        end_date = current_date + timedelta(days=365 * 2)  # Two years from the current date

        while current_date <= end_date:
            # First payment record
            first_payment_date = current_date.replace(day=first_payment_day)
            if first_payment_date < current_date:
                first_payment_date = first_payment_date.replace(month=first_payment_date.month + 1)
            first_payment = Payment(user_name=user, amount=amount, payment_date=first_payment_date)
            db.session.add(first_payment)

            # Second payment record
            second_payment_date = current_date.replace(day=second_payment_day)
            if second_payment_date < current_date:
                second_payment_date = second_payment_date.replace(month=second_payment_date.month + 1)
            second_payment = Payment(user_name=user, amount=amount, payment_date=second_payment_date)
            db.session.add(second_payment)

            # Move to the next month
            current_date = current_date.replace(day=1)
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)

        db.session.commit()
        # Return a success response
        return jsonify({'message': 'Payment data saved successfully'}), 200
    except Exception as e:
        # Return an error response if there's an exception
        return jsonify({'error': str(e)}), 500

# statistics 
@app.route('/api/statistics', methods=['POST'])
def get_statistics():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        date = data.get('date')

        # Get a database connection from the SQLAlchemy engine
        connection = db.engine.connect()

        # Execute a raw SQL query to fetch data from the "statistics" view based on the provided date
        query = text(f"SELECT * FROM statistics WHERE payment_date = '{date}'")
        result = connection.execute(query)
        formatted_data =  {}
        # Parse the query result and format it as a list of dictionaries
        statistics_list = []
        for row in result:
            row_data = row
            formatted_data = {
                'date': row_data[0].strftime('%d-%m-%Y'),
                'count': int(row_data[1]),
                'summ': float(row_data[2])
            }
            print(formatted_data)
            statistics_list.append(formatted_data)

        # Close the database connection
        connection.close()

        # Return the formatted statistics data as JSON response
        return jsonify(formatted_data), 200

    except Exception as e:
        # Return an error response if there's an exception
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
