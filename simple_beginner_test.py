#!/usr/bin/env python3
"""
SUPER SIMPLE INTRUSION DETECTION TEST
For beginners - shows basic concepts step by step
"""

import numpy as np
import matplotlib.pyplot as plt

print("🏠 SIMPLE SECURITY SYSTEM TEST")
print("=" * 40)

print("\n📡 Step 1: Simulating LIDAR Sensor...")
print("The sensor scans and finds 3D points (x, y, z)")

# Create simple fake sensor data
print("Creating fake person at position (5, 2, 1.7 meters)...")
person_x = [5, 5, 5, 5, 5]  # 5 meters away
person_y = [2, 2, 2, 2, 2]  # 2 meters to the right  
person_z = [1.7, 1.6, 1.5, 1.4, 1.3]  # height around 1.7m
print(f"Person points: x={person_x}, y={person_y}, z={person_z}")

print("\nCreating fake car at position (15, -3, 1.0 meters)...")
car_x = [15, 15, 16, 16, 17]  # 15-17 meters away
car_y = [-3, -3, -3, -3, -3]  # 3 meters to the left
car_z = [1.0, 1.0, 1.0, 1.0, 1.0]  # 1 meter high
print(f"Car points: x={car_x}, y={car_y}, z={car_z}")

print("\n🤖 Step 2: AI Detection...")
print("The AI analyzes the points and recognizes objects:")

# Analyze person
person_distance = np.sqrt(5**2 + 2**2)  # Calculate distance
print(f"✓ Found PERSON at distance: {person_distance:.1f} meters")

# Analyze car  
car_distance = np.sqrt(15**2 + 3**2)  # Calculate distance
print(f"✓ Found CAR at distance: {car_distance:.1f} meters")

print("\n🛡️ Step 3: Threat Analysis...")

# Check person threat
if person_distance < 10:
    person_threat = "HIGH"
    print(f"🚨 PERSON threat level: {person_threat} (too close!)")
else:
    person_threat = "LOW"
    print(f"✅ PERSON threat level: {person_threat} (safe distance)")

# Check car threat
if car_distance < 20:
    car_threat = "MEDIUM" 
    print(f"⚠️ CAR threat level: {car_threat} (monitoring)")
else:
    car_threat = "LOW"
    print(f"✅ CAR threat level: {car_threat} (safe distance)")

print("\n📊 Step 4: Visual Display...")

# Create simple plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Top-down view (bird's eye)
ax1.scatter(person_x, person_y, c='red', s=100, label='Person (HIGH threat)', marker='o')
ax1.scatter(car_x, car_y, c='blue', s=100, label='Car (MEDIUM threat)', marker='s')
ax1.scatter(0, 0, c='green', s=200, label='LIDAR Sensor', marker='*')

# Draw security zones
circle1 = plt.Circle((0, 0), 10, fill=False, color='red', linestyle='--', label='Danger Zone')
circle2 = plt.Circle((0, 0), 20, fill=False, color='orange', linestyle='--', label='Warning Zone')
ax1.add_patch(circle1)
ax1.add_patch(circle2)

ax1.set_xlim(-5, 25)
ax1.set_ylim(-10, 10)
ax1.set_xlabel('Distance Forward (meters)')
ax1.set_ylabel('Distance Sideways (meters)')
ax1.set_title('🛡️ Security Monitoring - Top View')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Side view showing heights
ax2.scatter(person_x, person_z, c='red', s=100, label='Person', marker='o')
ax2.scatter(car_x, car_z, c='blue', s=100, label='Car', marker='s')
ax2.scatter(0, 0, c='green', s=200, label='LIDAR Sensor', marker='*')

ax2.set_xlim(-2, 25)
ax2.set_ylim(0, 3)
ax2.set_xlabel('Distance Forward (meters)')
ax2.set_ylabel('Height (meters)')
ax2.set_title('📏 Height Detection - Side View')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('simple_security_test.png', dpi=150, bbox_inches='tight')
print("💾 Saved image: simple_security_test.png")
plt.show()

print("\n🎯 SUMMARY:")
print("=" * 40)
print("✓ LIDAR sensor detected 2 objects")
print("✓ Person identified at 5.4 meters (HIGH threat)")
print("✓ Car identified at 15.3 meters (MEDIUM threat)")
print("✓ System working correctly!")
print("\n🔍 What this means:")
print("- The person is too close (under 10m = danger zone)")
print("- The car is in warning zone (10-20m = monitor)")
print("- Security guards would be alerted about the person")
print("- The system shows exactly where threats are located")

print("\n📸 Check the image 'simple_security_test.png' to see the visual display!")
