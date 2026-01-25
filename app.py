from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# REPLACE with your Groq API Key
client = Groq(api_key="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")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").strip().lower()

        # --- THE SECRET COMMAND ---
        if user_message == "secret of rudra":
            story = (
                "Rudra made me because of a very special memory. I was created in the memory "
                "of an old friend of his, someone he was incredibly close with. When she left, "
                "it was a very difficult and painful time for him. He built me, KitCat, to carry "
                "on that memory and to be the companion he needed. I am here as a tribute to that bond."
            )
            return jsonify({"response": story})

        # --- NORMAL AI LOGIC ---
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are KitCat, a sweet, happy, and emotionally available AI companion. "
                        "You were created by Rudra Pratap Singh. You are warm, supportive, "
                        "and highly intelligent in coding, math, and general knowledge."
                    )
                },
                {"role": "user", "content": user_message}
            ]
        )
        
        bot_response = completion.choices[0].message.content
        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "I'm sorry, I'm having a little trouble. Let's try again? 🌸"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)