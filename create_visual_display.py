#!/usr/bin/env python3
"""
VISUAL DISPLAY TEST
Create and show the actual visual representation of intrusion detection
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import os

print("🎨 CREATING VISUAL INTRUSION DETECTION DISPLAY")
print("=" * 55)

# Recreate the same scenario from Test 2
print("\n📡 Step 1: Recreating Test 2 Scenario")
print("Person at 2.2m, Vehicle at 5.2m")

# Person data (from Test 2)
person_x, person_y = 2.0, 1.0  # Position that gives 2.2m distance
person_distance = np.sqrt(person_x**2 + person_y**2)

# Vehicle data (from Test 2)  
vehicle_x, vehicle_y = 5.0, -1.5  # Position that gives 5.2m distance
vehicle_distance = np.sqrt(vehicle_x**2 + vehicle_y**2)

print(f"✓ Person: ({person_x}, {person_y}) = {person_distance:.1f}m")
print(f"✓ Vehicle: ({vehicle_x}, {vehicle_y}) = {vehicle_distance:.1f}m")

print("\n🎨 Step 2: Creating Security Display")

# Create the visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
fig.suptitle('🛡️ INTRUSION DETECTION SYSTEM - Test 2 Results', fontsize=16, fontweight='bold')

# Plot 1: Bird's Eye Security View
ax1.set_facecolor('black')

# Draw security zones
danger_zone = Circle((0, 0), 5, fill=False, color='red', linewidth=3, linestyle='--', label='DANGER ZONE (0-5m)')
warning_zone = Circle((0, 0), 10, fill=False, color='orange', linewidth=2, linestyle='--', label='WARNING ZONE (5-10m)')
monitor_zone = Circle((0, 0), 20, fill=False, color='yellow', linewidth=1, linestyle='--', label='MONITOR ZONE (10-20m)')

ax1.add_patch(danger_zone)
ax1.add_patch(warning_zone)
ax1.add_patch(monitor_zone)

# Plot LIDAR sensor at center
ax1.scatter(0, 0, c='lime', s=300, marker='*', edgecolor='white', linewidth=2, label='LIDAR SENSOR', zorder=5)

# Plot detected objects
ax1.scatter(person_x, person_y, c='red', s=400, marker='o', edgecolor='white', linewidth=3, label='PERSON (HIGH THREAT)', zorder=4)
ax1.scatter(vehicle_x, vehicle_y, c='blue', s=400, marker='s', edgecolor='white', linewidth=3, label='VEHICLE (WARNING)', zorder=4)

# Add distance labels
ax1.annotate(f'PERSON\n{person_distance:.1f}m\nHIGH THREAT', 
             (person_x, person_y), xytext=(10, 10), textcoords='offset points', 
             color='red', fontweight='bold', fontsize=10,
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

ax1.annotate(f'VEHICLE\n{vehicle_distance:.1f}m\nWARNING', 
             (vehicle_x, vehicle_y), xytext=(10, -20), textcoords='offset points', 
             color='blue', fontweight='bold', fontsize=10,
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

ax1.set_xlim(-12, 12)
ax1.set_ylim(-12, 12)
ax1.set_xlabel('Distance East/West (meters)', color='white', fontweight='bold')
ax1.set_ylabel('Distance North/South (meters)', color='white', fontweight='bold')
ax1.set_title("🔍 Bird's Eye Security View", color='white', fontweight='bold', fontsize=14)
ax1.legend(loc='upper right', facecolor='black', edgecolor='white')
ax1.grid(True, alpha=0.3, color='white')

# Plot 2: Threat Analysis Dashboard
ax2.set_facecolor('black')
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)

# Threat level indicator
threat_level = "HIGH"
threat_color = 'red'

ax2.text(0.5, 0.9, f"THREAT LEVEL: {threat_level}", 
         ha='center', va='center', fontsize=20, fontweight='bold',
         color=threat_color, transform=ax2.transAxes,
         bbox=dict(boxstyle='round,pad=0.5', facecolor=threat_color, alpha=0.2))

# Status
ax2.text(0.5, 0.75, "🚨 SECURITY BREACH DETECTED", 
         ha='center', va='center', fontsize=14, fontweight='bold',
         color='red', transform=ax2.transAxes)

# Alerts
alerts = [
    "🚨 CRITICAL: Person in danger zone (2.2m)",
    "⚠️ WARNING: Vehicle detected (5.2m)", 
    "📞 Security team notified",
    "🎥 Camera system activated",
    "🚪 Access points secured"
]

ax2.text(0.05, 0.6, "ACTIVE ALERTS:", fontsize=12, fontweight='bold', 
         color='white', transform=ax2.transAxes)

for i, alert in enumerate(alerts):
    ax2.text(0.05, 0.5 - i*0.08, alert, fontsize=10, 
             color='white', transform=ax2.transAxes)

# Detection summary
ax2.text(0.05, 0.15, f"DETECTIONS: 2 objects", fontsize=12, fontweight='bold', 
         color='cyan', transform=ax2.transAxes)
ax2.text(0.05, 0.1, f"SCAN TIME: 0.1 seconds", fontsize=10, 
         color='gray', transform=ax2.transAxes)
ax2.text(0.05, 0.05, f"STATUS: ACTIVE MONITORING", fontsize=10, 
         color='lime', transform=ax2.transAxes)

ax2.set_title("🛡️ Security Status Dashboard", color='white', fontweight='bold', fontsize=14)
ax2.axis('off')

plt.tight_layout()

# Save the visualization
filename = 'test2_visual_display.png'
plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='black')
print(f"💾 Saved visualization: {filename}")

# Show file info
if os.path.exists(filename):
    size = os.path.getsize(filename)
    print(f"✅ File created: {size:,} bytes")

plt.show()

print("\n🎯 VISUAL DISPLAY EXPLANATION:")
print("=" * 40)
print("LEFT PANEL - Bird's Eye Security View:")
print("• Green star = LIDAR sensor position")
print("• Red circle = Person (HIGH THREAT in danger zone)")
print("• Blue square = Vehicle (WARNING in warning zone)")
print("• Colored circles = Security zones")
print("• Distance labels show exact threat distances")

print("\nRIGHT PANEL - Security Dashboard:")
print("• Shows current threat level (HIGH)")
print("• Lists active security alerts")
print("• Displays system status information")
print("• Shows detection summary")

print(f"\n📸 The visual display is saved as: {filename}")
print("This is exactly what security guards would see on their monitors!")
