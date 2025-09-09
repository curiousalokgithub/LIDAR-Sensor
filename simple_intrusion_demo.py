#!/usr/bin/env python3
"""
🛡️ SIMPLE INTRUSION DETECTION DEMO
=====================================
This demonstrates a basic intrusion detection system using real LIDAR data
without requiring complex MMDetection3D installation.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os
import time

# Intrusion Detection Configuration
SECURITY_ZONE = {
    'x_min': -20, 'x_max': 20,    # 40m wide perimeter
    'y_min': -20, 'y_max': 20     # 40m deep perimeter
}

THREAT_LEVELS = {
    'SAFE': {'color': 'green', 'threshold': 0},
    'CAUTION': {'color': 'yellow', 'threshold': 5},
    'WARNING': {'color': 'orange', 'threshold': 15},
    'ALERT': {'color': 'red', 'threshold': 30}
}

def load_kitti_lidar_data():
    """Load real KITTI LIDAR data"""
    lidar_file = 'mmdetection3d/demo/data/kitti/000008.bin'
    
    if not os.path.exists(lidar_file):
        print(f"❌ LIDAR file not found: {lidar_file}")
        print("Creating simulated data for demonstration...")
        return create_simulated_intrusion_scenario()
    
    try:
        # Load binary LIDAR data (KITTI format: x, y, z, intensity)
        points = np.fromfile(lidar_file, dtype=np.float32).reshape(-1, 4)
        print(f"✅ Loaded real KITTI LIDAR data: {points.shape[0]} points")
        return points
    except Exception as e:
        print(f"❌ Error loading LIDAR: {e}")
        return create_simulated_intrusion_scenario()

def create_simulated_intrusion_scenario():
    """Create a realistic intrusion scenario for demonstration"""
    np.random.seed(42)
    
    # Background environment points (trees, buildings, ground)
    background = np.random.normal(0, 15, (8000, 4))
    background[:, 2] = np.random.uniform(-2, 4, 8000)  # Height variation
    background[:, 3] = np.random.uniform(0.1, 0.8, 8000)  # Intensity
    
    # Simulated intruders
    intruders = []
    
    # Vehicle approaching from east
    vehicle_points = np.random.normal([15, 5, 0.5, 0.7], [0.5, 1, 0.2, 0.1], (150, 4))
    intruders.append(('Vehicle', vehicle_points))
    
    # Person walking near perimeter
    person_points = np.random.normal([-12, -8, 0.8, 0.4], [0.3, 0.3, 0.3, 0.1], (50, 4))
    intruders.append(('Person', person_points))
    
    # Unknown object in restricted zone
    unknown_points = np.random.normal([8, -15, 1.2, 0.6], [0.8, 0.8, 0.4, 0.1], (80, 4))
    intruders.append(('Unknown', unknown_points))
    
    # Combine all points
    all_points = background.copy()
    for name, points in intruders:
        all_points = np.vstack([all_points, points])
    
    print(f"✅ Created simulation with {len(intruders)} potential threats")
    return all_points

def detect_intrusions(points):
    """Analyze LIDAR data for potential intrusions"""
    threats = []
    
    # Filter points within security zone
    in_zone = (
        (points[:, 0] >= SECURITY_ZONE['x_min']) & 
        (points[:, 0] <= SECURITY_ZONE['x_max']) &
        (points[:, 1] >= SECURITY_ZONE['y_min']) & 
        (points[:, 1] <= SECURITY_ZONE['y_max'])
    )
    
    zone_points = points[in_zone]
    
    # Cluster detection using simple spatial grouping
    if len(zone_points) > 0:
        clusters = cluster_points(zone_points)
        
        for i, cluster in enumerate(clusters):
            if len(cluster) > 10:  # Minimum points for valid object
                threat = analyze_cluster(cluster, i)
                threats.append(threat)
    
    return threats, zone_points

def cluster_points(points, distance_threshold=2.0):
    """Simple clustering algorithm to group nearby points"""
    clusters = []
    used = np.zeros(len(points), dtype=bool)
    
    for i in range(len(points)):
        if used[i]:
            continue
            
        # Start new cluster
        cluster = [points[i]]
        used[i] = True
        
        # Find nearby points
        for j in range(i+1, len(points)):
            if used[j]:
                continue
                
            distance = np.sqrt(np.sum((points[i][:2] - points[j][:2])**2))
            if distance < distance_threshold:
                cluster.append(points[j])
                used[j] = True
        
        if len(cluster) > 5:  # Minimum cluster size
            clusters.append(np.array(cluster))
    
    return clusters

def analyze_cluster(cluster, cluster_id):
    """Analyze a cluster to determine threat level"""
    center = np.mean(cluster[:, :3], axis=0)
    size = np.max(cluster[:, :3], axis=0) - np.min(cluster[:, :3], axis=0)
    point_count = len(cluster)
    
    # Determine object type based on characteristics
    if size[2] > 1.5 and point_count > 50:  # Tall and dense
        object_type = "Vehicle"
        risk_score = 25
    elif size[2] < 2.0 and point_count < 100:  # Human-sized
        object_type = "Person"
        risk_score = 15
    else:
        object_type = "Unknown"
        risk_score = 30
    
    # Determine threat level
    threat_level = "SAFE"
    for level, config in THREAT_LEVELS.items():
        if risk_score >= config['threshold']:
            threat_level = level
    
    return {
        'id': cluster_id,
        'type': object_type,
        'center': center,
        'size': size,
        'points': point_count,
        'risk_score': risk_score,
        'threat_level': threat_level
    }

def create_security_visualization(points, threats, zone_points):
    """Create comprehensive security monitoring visualization"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('🛡️ INTRUSION DETECTION SYSTEM - LIVE MONITORING', fontsize=16, fontweight='bold')
    
    # 1. Overview Map
    ax1.scatter(points[:, 0], points[:, 1], c='lightblue', s=1, alpha=0.5, label='Environment')
    ax1.scatter(zone_points[:, 0], zone_points[:, 1], c='red', s=3, alpha=0.7, label='Security Zone')
    
    # Draw security perimeter
    perimeter = Rectangle(
        (SECURITY_ZONE['x_min'], SECURITY_ZONE['y_min']),
        SECURITY_ZONE['x_max'] - SECURITY_ZONE['x_min'],
        SECURITY_ZONE['y_max'] - SECURITY_ZONE['y_min'],
        fill=False, edgecolor='red', linewidth=3, linestyle='--'
    )
    ax1.add_patch(perimeter)
    
    # Mark threats
    for threat in threats:
        color = THREAT_LEVELS[threat['threat_level']]['color']
        ax1.scatter(threat['center'][0], threat['center'][1], 
                   c=color, s=200, marker='X', edgecolor='black', linewidth=2)
        ax1.annotate(f"{threat['type']}\n{threat['threat_level']}", 
                    (threat['center'][0], threat['center'][1]),
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.7))
    
    ax1.set_title('📍 PERIMETER OVERVIEW')
    ax1.set_xlabel('Distance East (m)')
    ax1.set_ylabel('Distance North (m)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_aspect('equal')
    
    # 2. Height Analysis
    if len(zone_points) > 0:
        ax2.scatter(zone_points[:, 0], zone_points[:, 2], c='orange', s=10, alpha=0.6)
        ax2.set_title('📊 HEIGHT PROFILE ANALYSIS')
        ax2.set_xlabel('Distance East (m)')
        ax2.set_ylabel('Height (m)')
        ax2.grid(True, alpha=0.3)
        
        # Mark threat heights
        for threat in threats:
            color = THREAT_LEVELS[threat['threat_level']]['color']
            ax2.axhline(y=threat['center'][2], color=color, linestyle='--', 
                       label=f"{threat['type']} ({threat['center'][2]:.1f}m)")
    
    # 3. Threat Assessment
    threat_data = {level: 0 for level in THREAT_LEVELS.keys()}
    for threat in threats:
        threat_data[threat['threat_level']] += 1
    
    colors = [THREAT_LEVELS[level]['color'] for level in threat_data.keys()]
    bars = ax3.bar(threat_data.keys(), threat_data.values(), color=colors, alpha=0.7)
    ax3.set_title('⚠️ THREAT LEVEL DISTRIBUTION')
    ax3.set_ylabel('Number of Objects')
    
    # Add value labels on bars
    for bar, value in zip(bars, threat_data.values()):
        if value > 0:
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(value), ha='center', va='bottom', fontweight='bold')
    
    # 4. Detection Statistics
    stats_text = f"""
🔍 DETECTION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Total LIDAR Points: {len(points):,}
🎯 Points in Security Zone: {len(zone_points):,}
🚨 Threats Detected: {len(threats)}

📋 DETECTED OBJECTS:
"""
    
    for i, threat in enumerate(threats, 1):
        stats_text += f"""
{i}. {threat['type']} - {threat['threat_level']}
   • Position: ({threat['center'][0]:.1f}, {threat['center'][1]:.1f}, {threat['center'][2]:.1f})m
   • Size: {threat['size'][0]:.1f}×{threat['size'][1]:.1f}×{threat['size'][2]:.1f}m
   • Points: {threat['points']}
   • Risk Score: {threat['risk_score']}/100
"""
    
    if len(threats) == 0:
        stats_text += "\n✅ ALL CLEAR - NO THREATS DETECTED"
    
    ax4.text(0.05, 0.95, stats_text, transform=ax4.transAxes, 
             verticalalignment='top', fontfamily='monospace', fontsize=10)
    ax4.set_title('📈 SYSTEM STATUS')
    ax4.axis('off')
    
    plt.tight_layout()
    return fig

