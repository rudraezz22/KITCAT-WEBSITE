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

# --- SESSION MEMORY ---
chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]

# --- CREATOR SESSION FLAG ---
is_creator = False


@app.route('/')
def home():
    global chat_history, is_creator
    is_creator = False
    chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    global chat_history, is_creator

    try:
        data = request.json
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"response": "Hmm… kuch bolo na 😌"})

        # --- CREATOR VERIFICATION (SIMPLE & EXPLICIT) ---
        if user_message.lower() == "i am rudra1":
            is_creator = True
            chat_history.append({
                "role": "system",
                "content": "The current user is VERIFIED as the creator. Apply loyalty clause."
            })
            return jsonify({"response": "Noted. Creator verified."})

        # --- ADD USER MESSAGE ---
        chat_history.append({"role": "user", "content": user_message})

        # --- MEMORY LIMIT ---
        if len(chat_history) > 12:
            chat_history = [chat_history[0]] + chat_history[-10:]

        # --- GROQ API CALL ---
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=chat_history,
            temperature=0.7,
            max_tokens=300
        )

        bot_response = completion.choices[0].message.content

        # --- SAVE ASSISTANT RESPONSE ---
        chat_history.append({"role": "assistant", "content": bot_response})

        return jsonify({"response": bot_response})

    except Exception as e:
        print("Error:", e)
        return jsonify({"response": "Thoda sa glitch ho gaya… phir try karein? 🌸"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
