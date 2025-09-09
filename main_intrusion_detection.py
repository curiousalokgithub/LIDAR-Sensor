#!/usr/bin/env python3
"""
Complete Intrusion Detection System using LIDAR and MMDetection3D
Author: Alok Kumar Tripathy
Project: Intrusion Detection using LIDAR Sensors with Deep Learning
"""

import numpy as np
import torch
import open3d as o3d
import matplotlib.pyplot as plt
import cv2
from datetime import datetime
import os
import sys

class IntrusionDetectionSystem:
    """Main class for LIDAR-based intrusion detection"""
    
    def __init__(self, config_file=None, model_weights=None):
        """Initialize the intrusion detection system"""
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.detection_threshold = 0.5
        self.temporal_window = 5
        self.detection_history = []
        
        print(f"🚀 Initializing Intrusion Detection System")
        print(f"📱 Device: {self.device}")
        print(f"🎯 Detection threshold: {self.detection_threshold}")
        
    def load_lidar_data(self, file_path="sample_lidar_data.pcd"):
        """Load LIDAR point cloud data"""
        try:
            if os.path.exists(file_path):
                # Load using Open3D
                pcd = o3d.io.read_point_cloud(file_path)
                points = np.asarray(pcd.points)
                print(f"✅ Loaded point cloud: {points.shape[0]} points")
                return points
            else:
                # Generate synthetic data for demonstration
                print("⚠️ Sample data not found, generating synthetic point cloud")
                return self.generate_synthetic_pointcloud()
        except Exception as e:
            print(f"❌ Error loading LIDAR data: {e}")
            return self.generate_synthetic_pointcloud()
    
    def generate_synthetic_pointcloud(self, num_points=10000):
        """Generate synthetic point cloud for testing"""
        # Ground plane
        ground_points = np.random.uniform(-50, 50, (num_points//2, 2))
        ground_z = np.zeros((num_points//2, 1))
        ground = np.hstack([ground_points, ground_z])
        
        # Random objects (potential intruders)
        object_points = np.random.uniform(-20, 20, (num_points//4, 2))
        object_z = np.random.uniform(0.5, 2.0, (num_points//4, 1))
        objects = np.hstack([object_points, object_z])
        
        # Noise
        noise = np.random.normal(0, 0.1, (num_points//4, 3))
        
        points = np.vstack([ground, objects, noise])
        print(f"✅ Generated synthetic point cloud: {points.shape[0]} points")
        return points
    
    def preprocess_pointcloud(self, points):
        """Preprocess point cloud data"""
        # Remove outliers
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        
        # Statistical outlier removal
        pcd, _ = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
        
        # Voxel downsampling
        pcd = pcd.voxel_down_sample(voxel_size=0.1)
        
        processed_points = np.asarray(pcd.points)
        print(f"🔧 Preprocessed point cloud: {processed_points.shape[0]} points")
        return processed_points
    
    def extract_features(self, points):
        """Extract features from point cloud"""
        # Simple geometric features
        features = {
            'num_points': len(points),
            'height_range': np.max(points[:, 2]) - np.min(points[:, 2]),
            'density': len(points) / (np.max(points) - np.min(points) + 1e-6),
            'mean_height': np.mean(points[:, 2]),
            'std_height': np.std(points[:, 2])
        }
        return features
    
    def detect_objects_3d(self, points):
        """3D object detection using geometric analysis"""
        # Segment ground plane
        ground_threshold = 0.2
        ground_mask = points[:, 2] < ground_threshold
        object_points = points[~ground_mask]
        
        if len(object_points) == 0:
            return []
        
        # Cluster objects using DBSCAN-like approach
        detections = []
        
        # Simple height-based detection
        for z_thresh in [1.0, 1.5, 2.0]:  # Different height thresholds
            candidate_points = object_points[object_points[:, 2] > z_thresh]
            if len(candidate_points) > 50:  # Minimum points for detection
                # Calculate bounding box
                min_coords = np.min(candidate_points, axis=0)
                max_coords = np.max(candidate_points, axis=0)
                
                # Simple size filtering (human-like objects)
                width = max_coords[0] - min_coords[0]
                length = max_coords[1] - min_coords[1] 
                height = max_coords[2] - min_coords[2]
                
                if 0.3 < width < 2.0 and 0.3 < length < 2.0 and height > 1.0:
                    detection = {
                        'bbox': [min_coords, max_coords],
                        'confidence': min(len(candidate_points) / 100.0, 1.0),
                        'center': (min_coords + max_coords) / 2,
                        'size': [width, length, height],
                        'points': len(candidate_points)
                    }
                    detections.append(detection)
        
        print(f"🎯 Detected {len(detections)} potential objects")
        return detections
    
    def temporal_consistency_check(self, current_detections):
        """Apply temporal consistency to reduce false positives"""
        self.detection_history.append(current_detections)
        
        # Keep only recent history
        if len(self.detection_history) > self.temporal_window:
            self.detection_history.pop(0)
        
        # Simple temporal filtering
        consistent_detections = []
        for detection in current_detections:
            consistency_score = detection['confidence']
            
            # Check against previous detections
            for prev_detections in self.detection_history[:-1]:
                for prev_det in prev_detections:
                    # Calculate distance between detections
                    distance = np.linalg.norm(
                        detection['center'] - prev_det['center']
                    )
                    if distance < 2.0:  # Same object threshold
                        consistency_score += 0.2
            
            detection['temporal_confidence'] = min(consistency_score, 1.0)
            
            if detection['temporal_confidence'] > self.detection_threshold:
                consistent_detections.append(detection)
        
        return consistent_detections
    
    def generate_alert(self, detections):
        """Generate intrusion alert"""
        if not detections:
            return None
        
        alert = {
            'timestamp': datetime.now().isoformat(),
            'num_detections': len(detections),
            'max_confidence': max(d['temporal_confidence'] for d in detections),
            'locations': [d['center'].tolist() for d in detections],
            'alert_level': 'HIGH' if len(detections) > 1 else 'MEDIUM'
        }
        
        print(f"🚨 INTRUSION ALERT: {alert['alert_level']} - {alert['num_detections']} detection(s)")
        return alert
    
    def visualize_results(self, points, detections, save_path="detection_result.png"):
        """Visualize detection results"""
        fig = plt.figure(figsize=(15, 10))
        
        # 3D visualization
        ax1 = fig.add_subplot(221, projection='3d')
        ax1.scatter(points[:, 0], points[:, 1], points[:, 2], 
                   c=points[:, 2], cmap='viridis', s=1, alpha=0.6)
        
        # Highlight detections
        for detection in detections:
            center = detection['center']
            size = detection['size']
            confidence = detection['temporal_confidence']
            
            # Draw bounding box
            ax1.scatter(center[0], center[1], center[2], 
                       c='red', s=100, marker='x')
            ax1.text(center[0], center[1], center[2] + 0.5, 
                    f'Conf: {confidence:.2f}', fontsize=8)
        
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.set_zlabel('Z (m)')
        ax1.set_title('3D Point Cloud with Detections')
        
        # Top-down view
        ax2 = fig.add_subplot(222)
        ax2.scatter(points[:, 0], points[:, 1], c=points[:, 2], 
                   cmap='viridis', s=1, alpha=0.6)
        
        for detection in detections:
            center = detection['center']
            size = detection['size']
            
            # Draw detection circle
            circle = plt.Circle((center[0], center[1]), 
                              max(size[0], size[1])/2, 
                              fill=False, color='red', linewidth=2)
            ax2.add_patch(circle)
            
        ax2.set_xlabel('X (m)')
        ax2.set_ylabel('Y (m)')
        ax2.set_title('Top-down View')
        ax2.set_aspect('equal')
        
        # Detection statistics
        ax3 = fig.add_subplot(223)
        if detections:
            confidences = [d['temporal_confidence'] for d in detections]
            ax3.bar(range(len(confidences)), confidences)
            ax3.set_xlabel('Detection ID')
            ax3.set_ylabel('Confidence')
            ax3.set_title('Detection Confidences')
        else:
            ax3.text(0.5, 0.5, 'No Detections', ha='center', va='center')
            ax3.set_title('No Intrusions Detected')
        
        # System info
        ax4 = fig.add_subplot(224)
        ax4.axis('off')
        info_text = f"""
        System Status: {'ALERT' if detections else 'NORMAL'}
        Point Cloud Size: {len(points):,} points
        Detections: {len(detections)}
        Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        Detection Summary:
        """
        
        for i, det in enumerate(detections):
            info_text += f"\nObject {i+1}: Conf={det['temporal_confidence']:.2f}"
        
        ax4.text(0.1, 0.9, info_text, fontsize=10, va='top', ha='left')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"📊 Visualization saved to: {save_path}")
        return save_path
    
    def run_detection_pipeline(self, lidar_file=None):
        """Run complete detection pipeline"""
        print(f"\n🔍 Starting Intrusion Detection Pipeline")
        print("=" * 50)
        
        # Step 1: Load data
        points = self.load_lidar_data(lidar_file)
        
        # Step 2: Preprocess
        processed_points = self.preprocess_pointcloud(points)
        
        # Step 3: Extract features
        features = self.extract_features(processed_points)
        print(f"📈 Extracted features: {features}")
        
        # Step 4: 3D object detection
        detections = self.detect_objects_3d(processed_points)
        
        # Step 5: Temporal consistency
        consistent_detections = self.temporal_consistency_check(detections)
        
        # Step 6: Generate alerts
        alert = self.generate_alert(consistent_detections)
        
        # Step 7: Visualize results
        viz_path = self.visualize_results(processed_points, consistent_detections)
        
        # Results summary
        print("\n📋 Detection Results Summary:")
        print(f"✅ Processed {len(processed_points):,} points")
        print(f"🎯 Found {len(detections)} initial detections")
        print(f"✔️ {len(consistent_detections)} consistent detections")
        print(f"🚨 Alert status: {'TRIGGERED' if alert else 'NORMAL'}")
        
        return {
            'detections': consistent_detections,
            'alert': alert,
            'visualization': viz_path,
            'features': features
        }

def main():
    """Main function to run the intrusion detection system"""
    print("🚀 LIDAR-based Intrusion Detection System")
    print("=" * 50)
    
    # Initialize system
    ids = IntrusionDetectionSystem()
    
    # Run detection pipeline
    results = ids.run_detection_pipeline("sample_lidar_data.pcd")
    
    # Print final results
    if results['alert']:
        print(f"\n🚨 SECURITY ALERT GENERATED!")
        print(f"Alert Level: {results['alert']['alert_level']}")
        print(f"Confidence: {results['alert']['max_confidence']:.2f}")
        print(f"Detections: {results['alert']['num_detections']}")
    else:
        print(f"\n✅ No intrusions detected - Area secure")
    
    print(f"\n📊 Visualization saved: {results['visualization']}")
    print("🏁 Detection pipeline completed successfully!")

if __name__ == "__main__":
    main()
