#from this import d # :)
from typing_extensions import Self
import cv2
import sys
import numpy
import scipy
import pandas

class ll:
    def __init__(self, next: Self = None, prev: Self = None, im: cv2 = None, faces: cv2 = None) -> None:
        self.__next = next
        self.__prev = prev
        self.__im = im
        self.__faces = faces

    def setNext(self, next) -> None:
        self.__next = next

    def setPrev(self, prev) -> None:
        self.__prev = prev
    
    def setIm(self, im) -> None:
        self.__im = im

    def setFaces(self, faces) -> None:
        self.__faces = faces
    
    def getFaces(self) -> cv2:
        return self.__faces
    
    def getIm(self) -> cv2:
        return self.__im
    
    def getPrev(self) -> Self:
        return self.__prev
    
    def getNext(self) -> Self:
        return self.__next
    
    def __str__(self) -> str:
    #     if self.__next == None:
    #         return "Prev: {0}".format(self.__prev)
    #     elif self.__prev == None:
    #         return ""
    #     else:
    #         return "Next: {0}, prev: {1}".format(self.__next, self.__prev)
        pass

#Cite https://www.geeksforgeeks.org/hash-map-in-python/ for resource
class hashtable:
    def __init__(self, size: int = 0) -> None:
        self.__size = size
        self.__hashtable = self.createBuckets()
    
    #Created this myself
    def resize(self) -> Self:
        __newHashObject = hashtable(self.getSize()**2)
        __newHashTable = __newHashObject.getHashTable()
        __oldHashTable = self.getHashTable()

        for _oldbucket, _newbucket in zip(__oldHashTable, __newHashTable):
            for index, record, in enumerate(_oldbucket):
                record_key, record_val = record
                _newbucket.append((record_key, record_val))
        
        return __newHashObject
    
    def getSize(self) -> int:
        return self.__size
    
    def getHashTable(self) -> Self:
        return self.__hashtable

    def createBuckets(self) -> list:
        return [[] for _i in range(self.getSize())]
    
    def setVal(self, key, val) -> None:
        hashed_key = hash(key) % self.getSize()

        bucket = self.getHashTable()[hashed_key]

        f_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
            if record_key == key:
                f_key = True
                break
        
        if f_key:
            bucket[index] = (key, val)
        else:
            bucket.append((key,val))
    
    def getVal(self, key) -> ll or None:
        hashed_key = hash(key) % self.getSize()

        bucket = self.getHashTable()[hashed_key]

        f_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
            if record_key == key:
                f_key = True
                break
        
        if f_key:
            return record_val
        else:
            return None

    def deleteVal(self, key):
        hashed_key = hash(key) % self.getSize()

        bucket = self.getHashTable()[hashed_key]

        f_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
            if record_key == key:
                f_key = True
                break
        
        if f_key:
            bucket.pop(index) 
        return

    def __str__(self) -> str:
        return "".join(str(item) for item in self.getHashTable())

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
    cv2.waitKey(0)

def main() -> None:
    #User supplied values, image is arg1, cascading path is arg2
    image_path = sys.argv[1]
    cascPath = sys.argv[2]
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

if __name__ == "__main__":
    main()
    #hash_test()