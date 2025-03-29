from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime

app = Flask(__name__)

# Koneksi ke MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Ganti sesuai konfigurasi MongoDB Anda
db = client['sensor_database']  # Nama database
collection = db['sensor_data']  # Nama koleksi

@app.route('/')
def entry_point():
    return 'Hello World!'

# API untuk menerima data sensor dan menyimpannya ke MongoDB
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
        
        result = collection.insert_one(new_entry)  # Menyimpan ke MongoDB
        new_entry['_id'] = str(result.inserted_id)
        
        return jsonify({"message": "Data added successfully", "data": new_entry}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# READ (Mendapatkan semua data yang disimpan di MongoDB)
@app.route('/data', methods=['GET'])
def get_data():
    data = list(collection.find({}, {"_id": 0}))  # Mengambil semua data dan menghilangkan _id
    return jsonify(data)

# API untuk mendapatkan rata-rata suhu
@app.route('/sensor1/temperature/avg', methods=['GET'])
def get_avg_temperature():
    try:
        avg_temp = collection.aggregate([
            {"$group": {"_id": None, "avgTemperature": {"$avg": "$temperature"}}}
        ])
        avg_temp = list(avg_temp)
        if avg_temp:
            return jsonify({"average_temperature": avg_temp[0]["avgTemperature"]})
        else:
            return jsonify({"message": "No data available"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# API untuk mendapatkan rata-rata kelembapan
@app.route('/sensor1/kelembapan/avg', methods=['GET'])
def get_avg_humidity():
    try:
        avg_humidity = collection.aggregate([
            {"$group": {"_id": None, "avgHumidity": {"$avg": "$humidity"}}}
        ])
        avg_humidity = list(avg_humidity)
        if avg_humidity:
            return jsonify({"average_humidity": avg_humidity[0]["avgHumidity"]})
        else:
            return jsonify({"message": "No data available"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
