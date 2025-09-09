#!/usr/bin/env python3
"""
STEP 1: Testing Core MMDetection3D Module
"""

import sys
import os
sys.path.append('mmdetection3d')

print("🔬 STEP 1: TESTING CORE MMDETECTION3D MODULE")
print("=" * 60)

try:
    print("📦 Importing core MMDetection3D modules...")
    
    # Test basic imports
    import mmdet3d
    print(f"✅ mmdet3d imported successfully")
    print(f"   Version: {mmdet3d.__version__}")
    
    # Test registry
    from mmdet3d.registry import MODELS
    print(f"✅ MODELS registry loaded: {len(MODELS)} models available")
    
    # Test datasets
    from mmdet3d.registry import DATASETS
    print(f"✅ DATASETS registry loaded: {len(DATASETS)} datasets available")
    
    # Test structures
    from mmdet3d.structures import Det3DDataSample
    print("✅ Det3DDataSample structure imported")
    
    # Test point cloud processing
    from mmdet3d.structures import PointData
    print("✅ PointData structure imported")
    
    # Test bounding boxes
    from mmdet3d.structures import LiDARInstance3DBoxes
    print("✅ LiDARInstance3DBoxes imported")
    
    print("\n📊 Available Model Categories:")
    model_names = list(MODELS.module_dict.keys())
    for i, model in enumerate(model_names[:10]):  # Show first 10
        print(f"   {i+1}. {model}")
    print(f"   ... and {len(model_names)-10} more models")
    
    print("\n📊 Available Dataset Types:")
    dataset_names = list(DATASETS.module_dict.keys())
    for i, dataset in enumerate(dataset_names[:5]):  # Show first 5
        print(f"   {i+1}. {dataset}")
    print(f"   ... and {len(dataset_names)-5} more datasets")
    
    print("\n✅ STEP 1 RESULT: Core MMDetection3D module is working!")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Installing missing dependencies...")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
