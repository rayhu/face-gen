#!/usr/bin/env python3
"""
性能基准测试脚本
详细比较 MPS 和 CPU 的性能差异
"""

import torch
import time
import numpy as np

def benchmark_matrix_operations():
    """基准测试矩阵运算"""
    print("🧮 矩阵运算性能测试")
    print("=" * 40)
    
    # 测试不同大小的矩阵
    sizes = [500, 1000, 2000, 3000]
    
    for size in sizes:
        print(f"\n📊 矩阵大小: {size}x{size}")
        
        # 创建测试数据
        x = torch.randn(size, size)
        y = torch.randn(size, size)
        
        # CPU 测试
        start_time = time.time()
        z_cpu = torch.mm(x, y)
        cpu_time = time.time() - start_time
        
        # MPS 测试
        if torch.backends.mps.is_available():
            x_mps = x.to('mps')
            y_mps = y.to('mps')
            
            start_time = time.time()
            z_mps = torch.mm(x_mps, y_mps)
            mps_time = time.time() - start_time
            
            # 计算加速比
            speedup = cpu_time / mps_time
            print(f"  CPU 耗时: {cpu_time:.3f}秒")
            print(f"  MPS 耗时: {mps_time:.3f}秒")
            print(f"  ⚡ 加速比: {speedup:.2f}x")
            
            if speedup > 1:
                print(f"  ✅ MPS 更快")
            else:
                print(f"  ⚠️  CPU 更快")
        else:
            print("  ❌ MPS 不可用")

def benchmark_model_inference():
    """基准测试模型推理"""
    print("\n🤖 模型推理性能测试")
    print("=" * 40)
    
    # 测试不同大小的模型
    model_sizes = [
        (100, 50),
        (500, 200),
        (1000, 500),
        (2000, 1000)
    ]
    
    for input_size, output_size in model_sizes:
        print(f"\n📊 模型大小: {input_size} -> {output_size}")
        
        # 创建模型和输入
        model = torch.nn.Sequential(
            torch.nn.Linear(input_size, output_size),
            torch.nn.ReLU(),
            torch.nn.Linear(output_size, output_size // 2)
        )
        
        input_data = torch.randn(1, input_size)
        
        # CPU 测试
        model_cpu = model
        start_time = time.time()
        output_cpu = model_cpu(input_data)
        cpu_time = time.time() - start_time
        
        # MPS 测试
        if torch.backends.mps.is_available():
            model_mps = model.to('mps')
            input_mps = input_data.to('mps')
            
            start_time = time.time()
            output_mps = model_mps(input_mps)
            mps_time = time.time() - start_time
            
            # 计算加速比
            speedup = cpu_time / mps_time
            print(f"  CPU 耗时: {cpu_time:.3f}秒")
            print(f"  MPS 耗时: {mps_time:.3f}秒")
            print(f"  ⚡ 加速比: {speedup:.2f}x")
            
            if speedup > 1:
                print(f"  ✅ MPS 更快")
            else:
                print(f"  ⚠️  CPU 更快")
        else:
            print("  ❌ MPS 不可用")

def benchmark_convolution():
    """基准测试卷积运算"""
    print("\n🔄 卷积运算性能测试")
    print("=" * 40)
    
    # 测试不同大小的卷积
    conv_sizes = [
        (1, 3, 64, 64),    # 小图像
        (1, 3, 128, 128),  # 中等图像
        (1, 3, 256, 256),  # 大图像
        (1, 3, 512, 512)   # 超大图像
    ]
    
    for batch, channels, height, width in conv_sizes:
        print(f"\n📊 卷积大小: {batch}x{channels}x{height}x{width}")
        
        # 创建输入和卷积层
        input_data = torch.randn(batch, channels, height, width)
        conv_layer = torch.nn.Conv2d(channels, channels * 2, kernel_size=3, padding=1)
        
        # CPU 测试
        start_time = time.time()
        output_cpu = conv_layer(input_data)
        cpu_time = time.time() - start_time
        
        # MPS 测试
        if torch.backends.mps.is_available():
            input_mps = input_data.to('mps')
            conv_mps = conv_layer.to('mps')
            
            start_time = time.time()
            output_mps = conv_mps(input_mps)
            mps_time = time.time() - start_time
            
            # 计算加速比
            speedup = cpu_time / mps_time
            print(f"  CPU 耗时: {cpu_time:.3f}秒")
            print(f"  MPS 耗时: {mps_time:.3f}秒")
            print(f"  ⚡ 加速比: {speedup:.2f}x")
            
            if speedup > 1:
                print(f"  ✅ MPS 更快")
            else:
                print(f"  ⚠️  CPU 更快")
        else:
            print("  ❌ MPS 不可用")

def benchmark_memory_operations():
    """基准测试内存操作"""
    print("\n💾 内存操作性能测试")
    print("=" * 40)
    
    # 测试不同大小的张量操作
    sizes = [1000000, 5000000, 10000000, 20000000]  # 元素数量
    
    for size in sizes:
        print(f"\n📊 张量大小: {size:,} 元素")
        
        # 创建测试数据
        x = torch.randn(size)
        y = torch.randn(size)
        
        # CPU 测试
        start_time = time.time()
        z_cpu = x + y
        cpu_time = time.time() - start_time
        
        # MPS 测试
        if torch.backends.mps.is_available():
            x_mps = x.to('mps')
            y_mps = y.to('mps')
            
            start_time = time.time()
            z_mps = x_mps + y_mps
            mps_time = time.time() - start_time
            
            # 计算加速比
            speedup = cpu_time / mps_time
            print(f"  CPU 耗时: {cpu_time:.3f}秒")
            print(f"  MPS 耗时: {mps_time:.3f}秒")
            print(f"  ⚡ 加速比: {speedup:.2f}x")
            
            if speedup > 1:
                print(f"  ✅ MPS 更快")
            else:
                print(f"  ⚠️  CPU 更快")
        else:
            print("  ❌ MPS 不可用")

def overall_summary():
    """总体性能总结"""
    print("\n📈 性能总结")
    print("=" * 40)
    
    # 检测设备信息
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"🎯 当前设备: {device}")
    
    if device.type == "mps":
        print("✅ MPS 设备可用")
        print("💡 性能建议:")
        print("   - 对于大型矩阵运算，MPS 通常比 CPU 快 2-5 倍")
        print("   - 对于小型运算，CPU 可能更快（数据传输开销）")
        print("   - 对于深度学习模型，MPS 通常有明显优势")
        print("   - 建议根据具体任务选择最优设备")
    else:
        print("❌ MPS 设备不可用")
        print("💡 可能的原因:")
        print("   - 不是 Apple Silicon Mac")
        print("   - macOS 版本低于 12.3")
        print("   - PyTorch 版本不支持 MPS")

if __name__ == "__main__":
    print("🚀 Apple Silicon 性能基准测试")
    print("=" * 50)
    
    # 运行各项测试
    benchmark_matrix_operations()
    benchmark_model_inference()
    benchmark_convolution()
    benchmark_memory_operations()
    overall_summary()
    
    print("\n🎉 性能测试完成！") 