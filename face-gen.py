#!/usr/bin/env python3
"""
Face-Gen: Digital Avatar Generator
A simple startup script for the face-gen project
"""

import os
import sys
import subprocess
import socket
import time

def find_available_port(start_port=5000, max_attempts=100):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def start_face_gen():
    """Start the Face-Gen application"""
    print("🎭 Face-Gen: Digital Avatar Generator")
    print("=" * 50)
    
    # Check if conda environment is activated
    if 'face-gen' not in os.environ.get('CONDA_DEFAULT_ENV', ''):
        print("⚠️  Please activate the face-gen conda environment first:")
        print("   conda activate face-gen")
        return False
    
    # Set environment variable
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
    
    # Find available port
    port = find_available_port()
    if port is None:
        print("❌ No available ports found")
        return False
    
    print(f"✅ Found available port: {port}")
    
    # Update the Flask app to use the found port
    main_py_path = "app/main.py"
    if os.path.exists(main_py_path):
        with open(main_py_path, 'r') as f:
            content = f.read()
        
        # Replace the port in the file
        import re
        content = re.sub(r'port=\d+', f'port={port}', content)
        
        with open(main_py_path, 'w') as f:
            f.write(content)
    
    print(f"🚀 Starting Face-Gen on port {port}...")
    print(f"🌐 Open your browser to: http://localhost:{port}")
    print("🔄 Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        # Start the Flask app
        subprocess.run([
            sys.executable, 'app/main.py'
        ], env=os.environ)
    except KeyboardInterrupt:
        print("\n🛑 Face-Gen stopped")
    except Exception as e:
        print(f"❌ Error starting Face-Gen: {e}")
        return False
    
    return True

def main():
    """Main function"""
    try:
        return start_face_gen()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 