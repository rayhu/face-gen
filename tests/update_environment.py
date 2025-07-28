#!/usr/bin/env python3
"""
环境更新脚本
用于确保 Apple Silicon 优化的依赖都正确安装
"""

import subprocess
import sys
import os

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def update_environment():
    """更新环境依赖"""
    print("🚀 Apple Silicon 环境优化")
    print("=" * 40)
    
    # 检查是否在 conda 环境中
    if not os.environ.get('CONDA_DEFAULT_ENV'):
        print("❌ 请先激活 conda 环境")
        return False
    
    print(f"📦 当前环境: {os.environ.get('CONDA_DEFAULT_ENV')}")
    
    # 更新 PyTorch 到 Apple Silicon 优化版本
    commands = [
        ("pip install --upgrade torch torchvision torchaudio", "更新 PyTorch 到最新版本"),
        ("pip install --upgrade accelerate", "更新 Accelerate 库"),
        ("pip install --upgrade transformers", "更新 Transformers 库"),
        ("pip install --upgrade huggingface-hub", "更新 Hugging Face Hub"),
        ("pip install --upgrade safetensors", "更新 SafeTensors"),
        ("pip install --upgrade psutil", "更新 psutil"),
    ]
    
    success_count = 0
    for command, description in commands:
        if run_command(command, description):
            success_count += 1
    
    print(f"\n📊 更新结果: {success_count}/{len(commands)} 成功")
    
    if success_count == len(commands):
        print("🎉 所有依赖更新成功！")
        return True
    else:
        print("⚠️  部分依赖更新失败，但环境仍可使用")
        return True

def test_environment():
    """测试环境配置"""
    print("\n🧪 测试环境配置")
    print("-" * 20)
    
    test_imports = [
        ("torch", "PyTorch"),
        ("torchaudio", "TorchAudio"),
        ("torchvision", "TorchVision"),
        ("transformers", "Transformers"),
        ("accelerate", "Accelerate"),
        ("tortoise", "Tortoise TTS"),
    ]
    
    success_count = 0
    for module, name in test_imports:
        try:
            __import__(module)
            print(f"✅ {name} 导入成功")
            success_count += 1
        except ImportError as e:
            print(f"❌ {name} 导入失败: {e}")
    
    print(f"\n📊 导入测试: {success_count}/{len(test_imports)} 成功")
    
    # 测试 MPS
    try:
        import torch
        if torch.backends.mps.is_available():
            print("✅ MPS 设备可用")
            success_count += 1
        else:
            print("❌ MPS 设备不可用")
    except Exception as e:
        print(f"❌ MPS 测试失败: {e}")
    
    return success_count >= len(test_imports)

if __name__ == "__main__":
    print("🔧 Apple Silicon 环境优化工具")
    print("=" * 40)
    
    # 更新环境
    update_success = update_environment()
    
    # 测试环境
    test_success = test_environment()
    
    if update_success and test_success:
        print("\n🎉 环境优化完成！您的 Apple Silicon Mac 已准备就绪。")
    else:
        print("\n⚠️  环境优化部分完成，建议检查失败的组件。") 