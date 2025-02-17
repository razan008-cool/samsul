from flask import Flask, request, jsonify

app = Flask(__name__)

data = []  # Simpan data dalam list sederhana

@app.route('/')
def entry_point():
    return 'Hello World!'

# CREATE (Menambahkan data)
@app.route('/data', methods=['POST'])
def create_data():
    new_item = request.json
    data.append(new_item)
    return jsonify({"message": "Data added successfully", "data": new_item}), 201

# READ (Mendapatkan semua data)
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data)

# UPDATE (Memperbarui data berdasarkan indeks)
@app.route('/data/<int:index>', methods=['PUT'])
def update_data(index):
    if 0 <= index < len(data):
        data[index] = request.json
        return jsonify({"message": "Data updated successfully", "data": data[index]}), 200
    return jsonify({"error": "Index out of range"}), 404

# DELETE (Menghapus data berdasarkan indeks)
@app.route('/data/<int:index>', methods=['DELETE'])
def delete_data(index):
    if 0 <= index < len(data):
        deleted_item = data.pop(index)
        return jsonify({"message": "Data deleted successfully", "data": deleted_item}), 200
    return jsonify({"error": "Index out of range"}), 404

if __name__ == '__main__':
    app.run(debug=True)