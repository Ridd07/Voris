import cv2
import time

def test_camera():
    # Priority: DSHOW (common on Windows), MSMF (modern Windows), Default
    backends = [
        ("DSHOW", cv2.CAP_DSHOW), 
        ("MSMF", cv2.CAP_MSMF), 
        ("Default", None)
    ]
    indices = [0, 1]
    
    results = []
    
    for backend_name, backend in backends:
        for index in indices:
            print(f"Testing index {index} with backend {backend_name}...")
            
            cap = None
            try:
                if backend is not None:
                    cap = cv2.VideoCapture(index, backend)
                else:
                    cap = cv2.VideoCapture(index)
                
                # Small wait for hardware to respond
                time.sleep(0.5)
                
                if cap is not None and cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        print(f"!!! SUCCESS !!! Working configuration: index={index}, backend={backend_name}")
                        results.append((index, backend_name))
                    else:
                        print(f"Opened index {index} with {backend_name} but could not read frame.")
                    cap.release()
                else:
                    print(f"Failed to open index {index} with {backend_name}")
            except Exception as e:
                print(f"Error with {backend_name}/index {index}: {e}")
            finally:
                if cap:
                    cap.release()

    if results:
        print("\nAll working configurations found:")
        for res in results:
            print(f" - Index {res[0]} with {res[1]}")
    else:
        print("\nNo working camera configuration found.")

if __name__ == "__main__":
    test_camera()
