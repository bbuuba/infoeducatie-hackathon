import cv2
from deepface import DeepFace

# Load face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def get_emotion(face_roi):
    try:
        # Perform emotion analysis on the face ROI
        result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
        # Determine the dominant emotion
        emotion = result[0]['dominant_emotion']
        return emotion
    except Exception as e:
        print(f"Error in emotion detection: {e}")
        return "Unknown"

def capture_and_analyze():
    # Initialize webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Unable to access the webcam.")
        return "Unknown"

    # Capture a single frame
    ret, frame = cap.read()
    
    # Release the webcam
    cap.release()
    
    if not ret:
        print("Error: Unable to capture an image.")
        return "Unknown"

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Variable to store the detected emotion
    emotion = "None"

    for (x, y, w, h) in faces:
        # Extract the face ROI (Region of Interest)
        face_roi = frame[y:y + h, x:x + w]

        # Analyze the emotion in the face ROI
        emotion = get_emotion(face_roi)
    
    # Optionally display the result on the frame
    cv2.putText(frame, f'Emotion: {emotion}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.imshow('Emotion Detection', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(emotion)
    return emotion

capture_and_analyze()
