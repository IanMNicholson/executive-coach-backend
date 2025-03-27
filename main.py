from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI
import traceback

app = Flask(__name__)
CORS(app)

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET"])
def home():
    return "Executive Coach ChatGPT backend is running!"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        messages = data.get("messages", [])

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )

        reply_content = response.choices[0].message.content
        return jsonify({"reply": {"role": "assistant", "content": reply_content}})

    except Exception as e:
        print("🔥 ERROR:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

