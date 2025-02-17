from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

data = []

@app.route('/')
def entry_point():
    return 'Hello World!'

@app.route('/sensor1', methods=['POST'])
def sensor_data():
    try:
        json_data = request.json
        temperature = json_data.get('temperature')
        humidity = json_data.get('humidity')
        timestamp = datetime.datetime.now().isoformat()
        
        new_entry = {
            "temperature": temperature,
            "humidity": humidity,
            "timestamp": timestamp
        }
        
        data.append(new_entry)
        return jsonify({"message": "Data added successfully", "data": new_entry}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
