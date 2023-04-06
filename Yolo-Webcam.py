from ultralytics import YOLO
import cv2
import cvzone
import math

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

model = YOLO("../Yolo-Weights/yolov8l.pt")

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

while True:
    success, img = cap.read()
    results = model(img, stream = True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]

            # The following is to display a box around detected objects using opencv and not the fancy cvzone boxes
            # x1, y1, x2, y2 = int(x1),int(y1), int(x2), int(y2)
            # cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,255), 3)

            # Boundary Box
            w, h = x2-x1, y2-y1 # finding w and h
            x1, y1 , w, h = int(x1),int(y1), int(w), int(h)
            bbox = x1, y1 , w, h
            cvzone.cornerRect(img, bbox) # displaying box around obj

            # confidence
            confidence = math.ceil((box.conf[0] * 100)) / 100 # rounding confidence levels

            # Class Names
            cls = int(box.cls[0])


            # displaying confidence: the max functions are used to say...
            # if the value or x or y is less than 0 (off screen), then use 0 instead
            cvzone.putTextRect(img, f'{classNames[cls]}  {confidence}', (max(0, x1), max(35, y1)), scale=2, thickness=2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
