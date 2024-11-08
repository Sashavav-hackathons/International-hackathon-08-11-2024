from flask import Flask, request, jsonify
from flask_cors import CORS  # Импортируем CORS
# from my_ai_module import get  # Импорт функции get()

def get(user_message):
    return user_message

app = Flask(__name__)
CORS(app)  # Включаем CORS для всех маршрутов

@app.route('/api/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get("message")
    ai_response = get(user_message)
    return jsonify({"response": ai_response})

if __name__ == '__main__':
    app.run(port=5000)
