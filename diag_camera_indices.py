import cv2

def test_camera():
    backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, None]
    indices = [0, 1, 2]
    
    for backend in backends:
        for index in indices:
            backend_name = "Default" if backend is None else ("DSHOW" if backend == cv2.CAP_DSHOW else "MSMF")
            print(f"Testing index {index} with backend {backend_name}...")
            
            try:
                if backend is not None:
                    cap = cv2.VideoCapture(index, backend)
                else:
                    cap = cv2.VideoCapture(index)
                
                if cap.isOpened():
                    print(f"SUCCESS: Camera found at index {index} with backend {backend_name}")
                    ret, frame = cap.read()
                    if ret:
                        print(f"SUCCESS: Successfully read a frame from index {index}")
                    else:
                        print(f"WARNING: Camera opened at index {index} but failed to read frame.")
                    cap.release()
                    return index, backend
                else:
                    print(f"FAILED: Could not open index {index} with backend {backend_name}")
            except Exception as e:
                print(f"ERROR: Exception testing index {index} with backend {backend_name}: {e}")

if __name__ == "__main__":
    test_camera()
