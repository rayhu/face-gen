# Face-Gen Docker Deployment Guide

## 🐳 Docker and MPS Compatibility

### ❌ MPS Limitations in Docker

1. **Container Isolation**: Docker containers cannot directly access the host's Metal framework
2. **Driver Limitations**: MPS requires macOS Metal drivers, which are not available in containers
3. **Architecture Limitations**: Apple Silicon MPS has limited support in containerized environments

### ✅ Solution

We provide an intelligent device detection system that automatically selects the best available device:

- **Local Environment**: Prioritizes MPS (Apple Silicon GPU)
- **Docker Environment**: Automatically falls back to CPU or CUDA
- **Cloud Environment**: Supports CUDA (NVIDIA GPU) or CPU

## 🚀 Docker Deployment

### 1. Build Docker Image

```bash
# Build image
docker build -t face-gen .

# Or use docker-compose
docker-compose build
```

### 2. Run Container

```bash
# Using docker run
docker run -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/audio:/app/audio \
  -v $(pwd)/video:/app/video \
  -v $(pwd)/assets:/app/assets \
  face-gen

# Or use docker-compose
docker-compose up -d
```

### 3. Access Application

Open your browser and navigate to: **http://localhost:5000**

## 📊 Performance Comparison

### Local Environment vs Docker Environment

| Environment | MPS Support | Performance | Recommended Use |
|-------------|-------------|-------------|-----------------|
| **Local macOS** | ✅ Full Support | 2-5x Acceleration | Development, Testing |
| **Docker macOS** | ❌ Not Supported | CPU Performance | Deployment, Production |
| **Docker Linux** | ❌ Not Supported | CPU/CUDA | Server Deployment |

### Performance Benchmarks

```bash
# Local Environment (MPS)
python app/scripts/tts_generate.py
# Expected time: 30-60 seconds

# Docker Environment (CPU)
docker run face-gen python app/scripts/tts_generate.py
# Expected time: 2-5 minutes
```

## 🔧 Advanced Configuration

### 1. Using Host Network (macOS)

```bash
# Using host network on macOS may provide better performance
docker run --network host \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/audio:/app/audio \
  -v $(pwd)/video:/app/video \
  face-gen
```

### 2. Multi-stage Build Optimization

```dockerfile
# Optimized Dockerfile
FROM python:3.10-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production image
FROM python:3.10-slim

# Copy installed packages
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV KMP_DUPLICATE_LIB_OK=TRUE

EXPOSE 5000
CMD ["python", "app/main.py"]
```

### 3. Production Environment Configuration

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  face-gen:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
      - ./audio:/app/audio
      - ./video:/app/video
    environment:
      - FLASK_ENV=production
      - KMP_DUPLICATE_LIB_OK=TRUE
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 2G
```

## 🐛 Troubleshooting

### Common Issues

1. **MPS Not Available**
   ```bash
   # Check device detection
   docker run face-gen python app/scripts/device_detection.py
   ```

2. **Insufficient Memory**
   ```bash
   # Increase memory limit
   docker run --memory=4g face-gen
   ```

3. **Model Download Failed**
   ```bash
   # Rebuild image
   docker build --no-cache -t face-gen .
   ```

### Performance Optimization

1. **Use SSD Storage**
   ```bash
   # Mount data directory to SSD
   docker run -v /ssd/face-gen:/app/data face-gen
   ```

2. **Increase CPU Cores**
   ```bash
   # Allocate more CPU cores
   docker run --cpus=4 face-gen
   ```

3. **Use GPU (if available)**
   ```bash
   # Use NVIDIA GPU
   docker run --gpus all face-gen
   ```

## 📈 Monitoring and Logs

### Health Checks

```bash
# Check application status
curl http://localhost:5000/status

# View container logs
docker logs face-gen-container
```

### Performance Monitoring

```bash
# Monitor container resource usage
docker stats face-gen-container

# Check device usage
docker exec face-gen-container python app/scripts/device_detection.py
```

## 🎯 Best Practices

### Development Environment
- Use local environment for best MPS performance
- Use Docker for consistency testing

### Production Environment
- Use Docker to ensure deployment consistency
- Configure appropriate resource limits
- Use load balancer for high concurrency

### Performance Recommendations
1. **Local Development**: Prioritize MPS for best performance
2. **Docker Deployment**: Accept CPU performance, ensure stability
3. **Cloud Deployment**: Consider GPU instances for better performance

## 🔄 Migration Strategy

### From Local to Docker

1. **Test Compatibility**
   ```bash
   # Test functionality in Docker
   docker run face-gen python test_setup.py
   ```

2. **Performance Benchmarking**
   ```bash
   # Compare local and Docker performance
   time python app/scripts/tts_generate.py  # Local
   time docker run face-gen python app/scripts/tts_generate.py  # Docker
   ```

3. **Gradual Migration**
   - Test in Docker first
   - Deploy after confirming functionality
   - Monitor performance metrics

---

**Summary**: MPS is not available in Docker, but our intelligent device detection system automatically selects the best available device, ensuring the application runs properly in any environment. 