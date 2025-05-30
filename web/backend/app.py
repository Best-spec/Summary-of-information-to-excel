from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # เปิดให้ frontend เรียกได้ข้าม origin

@app.route('/api/summary')
def summary():
    return jsonify({
        "users": 321,
        "sales": 654,
        "growth": 8.7
    })

if __name__ == '__main__':
    app.run(debug=True,port=5001)