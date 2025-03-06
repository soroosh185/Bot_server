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

# **📌 API برای تولید لایسنس جدید**
@app.route('/generate_license', methods=['POST'])
def generate_license_route():
    data = request.get_json()
    user_id = str(data.get("user_id"))  # کار با `user_id` به عنوان رشته برای سازگاری

    if not user_id:
        return jsonify({"status": "error", "message": "❌ شناسه کاربر ارسال نشده!"}), 400

    # بارگیری مجدد لایسنس‌ها از فایل
    licenses = load_licenses()

    # بررسی اگر کاربر قبلاً لایسنس گرفته باشد
    if user_id in licenses:
        return jsonify({"status": "success", "license": licenses[user_id]})

    # تولید لایسنس جدید
    new_license = '-'.join([''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(4)])
    licenses[user_id] = new_license
    save_licenses(licenses)  # ذخیره اطلاعات جدید

    return jsonify({"status": "success", "license": new_license})

# **📌 API برای بررسی اعتبار لایسنس**
@app.route('/check_license', methods=['POST'])
def check_license():
    data = request.get_json()
    license_key = str(data.get("key")).strip()  # حذف فاصله‌های اضافی

    # بارگیری لایسنس‌ها از فایل قبل از بررسی
    licenses = load_licenses()

    print(f"🔍 بررسی لایسنس: {license_key}")  # نمایش لایسنس دریافتی در لاگ
    print(f"📂 لایسنس‌های ذخیره‌شده: {licenses}")  # نمایش همه لایسنس‌ها در لاگ

    return "valid" if license_key in licenses.values() else "invalid"

# اجرای سرور روی پورت 5000
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host='0.0.0.0', port=port)
