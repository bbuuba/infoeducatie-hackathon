import cv2
import time
import threading
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.face import FaceClient
from azure.ai.vision.face.models import FaceAttributeType

subscription_key = "FACE_API_KEY"  # Replace with your actual subscription key
endpoint = "FACE_ENDPOINT"  # Replace with your actual endpoint

face_client = FaceClient(endpoint, AzureKeyCredential(subscription_key))

class FaceDetector(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.org = (50, 30)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1
        self.color = (0, 255, 0)
        self.thickness = 2
        self.frame2 = None
        self.frame = None
        self.cap = cv2.VideoCapture(0)
        self.counter = 0

    def run(self):
        _, self.frame = self.cap.read()
        self.frame2 = self.frame.copy()
        while True:
            _, frame = self.cap.read()
            self.frame = frame.copy()
            frame = cv2.putText(frame, "Real Time", self.org, self.font, self.font_scale, self.color, self.thickness, cv2.LINE_AA)
            frame_full = cv2.hconcat([frame, self.frame2])
            cv2.imshow(self.name, frame_full)
            if cv2.getWindowProperty(self.name, cv2.WND_PROP_VISIBLE) < 1:
                break
        cv2.destroyAllWindows()

    def detect_faces(self, local_image):
     face_attributes = ["emotion", "age", "gender"]
     detected_faces = face_client.face.detect_with_stream(
        local_image,
        return_face_attributes=face_attributes,
        detection_model='detection_01'
    )
     return detected_faces


    def detector(self):
        emotions_ref = ["neutral", "sadness", "happiness"]
        while True:
            time.sleep(1)
            frame = self.frame.copy()
            cv2.imwrite('test.jpg', frame)
            local_image = open('test.jpg', "rb")
            faces = self.detect_faces(local_image)
            if faces:
                emotion = self.get_emotion(faces[0].face_attributes.emotion)
                if emotion[0] in emotions_ref:
                    self.counter += 1
                    emotions_ref.remove(emotion[0])
                left, top, width, height = self.get_rectangle(faces[0])
                frame = cv2.rectangle(frame, (left, top), (left + width, top + height + 100), (255, 0, 0), 3)
                frame = cv2.rectangle(frame, (left, top + height), (left + width, top + height + 100), (255, 0, 0), cv2.FILLED)
                frame = cv2.putText(frame, "emotion: " + str(emotion[0]), (left, top + height + 80), self.font, 0.6, self.color, self.thickness, cv2.LINE_AA)
                frame = cv2.putText(frame, "#emotions : " + str(self.counter), (400, 30), self.font, self.font_scale, self.color, self.thickness, cv2.LINE_AA)
                self.frame2 = frame

    def get_emotion(self, emotion_obj):
        emotion_dict = {
            'anger': emotion_obj.anger,
            'contempt': emotion_obj.contempt,
            'disgust': emotion_obj.disgust,
            'fear': emotion_obj.fear,
            'happiness': emotion_obj.happiness,
            'neutral': emotion_obj.neutral,
            'sadness': emotion_obj.sadness,
            'surprise': emotion_obj.surprise
        }
        emotion_name = max(emotion_dict, key=emotion_dict.get)
        emotion_confidence = emotion_dict[emotion_name]
        return emotion_name, emotion_confidence

    def get_rectangle(self, face):
        rect = face.face_rectangle
        left = rect.left
        top = rect.top
        width = rect.width
        height = rect.height
        return left, top, width, height

detector = FaceDetector(1, "Face Detection - Azure")
detector.start()
time.sleep(0.5)
detector.detector()
