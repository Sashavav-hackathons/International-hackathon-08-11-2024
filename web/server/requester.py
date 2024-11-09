from flask import request, jsonify
from flask import Blueprint, render_template
import sys
import os
rag_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../rag'))
sys.path.append(rag_path)

from rag import Rag

request_blueprint = Blueprint('main', __name__)

@request_blueprint.route('/c', methods=['GET'])
def print_index():
    return render_template('index.html')

@request_blueprint.route('/api/query', methods=['POST'])
def query():
    user_message = request.json.get("message")
    ai_response = Rag.query(user_message)
    return jsonify({"response": ai_response})

@request_blueprint.route('/api/load_file', methods=['POST'])
def load_file():
    return 'hey!!'