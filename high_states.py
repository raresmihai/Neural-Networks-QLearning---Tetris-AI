from numpy import rot90

def _columnHeight(state, column):
    for line in xrange(20):
        if state[line][column][0] == 0:
            return (20 - line)
    return 0

def BoardHeight(state): 
    boardHeight = 0
    for column in xrange(10):
        boardHeight += _columnHeight(state, column)
    return int(boardHeight)/10

def BoardLevel(state):
    maxHeightDifference = max_height_difference(state)
    return maxHeightDifference <= 3

def _has_height_Valley(state, column, height):
    try:
        if column == 0:
            return (_columnHeight(state, 1) - _columnHeight(state, 0) == height)
        elif column == 9:
            return (_columnHeight(state, 8) - _columnHeight(state, 9) == height)
        leftHeight = _columnHeight(state, column-1)
        currentHeight = _columnHeight(state, column)
        rightHeight = _columnHeight(state, column+1)
        return (leftHeight - currentHeight == height and rightHeight - currentHeight == height)
    except Exception:
        return False

def _has_Valley(state, column):
    try:
        if column == 0:
            return (_columnHeight(state, 1) - _columnHeight(state, 0) >= 4)
        elif column == 9:
            return (_columnHeight(state, 8) - _columnHeight(state, 9) >= 4)
        leftHeight = _columnHeight(state, column-1)
        currentHeight = _columnHeight(state, column)
        rightHeight = _columnHeight(state, column+1)
        return (leftHeight - currentHeight >= 4 and rightHeight - currentHeight >= 4)
    except Exception:
        return False

def HasSingleValley(state):
    for column in xrange(10):
        if _has_Valley(state, column):
            return 1
    return 0

def HasMultipleValleys(state):
    numberValleys = 0
    for column in xrange(10):
        if _has_Valley(state, column):
            numberValleys += 1
    if numberValleys > 1:
        return 1
    return 0

def _BurriedHolesColumn(state, column):
    countHoles = 0
    for i in xrange(20):
        if state[i][column][0] == 0:
            for k in xrange(i + 1, 20):
                if state[k][column][0] == 1:
                    countHoles += 1
            break
    return countHoles

def numberOfBurriedHoles(state):
    burriedHoles = 0
    for column in xrange(10):
        burriedHoles += _BurriedHolesColumn(state, column)
    return burriedHoles

#Used as a high state, convert the actual value to 5 values depending on range
def BurriedHoles(state):
    burriedHoles = numberOfBurriedHoles(state)
    if burriedHoles == 0:
        return 0
    elif burriedHoles <= 5:
        return 5
    elif burriedHoles < 10:
        return 10
    elif burriedHoles == 10:
        return 15
    else:
        return 20

def has_I_valley(state):
    for column in xrange(9):
        if _has_height_Valley(state, column, height=4):
            return True
    return False


def has_L_valley(state):
    for column in xrange(9):
        if _has_height_Valley(state, column, height=2):
            return True
    return False

def max_height_difference(state):
    allHeights = [_columnHeight(state,column) for column in xrange(0,10)] 
    allHeights.sort()
    return allHeights[9] - allHeights[0]

def heights_difference(state, piece, column, rotation):
    start = column
    rotated_piece = rot90(piece[0], k = 4 - rotation)
    end = min(10,column + len(rotated_piece[0]))
    max_piece_height = 0
    for i in xrange(start,end):
        height = _columnHeight(state, i)
        if height > max_piece_height:
            max_piece_height = height
    difference_height_sum = 0
    for c in xrange(0, 10):
        if c < start or c >= end:
            height_c1 = _columnHeight(state, c)
            difference_height_sum += abs(max_piece_height - height_c1)
    return difference_height_sum

def heights_sum(state):
    sum = 0
    for c1 in xrange(0,9):
        sum += _columnHeight(state, c1)
    return sum

def max_height(state):
    allHeights = [_columnHeight(state,column) for column in xrange(0,10)]
    allHeights.sort()
    return allHeights[9]


#get the bottom most '0' in the piece (cell occupied) on column 0 , e.g.  00
#                                                                        -10  -> will return height = 1, not 3
#                                                                        -10
def get_down_height(piece, column = 0):
    try:
        piece_height = len(piece[0]) - 1
        while piece_height >= 0:
            if piece[0][piece_height][column] == 0:
                return piece_height + 1
            piece_height -= 1
        return len(piece[0])
    except Exception as e:
        print(e)

def get_peak_height(piece, column):
    try:
        piece_height = len(piece[0]) - 1
        while piece_height >= 0:
            if piece[0][piece_height][column] == -1:
                return piece_height + 1
            piece_height -= 1
        return len(piece[0])
    except Exception as e:
        print(e)