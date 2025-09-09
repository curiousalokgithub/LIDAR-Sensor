#!/usr/bin/env python3
"""
STEP 3: Testing Configuration Files
Testing the model configurations in MMDetection3D
"""

import os
import glob
import matplotlib.pyplot as plt

print("🔬 STEP 3: TESTING CONFIGURATION FILES")
print("=" * 60)

# Test 1: Explore config structure
configs_path = "mmdetection3d/configs"
print(f"\n📁 Configuration Directory Analysis:")

config_categories = {}
total_configs = 0

if os.path.exists(configs_path):
    for category in os.listdir(configs_path):
        category_path = os.path.join(configs_path, category)
        if os.path.isdir(category_path):
            # Count config files in this category
            config_files = glob.glob(os.path.join(category_path, "*.py"))
            config_categories[category] = len(config_files)
            total_configs += len(config_files)
            
            print(f"  📂 {category}: {len(config_files)} configurations")
            
            # Show first few configs as examples
            if config_files:
                for i, config_file in enumerate(config_files[:2]):  # Show first 2
                    config_name = os.path.basename(config_file)
                    size = os.path.getsize(config_file)
                    print(f"    ├─ {config_name} ({size} bytes)")
                if len(config_files) > 2:
                    print(f"    └─ ... and {len(config_files)-2} more")

print(f"\n📊 Total Configurations: {total_configs}")

# Test 2: Analyze specific intrusion detection relevant configs
print(f"\n🎯 Intrusion Detection Relevant Configurations:")

relevant_configs = ['pointpillars', 'votenet', 'centerpoint', 'pointnet2']

for config_type in relevant_configs:
    if config_type in config_categories:
        config_path = os.path.join(configs_path, config_type)
        config_files = glob.glob(os.path.join(config_path, "*.py"))
        
        print(f"\n📋 {config_type.upper()} Configurations ({len(config_files)} files):")
        print("  Use case: ", end="")
        
        if config_type == 'pointpillars':
            print("Real-time LIDAR detection (Best for intrusion detection)")
        elif config_type == 'votenet':
            print("Indoor object detection with voting mechanism")
        elif config_type == 'centerpoint':
            print("Center-based 3D object detection")
        elif config_type == 'pointnet2':
            print("Classic point cloud processing")
        
        # Show example configs
        for config_file in config_files[:3]:  # Show first 3
            config_name = os.path.basename(config_file)
            print(f"    ✅ {config_name}")

# Test 3: Read a sample configuration
print(f"\n📖 Sample Configuration Analysis:")

# Try to read a PointPillars config (good for intrusion detection)
pointpillars_path = os.path.join(configs_path, "pointpillars")
if os.path.exists(pointpillars_path):
    config_files = glob.glob(os.path.join(pointpillars_path, "*.py"))
    if config_files:
        sample_config = config_files[0]
        print(f"  Reading: {os.path.basename(sample_config)}")
        
        try:
            with open(sample_config, 'r') as f:
                lines = f.readlines()
            
            print(f"  📄 Config file has {len(lines)} lines")
            
            # Extract key information
            key_settings = []
            for line in lines[:30]:  # Check first 30 lines
                line = line.strip()
                if any(keyword in line.lower() for keyword in ['class_names', 'point_cloud_range', 'voxel_size']):
                    key_settings.append(line)
            
            if key_settings:
                print("  🔑 Key Settings Found:")
                for setting in key_settings:
                    print(f"    {setting}")
            
        except Exception as e:
            print(f"  ❌ Error reading config: {e}")

# Test 4: Create visualization of config analysis
print(f"\n🎨 Creating Configuration Analysis Visualization:")

# Prepare data for visualization
categories = list(config_categories.keys())
counts = list(config_categories.values())

# Create visualization
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('MMDetection3D Configuration Analysis', fontsize=16, fontweight='bold')

# Plot 1: Configuration categories bar chart
ax1.bar(categories[:8], counts[:8])  # Show top 8 categories
ax1.set_title('Configuration Categories')
ax1.set_ylabel('Number of Configs')
ax1.tick_params(axis='x', rotation=45)
ax1.grid(True, alpha=0.3)

# Plot 2: Intrusion detection relevant configs pie chart
relevant_data = {k: config_categories.get(k, 0) for k in relevant_configs}
relevant_names = list(relevant_data.keys())
relevant_values = list(relevant_data.values())

ax2.pie(relevant_values, labels=relevant_names, autopct='%1.1f%%', startangle=90)
ax2.set_title('Intrusion Detection Relevant Configs')

# Plot 3: Configuration recommendations
ax3.axis('off')
ax3.text(0.1, 0.9, 'RECOMMENDED CONFIGURATIONS', fontsize=14, fontweight='bold', transform=ax3.transAxes)

recommendations = [
    "🎯 PointPillars: Best for real-time intrusion detection",
    "🏢 VoteNet: Good for indoor security applications", 
    "🚗 CenterPoint: Excellent for vehicle detection",
    "🔧 PointNet2: Foundation for custom models",
]

y_pos = 0.7
for rec in recommendations:
    ax3.text(0.1, y_pos, rec, fontsize=10, transform=ax3.transAxes)
    y_pos -= 0.15

# Plot 4: Usage statistics
ax4.axis('off')
ax4.text(0.1, 0.9, 'CONFIGURATION STATISTICS', fontsize=14, fontweight='bold', transform=ax4.transAxes)

stats = [
    f"Total Configurations: {total_configs}",
    f"Model Categories: {len(config_categories)}",
    f"Intrusion Detection Ready: {sum(relevant_values)}",
    f"Most Configs: {max(config_categories, key=config_categories.get)} ({max(counts)})",
]

y_pos = 0.7
for stat in stats:
    ax4.text(0.1, y_pos, stat, fontsize=10, transform=ax4.transAxes)
    y_pos -= 0.15

plt.tight_layout()
plt.savefig('mmdet3d_config_analysis_step3.png', dpi=150, bbox_inches='tight')
print("  ✅ Saved configuration analysis: mmdet3d_config_analysis_step3.png")

plt.show()

print(f"\n✅ STEP 3 COMPLETED: Configuration analysis successful!")
print(f"   - Analyzed {total_configs} configuration files")
print(f"   - Identified {len(config_categories)} model categories")
print(f"   - Found {sum(relevant_values)} intrusion detection relevant configs")
print(f"   - Generated configuration analysis visualization")

print("\n" + "="*60)
