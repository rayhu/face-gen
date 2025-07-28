#!/usr/bin/env python3
"""
MPS 设备测试脚本
用于验证 Apple Silicon 的 MPS 加速是否可用
"""

import torch
import sys

def test_mps_availability():
    """测试 MPS 设备可用性"""
    print("🚀 Apple Silicon MPS 设备测试")
    print("=" * 40)
    
    # 检查 PyTorch 版本
    print(f"📦 PyTorch 版本: {torch.__version__}")
    
    # 检查 MPS 是否可用
    mps_available = torch.backends.mps.is_available()
    print(f"🔍 MPS 可用性: {mps_available}")
    
    if mps_available:
        print("✅ MPS 设备可用！")
        
        # 检查 MPS 是否已构建
        mps_built = torch.backends.mps.is_built()
        print(f"🔧 MPS 已构建: {mps_built}")
        
        # 创建 MPS 设备
        device = torch.device("mps")
        print(f"📱 设备类型: {device}")
        
        # 测试基本张量操作
        try:
            print("🧪 测试 MPS 张量操作...")
            x = torch.randn(3, 3).to(device)
            y = torch.randn(3, 3).to(device)
            z = torch.mm(x, y)
            print(f"✅ 矩阵乘法测试成功，结果形状: {z.shape}")
            
            # 测试模型移动到 MPS
            model = torch.nn.Linear(10, 5).to(device)
            input_tensor = torch.randn(1, 10).to(device)
            output = model(input_tensor)
            print(f"✅ 模型推理测试成功，输出形状: {output.shape}")
            
            print("\n🎉 MPS 设备测试全部通过！")
            return True
            
        except Exception as e:
            print(f"❌ MPS 测试失败: {str(e)}")
            return False
    else:
        print("❌ MPS 设备不可用")
        print("💡 可能的原因:")
        print("   - 不是 Apple Silicon Mac")
        print("   - macOS 版本低于 12.3")
        print("   - PyTorch 版本不支持 MPS")
        return False

def test_torch_device():
    """测试设备选择逻辑"""
    print("\n🔧 设备选择测试")
    print("-" * 20)
    
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"✅ 选择的设备: {device}")
    
    if device.type == "mps":
        print("🚀 将使用 Apple Silicon MPS 加速")
    else:
        print("💻 将使用 CPU 计算")
    
    return device

if __name__ == "__main__":
    success = test_mps_availability()
    test_device = test_torch_device()
    
    if success:
        print(f"\n🎯 建议: 您的代码可以使用 {test_device} 设备进行加速")
    else:
        print(f"\n⚠️  建议: 您的代码将使用 {test_device} 设备") 