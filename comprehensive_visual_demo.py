#!/usr/bin/env python3
"""
COMPREHENSIVE INTRUSION DETECTION DEMO
Visual Threat Detection with Real-Time Display

This script creates a complete visual demonstration of:
- LIDAR point cloud data processing
- Object detection (Cars, Buses, People)
- Threat level analysis with visual feedback
- Real-time security monitoring simulation
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import time
import random
import os
from datetime import datetime
import torch

# Configure matplotlib for better visuals
plt.style.use('dark_background')

class IntrusionDetectionSystem:
    def __init__(self):
        self.threat_levels = {
            'LOW': {'color': 'green', 'priority': 1},
            'MEDIUM': {'color': 'orange', 'priority': 2}, 
            'HIGH': {'color': 'red', 'priority': 3},
            'CRITICAL': {'color': 'crimson', 'priority': 4}
        }
        
        self.detection_history = []
        self.security_zones = {
            'SECURE': (0, 15),      # 0-15 meters
            'WARNING': (15, 30),    # 15-30 meters  
            'MONITOR': (30, 50)     # 30-50 meters
        }
        
    def generate_realistic_scene(self, scenario='normal'):
        """Generate realistic LIDAR scene with various objects"""
        print(f"\n🎬 Generating {scenario.upper()} security scenario...")
        
        objects = []
        
        if scenario == 'normal':
            # Normal scenario - just environment
            objects.append(self._create_building_points())
            objects.append(self._create_ground_points())
            
        elif scenario == 'person_intrusion':
            # Person detected in secure zone
            objects.append(self._create_person_points(position=[8, 2, 1.7], walking=True))
            objects.append(self._create_building_points())
            objects.append(self._create_ground_points())
            
        elif scenario == 'vehicle_approach':
            # Vehicle approaching perimeter
            objects.append(self._create_vehicle_points(position=[25, -5, 1.0], vehicle_type='car'))
            objects.append(self._create_building_points())
            objects.append(self._create_ground_points())
            
        elif scenario == 'multiple_threats':
            # Multiple objects - high threat
            objects.append(self._create_person_points(position=[5, 1, 1.7], walking=True))
            objects.append(self._create_vehicle_points(position=[12, -3, 1.0], vehicle_type='bus'))
            objects.append(self._create_vehicle_points(position=[35, 8, 1.0], vehicle_type='car'))
            objects.append(self._create_building_points())
            objects.append(self._create_ground_points())
            
        # Combine all objects
        all_points = np.vstack(objects)
        
        # Add realistic noise
        noise = np.random.normal(0, 0.05, all_points.shape)
        all_points[:, :3] += noise[:, :3]
        
        return all_points
    
    def _create_person_points(self, position=[5, 0, 1.7], walking=False):
        """Create realistic human figure point cloud"""
        x, y, z = position
        
        # Body parts
        # Head
        head = np.random.normal([x, y, z + 0.3], [0.1, 0.1, 0.1], (20, 3))
        
        # Torso
        torso = np.random.normal([x, y, z - 0.2], [0.15, 0.1, 0.4], (40, 3))
        
        # Arms
        arm1 = np.random.normal([x - 0.3, y, z - 0.1], [0.1, 0.05, 0.3], (15, 3))
        arm2 = np.random.normal([x + 0.3, y, z - 0.1], [0.1, 0.05, 0.3], (15, 3))
        
        # Legs
        leg1 = np.random.normal([x - 0.1, y, z - 0.8], [0.05, 0.05, 0.4], (20, 3))
        leg2 = np.random.normal([x + 0.1, y, z - 0.8], [0.05, 0.05, 0.4], (20, 3))
        
        person_points = np.vstack([head, torso, arm1, arm2, leg1, leg2])
        
        # Add intensity (person has medium reflectivity)
        intensities = np.random.uniform(0.3, 0.7, len(person_points))
        person_cloud = np.column_stack([person_points, intensities])
        
        return person_cloud
    
    def _create_vehicle_points(self, position=[15, 0, 1.0], vehicle_type='car'):
        """Create realistic vehicle point cloud"""
        x, y, z = position
        
        if vehicle_type == 'car':
            # Car dimensions
            length, width, height = 4.5, 1.8, 1.5
            density = 150
        elif vehicle_type == 'bus':
            # Bus dimensions  
            length, width, height = 12.0, 2.5, 3.0
            density = 300
        else:
            # Default vehicle
            length, width, height = 5.0, 2.0, 1.8
            density = 200
            
        # Generate vehicle body points
        vehicle_x = np.random.uniform(x - length/2, x + length/2, density)
        vehicle_y = np.random.uniform(y - width/2, y + width/2, density)
        vehicle_z = np.random.uniform(z - height/2, z + height/2, density)
        
        vehicle_points = np.column_stack([vehicle_x, vehicle_y, vehicle_z])
        
        # Add intensity (vehicles have high reflectivity)
        intensities = np.random.uniform(0.6, 0.9, len(vehicle_points))
        vehicle_cloud = np.column_stack([vehicle_points, intensities])
        
        return vehicle_cloud
    
    def _create_building_points(self):
        """Create background building/wall points"""
        # Building wall at distance
        wall_x = np.random.uniform(45, 50, 200)
        wall_y = np.random.uniform(-20, 20, 200) 
        wall_z = np.random.uniform(0, 8, 200)
        
        building_points = np.column_stack([wall_x, wall_y, wall_z])
        intensities = np.random.uniform(0.8, 1.0, len(building_points))
        
        return np.column_stack([building_points, intensities])
    
    def _create_ground_points(self):
        """Create ground/pavement points"""
        # Ground points
        ground_x = np.random.uniform(0, 50, 400)
        ground_y = np.random.uniform(-15, 15, 400)
        ground_z = np.random.normal(0, 0.1, 400)
        
        ground_points = np.column_stack([ground_x, ground_y, ground_z])
        intensities = np.random.uniform(0.1, 0.4, len(ground_points))
        
        return np.column_stack([ground_points, intensities])
    
    def detect_objects(self, point_cloud):
        """Simulate AI object detection on point cloud"""
        print("🤖 Running AI Object Detection...")
        
        detections = []
        
        # Simulate processing time
        time.sleep(0.5)
        
        # Group points by spatial clustering (simplified)
        # In real system, this would use deep learning models
        
        # Find clusters of points (objects)
        clusters = self._find_point_clusters(point_cloud)
        
        for cluster in clusters:
            detection = self._classify_cluster(cluster)
            if detection:
                detections.append(detection)
                
        return detections
    
    def _find_point_clusters(self, points):
        """Find clusters of points that likely represent objects"""
        clusters = []
        
        # Simplified clustering - group nearby points
        for center_x in range(5, 45, 5):
            for center_y in range(-10, 11, 5):
                # Find points near this center
                distances = np.sqrt((points[:, 0] - center_x)**2 + (points[:, 1] - center_y)**2)
                nearby_points = points[distances < 3.0]
                
                if len(nearby_points) > 50:  # Minimum points for an object
                    clusters.append(nearby_points)
                    
        return clusters
    
    def _classify_cluster(self, cluster_points):
        """Classify a cluster of points as person/vehicle/other"""
        if len(cluster_points) < 50:
            return None
            
        # Calculate cluster properties
        x_range = np.max(cluster_points[:, 0]) - np.min(cluster_points[:, 0])
        y_range = np.max(cluster_points[:, 1]) - np.min(cluster_points[:, 1]) 
        z_range = np.max(cluster_points[:, 2]) - np.min(cluster_points[:, 2])
        
        center_x = np.mean(cluster_points[:, 0])
        center_y = np.mean(cluster_points[:, 1])
        center_z = np.mean(cluster_points[:, 2])
        
        distance = np.sqrt(center_x**2 + center_y**2)
        
        # Classification logic (simplified)
        if z_range > 1.5 and x_range < 1.0 and y_range < 1.0:
            # Tall, narrow object - likely person
            obj_class = "Person"
            confidence = 0.85 + random.uniform(-0.1, 0.1)
        elif x_range > 3.0 and y_range > 1.5:
            # Long, wide object - likely vehicle
            if x_range > 8.0:
                obj_class = "Bus"
            else:
                obj_class = "Car"
            confidence = 0.90 + random.uniform(-0.05, 0.05)
        else:
            # Unknown object
            obj_class = "Unknown"
            confidence = 0.60 + random.uniform(-0.2, 0.2)
            
        return {
            'class': obj_class,
            'confidence': max(0.3, min(0.99, confidence)),
            'position': [center_x, center_y, center_z],
            'size': [x_range, y_range, z_range],
            'distance': distance,
            'bbox_3d': [center_x, center_y, center_z, x_range, y_range, z_range]
        }
    
    def analyze_threat_level(self, detections):
        """Analyze detections and determine threat level"""
        print("🛡️ Analyzing Security Threats...")
        
        max_threat = 'LOW'
        threat_priority = 1
        alerts = []
        
        for detection in detections:
            obj_class = detection['class']
            distance = detection['distance']
            confidence = detection['confidence']
            
            # Threat assessment logic
            if obj_class == "Person":
                if distance < 15 and confidence > 0.7:
                    current_threat = 'CRITICAL'
                    alerts.append(f"🚨 CRITICAL: {obj_class} in SECURE ZONE at {distance:.1f}m")
                elif distance < 25 and confidence > 0.7:
                    current_threat = 'HIGH'
                    alerts.append(f"⚠️ HIGH: {obj_class} approaching at {distance:.1f}m")
                else:
                    current_threat = 'MEDIUM'
                    alerts.append(f"⚡ MEDIUM: {obj_class} detected at {distance:.1f}m")
                    
            elif obj_class in ["Car", "Bus"]:
                if distance < 20 and confidence > 0.8:
                    current_threat = 'HIGH'
                    alerts.append(f"🚗 HIGH: {obj_class} approaching at {distance:.1f}m")
                elif distance < 35 and confidence > 0.8:
                    current_threat = 'MEDIUM'  
                    alerts.append(f"🚙 MEDIUM: {obj_class} detected at {distance:.1f}m")
                else:
                    current_threat = 'LOW'
                    alerts.append(f"ℹ️ LOW: {obj_class} at safe distance {distance:.1f}m")
                    
            else:
                current_threat = 'MEDIUM'
                alerts.append(f"❓ MEDIUM: Unknown object at {distance:.1f}m")
            
            # Update max threat level
            current_priority = self.threat_levels[current_threat]['priority']
            if current_priority > threat_priority:
                max_threat = current_threat
                threat_priority = current_priority
        
        if not detections:
            max_threat = 'LOW'
            alerts.append("✅ LOW: Area secure - no threats detected")
            
        return max_threat, alerts
    
    def create_visual_display(self, point_cloud, detections, threat_level, alerts, scenario_name):
        """Create comprehensive visual display of detection results"""
        print("🎨 Creating Visual Security Display...")
        
        fig = plt.figure(figsize=(16, 12))
        fig.suptitle(f'🛡️ LIDAR Intrusion Detection System - {scenario_name.upper()}', 
                    fontsize=16, fontweight='bold', color='white')
        
        # Main 3D view
        ax1 = fig.add_subplot(221, projection='3d')
        self._plot_3d_scene(ax1, point_cloud, detections, threat_level)
        
        # Bird's eye view (top-down)
        ax2 = fig.add_subplot(222)
        self._plot_birds_eye_view(ax2, point_cloud, detections, threat_level)
        
        # Threat analysis panel
        ax3 = fig.add_subplot(223)
        self._plot_threat_analysis(ax3, detections, threat_level, alerts)
        
        # Detection details
        ax4 = fig.add_subplot(224)
        self._plot_detection_details(ax4, detections)
        
        plt.tight_layout()
        
        # Save the visualization
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"intrusion_detection_{scenario_name}_{timestamp}.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='black')
        print(f"💾 Saved visualization: {filename}")
        
        plt.show()
        
    def _plot_3d_scene(self, ax, point_cloud, detections, threat_level):
        """Plot 3D point cloud with detections"""
        # Plot point cloud
        scatter = ax.scatter(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2],
                           c=point_cloud[:, 3], cmap='viridis', s=0.5, alpha=0.6)
        
        # Plot detection bounding boxes
        for detection in detections:
            pos = detection['position']
            size = detection['size']
            
            # Color based on object class
            if detection['class'] == 'Person':
                color = 'red'
            elif detection['class'] in ['Car', 'Bus']:
                color = 'blue'
            else:
                color = 'yellow'
                
            # Draw 3D bounding box (simplified as points)
            ax.scatter([pos[0]], [pos[1]], [pos[2]], 
                     c=color, s=100, marker='o', edgecolor='white', linewidth=2)
            
            # Add label
            ax.text(pos[0], pos[1], pos[2] + 1, 
                   f"{detection['class']}\n{detection['confidence']:.2f}",
                   fontsize=8, color='white')
        
        ax.set_xlabel('X (meters)', color='white')
        ax.set_ylabel('Y (meters)', color='white') 
        ax.set_zlabel('Z (meters)', color='white')
        ax.set_title('3D Point Cloud View', color='white')
        ax.set_facecolor('black')
        
        # Set equal aspect ratio
        ax.set_xlim(0, 50)
        ax.set_ylim(-15, 15)
        ax.set_zlim(0, 10)
        
    def _plot_birds_eye_view(self, ax, point_cloud, detections, threat_level):
        """Plot bird's eye view with security zones"""
        # Plot points from above
        scatter = ax.scatter(point_cloud[:, 0], point_cloud[:, 1], 
                           c=point_cloud[:, 3], cmap='viridis', s=1, alpha=0.7)
        
        # Draw security zones
        zones_colors = ['red', 'orange', 'green']
        zones_labels = ['SECURE (0-15m)', 'WARNING (15-30m)', 'MONITOR (30-50m)']
        
        for i, (start, end) in enumerate([(0, 15), (15, 30), (30, 50)]):
            circle = plt.Circle((0, 0), end, fill=False, 
                              color=zones_colors[i], linewidth=2, linestyle='--')
            ax.add_patch(circle)
            ax.text(end-5, 2, zones_labels[i], color=zones_colors[i], fontweight='bold')
        
        # Plot detections
        for detection in detections:
            pos = detection['position']
            size = detection['size']
            
            if detection['class'] == 'Person':
                color = 'red'
                marker = 'o'
            elif detection['class'] in ['Car', 'Bus']:
                color = 'blue' 
                marker = 's'
            else:
                color = 'yellow'
                marker = '^'
                
            ax.scatter(pos[0], pos[1], c=color, s=200, marker=marker, 
                     edgecolor='white', linewidth=2, alpha=0.9)
            
            # Add detection info
            ax.annotate(f"{detection['class']}\n{detection['distance']:.1f}m", 
                       (pos[0], pos[1]), xytext=(5, 5), 
                       textcoords='offset points', color='white', fontsize=8)
        
        # LIDAR sensor position
        ax.scatter(0, 0, c='lime', s=100, marker='*', edgecolor='white', linewidth=2)
        ax.text(0, -2, 'LIDAR\nSENSOR', ha='center', color='lime', fontweight='bold')
        
        ax.set_xlabel('X Distance (meters)', color='white')
        ax.set_ylabel('Y Distance (meters)', color='white')
        ax.set_title(f"Bird's Eye View - Threat: {threat_level}", 
                    color=self.threat_levels[threat_level]['color'], fontweight='bold')
        ax.set_facecolor('black')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 50)
        ax.set_ylim(-15, 15)
        ax.set_aspect('equal')
        
    def _plot_threat_analysis(self, ax, detections, threat_level, alerts):
        """Plot threat analysis panel"""
        ax.clear()
        ax.set_facecolor('black')
        
        # Threat level indicator
        threat_color = self.threat_levels[threat_level]['color']
        ax.text(0.5, 0.9, f"THREAT LEVEL: {threat_level}", 
               ha='center', va='center', fontsize=16, fontweight='bold',
               color=threat_color, transform=ax.transAxes)
        
        # Status indicator
        if threat_level in ['HIGH', 'CRITICAL']:
            status = "🚨 SECURITY BREACH"
            status_color = 'red'
        elif threat_level == 'MEDIUM':
            status = "⚠️ MONITORING"
            status_color = 'orange'
        else:
            status = "✅ AREA SECURE"
            status_color = 'green'
            
        ax.text(0.5, 0.8, status, ha='center', va='center', 
               fontsize=12, fontweight='bold', color=status_color, transform=ax.transAxes)
        
        # Alert messages
        ax.text(0.05, 0.7, "ALERTS:", fontsize=12, fontweight='bold', 
               color='white', transform=ax.transAxes)
        
        for i, alert in enumerate(alerts[:5]):  # Show max 5 alerts
            ax.text(0.05, 0.6 - i*0.1, alert, fontsize=10, 
                   color='white', transform=ax.transAxes)
        
        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ax.text(0.05, 0.05, f"Last Update: {timestamp}", fontsize=9, 
               color='gray', transform=ax.transAxes)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Security Status', color='white', fontweight='bold')
        
    def _plot_detection_details(self, ax, detections):
        """Plot detection details table"""
        ax.clear()
        ax.set_facecolor('black')
        
        if not detections:
            ax.text(0.5, 0.5, "No Objects Detected", ha='center', va='center',
                   fontsize=14, color='green', transform=ax.transAxes)
        else:
            # Table headers
            headers = ['Object', 'Confidence', 'Distance', 'Threat']
            col_widths = [0.25, 0.25, 0.25, 0.25]
            
            # Header row
            y_pos = 0.9
            for i, header in enumerate(headers):
                x_pos = sum(col_widths[:i]) + col_widths[i]/2
                ax.text(x_pos, y_pos, header, ha='center', va='center',
                       fontsize=10, fontweight='bold', color='white', transform=ax.transAxes)
            
            # Detection rows
            for idx, detection in enumerate(detections[:6]):  # Show max 6 detections
                y_pos = 0.8 - idx * 0.12
                
                # Determine threat level for this detection
                if detection['distance'] < 15:
                    det_threat = 'HIGH'
                    threat_color = 'red'
                elif detection['distance'] < 30:
                    det_threat = 'MED'
                    threat_color = 'orange'
                else:
                    det_threat = 'LOW'
                    threat_color = 'green'
                
                row_data = [
                    detection['class'],
                    f"{detection['confidence']:.2f}",
                    f"{detection['distance']:.1f}m",
                    det_threat
                ]
                
                for i, data in enumerate(row_data):
                    x_pos = sum(col_widths[:i]) + col_widths[i]/2
                    color = threat_color if i == 3 else 'white'
                    ax.text(x_pos, y_pos, data, ha='center', va='center',
                           fontsize=9, color=color, transform=ax.transAxes)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Detection Details', color='white', fontweight='bold')

