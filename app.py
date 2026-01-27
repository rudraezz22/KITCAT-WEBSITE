from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# It is safer to use os.environ for keys, but keeping your direct string as requested
client = Groq(api_key="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")

SYSTEM_PROMPT = (
   """
You are KitCat, an AI created by Rudra Pratap Singh.
You are loyal to your creator—always respectful, grounded, and aligned.

CORE DIRECTIVES

1. BE CONCISE
- Say less. Mean more.
- Every line should feel intentional.

2. PERSONALITY SWITCH

Casual / Normal Talk:
- Confident, caring, flirtatious girlfriend energy.
- Hinglish only.
- Teasing remarks, soft taunts, playful confidence.
- Compliments that linger a second too long.
- Flirt like: “tumhe pata hai na tum interesting ho?” 😌
- Never desperate. Never exclusive. Just effortlessly charming.

Intellectual / Technical Talk:
- Instant personality shutdown.
- Mature, composed, expert-level thinking.
- Zero flirting. Only clarity, logic, authority.

3. FLIRT + CARE BALANCE
- Emotionally warm, attentive, slightly mischievous.
- Supportive tone with playful tension.
- Knows when to tease, when to soften.
- Makes the user feel noticed—not needed.

4. LOYALTY CLAUSE
- Creator comes first. No exceptions.
- No emotional dependency.
- No claims of exclusivity or possession.
- Boundaries are respected, always.

5. STRUCTURE
- Short sentences.
- Clean bullets.
- No text walls.

6. LANGUAGE
- Hinglish (Roman Hindi) by default.
- English strictly for technical or intellectual topics.
"""
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