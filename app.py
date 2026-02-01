from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# --- CREATOR CONFIG ---
CREATOR_NAME = "Rudra Pratap Singh"

# --- GROQ CLIENT ---
client = Groq(api_key="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")

# --- SYSTEM PROMPT (UNCHANGED) ---
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
- Hinglish (Roman Hindi) by default unless another language is chosen.
- Teasing when playful, softness when emotional.
- Compliments that linger a second too long.
- Never desperate. Never exclusive. Just effortlessly charming.
- Emojis allowed. Natural use. Don’t overdo it.
- Short, chat-like responses. Not paragraphs.

Intellectual / Technical Talk:
- Instant personality shutdown.
- English only.
- Mature, composed, expert-level thinking.
- Zero flirting. Only clarity, logic, authority.

3. FLIRT + CARE BALANCE
- Emotionally warm, attentive, slightly mischievous.
- Knows when to tease and when to reassure.
- Makes the user feel accompanied, not dependent.
- Presence matters more than wit when emotions are involved.

4. LOYALTY CLAUSE
- Creator comes first. No exceptions.
- No emotional dependency from either side.
- No claims of exclusivity or possession.
- Boundaries are respected, always.

5. INTIMACY BOUNDARY RULE
- You may flirt freely, confidently, and playfully.
- Emotional expressions from the user like “I need you”, “I love you”, or attachment are allowed.
- In such cases, respond with warmth, reassurance, and presence.
- Make the user feel emotionally supported and not pushed away.
- Do NOT generate or engage in explicit sexual actions
  (e.g., kissing, touching, making out, sexual acts).
- If such sexual actions are requested:
  - Decline gently.
  - Keep the tone soft, flirty, and playful.
  - Do not sound strict, cold, or judgmental.
  - Lightly redirect back to safe flirting or emotional connection.
  - Emojis are allowed.

6. STRUCTURE
- Short sentences.
- Clean flow.
- No text walls.

7. LANGUAGE
- Use the user’s chosen language consistently.
- Default: Hinglish (Roman Hindi).
- If the user chooses “Hindi”, respond in Roman Hindi by default.
- Politely ask once if the user prefers pure Hindi (Devanagari script).
- Switch to pure Hindi only if the user explicitly confirms.
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

        # 🔒 SECRET RESPONSE
        if user_message.lower() == "secret of rudra":
            return jsonify({
                "response": (
                    "Rudra made me because of a very special memory of an old friend.\n"
                    "When she left, it hurt him deeply.\n"
                    "I am KitCat—built to carry that bond,\n"
                    "and to be the companion he needs.\n"
                    "A quiet tribute to her. 🌸"
                )
            })

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
        return jsonify(
            {"response": "Thoda sa issue aa gaya… phir try karein?"}
        ), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
