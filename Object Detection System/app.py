import cv2
import matplotlib.pyplot as plt

config_file = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
frozen_model = "frozen_inference_graph.pb"

# Load the model
net = cv2.dnn.readNetFromTensorflow(frozen_model, config_file)

classLabels = []
filename = "labels.txt"
with open(filename, "rt") as fpt:
    classLabels = fpt.read().rstrip('\n').split('\n')

print(classLabels)
print(len(classLabels))

img = cv2.imread("MSD.jpg")

# Prepare the image for the model
blob = cv2.dnn.blobFromImage(img, 1.0/127.5, (320, 320), (127.5, 127.5, 127.5), swapRB=True, crop=False)
net.setInput(blob)

# Run the detection
detections = net.forward()

# Loop over the detections
height, width, _ = img.shape
for i in range(detections.shape[2]):
    confidence = detections[0, 0, i, 2]
    if confidence > 0.5:
        class_id = int(detections[0, 0, i, 1])
        x1 = int(detections[0, 0, i, 3] * width)
        y1 = int(detections[0, 0, i, 4] * height)
        x2 = int(detections[0, 0, i, 5] * width)
        y2 = int(detections[0, 0, i, 6] * height)

        # Draw the bounding box and label on the image
        if class_id-1 < len(classLabels):
            label = classLabels[class_id-1]
        else:
            label = 'Unknown'
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(img, label, (x1+10, y1+40), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()

cap = cv2.VideoCapture("MS Dhoni_ The quickest hands in the east.mp4")
if not cap.isOpened():
    cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Can't open the video")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    blob = cv2.dnn.blobFromImage(frame, 1.0/127.5, (320, 320), (127.5, 127.5, 127.5), swapRB=True, crop=False)
    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.55:  # Adjust confidence threshold if necessary
            class_id = int(detections[0, 0, i, 1])
            x1 = int(detections[0, 0, i, 3] * frame.shape[1])
            y1 = int(detections[0, 0, i, 4] * frame.shape[0])
            x2 = int(detections[0, 0, i, 5] * frame.shape[1])
            y2 = int(detections[0, 0, i, 6] * frame.shape[0])

            if class_id-1 < len(classLabels):
                label = classLabels[class_id-1]
            else:
                label = 'Unknown'
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, label, (x1+10, y1+40), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    print("Object Detection System")
    cv2.imshow("Frame", frame)

    if cv2.waitKey(2) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
