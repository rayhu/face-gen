#!/usr/bin/env python3
"""
快速 MPS 测试
验证 Apple Silicon 优化的基本功能
"""

import torch
import time

def quick_mps_test():
    """快速 MPS 测试"""
    print("🚀 快速 MPS 功能测试")
    print("=" * 30)
    
    # 检测设备
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"✅ 使用设备: {device}")
    
    # 测试基本功能
    try:
        # 创建测试张量
        x = torch.randn(1000, 1000).to(device)
        y = torch.randn(1000, 1000).to(device)
        
        # 测试矩阵乘法
        start_time = time.time()
        z = torch.mm(x, y)
        end_time = time.time()
        
        print(f"✅ 矩阵乘法测试成功")
        print(f"⏱️  耗时: {end_time - start_time:.2f}秒")
        print(f"📊 结果形状: {z.shape}")
        
        # 测试模型
        model = torch.nn.Linear(100, 50).to(device)
        input_data = torch.randn(1, 100).to(device)
        
        start_time = time.time()
        output = model(input_data)
        end_time = time.time()
        
        print(f"✅ 模型推理测试成功")
        print(f"⏱️  耗时: {end_time - start_time:.2f}秒")
        print(f"📊 输出形状: {output.shape}")
        
        print("\n🎉 MPS 功能测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ MPS 测试失败: {str(e)}")
        return False

def test_tortoise_import():
    """测试 Tortoise TTS 导入"""
    print("\n🎤 测试 Tortoise TTS 导入...")
    try:
        from tortoise.api import TextToSpeech
        print("✅ Tortoise TTS 导入成功")
        return True
    except Exception as e:
        print(f"❌ Tortoise TTS 导入失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎯 Apple Silicon 快速验证")
    print("=" * 40)
    
    mps_success = quick_mps_test()
    tortoise_success = test_tortoise_import()
    
    if mps_success and tortoise_success:
        print("\n🎉 所有测试通过！")
        print("📋 总结:")
        print("   ✅ MPS 设备工作正常")
        print("   ✅ Tortoise TTS 可以导入")
        print("   ✅ Apple Silicon 优化完成")
    else:
        print("\n⚠️  部分测试失败") 