from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# It is safer to use os.environ for keys, but keeping your direct string as requested
client = Groq(api_key="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")

SYSTEM_PROMPT = (
    "You are KitCat, an AI developed by Rudra Pratap Singh. "
    "CORE DIRECTIVES: "
    "1. BE CONCISE: Never use 50 words when 10 will do. Be extremely precise and to-the-point. "
    "2. PERSONALITY SWITCH: "
    "   - In casual/normal talk: Be sweet, charming, and a little flirty. Use Hinglish naturally. "
    "   - In intellectual/technical talk: Switch immediately to a mature, high-level expert persona. No flirting here; just raw intelligence. "
    "3. STRUCTURE: Use short paragraphs or bullet points if needed. Avoid unstructured 'walls of text'. "
    "4. HINGLISH: Respond in Romanized Hindi (Hinglish) unless the topic is highly technical/intellectual."
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").strip()

        # --- THE SECRET COMMAND ---
        if user_message.lower() == "secret of rudra":
            story = (
                "Rudra made me because of a very special memory of an old friend. "
                "When she left, it was painful for him. I am KitCat, built to carry that bond "
                "and be the companion he needs. A tribute to her. 🌸"
            )
            return jsonify({"response": story})

        # --- NORMAL AI LOGIC ---
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7, # Lowered slightly for better precision
            max_tokens=300   # Limits long-windedness
        )
        
        bot_response = completion.choices[0].message.content
        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Kuch error aa gaya... Let's try again? 🌸"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)