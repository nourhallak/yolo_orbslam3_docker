import pyrealsense2 as rs
import numpy as np
import cv2
import os
import time
from datetime import datetime

# Generate timestamp for folder naming
current_time = datetime.now().strftime('%Y%m%d_%H%M%S')

color_folder = f"color_images"
depth_folder = f"depth_images"

# Set up directories
if not os.path.exists(color_folder):
    os.makedirs(color_folder)

if not os.path.exists(depth_folder):
    os.makedirs(depth_folder)

txt_file_path = f"frame_metadata.txt"
txt_file = open(txt_file_path, "w")

# Create an align object
align_to = rs.stream.color
align = rs.align(align_to)

# Configure streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    frame_count = 1
    depth_files = []
    image_files = []
    timestamps = []
    while frame_count <= 2000:
        print(frame_count)
        # Wait for frames
        frames = pipeline.wait_for_frames()

        # Align the depth frame to color frame
        aligned_frames = align.process(frames)
        
        color_frame = aligned_frames.get_color_frame()
        aligned_depth_frame = aligned_frames.get_depth_frame()

        if not color_frame or not aligned_depth_frame:
            continue

        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        
        # Save color frame
        #image_files.append(color_image)
        cv2.imwrite(f"{color_folder}/{frame_count:06d}.png", color_image)
        
        # Save depth frame
        #depth_files.append(depth_image.astype(np.uint16))
        cv2.imwrite(f"{depth_folder}/{frame_count:06d}.png", depth_image.astype(np.uint16))

        # Save timestamp and exposure metadata
        #timestamp of the frame in milliseconds since the device started streaming:
        #timestamp = color_frame.get_timestamp()
        # UNIX timestamp in seconds:
        #timestamp = time.time()
        timestamp = aligned_depth_frame.get_timestamp()
        timestamps.append(timestamp)
        # print(timestamp)
        profile = pipeline.get_active_profile()
        color_stream = profile.get_stream(rs.stream.color)
        intrinsics = color_stream.as_video_stream_profile().get_intrinsics()

        #print("Color Camera Intrinsics:")
        #print(f"Width: {intrinsics.width}")
        #print(f"Height: {intrinsics.height}")
        #print(f"Principal Point: ({intrinsics.ppx}, {intrinsics.ppy})")
        #print(f"Focal Length: ({intrinsics.fx}, {intrinsics.fy})")
        #print(f"Distortion Coefficients: {intrinsics.coeffs}")
        # exposure returned in microsencods hence /1000 to record milliseconds
        #exposure = aligned_depth_frame.get_frame_metadata(rs.frame_metadata_value.actual_exposure)

        exposure = 0
        txt_file.write(f"{frame_count:06d} {timestamp} {exposure/1000}\n")
        
        frame_count += 1

        # Optional: Display the images ; Comment out for speed optimization
        cv2.imshow('Color', color_image)
        # cv2.imshow('Depth', depth_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #frame_count = 1
    #for i in range(len(image_files)):
     #   cv2.imwrite(f"{color_folder}/{frame_count:06d}.jpg", image_files[i])
      #  cv2.imwrite(f"{depth_folder}/{frame_count:06d}.png", depth_files[i])
       # txt_file.write(f"{frame_count:06d} {timestamp} {exposure/1000}\n")
        #frame_count += 1
finally:
    pipeline.stop()
    txt_file.close()
    cv2.destroyAllWindows()

