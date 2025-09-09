#!/usr/bin/env python3
"""
Simple Intrusion Detection System Demo
Author: Alok Kumar Tripathy
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

class SimpleIntrusionDetection:
    """Simple LIDAR-based intrusion detection"""
    
    def __init__(self):
        self.detection_threshold = 0.5
        print("Initializing Intrusion Detection System")
        
    def generate_sample_data(self):
        """Generate sample point cloud data"""
        # Ground plane
        ground = np.random.uniform(-20, 20, (5000, 2))
        ground_z = np.zeros((5000, 1))
        ground_points = np.hstack([ground, ground_z])
        
        # Object (potential intruder)
        object_x = np.random.normal(5, 0.5, 100)
        object_y = np.random.normal(5, 0.5, 100)  
        object_z = np.random.uniform(0.5, 2.0, 100)
        object_points = np.column_stack([object_x, object_y, object_z])
        
        return np.vstack([ground_points, object_points])
    
    def detect_intrusions(self, points):
        """Simple intrusion detection"""
        # Filter points above ground
        elevated_points = points[points[:, 2] > 0.3]
        
        if len(elevated_points) > 50:
            # Calculate bounding box
            min_coords = np.min(elevated_points, axis=0)
            max_coords = np.max(elevated_points, axis=0)
            
            width = max_coords[0] - min_coords[0]
            height = max_coords[2] - min_coords[2]
            
            # Check if it looks like a person
            if 0.5 < width < 2.0 and height > 1.0:
                return {
                    'detected': True,
                    'confidence': 0.85,
                    'location': (min_coords + max_coords) / 2,
                    'size': [width, height]
                }
        
        return {'detected': False}
    
    def visualize(self, points, detection, save_path="detection_result.png"):
        """Create visualization"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # 3D scatter plot
        ax1.scatter(points[:, 0], points[:, 1], c=points[:, 2], s=1)
        
        if detection['detected']:
            loc = detection['location']
            ax1.scatter(loc[0], loc[1], c='red', s=100, marker='X')
            ax1.set_title(f"INTRUSION DETECTED - Confidence: {detection['confidence']:.2f}")
        else:
            ax1.set_title("NO INTRUSION DETECTED")
            
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        
        # Height profile
        ax2.hist(points[:, 2], bins=50, alpha=0.7)
        ax2.axvline(x=0.3, color='red', linestyle='--', label='Ground threshold')
        ax2.set_xlabel('Height (m)')
        ax2.set_ylabel('Point count')
        ax2.set_title('Height Distribution')
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig(save_path)
        print(f"Visualization saved: {save_path}")
        return save_path
    
    def run_detection(self):
        """Run complete detection pipeline"""
        print("Starting detection pipeline...")
        
        # Generate sample data
        points = self.generate_sample_data()
        print(f"Generated {len(points)} points")
        
        # Run detection
        result = self.detect_intrusions(points)
        
        # Create visualization
        viz_path = self.visualize(points, result)
        
        # Print results
        if result['detected']:
            print("SECURITY ALERT: Intrusion detected!")
            print(f"Confidence: {result['confidence']:.2f}")
            print(f"Location: {result['location']}")
        else:
            print("Area secure - no intrusions detected")
            
        return result

def main():
    """Main function"""
    print("="*50)
    print("LIDAR Intrusion Detection System")
    print("="*50)
    
    # Create and run detection system
    detector = SimpleIntrusionDetection()
    result = detector.run_detection()
    
    print("="*50)
    print("Detection completed!")
    print("="*50)

if __name__ == "__main__":
    main()
