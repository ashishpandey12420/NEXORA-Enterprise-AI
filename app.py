
import os
import requests

from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify

from ddgs import DDGS
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'pptx', 'txt', 'jpg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Check allowed file extensions
def allowed_file(filename):
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# HOME
@app.route('/')
def home():
    return render_template('index.html')


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return jsonify({
            'success': False,
            'message': 'Login functionality is not implemented yet.'
        })

    return render_template('login.html')


# SIGNUP
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return jsonify({
            'success': False,
            'message': 'Signup functionality is not implemented yet.'
        })

    return render_template('signup.html')


# UPLOAD
@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':

        if 'studyFile' not in request.files:
            flash('No file selected!')
            return redirect(request.url)

        file = request.files['studyFile']

        if file.filename == '':
            flash('No file selected!')
            return redirect(request.url)

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            file.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    filename
                )
            )

            flash('File uploaded successfully!')
            return redirect(url_for('browse'))

    return render_template('upload.html')


# BROWSE
@app.route('/browse')
def browse():
    return render_template('browse.html')


# DOWNLOAD
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True
    )


# NEXORA AI CHAT API
@app.route('/api/chat', methods=['POST'])
def chat():

    data = request.get_json(silent=True) or {}

    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({
            'error': 'Please enter a message.'
        }), 400

    try:

        response = requests.post(
            'http://localhost:11434/api/chat',

            json={
                'model': 'qwen2.5-coder:7b',

                'messages': [
                    {
                        'role': 'system',
                        'content': (
                            'You are NEXORA AI, an intelligent and helpful '
                            'AI assistant. Answer clearly and professionally. '
                            'Understand Hindi, Hinglish and English. '
                            'Reply in the language used by the user.'
                        )
                    },
                    {
                        'role': 'user',
                        'content': user_message
                    }
                ],

                'stream': False
            },

            timeout=180
        )

        response.raise_for_status()

        result = response.json()

        ai_reply = result.get('message', {}).get('content', '')

        if not ai_reply:
            return jsonify({
                'error': 'AI returned an empty response.'
            }), 502

        return jsonify({
            'success': True,
            'reply': ai_reply
        })

    except requests.exceptions.ConnectionError:

        return jsonify({
            'error': 'Ollama is not running. Please start Ollama.'
        }), 503

    except requests.exceptions.Timeout:

        return jsonify({
            'error': 'AI response timed out. Please try again.'
        }), 504

    except requests.exceptions.RequestException as e:

        return jsonify({
            'error': f'Ollama API error: {str(e)}'
        }), 502

# NEXORA INTERNET SEARCH API
@app.route('/api/search', methods=['POST'])
def search():

    data = request.get_json(silent=True) or {}
    query = data.get('query', '').strip()

    if not query:
        return jsonify({'error': 'Please enter a search query.'}), 400

    try:
        with DDGS() as ddgs:
            results = list(
                ddgs.text(query, max_results=8)
            )

        search_results = []

        for item in results:
            search_results.append({
                'title': item.get('title', ''),
                'url': item.get('href', ''),
                'description': item.get('body', '')
            })

        return jsonify({
            'success': True,
            'query': query,
            'results': search_results
        })

    except Exception as e:
        return jsonify({
            'error': f'Search failed: {str(e)}'
        }), 500
# START SERVER

if __name__ == '__main__':
    app.run(debug=True)