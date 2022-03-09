from typing_extensions import Self

import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from platform import system

from cv2 import VideoCapture
from hashtable import hashtable
from ll import ll
import cv2
import sys

from head_pose_estimation.mark_detector import *
from head_pose_estimation.pose_estimator import PoseEstimator
#import tensorflow

#input: cascade and color object of cv2
#output: parameter tuple of faces
def __faces(cascade, color) -> cv2:
    #Detect multi scale detects objects, since we call the fase cascade, that is what we are detecting.
    faces = cascade.detectMultiScale(
        color,
        scaleFactor=1.1, #Some faces may be closer to camera, compensate that
        minNeighbors=5, #Defines how many objects are detected near the current one, since we use a "moving window" for detection.
        minSize=(30,30), #Defines the size of the "moving window"
        flags = cv2.CASCADE_SCALE_IMAGE
    )
    return faces
    
#input: faces object tuple, image cv2 object
#output: draw rectangles around face, wait for user input
def __faceDetection(faces, image) -> None:
    #print("Found {0} faces!").format(len(faces))
    for (x,y,w,h) in faces:
        cv2.rectangle(image, (x,y), (x+w, y+h), (0, 255, 0), 2)
    
    cv2.imshow("Faces found", image)

#input: eyes object tuple, image cv2 object
#output: halt, draw rectangles, supposed to run before face detection
def __eyesDetection(eyes, image) -> None:
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(image,(ex,ey),(ex+ew,ey+eh),(255,255,0),2)

def picture_mode(ARGUMENT: bool, table: hashtable) -> None:
    #User supplied values, image is arg1, cascading path is arg2
    if ARGUMENT:
        image_path = sys.argv[2]
        cascPath = sys.argv[3]
    else:
        image_path = cascPath = ""
    
    userInput = "yes"
    head = ll()
    ptr = head

    while userInput.lower() == "yes":
        if not (cascPath):
            cascPath = input("Specify Cascading XML:\n")
            pass
        
        if not (image_path):
            image_path = input("Specify Image Path:\n")
            pass

        faceCascade = cv2.CascadeClassifier(cascPath)

        #Reading the image. Most of the operations in OpenCV are done in grayscale, hence why we use the Gray colorway. These create objects that we store into variables.
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #Detect faces in the image
        faces = __faces(faceCascade, gray)

        #Output detection of faces
        __faceDetection(faces, image)
        cv2.waitKey(0)

        node = ll(None, ptr, image, faces)
        ptr.setNext(node)
        node.setPrev(ptr)
        ptr = node

        table.setVal(image_path, node)
        print(table)

        #Loop handler
        while True:
            userInput = input("Continue? Yes / No\n")
            if userInput.lower() == "yes" or userInput.lower() == "no":
                image_path = ""
                break
            #print(userInput.lower())

    cv2.destroyAllWindows()
    return

#Test the hashtable class and hashing capabilities
def hash_test() -> None:
    hash_table = hashtable(50)
    # insert some values
    hash_table.setVal('gfg@example.com', 'some value')
    print(hash_table)
    print()
    
    hash_table.setVal('portal@example.com', 'some other value')
    print(hash_table)
    print()
    
    # search/access a record with key
    print(hash_table.getVal('portal@example.com'))
    print()
    
    # delete or remove a value
    hash_table.deleteVal('portal@example.com')
    print(hash_table)

    hash_table2 = hash_table.resize()
    print("resize:\n", hash_table2)

#Test webcam and draw boxes using haarcascade_frontalface
def webcam_test() -> None:
    #https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
    face_cascade = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')
    #https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
    eye_cascade = cv2.CascadeClassifier('../haarcascade_eye.xml')
    cap = cv2.VideoCapture(1)

    while True:
        ret, image = cap.read()
        faces = __faces(face_cascade, image)
        eyes = __faces(eye_cascade, image)
        __eyesDetection(eyes, image)
        __faceDetection(faces, image)
        
        #eyes = eye_cascade.detectMultiScale(gray)
        
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        
    cap.release()
    cv2.destroyAllWindows()

def webcam_mode() -> None:
    cap = VideoCapture(1)

    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    pose_estimation = PoseEstimator(img_size=(height, width))

    mark_detector = MarkDetector()

    meter = cv2.TickMeter()

    while True:
        ret, image = cap.read()

        if ret is False:
            break
            
        image = cv2.flip(image, 2)

        face = mark_detector.extract_cnn_facebox(image)

        if face is not None:
            x1, y1, x2, y2 = face
            face_image = image[y1:y2,x1:x2]

            meter.start()
            marks = mark_detector.detect_marks(face_image)
            meter.stop()

            marks *= (x2 - x1)
            marks[:, 0] += x1
            marks[:, 1] += y1

            # Try pose estimation with 68 points.
            pose = pose_estimation.solve_pose_by_68_points(marks)

            pose_estimation.draw_annotation_box(
                image, pose[0], pose[1], color=(0, 255, 0))

            pose_estimation.draw_axes(image, pose[0], pose[1])

            mark_detector.draw_box(image, [face])

        cv2.imshow("Preview", image)
        if cv2.waitKey(1) == 27:
            break


#Initalize all hashtable data
def init() -> hashtable:
    hash_table = hashtable(50)
    #print(hash_table)
    return hash_table

#Only execute if this is the file being ran
if __name__ == "__main__":
    ARGUMENT = False
    try:
        ARGUMENT = True if (
            sys.argv[1] == "--picture"
            and sys.argv[2]
            and sys.argv[3]
            ) else False
    except:
        pass
    
    table = init()
    if sys.argv[1] == "--picture":
        picture_mode(ARGUMENT, table)
    elif sys.argv[1] == "--camera":
        webcam_mode()
    elif sys.argv[1] == "--test":
        webcam_test()
        hash_test()
    