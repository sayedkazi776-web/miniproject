"""
Quick test script for CCTV/RTSP cameras
Run: python test_cctv.py
"""
import cv2
import sys

print("=" * 70)
print("🎥 CCTV/RTSP Camera Test Tool")
print("=" * 70)
print()

# Get RTSP URL from user
rtsp_url = input("Enter your RTSP URL (or '0' for webcam): ").strip()

if not rtsp_url:
    print("❌ No URL entered. Exiting.")
    sys.exit(1)

print()
print(f"Testing: {rtsp_url}")
print("Press 'q' to quit the video window")
print("-" * 70)

# Open video capture
print("\n[1/3] Opening video source...")
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("❌ ERROR: Could not open video source!")
    print()
    print("Common issues and fixes:")
    print("-" * 70)
    
    if rtsp_url.isdigit():
        print("For webcam:")
        print("  • Check camera permissions in Windows Settings")
        print("  • Try different index: 0, 1, 2, etc.")
        print("  • Make sure no other app is using the camera")
    else:
        print("For RTSP/IP camera:")
        print("  • Verify camera IP address is correct")
        print("  • Check username and password")
        print("  • Test RTSP URL in VLC Media Player first")
        print("  • Try different stream path (stream1, stream2, etc.)")
        print("  • Check RTSP port (usually 554)")
        print("  • Verify network connectivity: ping camera IP")
        print("  • Check firewall settings")
        print("  • Ensure camera is powered on")
    
    print()
    print("Example RTSP URLs:")
    print("  • Hikvision: rtsp://admin:password@192.168.1.64:554/Streaming/Channels/101")
    print("  • Dahua: rtsp://admin:password@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0")
    print("  • Generic: rtsp://username:password@192.168.1.100:554/stream1")
    sys.exit(1)

print("✅ Video source opened successfully!")

# Get camera properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

print(f"\n[2/3] Camera properties:")
print(f"  • Resolution: {width}x{height}")
print(f"  • FPS: {fps:.2f}")

# Read and display frames
print(f"\n[3/3] Reading frames...")
print("🎬 Video window should appear. Press 'q' to quit.")

frame_count = 0
failed_reads = 0
max_failed_reads = 30

try:
    while True:
        ret, frame = cap.read()
        
        if not ret:
            failed_reads += 1
            if failed_reads >= max_failed_reads:
                print(f"\n❌ Failed to read {max_failed_reads} consecutive frames")
                print("Camera may have disconnected or stopped responding.")
                break
            continue
        
        failed_reads = 0  # Reset counter on successful read
        
        # Draw info overlay on frame
        info_text = f"Frame: {frame_count} | Res: {width}x{height}"
        cv2.putText(frame, info_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Display frame
        cv2.imshow('CCTV Test - Press Q to Quit', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\n✅ Test completed successfully!")
            break
        
        frame_count += 1
        
        # Print progress every 50 frames
        if frame_count % 50 == 0:
            print(f"  ✓ Received {frame_count} frames...")
    
    print("-" * 70)
    if frame_count > 0:
        print("✅ SUCCESS: Video stream is working!")
        print(f"   Total frames received: {frame_count}")
        print(f"   Camera is compatible with this system!")
    else:
        print("⚠️  No frames received")

except KeyboardInterrupt:
    print("\n\n⚠️  Test interrupted by user")
except Exception as e:
    print(f"\n❌ Error during test: {e}")
finally:
    cap.release()
    cv2.destroyAllWindows()

print("-" * 70)
print("Test complete!")
print()
print("Next steps:")
print("  1. If test worked → Add this camera to your system")
print("  2. Use the RTSP URL in the 'Add Camera' form")
print("  3. See CCTV_CAMERA_SETUP.md for detailed instructions")
print("=" * 70)


