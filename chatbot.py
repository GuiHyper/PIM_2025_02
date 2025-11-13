from flask import Flask, render_template_string, request, jsonify
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

app = Flask('chatbot_academico')

if api_key:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="<OPENROUTER_API_KEY>",
    )
    openai_enabled = True
else:
    client = None
    openai_enabled = False

print("Iniciando Chatbot Acadêmico Colaborativo...")
print(f"OpenAI habilitado: {openai_enabled}")

HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Chatbot Acadêmico Colaborativo com Apoio de IA</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f2f5; }
        #chat { max-width: 650px; margin: auto; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        .msg { margin: 12px 0; }
        .user { color: #007bff; }
        .bot { color: #28a745; }
        input { width: 70%; padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 6px; }
        button { padding: 10px 18px; font-size: 16px; background-color: #007bff; color: white; border: none; border-radius: 6px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div id="chat">
        <h2>💬 Chatbot Acadêmico Colaborativo com Apoio de IA</h2>
        <p>Bem-vindo! Sou um assistente especializado no tema “Desenvolvimento de um Sistema Acadêmico Colaborativo com Apoio de IA”.</p>
        <div id="messages"></div>
        <input type="text" id="user_input" placeholder="Digite sua pergunta sobre o tema..." autofocus>
        <button onclick="sendMessage()">Enviar</button>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById("user_input");
            const msg = input.value.trim();
            if (!msg) return;

            const chat = document.getElementById("messages");
            chat.innerHTML += `<div class='msg user'><b>Você:</b> ${msg}</div>`;
            input.value = "";

            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: msg })
            });
            const data = await response.json();
            chat.innerHTML += `<div class='msg bot'><b>Chatbot:</b> ${data.reply}</div>`;

            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if not openai_enabled:
        return jsonify({"reply": "A chave da OpenAI não está configurada. Configure o arquivo .env primeiro."})

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um assistente acadêmico colaborativo e especialista no tema "
                        "'Desenvolvimento de um Sistema Acadêmico Colaborativo com Apoio de IA'. "
                        "Seu papel é ajudar estudantes a compreender conceitos de sistemas educacionais, "
                        "inteligência artificial aplicada à educação, colaboração entre usuários, "
                        "desenvolvimento web, banco de dados e integração de modelos de IA. "
                        "Responda sempre de forma explicativa, coerente e com base acadêmica."
                    )
                },
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Ocorreu um erro: {e}"})