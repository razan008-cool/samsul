from flask import Flask, jsonify

app = Flask(__name__)

temperature_data = [25.3, 27.8, 26.4, 28.0, 24.9]

@app.route('/sensor1/temperature/avg', methods=['GET'])
def get_average_temperature():
    if not temperature_data:
        return jsonify({"error": "No temperature data available"}), 404

    avg_temp = sum(temperature_data) / len(temperature_data)
    return jsonify({"average_temperature": avg_temp})

if __name__ == '__main__':
    app.run(debug=True)
