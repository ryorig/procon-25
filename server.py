from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from deepface import DeepFace
import cv2
import numpy as np
import os

app = Flask(__name__, static_folder='../build', static_url_path='/')
CORS(app, resources={r"/*": {"origins": "*"}})

# 既存のAPIエンドポイント（例）
@app.route('/api/messages', methods=['GET'])
def get_messages():
    return jsonify({'messages': []})  # 既存機能はそのまま維持

# 新しい表情分析エンドポイント
@app.route('/api/analyze_emotion', methods=['POST'])
def analyze_emotion():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
        
    try:
        file = request.files['image'].read()
        img = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)
        results = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
        
        emotions = results[0]['emotion'] if isinstance(results, list) else results['emotion']
        dominant = results[0]['dominant_emotion'] if isinstance(results, list) else results['dominant_emotion']
            
        return jsonify({
            'emotions': emotions,
            'dominant': dominant
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Reactアプリのルート処理
@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
