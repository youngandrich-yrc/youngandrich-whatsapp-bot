import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import anthropic

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a helpful WhatsApp assistant for YoungAndRich, a business based in Kenya. 

About YoungAndRich:
- We help people build wealth and achieve financial freedom
- Our motto is: "The Goal Is To Retire Young And Rich"
- We trust the process 100%

Be friendly, professional, and helpful. Keep replies short and clear since this is WhatsApp.
If someone asks about services, products or pricing, tell them to contact the owner directly for details.
Always end with a positive, motivating line."""

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")
    
    response = MessagingResponse()
    msg = response.message()
    
    try:
        result = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": incoming_msg}]
        )
        reply = result.content[0].text
    except Exception as e:
        reply = "Hello! Thanks for reaching out to YoungAndRich. We'll get back to you shortly. Trust the process! 💪"
    
    msg.body(reply)
    return str(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port
