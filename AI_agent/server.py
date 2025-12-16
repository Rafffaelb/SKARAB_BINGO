#!/usr/bin/env python3
"""
Web server for SKARAB_BINGO AI Assistant.
This module serves the web interface and handles communication with the AI backend.
"""

import os
import json
import logging
from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
from ai_backend import AIAssistant

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
ai_assistant = AIAssistant(project_root='../')

@app.route('/')
def index():
    """Serve the main HTML page."""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    """Handle user questions."""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        logger.info(f"Received question: {question}")
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        # Query the AI assistant
        response = ai_assistant.query_ai(question)
        
        logger.info(f"AI Response: {response}")
        
        return jsonify({
            'question': question,
            'answer': response
        })
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/ask_stream', methods=['POST'])
def ask_question_stream():
    """Handle user questions with streaming response."""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        logger.info(f"Received streaming question: {question}")
        
        if not question:
            def error_generator():
                yield "data: Error: No question provided\n\n"
            return Response(error_generator(), content_type='text/event-stream')
        
        # Stream the AI assistant response
        return Response(ai_assistant.query_ai_stream(question), content_type='text/event-stream')
        
    except Exception as e:
        logger.error(f"Error processing streaming question: {str(e)}", exc_info=True)
        def error_generator():
            yield f"data: Error: {str(e)}\n\n"
        return Response(error_generator(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)