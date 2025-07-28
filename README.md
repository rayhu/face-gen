# Face-Gen: Digital Avatar Generator

A Flask-based web application that creates talking face videos using AI-powered text-to-speech and lip-sync technology.

## 🚀 Features

- **Modern Web Interface**: Beautiful, responsive UI with drag-and-drop file upload
- **AI Text-to-Speech**: Powered by Tortoise TTS for high-quality speech synthesis
- **Lip-Sync Technology**: Uses Wav2Lip for realistic mouth movement synchronization
- **Apple Silicon Optimization**: Full MPS support for faster processing on Mac
- **Real-time Processing**: Live progress updates and error handling
- **Video Download**: Direct download of generated videos

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **AI Models**: 
  - Tortoise TTS for speech synthesis
  - Wav2Lip for lip-sync
- **Hardware Acceleration**: Apple Silicon MPS support

## 📋 Requirements

- Python 3.10+
- Conda environment
- Apple Silicon Mac (for MPS acceleration)
- macOS 12.3+ (for MPS support)

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd facegen

# Create and activate conda environment
conda env create -f environment.yml
conda activate face-gen

# Set environment variable for Apple Silicon
export KMP_DUPLICATE_LIB_OK=TRUE
```

### 2. Install Wav2Lip

```bash
# Run the installation script
python install_wav2lip.py
```

### 3. Start Face-Gen

```bash
# Simple start (recommended)
python face-gen.py

# Or manual start
python app/main.py
```

### 4. Access the Web Interface

Open your browser and navigate to the displayed URL (usually `http://localhost:5000`)

## 📁 Project Structure

```
facegen/
├── app/
│   ├── main.py              # Flask application
│   ├── templates/
│   │   └── index.html       # Web interface
│   └── scripts/
│       ├── tts_generate.py  # Text-to-speech generation
│       └── wav2lip_run.py   # Lip-sync video generation
├── uploads/                 # Uploaded face images
├── audio/                   # Generated audio files
├── video/                   # Generated video files
├── Wav2Lip/                 # Wav2Lip installation
├── environment.yml          # Conda environment
├── face-gen.py             # Simple startup script
├── install_wav2lip.py      # Wav2Lip installer
└── README.md               # This file
```

## 🎯 Usage

### Web Interface

1. **Upload Face Image**: Drag and drop or click to upload a face image
2. **Enter Text**: Type the text you want your avatar to speak
3. **Generate**: Click "Generate Digital Avatar" to start processing
4. **Download**: Download the generated video when complete

### Supported File Formats

- **Images**: PNG, JPG, JPEG, GIF (Max 16MB)
- **Output**: MP4 video with audio

## ⚡ Performance

### Apple Silicon Optimization

The application is optimized for Apple Silicon Macs with MPS acceleration:

- **MPS Detection**: Automatic device detection and optimization
- **Fallback Support**: Graceful fallback to CPU if MPS fails
- **Performance Monitoring**: Real-time performance tracking

### Performance Benchmarks

Based on testing on Apple Silicon Macs:

- **Small Operations**: CPU may be faster due to data transfer overhead
- **Large Operations**: MPS typically 2-5x faster for matrix operations
- **Deep Learning**: MPS provides significant acceleration for model inference

## 🔧 Configuration

### Environment Variables

```bash
# Required for Apple Silicon
export KMP_DUPLICATE_LIB_OK=TRUE

# Optional: Custom port
export FLASK_PORT=5000
```

### Flask Configuration

- **Max File Size**: 16MB
- **Upload Folder**: `uploads/`
- **Audio Folder**: `audio/`
- **Video Folder**: `video/`

## 🐛 Troubleshooting

### Common Issues

1. **MPS Not Available**
   - Ensure macOS 12.3+
   - Check PyTorch installation
   - Verify Apple Silicon Mac

2. **Wav2Lip Installation Failed**
   - Run `python install_wav2lip.py`
   - Check internet connection
   - Verify Python 3.10+

3. **TTS Generation Failed**
   - Check Tortoise TTS installation
   - Verify text input
   - Check disk space

4. **Video Generation Failed**
   - Verify Wav2Lip installation
   - Check input file formats
   - Ensure sufficient disk space

### Debug Mode

```bash
# Enable debug mode
export FLASK_DEBUG=1
python app/main.py
```

## 🔄 API Endpoints

### Main Routes

- `GET /` - Main web interface
- `POST /` - Generate digital avatar
- `GET /download/<unique_id>` - Download generated video
- `GET /status` - System status check

### Request Format

```json
{
  "face_image": "file",
  "text": "string"
}
```

### Response Format

```json
{
  "success": true,
  "message": "Digital avatar generated successfully!",
  "video_path": "path/to/video.mp4",
  "unique_id": "uuid"
}
```

## 🛡️ Security

- **File Validation**: Strict file type checking
- **Size Limits**: 16MB maximum file size
- **Secure Filenames**: UUID-based unique naming
- **Input Sanitization**: Text input validation

## 📈 Performance Tips

1. **Use High-Quality Images**: Clear, front-facing photos work best
2. **Optimize Text Length**: Shorter texts process faster
3. **Close Other Applications**: Free up system resources
4. **Use SSD Storage**: Faster file I/O operations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0.

## 🙏 Acknowledgments

- [Tortoise TTS](https://github.com/neonbjb/tortoise-tts) for speech synthesis
- [Wav2Lip](https://github.com/Rudrabha/Wav2Lip) for lip-sync technology
- [Flask](https://flask.palletsprojects.com/) for web framework
- [Bootstrap](https://getbootstrap.com/) for UI components

## 📞 Support

For issues and questions:

1. Check the troubleshooting section
2. Review the logs in debug mode
3. Create an issue on GitHub

---

**Made with ❤️ for the AI community**

