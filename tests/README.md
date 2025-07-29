# Face-Gen Test Suite

This folder contains all test files for the Face-Gen digital avatar generator.

## Available Tests

### Core Tests
- **`test_device_detection.py`** - Tests the device detection system (MPS/CUDA/CPU)
- **`test_setup.py`** - Tests the overall system setup and dependencies
- **`test_docker.py`** - Tests Docker deployment and compatibility

### Performance Tests
- **`performance_benchmark.py`** - Performance benchmarks for different devices
- **`tts_performance_test.py`** - TTS performance comparison tests
- **`quick_mps_test.py`** - Quick MPS availability and functionality tests

### Utility Tests
- **`simple_mps_test.py`** - Simple MPS device tests
- **`test_tortoise.py`** - Tortoise TTS functionality tests
- **`test_mps.py`** - MPS device compatibility tests
- **`final_test.py`** - Complete system integration tests
- **`update_environment.py`** - Environment update and verification tests

## Running Tests

### Run All Tests
```bash
# From the project root
python tests/run_tests.py

# Or from the tests folder
cd tests
python run_tests.py
```

### Run Specific Test
```bash
# Run device detection test
python tests/run_tests.py test_device_detection

# Run setup test
python tests/run_tests.py test_setup

# Run Docker test
python tests/run_tests.py test_docker
```

### Run Individual Test Files
```bash
# Run device detection test directly
python tests/test_device_detection.py

# Run setup test directly
python tests/test_setup.py

# Run Docker test directly
python tests/test_docker.py
```

## Test Categories

### 1. Device Detection Tests
Tests the intelligent device detection system that automatically selects the best available device (MPS/CUDA/CPU).

### 2. Setup Verification Tests
Tests that all dependencies are properly installed and the system is ready for use.

### 3. Docker Compatibility Tests
Tests Docker deployment and ensures the application works correctly in containerized environments.

### 4. Performance Tests
Benchmarks and performance comparisons between different devices and configurations.

## Test Configuration

### Environment Setup
```bash
# Activate the conda environment
conda activate face-gen

# Set required environment variables
export KMP_DUPLICATE_LIB_OK=TRUE
```

### Test Dependencies
All tests require the main application dependencies to be installed:
- Flask
- PyTorch
- Tortoise TTS
- Wav2Lip
- Other dependencies listed in `requirements.txt`

## Test Results

### Expected Output
```
Face-Gen Test Suite
==================================================

Running test_device_detection.py...
--------------------------------------------------
PASS: test_device_detection.py

Running test_setup.py...
--------------------------------------------------
PASS: test_setup.py

Running test_docker.py...
--------------------------------------------------
PASS: test_docker.py

Test Summary
====================
test_device_detection.py: PASS
test_setup.py: PASS
test_docker.py: PASS

Overall: 3/3 tests passed
All tests passed!
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure you're running tests from the project root
   - Check that the conda environment is activated
   - Verify all dependencies are installed

2. **Device Detection Failures**
   - Check macOS version (12.3+ for MPS)
   - Verify PyTorch installation
   - Ensure Apple Silicon Mac for MPS tests

3. **Docker Test Failures**
   - Ensure Docker is installed and running
   - Check Docker permissions
   - Verify Docker build context

### Debug Mode
```bash
# Run tests with verbose output
python -v tests/test_device_detection.py

# Run with Python debugger
python -m pdb tests/test_device_detection.py
```

## Performance Testing

### Device Comparison
Tests compare performance between:
- **CPU**: Baseline performance
- **MPS**: Apple Silicon GPU acceleration
- **CUDA**: NVIDIA GPU acceleration (if available)

### Benchmark Metrics
- **Matrix Operations**: Large tensor operations
- **Model Inference**: AI model performance
- **Memory Operations**: Tensor memory operations
- **End-to-End**: Complete workflow performance

## Continuous Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    conda activate face-gen
    python tests/run_tests.py
```

---

**Test Status**: All tests are designed to ensure the Face-Gen application works correctly across different environments and configurations. 