from flask import Flask, request, render_template, jsonify, send_file
import os
import uuid
import time
from werkzeug.utils import secure_filename
from scripts.tts_generate import generate_tts
from scripts.wav2lip_run import run_wav2lip, check_wav2lip_installation

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
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    """Main page for digital avatar generation"""
    if request.method == "POST":
        try:
            # Get form data
            text = request.form.get("text", "").strip()
            if not text:
                return jsonify({"error": "Text input is required"}), 400
            
            # Handle file upload
            if 'face_image' not in request.files:
                return jsonify({"error": "Face image is required"}), 400
            
            file = request.files['face_image']
            if file.filename == '':
                return jsonify({"error": "No file selected"}), 400
            
            if not allowed_file(file.filename):
                return jsonify({"error": "Invalid file type. Please upload PNG, JPG, JPEG, or GIF"}), 400
            
            # Generate unique filename
            unique_id = str(uuid.uuid4())
            filename = secure_filename(file.filename)
            face_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{filename}")
            
            # Save uploaded file
            file.save(face_path)
            
            # Generate audio file path
            audio_path = os.path.join(app.config['AUDIO_FOLDER'], f"{unique_id}_audio.wav")
            
            # Generate TTS
            print(f"🎤 Generating TTS for text: {text[:50]}...")
            if not generate_tts(text, audio_path):
                return jsonify({"error": "TTS generation failed"}), 500
            
            # Generate video file path
            video_path = os.path.join(app.config['VIDEO_FOLDER'], f"{unique_id}_output.mp4")
            
            # Check Wav2Lip installation
            if not check_wav2lip_installation():
                return jsonify({"error": "Wav2Lip not properly installed"}), 500
            
            # Generate video
            print(f"🎬 Generating video...")
            if not run_wav2lip(face_path, audio_path, video_path):
                return jsonify({"error": "Video generation failed"}), 500
            
            # Return success response
            return jsonify({
                "success": True,
                "message": "Digital avatar generated successfully!",
                "video_path": video_path,
                "unique_id": unique_id
            })
            
        except Exception as e:
            print(f"❌ Error in main route: {str(e)}")
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    return render_template("index.html")

@app.route("/download/<unique_id>")
def download_video(unique_id):
    """Download generated video"""
    try:
        video_path = os.path.join(app.config['VIDEO_FOLDER'], f"{unique_id}_output.mp4")
        if os.path.exists(video_path):
            return send_file(video_path, as_attachment=True, download_name="digital_avatar.mp4")
        else:
            return jsonify({"error": "Video not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Download error: {str(e)}"}), 500

@app.route("/status")
def status():
    """Check system status"""
    status_info = {
        "wav2lip_installed": check_wav2lip_installation(),
        "directories": {
            "uploads": os.path.exists(app.config['UPLOAD_FOLDER']),
            "audio": os.path.exists(app.config['AUDIO_FOLDER']),
            "video": os.path.exists(app.config['VIDEO_FOLDER'])
        }
    }
    return jsonify(status_info)

if __name__ == "__main__":
    print("🚀 Starting Digital Avatar Generator...")
    print("✅ Flask app initialized")
    print("✅ Directories created")
    app.run(debug=True, host='0.0.0.0', port=5000)