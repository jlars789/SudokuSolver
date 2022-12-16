import random
import math
import copy
class Board:
    def __init__(self, vals=None, diff=3):

        if vals is not None:
            for i in range(9):
                self.arr[i] = vals
        else:
            bo = generate(diff)
            self.arr = bo[0] 
            self.sln = bo[1]

    def setVal(self, i, j, val):
        self.arr[i][j] = val

    def solution(self):
        return self.sln
    
    def printBoard(self):
        self.printArray(self.arr)
    
    def printSolution(self):
        self.printArray(self.sln)

    def printArray(self, arr):
        for i in range(9):
            for j in range(9):
                if arr[i][j] < 0:
                    print("[ ]", end='')
                else:
                    print("[{}]".format(arr[i][j]+1), end='')
                if (j + 1) % 3 == 0 and (j not in (0, 8)):
                    print(" | ", end='')
            print(" ")
            if (i+1) % 3 == 0 and (i not in (0, 8)):
                print("-"*33)

VAL_ARR = [0, 1, 2, 3, 4, 5, 6, 7, 8]

DEFAULT_BOARD = [
    [0,1,2, 3,4,5, 6,7,8], 
    [3,4,5, 6,7,8, 0,1,2],
    [6,7,8, 0,1,2, 3,4,5],
    [1,2,0, 4,5,3, 7,8,6],
    [4,5,3, 7,8,6, 1,2,0],
    [7,8,6, 1,2,0, 4,5,3],
    [2,0,1, 5,3,4, 8,6,7],
    [5,3,4, 8,6,7, 2,0,1],
    [8,6,7, 2,0,1, 5,3,4]
]


def generate(diff):

    arr = DEFAULT_BOARD    

    arr = fullShuffle(arr)

    sln = copy.deepcopy(arr)
    removeCount = 0
    if diff > 0:
        removeCount = 81 - int(81/(math.log((diff+1) * 2))) + diff + random.randrange(9-diff) 
    
    arr = removeValues(arr, removeCount)

    return arr, sln


def fullShuffle(arr):
    for i in range(9):
        arr = swapVals(arr)
    
    arr = shuffleRows(arr)
    arr = shuffleCols(arr)
    return arr

def swapVals(arr):
    val_list = VAL_ARR.copy()
    val1 = val_list[random.randrange(9)]
    val_list.remove(val1)
    val2 = val_list[random.randrange(8)]
    for r in range(9):
        for c in range(9):
            if arr[r][c] == val1:
                arr[r][c] = val2
            elif arr[r][c] == val2:
                arr[r][c] = val1
    return arr

def shuffleRows(arr):
    block = 0
    for i in range(9):
        randomVal = random.randrange(3)
        block = math.floor(i/3)
        arr = swapRows(arr, i, block * 3 + randomVal)
    
    return arr

def swapRows(arr, r1, r2):
    rowS = arr[r1]
    arr[r1] = arr[r2]
    arr[r2] = rowS
    return arr
    

def shuffleCols(arr):
    block = 0
    for i in range(9):
        randomVal = random.randrange(3)
        block = math.floor(i/3)
        arr = swapCols(arr, i, block*3+randomVal)

    return arr

def swapCols(arr, c1, c2):

    for i in range(9):
        colVal = arr[i][c1]
        arr[i][c1] = arr[i][c2]
        arr[i][c2] = colVal
    
    return arr

def removeValues(arr, removeCount):
    removeArr = []
    for i in range(81):
        removeArr.append(1)

    removed = 0
    while removed < removeCount:
        rand = random.randrange(81)
        if removeArr[rand] > 0:
            removeArr[rand] = -2
            removed += 1
        
    for i in range(81):
        r = math.floor(i/9)
        c = i % 9

        if removeArr[i] < 0:
            arr[r][c] = -2

    return arr

