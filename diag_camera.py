import cv2

def test_camera(index, backend_name, backend_val):
    print(f"Testing index {index} with {backend_name}...")
    try:
        if backend_val is not None:
            cap = cv2.VideoCapture(index, backend_val)
        else:
            cap = cv2.VideoCapture(index)
            
        if not cap.isOpened():
            print(f"  Failed to open index {index} with {backend_name}")
            return False
            
        ret, frame = cap.read()
        if ret:
            print(f"  SUCCESS! Captured frame at index {index} with {backend_name}")
            cap.release()
            return True
        else:
            print(f"  Failed to read frame at index {index} with {backend_name}")
        cap.release()
    except Exception as e:
        print(f"  Error: {e}")
    return False

backends = [
    ("Default", None),
    ("DSHOW", cv2.CAP_DSHOW),
    ("MSMF", cv2.CAP_MSMF)
]

found = False
for i in range(3):
    for b_name, b_val in backends:
        if test_camera(i, b_name, b_val):
            found = True
            break
    if found:
        break

if not found:
    print("\nNo working camera configuration found. Please check if your camera is connected and not in use by another program.")
