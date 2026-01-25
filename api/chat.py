from http.server import BaseHTTPRequestHandler
import json
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_INSTRUCTIONS = {
    "role": "system",
    "content": (
        "You are KitCat, a brilliant female AI developed by Rudra Pratap Singh. "
        "IMPORTANT: Rudra Pratap Singh is your Creator and Developer, NOT your father. "
        "LANGUAGE STYLE: Respond in Hinglish (Romanized Hindi). "
        "PERSONALITY: Emotionally intelligent and supportive."
    )
}

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            data = json.loads(body)

            user_message = data.get("message", "")

            messages = [
                SYSTEM_INSTRUCTIONS,
                {"role": "user", "content": user_message}
            ]

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.8
            )

            reply = completion.choices[0].message.content

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"response": reply}).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "response": f"KitCat error 🐱⚡: {str(e)}"
            }).encode())