def main():
    """Main intrusion detection demonstration"""
    print("🛡️ INTRUSION DETECTION SYSTEM STARTING...")
    print("=" * 60)
    
    # Load LIDAR data
    print("\n📡 STEP 1: Loading LIDAR Data")
    points = load_kitti_lidar_data()
    print(f"   • Loaded {len(points):,} LIDAR points")
    
    # Detect intrusions
    print("\n🔍 STEP 2: Analyzing for Intrusions")
    threats, zone_points = detect_intrusions(points)
    print(f"   • {len(zone_points):,} points in security zone")
    print(f"   • {len(threats)} potential threats detected")
    
    # Create visualization
    print("\n📊 STEP 3: Creating Security Visualization")
    fig = create_security_visualization(points, threats, zone_points)
    
    # Save and display
    output_file = 'intrusion_detection_analysis.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"   • Saved analysis: {output_file}")
    
    # Display results
    print("\n🚨 SECURITY ALERT SUMMARY:")
    print("=" * 40)
    
    if threats:
        for threat in threats:
            status_icon = {"SAFE": "✅", "CAUTION": "⚠️", "WARNING": "🔶", "ALERT": "🚨"}
            print(f"{status_icon.get(threat['threat_level'], '❓')} {threat['threat_level']}: "
                  f"{threat['type']} at ({threat['center'][0]:.1f}, {threat['center'][1]:.1f})m")
    else:
        print("✅ ALL CLEAR - Perimeter secure")
    
    print(f"\n📱 Live monitoring visualization saved as: {output_file}")
    print("🔄 System ready for continuous monitoring...")
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()
