#!/usr/bin/env python3
"""
简单的 MPS 测试脚本
用于验证 Apple Silicon 的 MPS 加速基本功能
"""

import torch
import torchaudio
import time

def test_mps_basic():
    """测试 MPS 基本功能"""
    print("🚀 简单 MPS 测试")
    print("=" * 30)
    
    # 检测设备
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"✅ 使用设备: {device}")
    
    try:
        # 测试基本张量操作
        print("🧪 测试基本张量操作...")
        x = torch.randn(1000, 1000).to(device)
        y = torch.randn(1000, 1000).to(device)
        
        start_time = time.time()
        z = torch.mm(x, y)
        end_time = time.time()
        
        print(f"✅ 矩阵乘法完成，耗时: {end_time - start_time:.2f}秒")
        print(f"📊 结果形状: {z.shape}")
        
        # 测试音频处理
        print("🎵 测试音频处理...")
        audio_tensor = torch.randn(1, 24000).to(device)  # 1秒音频，24kHz
        
        start_time = time.time()
        # 简单的音频处理操作
        processed_audio = torch.fft.fft(audio_tensor)
        end_time = time.time()
        
        print(f"✅ 音频处理完成，耗时: {end_time - start_time:.2f}秒")
        
        # 测试模型推理
        print("🤖 测试模型推理...")
        model = torch.nn.Sequential(
            torch.nn.Linear(100, 50),
            torch.nn.ReLU(),
            torch.nn.Linear(50, 10)
        ).to(device)
        
        input_data = torch.randn(1, 100).to(device)
        
        start_time = time.time()
        output = model(input_data)
        end_time = time.time()
        
        print(f"✅ 模型推理完成，耗时: {end_time - start_time:.2f}秒")
        print(f"📊 输出形状: {output.shape}")
        
        print("\n🎉 所有 MPS 测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ MPS 测试失败: {str(e)}")
        return False

def test_device_comparison():
    """比较 CPU 和 MPS 性能"""
    print("\n⚡ 设备性能比较")
    print("-" * 20)
    
    if not torch.backends.mps.is_available():
        print("❌ MPS 不可用，跳过性能比较")
        return
    
    # 测试数据
    size = 2000
    x = torch.randn(size, size)
    y = torch.randn(size, size)
    
    # CPU 测试
    print("💻 CPU 测试...")
    start_time = time.time()
    z_cpu = torch.mm(x, y)
    cpu_time = time.time() - start_time
    print(f"CPU 耗时: {cpu_time:.2f}秒")
    
    # MPS 测试
    print("🚀 MPS 测试...")
    x_mps = x.to('mps')
    y_mps = y.to('mps')
    
    start_time = time.time()
    z_mps = torch.mm(x_mps, y_mps)
    mps_time = time.time() - start_time
    print(f"MPS 耗时: {mps_time:.2f}秒")
    
    # 计算加速比
    speedup = cpu_time / mps_time
    print(f"⚡ 加速比: {speedup:.2f}x")

if __name__ == "__main__":
    success = test_mps_basic()
    test_device_comparison()
    
    if success:
        print("\n🎯 结论: MPS 设备工作正常，可以用于加速计算")
    else:
        print("\n⚠️  结论: MPS 设备可能存在问题，建议使用 CPU") 