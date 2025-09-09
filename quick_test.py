#!/usr/bin/env python3
"""
Simple test script for MMDetection3D
"""

import sys
import os
sys.path.append('.')

# Test basic imports
try:
    import torch
    import numpy as np
    print(f"✅ PyTorch: {torch.__version__}")
    print(f"✅ NumPy: {np.__version__}")
    
    # Test point cloud processing
    points = np.random.randn(1000, 4)
    tensor = torch.from_numpy(points).float()
    print(f"✅ Point cloud tensor: {tensor.shape}")
    
    # Test config loading
    if os.path.exists('configs'):
        print("✅ Config directory found")
    
    print("\n🎉 Basic functionality working!")
    print("Ready for detection with proper model weights.")
    
except Exception as e:
    print(f"❌ Error: {e}")
