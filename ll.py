import cv2
from typing_extensions import Self

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