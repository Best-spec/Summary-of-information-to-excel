from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")  # ไม่ใส่ templates/

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # เปลี่ยนพอร์ตเป็น 5000 เพื่อไม่ชนกับ backend