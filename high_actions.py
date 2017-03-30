import numpy as np
import high_states
import copy

class HighActions:
    def __init__(self):
        self.actions = ["minimize_holes", "minimize_height", "maximize_lines", \
            "create_I_valley", "create_L_valley", "level_board", "mix_actions"]
        self.column = 0

    def get_action_name(self,action_number):
        return self.actions[action_number]

    def minimize_holes(self, state, currentPiece):
        board_min_holes = 200
        min_height_difference = 20
        best_state = None
        for rotation in xrange(0,4):
            for column in xrange(0,10):
                new_state = self.move_piece(state, currentPiece, column, rotation)
                if new_state is not None:
                    board_holes = high_states.numberOfBurriedHoles(new_state)
                    height_difference = high_states.max_height_difference(new_state)
                    if board_holes < board_min_holes:
                        board_min_holes = board_holes
                        best_state = new_state
                        self.column = column
                        min_height_difference = height_difference
                    elif board_holes == board_min_holes and height_difference < min_height_difference:
                        min_height_difference = height_difference
                        best_state = new_state
                        self.column = column
        return best_state

    def minimize_height(self, state, currentPiece):
        min_height = 200
        min_height_difference = 20
        best_state = None
        for rotation in xrange(0,4):
            for column in xrange(0,10):
                new_state = self.move_piece(state, currentPiece, column, rotation)
                if new_state is not None:
                    avg_height = high_states.BoardHeight(new_state)
                    height_difference = high_states.max_height_difference(new_state)
                    if avg_height < min_height:
                        min_height = avg_height
                        min_height_difference = height_difference
                        best_state = new_state
                        self.column = column
                    elif avg_height == min_height and height_difference < min_height_difference:
                        min_height_difference = height_difference
                        best_state = new_state
                        self.column = column
        return best_state

    def maximize_lines(self, state, currentPiece):
        max_lines_cleared = -1
        best_state = self.move_piece(state, currentPiece, np.random.randint(0,10), np.random.randint(0,4))
        for rotation in xrange(0,4):
            for column in xrange(0,10):
                new_state = self.move_piece(state, currentPiece, column, rotation)
                if new_state is not None:
                    lines_cleared = self.number_of_lines_cleared(new_state)
                    if lines_cleared > max_lines_cleared:
                        max_lines_cleared = lines_cleared
                        best_state = new_state
                        self.column = column
        return best_state

    def create_I_valley(self, state, currentPiece):
        best_state = self.move_piece(state, currentPiece, 0,0)
        for rotation in xrange(0,4):
            for column in xrange(0,10):
                new_state = self.move_piece(state, currentPiece, column, rotation)
                if new_state is not None and high_states.has_I_valley(new_state):
                    best_state = new_state
                    self.column = column
        return best_state


    def create_L_valley(self, state, currentPiece):
        best_state = self.move_piece(state, currentPiece, 0,0)
        for rotation in xrange(0,4):
            for column in xrange(0,10):
                new_state = self.move_piece(state, currentPiece, column, rotation)
                if new_state is not None and high_states.has_L_valley(new_state):
                     best_state = new_state
                     self.column = column
        return best_state

    def level_board(self, state, currentPiece):
        min_height_sum = 200000
        best_state = None
        for rotation in xrange(0,4):
            for column in xrange(0,10):
                new_state = self.move_piece(state, currentPiece, column, rotation)
                if new_state is not None:
                    height_sum = high_states.heights_difference(new_state, currentPiece, column, rotation)
                    if height_sum < min_height_sum:
                        min_height_sum = height_sum
                        best_state = new_state
                        self.column = column
        return best_state

    def mix_actions(self, state, currentPiece):
        minim_value = 20000
        best_state = None
        for rotation in xrange(0,4):
            for column in xrange(0,10):
                new_state = self.move_piece(state, currentPiece, column, rotation)
                if new_state is not None:
                    max_height_difference = high_states.max_height_difference(new_state)
                    burried_holes = high_states.numberOfBurriedHoles(new_state)
                    heights_sum = high_states.heights_sum(new_state)
                    value = max_height_difference + burried_holes + heights_sum
                    if value < minim_value:
                        minim_value = value
                        best_state = new_state
                        self.column = column
        return best_state

    #move piece at column and rotate it with rotation
    def move_piece(self, state, piece, column, rotation):
        state_copy = copy.deepcopy(state)
        piece_copy = copy.deepcopy(piece)
        piece_copy[0] = np.rot90(piece_copy[0], k = 4 - rotation)
        new_state = self.drop_piece(state_copy, piece_copy, column)
        return new_state

    #move the piece as bottom as possible
    def drop_piece(self, state, piece, startingColumn):
        pieceHeight = len(piece[0])
        pieceWidth = len(piece[0][0])
        firstColumnHeight = high_states.get_down_height(piece)
        gameOver = True
        placed = False
        startingLine = 20 - firstColumnHeight #- high_states._columnHeight(state, startingColumn)
        savedLine = startingLine
        if startingLine + pieceHeight > 20:
            startingLine  = 20 - pieceHeight
        try:
            while startingLine >= 0 and not placed:
                canPlace = True
                for line in xrange(startingLine,startingLine+pieceHeight):
                    for column in xrange(startingColumn,startingColumn+pieceWidth):
                        if column > 9:
                            canPlace = False
                            break
                        if state[line][column][0] == 0 and piece[0][line-startingLine][column-startingColumn] == 0:
                            canPlace = False
                            break

                if canPlace:
                    piece_rotated = np.rot90(piece[0], k=1)
                    width_rotated = len(piece_rotated[0])
                    min_width = min(pieceWidth,width_rotated)
                    ok = True
                    maxColumn = 11 - min_width
                    start = max(0,startingColumn-1)
                    maxColumn = min(startingColumn+2,maxColumn)
                    for column in xrange(start,maxColumn):
                        ok = True
                        for s_line in xrange(startingLine+pieceHeight-1,pieceHeight-2,-1):
                            for line in xrange(s_line,s_line-pieceHeight,-1):
                                for c in xrange(column,  column + min_width):
                                    if state[line][c][0] == 0 and piece[0][pieceHeight - (s_line-line)-1][column-c] == 0:
                                        ok = False
                                        break
                        if ok:
                            break
                    if not ok:
                        canPlace = False

                if canPlace:
                    placed = True
                    start_line = startingLine
                    bottomFound = False
                    while start_line <= 20 - pieceHeight and not bottomFound:
                        for line in xrange(start_line, start_line + pieceHeight):
                            for column in xrange(startingColumn, startingColumn + pieceWidth):
                                if column > 9:
                                    bottomFound = True
                                    break
                                if state[line][column][0] == 0 and piece[0][line - start_line][
                                            column - startingColumn] == 0:
                                    bottomFound = True
                                    break
                        if not bottomFound:
                            savedLine = start_line
                            start_line += 1

                startingLine -= 1
        except Exception as e:
            print e

        if placed:
            for line in xrange(savedLine, savedLine + pieceHeight):
                for column in xrange(startingColumn, startingColumn + pieceWidth):
                    if piece[0][line - savedLine][column - startingColumn] == 0:
                        state[line][column][0] = 0
                        state[line][column][1] = piece[1]
            gameOver = False

        if gameOver:
            return None
        else:
            return state

    #used in maximize lines
    def number_of_lines_cleared(self, state):
        if state is None:
            return 0

        number = 0
        for line in xrange(0,20):
            line_cleared = True
            for column in xrange(0,10):
                if state[line][column][0] == 1:
                    line_cleared = False
                    break
            if line_cleared:
                number += 1
        return number




    def getBurriedHoles(self, state, startingColumn, piece):
        endingColumn = min(10,startingColumn + len(piece[0][0]))
        burriedHoles = 0
        for c in xrange(startingColumn,endingColumn):
            burriedHoles += high_states._BurriedHolesColumn(state, c)
        return burriedHoles
