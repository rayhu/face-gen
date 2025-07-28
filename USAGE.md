# Face-Gen Usage Guide

## 🎭 Quick Start

### 1. Start the Application
```bash
# Activate the conda environment
conda activate face-gen

# Set environment variable
export KMP_DUPLICATE_LIB_OK=TRUE

# Start Face-Gen
python face-gen.py
```

### 2. Access the Web Interface
Open your browser and go to: **http://localhost:5001**

### 3. Create Your Digital Avatar
1. **Upload a face image** (PNG, JPG, JPEG, GIF - max 16MB)
2. **Enter the text** you want your avatar to speak
3. **Click "Generate Digital Avatar"**
4. **Wait for processing** (may take a few minutes)
5. **Download your video** when complete

## 🌟 Features

- **Drag & Drop Upload**: Simply drag your image to the upload area
- **Real-time Progress**: See the generation progress in real-time
- **Apple Silicon Optimized**: Faster processing on Mac with MPS
- **High-Quality Output**: Professional video generation
- **Easy Download**: One-click video download

## 📱 Supported Formats

### Input
- **Images**: PNG, JPG, JPEG, GIF
- **Text**: Any language supported by Tortoise TTS

### Output
- **Video**: MP4 format with audio
- **Quality**: High-definition lip-sync

## ⚡ Performance Tips

1. **Use Clear Images**: Front-facing photos work best
2. **Keep Text Short**: Shorter texts process faster
3. **Close Other Apps**: Free up system resources
4. **Use SSD Storage**: Faster file operations

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Use the smart startup script
python face-gen.py
```

**Model Download Issues**
```bash
# Reinstall Wav2Lip models
python install_wav2lip.py
```

**Slow Processing**
- Close other applications
- Ensure you're using Apple Silicon Mac
- Check available disk space

### Debug Mode
```bash
export FLASK_DEBUG=1
python app/main.py
```

## 🔧 Advanced Usage

### API Endpoints
- `GET /` - Main interface
- `POST /` - Generate avatar
- `GET /download/<id>` - Download video
- `GET /status` - System status

### Environment Variables
```bash
export KMP_DUPLICATE_LIB_OK=TRUE  # Required for Apple Silicon
export FLASK_DEBUG=1              # Enable debug mode
```

## 📊 System Status

Check if everything is working:
```bash
curl http://localhost:5001/status
```

Expected response:
```json
{
  "wav2lip_installed": true,
  "directories": {
    "uploads": true,
    "audio": true,
    "video": true
  }
}
```

## 🎯 Example Workflow

1. **Prepare**: Have a clear face image ready
2. **Start**: Run `python face-gen.py`
3. **Upload**: Drag your image to the interface
4. **Type**: Enter your text (e.g., "Hello, I am your digital avatar!")
5. **Generate**: Click the generate button
6. **Wait**: Processing takes 1-3 minutes
7. **Download**: Get your video file

## 🚀 Performance Comparison

### Apple Silicon MPS vs CPU
- **Large Operations**: MPS 2-5x faster
- **Model Inference**: Significant acceleration
- **Memory Operations**: Faster tensor operations
- **Small Operations**: CPU may be faster

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Verify your conda environment is activated
3. Ensure all dependencies are installed
4. Check the system status endpoint

---

**🎭 Face-Gen: Create amazing digital avatars with AI!** 