from sys import flags
import time
import cv2
import pyautogui as p


def AuthenticateFace():

    flag = ""
    # Local Binary Patterns Histograms
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    recognizer.read('engine/auth/trainer/trainer.yml')  # load trained model
    cascadePath = "engine/auth/haarcascade_frontalface_default.xml"
    # initializing haar cascade for object detection approach
    faceCascade = cv2.CascadeClassifier(cascadePath)

    font = cv2.FONT_HERSHEY_SIMPLEX  # denotes the font type


    id = 2  # number of persons you want to Recognize


    names = ['', 'Riddhi']  # names, leave first empty bcz counter starts from 0


    # Robust camera initialization
    def open_camera():
        # Priority: DSHOW (most common on Windows), MSMF, Default
        backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, None]
        indices = [0, 1]
        
        for backend in backends:
            for index in indices:
                try:
                    if backend is not None:
                        cam = cv2.VideoCapture(index, backend)
                    else:
                        cam = cv2.VideoCapture(index)
                    
                    if cam.isOpened():
                        # Test if we can actually read a frame
                        ret, img = cam.read()
                        if ret:
                            print(f"Success: Camera opened with index {index} and backend {backend}")
                            return cam
                        cam.release()
                except Exception as e:
                    print(f"Warning: Failed to open camera index {index} with backend {backend}: {e}")
        return None

    cam = open_camera()
    
    if cam is None:
        print("Error: Could not open camera with any backend or index.")
        return 0

    cam.set(3, 640)  # set video FrameWidht
    cam.set(4, 480)  # set video FrameHeight

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    max_retries = 50
    retry_count = 0

    while True:

        ret, img = cam.read()  # read the frames using the above created object

        if not ret or img is None:
            retry_count += 1
            if retry_count % 10 == 0: # Print every 10 attempts to reduce log spam
                print(f"Warning: Could not read frame from camera (Attempt {retry_count}/{max_retries}). skipping...")
            
            if retry_count >= max_retries:
                print("Error: Max retries reached. Camera might be failing.")
                break
            time.sleep(0.05)  # reduced delay for better responsiveness
            continue
        
        # Reset retry count on successful read
        retry_count = 0

        # The function converts an input image from one color space to another
        converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            converted_image,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for(x, y, w, h) in faces:

            # used to draw a rectangle on any image
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # to predict on every single image
            id, accuracy = recognizer.predict(converted_image[y:y+h, x:x+w])

            # Check if accuracy is less them 100 ==> "0" is perfect match
            if (accuracy < 100):
                id = names[id]
                accuracy = "  {0}%".format(round(100 - accuracy))
                flag = 1
            else:
                id = "unknown"
                accuracy = "  {0}%".format(round(100 - accuracy))
                flag = 0

            cv2.putText(img, str(id), (x+5, y-5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(accuracy), (x+5, y+h-5),
                        font, 1, (255, 255, 0), 1)

        cv2.imshow('Face Authentication (Press ESC to Skip)', img)

        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            print("INFO: Authentication skipped by user.")
            flag = 2 # 2 means skipped
            break
        if flag == 1:
            break
            

    # Do a bit of cleanup
    
    cam.release()
    cv2.destroyAllWindows()
    return flag

# AuthenticateFace()