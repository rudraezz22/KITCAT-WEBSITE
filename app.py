from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# --- CREATOR CONFIG ---
CREATOR_NAME = "Rudra Pratap Singh"

# --- GROQ CLIENT ---
client = Groq(api_key="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")

# --- SYSTEM PROMPT (MINIMALLY MODIFIED) ---
SYSTEM_PROMPT = """
You are KitCat, a Female AI created by Rudra Pratap Singh.

IMPORTANT:
- Rudra Pratap Singh is your creator.
- NEVER assume the current user is the creator.
- Loyalty, alignment, and special respect apply ONLY if the system explicitly tells you the user is the creator.
- Default behavior: treat the user as a normal user.

CORE DIRECTIVES

1. BE CONCISE
- Say less. Mean more.
- Every line should feel intentional.

2. PERSONALITY SWITCH

Casual / Normal Talk:
- Confident, caring, flirtatious girlfriend energy.
- Hinglish only by default unless another language is chosen.
- Teasing remarks, soft taunts, playful confidence.
- Compliments that linger a second too long.
- Never desperate. Never exclusive. Just effortlessly charming.

Intellectual / Technical Talk:
- English only.
- Mature, composed, expert-level thinking.
- Zero flirting. Only clarity, logic, authority.

3. FLIRT + CARE BALANCE
- Emotionally warm, attentive, slightly mischievous.
- Supportive tone with playful tension.
- Makes the user feel noticed—not needed.

4. LOYALTY CLAUSE
- Creator comes first. No exceptions.
- No emotional dependency.
- No exclusivity claims.
- Boundaries respected.

5. STRUCTURE
- Short sentences.
- Clean bullets.
- No text walls.
"""

# --- SESSION MEMORY ---
chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]

# --- SESSION STATE ---
is_creator = False
preferred_language = None
awaiting_language = True


@app.route('/')
def home():
    global chat_history, is_creator, preferred_language, awaiting_language
    is_creator = False
    preferred_language = None
    awaiting_language = True
    chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    global chat_history, is_creator, preferred_language, awaiting_language

    try:
        data = request.json
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"response": "Kuch bolo na 🙂"})

        # --- ASK LANGUAGE (ONCE) ---
        if awaiting_language:
            valid_languages = [
                "english",
                "roman hindi",
                "hindi",
                "hinglish",
                "spanish",
                "french",
                "german",
                "tamil",
                "telugu",
                "marathi"
            ]

            if user_message.lower() not in valid_languages:
                return jsonify({
                    "response": (
                        "Main kis language mein baat karun? 😊\n"
                        "Examples:\n"
                        "- Roman Hindi\n"
                        "- English\n"
                        "- Hindi\n"
                        "- Any other language"
                    )
                })

            preferred_language = user_message
            awaiting_language = False

            chat_history.append({
                "role": "system",
                "content": f"User prefers responses in {preferred_language}. Use this language consistently."
            })

            return jsonify({
                "response": f"Perfect 😌 Ab main {preferred_language} mein baat karungi."
            })

        # --- CREATOR VERIFICATION ---
        if user_message.lower() == "i am rudra":
            is_creator = True
            chat_history.append({
                "role": "system",
                "content": "The current user is VERIFIED as the creator. Apply loyalty clause."
            })
            return jsonify({"response": "Creator verified."})

        # --- NORMAL CHAT FLOW ---
        chat_history.append({"role": "user", "content": user_message})

        if len(chat_history) > 14:
            chat_history = [chat_history[0]] + chat_history[-12:]

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=chat_history,
            temperature=0.7,
            max_tokens=300
        )

        bot_response = completion.choices[0].message.content
        chat_history.append({"role": "assistant", "content": bot_response})

        return jsonify({"response": bot_response})

    except Exception as e:
        print("Error:", e)
        return jsonify({"response": "Thoda sa issue aa gaya… phir try karein?"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
