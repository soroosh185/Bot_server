from flask import Flask, request, jsonify
import random
import string
import json
import os

app = Flask(__name__)

# نام فایل ذخیره‌سازی لایسنس‌ها
LICENSE_FILE = "licenses.json"

# تابع برای خواندن لایسنس‌ها از فایل
def load_licenses():
    if os.path.exists(LICENSE_FILE):
        with open(LICENSE_FILE, "r") as file:
            return json.load(file)
    return {}

# تابع برای ذخیره لایسنس‌ها در فایل
def save_licenses(data):
    with open(LICENSE_FILE, "w") as file:
        json.dump(data, file, indent=4)

# بارگیری لایسنس‌های قبلی
LICENSES = load_licenses()

# تابع ساخت لایسنس تصادفی
def generate_license():
    return '-'.join([''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(4)])

# **📌 صفحه اصلی برای تست در مرورگر**
@app.route('/')
def home():
    return "🚀 سرور لایسنس فعال است و آماده کار می‌باشد!"

# **📌 API برای تولید لایسنس جدید**
@app.route('/generate_license', methods=['POST'])
def generate_license_route():
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"status": "error", "message": "❌ شناسه کاربر ارسال نشده!"}), 400

    # بررسی اگر کاربر قبلاً لایسنس گرفته باشد
    if user_id in LICENSES:
        return jsonify({"status": "success", "license": LICENSES[user_id]})

    # تولید لایسنس جدید
    new_license = generate_license()
    LICENSES[user_id] = new_license
    save_licenses(LICENSES)

    return jsonify({"status": "success", "license": new_license})

# **📌 API برای بررسی اعتبار لایسنس**
@app.route('/check_license', methods=['POST'])
def check_license():
    data = request.get_json()
    license_key = data.get("key")

    return "valid" if license_key in LICENSES.values() else "invalid"

# **📌 اجرای سرور روی پورت درست در Render**
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # دریافت پورت از متغیر محیطی
    app.run(host='0.0.0.0', port=port)
