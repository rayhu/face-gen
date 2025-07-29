from flask import Flask, render_template, request, jsonify, send_file
import os
import uuid
import time
from werkzeug.utils import secure_filename
from scripts.tts_generate import generate_tts
from scripts.wav2lip_run import run_wav2lip

app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['AUDIO_FOLDER'] = 'audio'
app.config['VIDEO_FOLDER'] = 'video'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)
os.makedirs(app.config['VIDEO_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Check if files were uploaded
        if 'face_image' not in request.files:
            return jsonify({'error': 'No face image uploaded'}), 400
        
        file = request.files['face_image']
        if file.filename == '':
            return jsonify({'error': 'No face image selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload an image.'}), 400
        
        # Get text input
        text = request.form.get('text', '').strip()
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Generate unique filenames
        timestamp = str(int(time.time()))
        face_filename = f"face_{timestamp}_{secure_filename(file.filename)}"
        audio_filename = f"audio_{timestamp}.wav"
        video_filename = f"video_{timestamp}.mp4"
        
        # Save uploaded face image
        face_path = os.path.join(app.config['UPLOAD_FOLDER'], face_filename)
        file.save(face_path)
        
        # Generate TTS
        audio_path = os.path.join(app.config['AUDIO_FOLDER'], audio_filename)
        print(f"Generating TTS for text: {text[:50]}...")
        
        if not generate_tts(text, audio_path):
            return jsonify({'error': 'TTS generation failed'}), 500
        
        # Generate video
        video_path = os.path.join(app.config['VIDEO_FOLDER'], video_filename)
        print(f"Generating video...")
        
        if not run_wav2lip(face_path, audio_path, video_path):
            return jsonify({'error': 'Video generation failed'}), 500
        
        # Return success response
        return jsonify({
            'success': True,
            'message': 'Digital avatar generated successfully',
            'video_filename': video_filename,
            'download_url': f'/download/{video_filename}'
        })
        
    except Exception as e:
        print(f"Error in main route: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/download/<filename>')
def download_video(filename):
    try:
        video_path = os.path.join(app.config['VIDEO_FOLDER'], filename)
        if not os.path.exists(video_path):
            return jsonify({'error': 'Video file not found'}), 404
        
        # Check if it's a download request (from download button)
        if request.args.get('download') == 'true':
            return send_file(
                video_path,
                as_attachment=True,
                download_name=filename
            )
        else:
            # For video playback in browser
            return send_file(
                video_path,
                mimetype='video/mp4'
            )
    except Exception as e:
        return jsonify({'error': 'File not found'}), 404

@app.route('/status')
def status():
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'directories': {
            'uploads': os.path.exists(app.config['UPLOAD_FOLDER']),
            'audio': os.path.exists(app.config['AUDIO_FOLDER']),
            'video': os.path.exists(app.config['VIDEO_FOLDER'])
        }
    })

if __name__ == "__main__":
    print("Starting Digital Avatar Generator...")
    print("Flask app initialized")
    print("Directories created")
    app.run(debug=True, host='0.0.0.0', port=5001)