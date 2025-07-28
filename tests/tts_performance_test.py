#!/usr/bin/env python3
"""
Tortoise TTS 性能测试
专门测试 TTS 任务中 MPS 和 CPU 的性能差异
"""

import torch
import time
import os
from tortoise.api import TextToSpeech

def test_tts_performance():
    """测试 TTS 性能"""
    print("🎤 Tortoise TTS 性能测试")
    print("=" * 40)
    
    # 测试文本
    test_texts = [
        "你好，这是一个测试。",
        "这是一个较长的测试文本，用于测试 TTS 的性能表现。",
        "这是一个非常长的测试文本，包含了更多的内容，用于测试在不同文本长度下 TTS 的性能表现。",
        "这是一个超长的测试文本，包含了大量的内容，用于测试在最大文本长度下 TTS 的性能表现，看看 MPS 和 CPU 的差异。"
    ]
    
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"✅ 使用设备: {device}")
    
    # 创建输出目录
    os.makedirs("audio", exist_ok=True)
    
    for i, text in enumerate(test_texts):
        print(f"\n📝 测试文本 {i+1} (长度: {len(text)} 字符)")
        print(f"文本内容: {text[:50]}{'...' if len(text) > 50 else ''}")
        
        # CPU 测试
        print("  💻 CPU 测试...")
        try:
            tts_cpu = TextToSpeech()
            start_time = time.time()
            gen_audio_cpu = tts_cpu.tts(text)
            cpu_time = time.time() - start_time
            
            # 保存 CPU 结果
            torchaudio.save(f"audio/cpu_test_{i+1}.wav", gen_audio_cpu.squeeze(0), 24000)
            cpu_file_size = os.path.getsize(f"audio/cpu_test_{i+1}.wav")
            
            print(f"    CPU 耗时: {cpu_time:.2f}秒")
            print(f"    CPU 文件大小: {cpu_file_size} bytes")
            
        except Exception as e:
            print(f"    ❌ CPU 测试失败: {str(e)}")
            cpu_time = float('inf')
            cpu_file_size = 0
        
        # MPS 测试
        print("  🚀 MPS 测试...")
        try:
            tts_mps = TextToSpeech()
            
            # 移动模型到 MPS
            if device.type == "mps":
                if hasattr(tts_mps, 'autoregressive'):
                    tts_mps.autoregressive = tts_mps.autoregressive.to(device)
                if hasattr(tts_mps, 'diffusion'):
                    tts_mps.diffusion = tts_mps.diffusion.to(device)
                if hasattr(tts_mps, 'vocoder'):
                    tts_mps.vocoder = tts_mps.vocoder.to(device)
                if hasattr(tts_mps, 'clvp'):
                    tts_mps.clvp = tts_mps.clvp.to(device)
            
            start_time = time.time()
            gen_audio_mps = tts_mps.tts(text)
            mps_time = time.time() - start_time
            
            # 将音频移回 CPU 并保存
            if device.type == "mps":
                gen_audio_mps = gen_audio_mps.cpu()
            
            torchaudio.save(f"audio/mps_test_{i+1}.wav", gen_audio_mps.squeeze(0), 24000)
            mps_file_size = os.path.getsize(f"audio/mps_test_{i+1}.wav")
            
            print(f"    MPS 耗时: {mps_time:.2f}秒")
            print(f"    MPS 文件大小: {mps_file_size} bytes")
            
        except Exception as e:
            print(f"    ❌ MPS 测试失败: {str(e)}")
            mps_time = float('inf')
            mps_file_size = 0
        
        # 性能比较
        if cpu_time != float('inf') and mps_time != float('inf'):
            speedup = cpu_time / mps_time
            print(f"  ⚡ 加速比: {speedup:.2f}x")
            
            if speedup > 1:
                print(f"  ✅ MPS 更快")
            else:
                print(f"  ⚠️  CPU 更快")
        else:
            print(f"  ❌ 无法比较性能")

def test_model_loading():
    """测试模型加载性能"""
    print("\n📦 模型加载性能测试")
    print("=" * 40)
    
    # CPU 模型加载
    print("💻 CPU 模型加载...")
    start_time = time.time()
    tts_cpu = TextToSpeech()
    cpu_load_time = time.time() - start_time
    print(f"  CPU 加载耗时: {cpu_load_time:.2f}秒")
    
    # MPS 模型加载
    print("🚀 MPS 模型加载...")
    start_time = time.time()
    tts_mps = TextToSpeech()
    
    # 移动模型到 MPS
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    if device.type == "mps":
        if hasattr(tts_mps, 'autoregressive'):
            tts_mps.autoregressive = tts_mps.autoregressive.to(device)
        if hasattr(tts_mps, 'diffusion'):
            tts_mps.diffusion = tts_mps.diffusion.to(device)
        if hasattr(tts_mps, 'vocoder'):
            tts_mps.vocoder = tts_mps.vocoder.to(device)
        if hasattr(tts_mps, 'clvp'):
            tts_mps.clvp = tts_mps.clvp.to(device)
    
    mps_load_time = time.time() - start_time
    print(f"  MPS 加载耗时: {mps_load_time:.2f}秒")
    
    # 比较加载时间
    load_speedup = cpu_load_time / mps_load_time
    print(f"  ⚡ 加载加速比: {load_speedup:.2f}x")

def cleanup_test_files():
    """清理测试文件"""
    print("\n🧹 清理测试文件...")
    test_files = [
        "audio/cpu_test_1.wav",
        "audio/cpu_test_2.wav", 
        "audio/cpu_test_3.wav",
        "audio/cpu_test_4.wav",
        "audio/mps_test_1.wav",
        "audio/mps_test_2.wav",
        "audio/mps_test_3.wav",
        "audio/mps_test_4.wav"
    ]
    
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"  ✅ 已删除: {file}")

if __name__ == "__main__":
    print("🎯 Tortoise TTS 性能基准测试")
    print("=" * 50)
    
    # 设置环境变量
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
    
    # 运行测试
    test_model_loading()
    test_tts_performance()
    
    print("\n📊 性能总结:")
    print("  - 对于 Tortoise TTS 任务，性能差异主要取决于:")
    print("    1. 文本长度")
    print("    2. 模型大小")
    print("    3. 数据传输开销")
    print("    4. 内存使用情况")
    
    # 清理文件
    cleanup_test_files()
    
    print("\n🎉 TTS 性能测试完成！") 