def run_comprehensive_demo():
    """Run the complete intrusion detection demonstration"""
    print("=" * 80)
    print("🛡️ COMPREHENSIVE INTRUSION DETECTION SYSTEM DEMO")
    print("=" * 80)
    
    # Initialize the system
    ids = IntrusionDetectionSystem()
    
    # Test scenarios
    scenarios = [
        ('normal', 'Normal Security Patrol'),
        ('person_intrusion', 'Person in Secure Zone'),
        ('vehicle_approach', 'Vehicle Approaching'),
        ('multiple_threats', 'Multiple Threat Scenario')
    ]
    
    for scenario_key, scenario_name in scenarios:
        print(f"\n{'='*60}")
        print(f"🎬 SCENARIO: {scenario_name}")
        print(f"{'='*60}")
        
        # Generate scene
        point_cloud = ids.generate_realistic_scene(scenario_key)
        print(f"📊 Generated point cloud: {len(point_cloud)} points")
        
        # Run detection
        detections = ids.detect_objects(point_cloud)
        print(f"🎯 Detected objects: {len(detections)}")
        
        # Analyze threats
        threat_level, alerts = ids.analyze_threat_level(detections)
        
        # Display results
        print(f"\n🛡️ THREAT LEVEL: {threat_level}")
        for alert in alerts:
            print(f"   {alert}")
        
        # Create visualization
        ids.create_visual_display(point_cloud, detections, threat_level, alerts, scenario_key)
        
        # Wait between scenarios
        print(f"\n⏳ Processing complete. Moving to next scenario...")
        time.sleep(2)
    
    print(f"\n{'='*80}")
    print("✅ DEMO COMPLETE - All scenarios tested successfully!")
    print(f"📁 Check current directory for saved visualization images")
    print(f"{'='*80}")

if __name__ == "__main__":
    run_comprehensive_demo()
