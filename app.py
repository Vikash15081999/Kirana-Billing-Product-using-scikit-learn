from flask import Flask, request, jsonify, render_template, send_file
import json
import base64
import os
from flask_cors import CORS

import threading, webbrowser

from predictor import predict

app = Flask(__name__, template_folder='templates')
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assets/<path:path>')
def serve_static(path):
    return send_file("assets/"+path)

@app.route('/api/image_upload',methods=["POST"])
def ImageUpload():
    if "image" in (request.files):
        file = request.files["image"]
        file.save("image.jpeg")

        resp = predict()

    result = {
        'error':False,
        'product': resp["category"],
        "prediction": str(resp["prediction"])
    }

    return json.dumps(result)


if __name__ == "__main__":
    threading.Timer(1.25, lambda: webbrowser.open("http://localhost:5000/") ).start()
    app.run(host="localhost",port=5000,debug=False)
