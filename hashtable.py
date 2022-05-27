import cv2
import ll
from typing_extensions import Self

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
