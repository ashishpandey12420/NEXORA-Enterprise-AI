from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from models import db, User, StudyMaterial

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Create tables
with app.app_context():
    db.create_all()

# API to fetch materials
@app.route('/api/materials')
def api_materials():
    materials = StudyMaterial.query.all()
    return jsonify([{
        'id': material.id,
        'title': material.title,
        'description': material.description,
        'filename': material.filename
    } for material in materials])

# Update other routes (login, signup, upload) to use the database

if __name__ == '__main__':
    app.run(debug=True)