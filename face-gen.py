#!/usr/bin/env python3
"""
Face-Gen: Digital Avatar Generator
Smart startup script that automatically finds an available port and starts the Flask application
"""

import os
import sys
import socket
import subprocess
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
    print("Face-Gen: Digital Avatar Generator")
    print("=" * 50)
    
    # Check if conda environment is activated
    if 'CONDA_DEFAULT_ENV' not in os.environ or os.environ['CONDA_DEFAULT_ENV'] != 'face-gen':
        print("Please activate the face-gen conda environment first:")
        print("conda activate face-gen")
        return False
    
    # Set environment variables
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
    
    # Find available port
    port = find_available_port()
    if port is None:
        print("No available ports found")
        return False
    
    print(f"Found available port: {port}")
    
    # Update the Flask app to use the found port
    main_py_path = "app/main.py"
    if os.path.exists(main_py_path):
        with open(main_py_path, 'r') as f:
            content = f.read()
        
        # Replace the port in the file
        content = content.replace('port=5001', f'port={port}')
        
        with open(main_py_path, 'w') as f:
            f.write(content)
    
    # Start the Flask app
    print(f"Starting Face-Gen on port {port}...")
    print(f"Open your browser to: http://localhost:{port}")
    print("Press Ctrl+C to stop the application")
    
    try:
        process = subprocess.Popen([
            sys.executable, 'app/main.py'
        ], env=os.environ)
        
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\nFace-Gen stopped")
            process.terminate()
            process.wait()
            
    except Exception as e:
        print(f"Error starting Face-Gen: {e}")
        return False
    
    return True

def main():
    """Main function"""
    try:
        success = start_face_gen()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 