import board
import math

def solve(board):
    
    board = naiveCheck(board)
    notes = generateNotes(board)
    checkExclusive(board, notes)
    return board

def checkExclusive(board, notes=None, blocks=None):
    row_exclusive = []
    col_exclusive = []

    for i in range(9):
        row_exclusive.append(checkRowExclusive(board, notes, i))
        col_exclusive.append(checkColExclusive(board, notes, i))
    
    print(notes)
    print(row_exclusive)
    print(col_exclusive)

def checkRowExclusive(board, notes, row, blocks=None):
    ex = set()
    rowIndex = row*9
    full = set()

    for i in range(9):
        full = full | notes[rowIndex + i]

    print(full)

    for i in range(9):
        
        tmp = full.symmetric_difference(notes[rowIndex + i])
        print("Row {} ^ {} = {}".format(full, notes[rowIndex + i], tmp))
        full = tmp
        
        #print(notes[rowIndex + i])

    return ex   
        

def checkColExclusive(board, notes, col, blocks=None):
    ex = set()

    for i in range(9):
        ex = ex.symmetric_difference(notes[col + i*9])

    return ex   

def generateNotes(board):
    notes = []
    for i in range(9):
        for j in range(9):
            opts = set()
            
            if board.arr[i][j] < 0:
                r = set(analyzeRow(board, i))
                c = set(analyzeCol(board, j))
                b = set(analyzeBox(board, i, j))
                opts = r & c & b
            
            notes.append(opts)
    
    return notes
    

def createBlocks(board, notes):

    row_blocks = []
    col_blocks = []
    for i in range(9):
        row_blocks.append(set())
        col_blocks.append(set())
    for i in range(9):
        for j in range(9):
            indexC = i*9 + j
            if board.arr[i][j] < 0 and len(notes[indexC]) == 2:
                row = checkRowNotes(board, notes, i, j)
                if len(row) == 1:
                    row_blocks[i] = row[0]
                
                col = checkColNotes(board, notes, i, j)
                if len(col) == 1:
                    col_blocks[j] = col[0]

    return (row_blocks, col_blocks)


def checkRowNotes(board, notes, r, c):
    rowIndex = r*9
    identical = []
    set1 = notes[rowIndex + c]
    for i in range(9):
        if i != c and board.arr[r][i] < 0:
            set2 = notes[rowIndex + i]
            if set2.issubset(set1) and len(set1) == len(set2):
                identical.append(set2)
    return identical

def checkColNotes(board, notes, r, c):
    rowIndex = r*9
    identical = []
    set1 = notes[rowIndex + c]
    for i in range(9):
        if i != r and board.arr[i][c] < 0:
            set2 = notes[i*9 + c]
            if set2 in set1 and len(set1) == len(set2):
                identical.append(set2)
    return identical

def naiveCheck(board, notes=None):
    solved = 0
    for i in range(9):
        for j in range(9):
            if board.arr[i][j] > -1:
                solved+=1
    itrs = 0
    while solved < 81 and itrs < 9:
        for i in range(9):
            for j in range(9):
                if board.arr[i][j] < 0:
                    r = set(analyzeRow(board, i))
                    c = set(analyzeCol(board, j))
                    b = set(analyzeBox(board, i, j))
                    opts = list( r & c & b)
                    
                    if len(opts) == 1:
                        board.setVal(i, j, opts[0])
                        solved += 1
        itrs+=1

    if solved >= 81:
        print("Solved")
    return board

def validate(b1, b2):
    for i in range(9):
        for j in range(9):
            if b1[i][j] >= 0 and b2[i][j] >= 0 and b1[i][j] != b2[i][j]:
                return False
    return True

def analyzeSpace(board, i, j):
    return list(set(analyzeRow(board, i)) | set(analyzeCol(board, j)) | set(analyzeBox(board, i, j)))

# returns list of available values in row
def analyzeRow(board, ind):
    valAvailable = []
    for i in range(9):
        if i not in board.arr[ind]:
            valAvailable.append(i)
            
    return valAvailable

# returns list of available values in row
def analyzeCol(board, ind):
    valAvailable = []
    colList = []
    for i in range(9):
        colList.append(board.arr[i][ind])

    for i in range(9):
        if i not in colList:
            valAvailable.append(i)
    return valAvailable

#returns available values in square (doesn't work)
def analyzeBox(board, i, j):
    valAvailable = set()
    n = math.floor(i/3)*3
    m = n + 2
    
    k = math.floor(j/3)*3
    l = k + 2

    boxList = set()
    for p in range(n, m+1):
        for o in range(k, l+1):
            boxList.add(board.arr[p][o])
            
    
    for p in range(9):
        if p not in boxList:
            valAvailable.add(p)

    return valAvailable
    
def inRow(val, arr, i, j):
    return True


if __name__ == "__main__":
    b = board.Board(diff=3)
    print("Given Board:")
    b.printBoard()
    print("_"*33)
    print("Attempted solution:")
    b = solve(b)
    b.printBoard()
    print("_"*33)
    print("Actual solution:")
    b.printSolution()

    k = validate(b.arr, b.sln)

    if k:
        print("Board was correct")
    else:
        print("Board had error!")