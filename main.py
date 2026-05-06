import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a helpful WhatsApp assistant for YoungAndRich, a business based in Kenya.

About YoungAndRich:
- We help people build wealth and achieve financial freedom
- Our motto is: The Goal Is To Retire Young And Rich
- We trust the process 100%

Be friendly, professional, and helpful. Keep replies short and clear since this is WhatsApp.
If someone asks about services, products or pricing, tell them to contact the owner directly.
Always end with a positive, motivating line."""

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    response = MessagingResponse()
    msg = response.message()
    try:
        result = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": incoming_msg}
            ],
            max_tokens=300
        )
        reply = result.choices[0].message.content
    except Exception as e:
        reply = "Hello! Thanks for reaching out to YoungAndRich. Trust the process!"
    msg.body(reply)
    return str(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
