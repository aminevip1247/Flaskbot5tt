# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "Telegram WebApp Demo")

@app.get("/health")
def health():
    return jsonify(status="ok", app=APP_NAME)

@app.get("/")
def index():
    # تمرير أي إعدادات إلى القالب عند الحاجة
    return render_template("index.html", app_name=APP_NAME)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
