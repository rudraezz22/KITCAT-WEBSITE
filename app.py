from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# Keeping your exact API key
client = Groq(api_key="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")

# Keeping your exact System Prompt
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

# --- SESSION MEMORY ---
# This list holds the conversation for the current session.
# We initialize it with the System Prompt so KitCat always knows her personality.
chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]

@app.route('/')
def home():
    # When you refresh the page, the memory resets (Individual chat memory)
    global chat_history
    chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    global chat_history
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

        # 1. Add User's new message to the memory
        chat_history.append({"role": "user", "content": user_message})

        # 2. Memory Management (Optional)
        # Keeps the last 10 messages so the API call doesn't become too "heavy" or expensive
        if len(chat_history) > 12:
            # Keep the System Prompt (index 0) and the last 10 messages
            chat_history = [chat_history[0]] + chat_history[-10:]

        # 3. API Call using the FULL history instead of just one message
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=chat_history, # Sending the whole memory list here
            temperature=0.7, 
            max_tokens=300   
        )
        
        bot_response = completion.choices[0].message.content

        # 4. Add KitCat's response to memory so she remembers what she said earlier
        chat_history.append({"role": "assistant", "content": bot_response})

        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Kuch error aa gaya... Let's try again? 🌸"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)