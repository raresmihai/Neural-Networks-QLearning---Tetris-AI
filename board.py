import random
import colors
import pygame
import tetris_test as test

class Board:

    def __init__(self):
        pygame.init()
        self.epsilon = 0
        self.pieces = ['I', 'L', 'J', 'O', 'T', 'Z', 'S']
        self.color = colors.Colors()
        self.matrixTetris = [[[1, self.color.GREY] for i in xrange(0, 10)] for j in xrange(0, 20)]
        self.currentPiece = None
        self.nextPiece = None
        self.nextNextPiece = None
        self.nextP = None
        self.currentP = None
        self.size = [580, 600]
        self.sizeSq = self.size[1] / 22
        self.centerX = None
        self.centerY = None
        self.fontSize = 15
        self.screen = pygame.display.set_mode(self.size)
        self.timer = 0
        self.pause = False

        
        #stats
        self.gamesPlayed = 0
        self.piecesPlaced = -2
        self.single_piecesPlaced = 0
        self.single_lines_1x = 0
        self.single_lines_2x = 0
        self.single_lines_3x = 0
        self.single_lines_4x = 0
        self.all_lines_1x = 0
        self.all_lines_2x = 0
        self.all_lines_3x = 0
        self.all_lines_4x = 0
        self.highestScore = 0
        self.scoreSum = 0
        self.averageScore = 0
        self.averagePieces = 0
        self.singleScore = 0

        self.setTetris()

    def updateSingleScore(self, score):
        self.singleScore = score

    def updateScore(self, score):
        self.singleScore = 0
        self.highestScore = int(max(self.highestScore, score))
        self.scoreSum += score
        self.averageScore =  int(self.scoreSum) / self.gamesPlayed

    def incrementAllLines(self, lines_count):
        if lines_count == 1:
            self.all_lines_1x += 1
        elif lines_count == 2:
            self.all_lines_2x += 1
        elif lines_count == 3:
            self.all_lines_3x += 1
        elif lines_count == 4:
            self.all_lines_4x += 1

    def updateSingleGameLines(self, x1, x2, x3, x4):
        self.single_lines_1x = max(self.single_lines_1x, x1)
        self.single_lines_2x = max(self.single_lines_2x, x2)
        self.single_lines_3x = max(self.single_lines_3x, x3)
        self.single_lines_4x = max(self.single_lines_4x, x4)

    def updateSinglePiecesPlaced(self, piecesCount):
        self.averagePieces = self.piecesPlaced / self.gamesPlayed
        self.single_piecesPlaced = max(self.single_piecesPlaced,piecesCount)

    def updateFont(self, sizeFont):
        self.fontSize = sizeFont
        self.font = pygame.font.SysFont('Calibri', self.fontSize, 0)

    def setTetris(self):
        self.updateCenters()
        self.updateFont(15)
        pygame.display.set_caption("Tetris")
        #pygame.display.set_icon(self.logo)

    def updateCenters(self):
        self.centerY = int(self.size[1] / 22 / self.sizeSq)
        if self.centerY is 0: self.centerY = 1
        self.centerX = int(self.size[0] / 12 / self.sizeSq)
        if self.centerX is 0: self.centerX = 1

    def get_init_state(self):
        self.gamesPlayed += 1
        self.matrixTetris = [[[1, self.color.GREY] for i in xrange(0, 10)] for j in xrange(0, 20)]
        return self.matrixTetris

    def generate_next_piece(self, piece=0, init=False):
        self.piecesPlaced += 1
        nextP = random.choice(self.pieces)
        if not init:
            if piece==0:
                self.currentPiece = getattr(self, nextP)()
            elif piece==1:
                self.nextPiece = getattr(self, nextP)()
            else:
                self.nextNextPiece = getattr(self, nextP)()
        else:
            self.currentPiece = self.nextPiece
            self.nextPiece = self.nextNextPiece
            self.nextNextPiece = getattr(self, nextP)()
        return nextP

    def get_next_piece_array(self, piece):
        if piece==0:
            return self.currentPiece
        elif piece==1:
            return self.nextPiece
        else:
            return self.nextNextPiece


    def get_piece_index(self,piece):
        return self.pieces.index(piece)

    def set_matrix_tetris(self, new_state):
        self.matrixTetris = new_state

    def I(self):
        nextPiece = [[[-1 for i in xrange(0, 4)] for j in xrange(0, 1)], self.color.ORANGE]
        for i in xrange(0, 4):
            nextPiece[0][0][i] = 0
        return nextPiece

    def L(self):
        nextPiece = [[[-1 for i in xrange(0, 3)] for j in xrange(0, 2)], self.color.BLUE]
        for i in xrange(0, 3):
            nextPiece[0][1][i] = 0
        nextPiece[0][0][2] = 0
        return nextPiece

    def J(self):
        nextPiece = [[[-1 for i in xrange(0, 3)] for j in xrange(0, 2)], self.color.TURQUAISE]
        for i in xrange(0, 3):
            nextPiece[0][1][i] = 0
        nextPiece[0][0][0] = 0
        return nextPiece

    def O(self):
        nextPiece = [[[-1 for i in xrange(0, 2)] for j in xrange(0, 2)], self.color.RED]
        for i in xrange(0, 2):
            for j in xrange(0, 2):
                nextPiece[0][i][j] = 0
        return nextPiece

    def T(self):
        nextPiece = [[[-1 for i in xrange(0, 3)] for j in xrange(0, 2)], self.color.GREEN]
        for i in xrange(0, 3):
            nextPiece[0][1][i] = 0
        nextPiece[0][0][1] = 0
        return nextPiece

    def Z(self):
        nextPiece = [[[-1 for i in xrange(0, 3)] for j in xrange(0, 2)], self.color.PURPLE]
        for i in xrange(0, 2):
            nextPiece[0][0][i] = 0
        for i in xrange(1, 3):
            nextPiece[0][1][i] = 0
        return nextPiece

    def S(self):
        nextPiece = [[[-1 for i in xrange(0, 3)] for j in xrange(0, 2)], self.color.PINK]
        for i in xrange(0, 2):
            nextPiece[0][1][i] = 0
        for i in xrange(1, 3):
            nextPiece[0][0][i] = 0
        return nextPiece

    def game_over(self, state):
        if state is None:
            return True
        for column in xrange(0,10):
            if state[0][column][0] == 0:
                return True
        return False

    def redraw(self, event):
        scale = event.size[1] / float(self.size[1])
        self.sizeSq *= scale
        self.fontSize = 15 * scale
        self.size[0] = event.size[0]
        self.size[1] = event.size[1]
        self.updateCenters()
        self.updateFont(int(self.fontSize))
        self.draw()

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.changeEpsilon(change=-1)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.changeEpsilon(change=1)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.changeTimerPlus()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.changeTimerMinus()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.do_pause()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                self.set_matrix_tetris(test.getMatrix())
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                self.action = 0
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                self.action = 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                self.action = 2
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                self.action = 3
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                self.action = 4
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_6:
                self.action = 5
        if self.matrixTetris is not None:
            self.updateMatrix()
            self.screen.fill(self.color.WHITE)
            self.drawWorld()
            self.drawCurrentPiece()

    #def matrixIsEmpty(self):
    #    for i in xrange(20):
    #        for j in xrange(10):
    #            if self.matrixTetris[i][j][0] != 1:
    #                return False
    #    return True

    def drawCurrentPiece(self):
        try:
            for i in xrange(self.centerY + 1, self.centerY + 1 + len(self.currentPiece[0])):
                for j in xrange(self.centerX + 11, self.centerX + 11 + len(self.currentPiece[0][0])):
                    pygame.draw.polygon(self.screen, self.currentPiece[1],
                                        [[self.sizeSq * j, self.sizeSq * i], [self.sizeSq * (j + 1), self.sizeSq * i],
                                         [self.sizeSq * (j + 1), self.sizeSq * (i + 1)],
                                         [self.sizeSq * j, self.sizeSq * (i + 1)]],
                                        self.currentPiece[0][i - (self.centerY + 1)][j - (self.centerX + 11)])
        except Exception:
            return
        pygame.display.update()

    def drawWorld(self):
        try:
            for i in xrange(self.centerY, self.centerY + 20):
                for j in xrange(self.centerX, self.centerX + 10):
                    pygame.draw.polygon(self.screen, self.matrixTetris[i - self.centerY][j - self.centerX][1],
                                        [[self.sizeSq * j, self.sizeSq * i], [self.sizeSq * (j + 1), self.sizeSq * i],
                                         [self.sizeSq * (j + 1), self.sizeSq * (i + 1)],
                                         [self.sizeSq * j, self.sizeSq * (i + 1)]],
                                        self.matrixTetris[i - self.centerY][j - self.centerX][0])

        except Exception:
            return
        # Next Piece
        self.screen.blit(self.font.render('Next piece', True, self.color.BLACK),
                         ((self.centerX + 11) * self.sizeSq, self.sizeSq))
        self.screen.blit(self.font.render('Score', True, self.color.BLUE),
                         ((self.centerX + 11) * self.sizeSq, self.sizeSq * 5))
        self.screen.blit(self.font.render(str(self.singleScore), True, self.color.GREEN),
                         ((self.centerX + 11) * self.sizeSq, self.sizeSq * 6))
        self.screen.blit(self.font.render('Stats in a single game', True, self.color.BLUE),
                         ((self.centerX + 11) * self.sizeSq, self.sizeSq * 8))
        self.screen.blit(self.font.render('Average score: ' + str(self.averageScore), True, self.color.BLACK),
                         ((self.centerX + 11) * self.sizeSq, self.sizeSq * 9))
        self.screen.blit(self.font.render('Highest score: ' + str(self.highestScore), True, self.color.BLACK),
                         ((self.centerX + 11) * self.sizeSq, self.sizeSq * 10))
        self.screen.blit(self.font.render('Average pieces placed: ' + str(self.averagePieces), True, self.color.BLACK),
                         ((self.centerX + 11) * self.sizeSq, self.sizeSq * 11))
        self.screen.blit(self.font.render('Most pieces placed: ' + str(self.single_piecesPlaced), True, self.color.BLACK),
                         ((self.centerX + 11) * self.sizeSq, self.sizeSq * 12))
        self.screen.blit(self.font.render('Most lines cleared', True, self.color.BLACK),
                         ((self.centerX + 11) * self.sizeSq, self.sizeSq * 13))
        self.screen.blit(self.font.render(self.getSingleLinesClearedString(), True, self.color.BLACK),
                         ((self.centerX + 11) * self.sizeSq, self.sizeSq * 14))
        self.screen.blit(self.font.render('Stats in all games', True, self.color.BLUE),
                         ((self.centerX + 11) * self.sizeSq, self.sizeSq * 16))
        self.screen.blit(self.font.render('Games played: ' + str(self.gamesPlayed), True, self.color.BLACK),
                         ((self.centerX + 11) * self.sizeSq, self.sizeSq * 17))
        self.screen.blit(self.font.render('Pieces placed: ' + str(self.piecesPlaced), True, self.color.BLACK),
                         ((self.centerX + 11) * self.sizeSq, self.sizeSq * 18))
        self.screen.blit(self.font.render('Lines cleared', True, self.color.BLACK),
                         ((self.centerX + 11) * self.sizeSq, self.sizeSq * 19))
        self.screen.blit(self.font.render(self.getAllLinesClearedString(), True, self.color.BLACK),
                         ((self.centerX + 11) * self.sizeSq, self.sizeSq * 20))

    def isCompleteLine(self, line):
        try:
            for j in range(10):
                if self.matrixTetris[line][j][0] != 0:
                    return False
            return True
        except Exception:
            return

    def findHeight(self, line):
        try:
            for i in xrange(line + 1, 20):
                for j in xrange(10):
                    for k in xrange(0, line):
                        if self.matrixTetris[line - k - 1][j][0] == 0 and self.matrixTetris[i][j][0] == 0:
                            print i - k - 1
                            return i - 1 + k
            return 20 - 1
        except Exception:
            return line

    def removeCompleteLines(self):
        try:
            i = 20 - 1
            while i >= 0:
                if self.isCompleteLine(i):
                    height = self.findHeight(i)
                    for column in xrange(10):
                        self.matrixTetris[i][column] = [1, self.color.GREY]
                    for pullDownI in range(i):
                        for j in range(10):
                            if self.matrixTetris[height - pullDownI][j][0] == 1 and self.matrixTetris[i - pullDownI - 1][j][
                                0] == 0:
                                self.matrixTetris[height - pullDownI][j] = self.matrixTetris[i - pullDownI - 1][j]
                                self.matrixTetris[i - pullDownI - 1][j] = [1, self.color.GREY]
                    i = 20 - 1
                else:
                    i -= 1
        except Exception:
            return 

    def updateMatrix(self):
        self.removeCompleteLines()

    def getAllLinesClearedString(self):
        s = '1x: '
        s += str(self.all_lines_1x)
        s += ' | 2x: '
        s += str(self.all_lines_2x)
        s += ' | 3x: '
        s += str(self.all_lines_3x)
        s += ' | 4x: '
        s += str(self.all_lines_4x)
        return s

    def getSingleLinesClearedString(self):
        s = '1x: '
        s += str(self.single_lines_1x)
        s += ' | 2x: '
        s += str(self.single_lines_2x)
        s += ' | 3x: '
        s += str(self.single_lines_3x)
        s += ' | 4x: '
        s += str(self.single_lines_4x)
        return s

    def boardIsCleared(self, state):
        for i in xrange(20):
            for j in xrange(10):
                if state[i][j][0] != 1:
                    return False
        return True

    def changeTimerPlus(self):
        self.timer += 200

    def changeTimerMinus(self):
        self.timer -= 200

    def do_pause(self):
        self.actions = ["minimize_holes", "minimize_height", "maximize_lines", "create_I_valley", "create_L_valley", "level_board"]
        self.action = None
        if self.pause:
            self.pause = False
        else:
            self.pause = True

    def changeEpsilon(self, change=-1):
        if change < 0 and self.epsilon > 0:
            if self.epsilon < 0.1:
                self.epsilon = 0
            else:
                self.epsilon -= 0.1
        elif change > 0 and self.epsilon < 1:
            if self.epsilon > 0.9:
                self.epsilon = 1
            else:
                self.epsilon += 0.1