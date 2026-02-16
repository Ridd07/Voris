import cv2

def test_cameras():
    print("Checking for available cameras...")
    for i in range(5):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            print(f"Camera found at index {i}")
            ret, frame = cap.read()
            if ret:
                print(f"  - Successfully captured a frame at index {i}")
            else:
                print(f"  - index {i} opened but failed to capture frame")
            cap.release()
        else:
            print(f"No camera found at index {i}")

if __name__ == "__main__":
    test_cameras()
    print("\nIf no cameras were found/captured, please check:")
    print("1. Is your webcam plugged in?")
    print("2. Is another app (Zoom, Teams, Browser) using the camera?")
    print("3. Check Privacy Settings -> Camera -> Allow desktop apps to access your camera.")
