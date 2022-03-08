#from this import d # :)
from typing_extensions import Self
import hashtable
import ll
import cv2
import sys
import numpy
import scipy
import pandas

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
def __detection(faces, image) -> None:
    #print("Found {0} faces!").format(len(faces))
    for (x,y,w,h) in faces:
        cv2.rectangle(image, (x,y), (x+w, y+h), (0, 255, 0), 2)
    
    cv2.imshow("Faces found", image)
    #cv2.waitKey(0)

def main(ARGUMENT: bool, table: hashtable) -> None:
    #User supplied values, image is arg1, cascading path is arg2
    if ARGUMENT:
        image_path = sys.argv[1]
        cascPath = sys.argv[2]
    else:
        image_path = cascPath = ""

    #Create the haar cascade:
    #print(cascPath)
    
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
        __detection(faces, image)

        node = ll(None, ptr, image, faces)
        ptr.setNext(node)
        node.setPrev(ptr)
        ptr = node

        #Loop handler
        while True:
            userInput = input("Continue? Yes / No\n")
            if userInput.lower() == "yes" or userInput.lower() == "no":
                break
            print(userInput.lower())

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
    #eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    cap = cv2.VideoCapture(0)

    while 1:
        ret, image = cap.read()
        faces = __faces(face_cascade, image)
        __detection(faces, image)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        
    cap.release()
    cv2.destroyAllWindows()

#Initalize all hashtable data
def init() -> hashtable:
    hash_table = hashtable(50)
    print(hash_table)
    return hash_table

#Only execute if this is the file being ran
if __name__ == "__main__":
    webcam_test()
    # ARGUMENT = True
    # try:
    #     ARGUMENT = True if (sys.argv[1] and sys.argv[2]) else False
    # except:
    #     pass
    
    # table = init()
    # main(ARGUMENT, table)
    # #hash_test()