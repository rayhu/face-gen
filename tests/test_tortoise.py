#!/usr/bin/env python3
"""
Tortoise TTS 测试脚本
用于验证安装是否成功并测试基本功能
"""

import os
import torch
import torchaudio
from tortoise.api import TextToSpeech

# 检测并使用 MPS 设备
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"✅ 当前使用设备: {device}")

def test_tortoise_tts():
    """测试 Tortoise TTS 基本功能"""
    print("🎤 开始测试 Tortoise TTS...")
    
    # 创建输出目录
    os.makedirs("audio", exist_ok=True)
    
    # 测试文本
    test_text = "Hello, this is a test of Tortoise TTS."
    
    try:
        # 初始化 TTS
        print("📝 初始化 Tortoise TTS...")
        tts = TextToSpeech()
        
        # 将模型移动到 MPS 设备
        if hasattr(tts, 'autoregressive'):
            tts.autoregressive = tts.autoregressive.to(device)
        if hasattr(tts, 'diffusion'):
            tts.diffusion = tts.diffusion.to(device)
        if hasattr(tts, 'vocoder'):
            tts.vocoder = tts.vocoder.to(device)
        if hasattr(tts, 'clvp'):
            tts.clvp = tts.clvp.to(device)
        
        # 生成语音 - 使用默认声音
        print("🎵 生成语音中...")
        output_path = "audio/test_output.wav"
        
        # 使用正确的 API - 不指定 voice_samples 使用默认声音
        gen_audio = tts.tts(test_text)
        
        # 将音频数据移回 CPU 并保存
        if device.type == "mps":
            gen_audio = gen_audio.cpu()
        
        torchaudio.save(output_path, gen_audio.squeeze(0), 24000)
        
        # 检查文件是否生成
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ 测试成功！")
            print(f"📁 输出文件: {output_path}")
            print(f"📊 文件大小: {file_size} bytes")
            print(f"🎯 测试文本: {test_text}")
        else:
            print("❌ 输出文件未生成")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Tortoise TTS 功能测试")
    print("=" * 40)
    
    success = test_tortoise_tts()
    
    if success:
        print("\n🎉 所有测试通过！Tortoise TTS 已准备就绪。")
    else:
        print("\n💥 测试失败，请检查安装。") 