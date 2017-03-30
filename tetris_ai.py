import board
import high_states
import tetris_nn
import numpy as np
import random
import high_actions

class TetrisAI():
    def __init__(self, model):
        self.board = board.Board()
        self.state = None
        self.currentPiece = self.board.generate_next_piece(0)
        self.nextPiece = self.board.generate_next_piece(1)
        self.nextNextPiece = self.board.generate_next_piece(2)
        self.high_actions = high_actions.HighActions()
        self.model = model
        self.iterations = 0
        self.GAME_OVER_REWARD = -200
        self.play()

    def play(self):
        gamma = 0.975
        batchSize = 100
        buffer = 50000
        epochs = 3000
        replay = [] #store tuples of (S,A,R,S')
        h = 0

        while True:
            #init state and stats
            self.state = self.board.get_init_state()
            self.board.draw()
            self.linesCleared_x1 = 0
            self.linesCleared_x2 = 0
            self.linesCleared_x3 = 0
            self.linesCleared_x4 = 0
            self.boardLevel = 0
            self.burriedHoles = 0
            self.piecesPlaced = 0
            self.currentGame_level = 1
            self.score = 0

            # Pause
            while self.board.pause:
                self.board.draw()
                if self.board.action is not None:
                    self.state = self.board.matrixTetris
                    new_state = self.make_move(self.board.action)

                    if new_state is None:
                        new_state = self.board.get_init_state()

                    # update lines stats
                    self.board.incrementAllLines(self.high_actions.number_of_lines_cleared(new_state))
                    self.updateSingleLinesCleared(new_state)

                    self.state = new_state
                    self.currentPiece = self.nextPiece
                    self.piecesPlaced += 1
                    self.nextPiece = self.board.generate_next_piece()
                    self.board.updateSingleScore(self.score)
                    self.board.set_matrix_tetris(self.state)

                    self.board.action = None

            status = 1
            #while game still in progress
            while status == 1 and not self.board.pause:
                # Delay
                if self.board.timer > 0:
                    board.pygame.time.delay(self.board.timer)

                #convert the state matrix to a high states array
                high_state = self.get_high_state(self.state, self.currentPiece, self.nextPiece)
                print high_state
                qval = self.model.predict(high_state.reshape(1,12), batch_size = 1)
                if random.random() < self.board.epsilon:
                    action = np.random.randint(0,7)
                else:
                    action = np.argmax(qval)

                new_state = self.make_move(action)
                column_placed = self.high_actions.column
                reward = self.get_reward(new_state, column_placed)
                print 'Reward: ', reward
                self.score = int(self.score + self.get_score(new_state, column_placed))
                new_high_state = self.get_high_state(new_state, self.nextPiece, self.nextNextPiece)

                #update lines stats
                self.board.incrementAllLines(self.high_actions.number_of_lines_cleared(new_state))
                self.updateSingleLinesCleared(new_state)

                #Experience replay storage
                if (len(replay) < buffer): #if buffer not filled, add to it
                    replay.append((high_state, action, reward, new_high_state))
                else: #if buffer full, overwrite old values
                    if (h < (buffer-1)):
                        h += 1
                    else:
                        h = 0
                    replay[h] = (high_state, action, reward, new_high_state)
                    #randomly sample our experience replay memory
                    minibatch = random.sample(replay, batchSize)
                    X_train = []
                    y_train = []
                    for memory in minibatch:
                        #Get max_Q(S',a)
                        old_state, action, mem_reward, next_state = memory
                        old_qval = self.model.predict(old_state.reshape(1,12), batch_size=1)
                        newQ = self.model.predict(next_state.reshape(1,12), batch_size=1)
                        maxQ = np.max(newQ)
                        y = np.zeros((1,7))
                        y[:] = old_qval[:]
                        if mem_reward != self.GAME_OVER_REWARD and mem_reward < 50 : #non-terminal state
                            update = (mem_reward + (gamma * maxQ))
                        else: #terminal state
                            update = mem_reward
                        y[0][action] = update
                        X_train.append(old_state.reshape(12,))
                        y_train.append(y.reshape(7,))

                    X_train = np.array(X_train)
                    y_train = np.array(y_train)

                    self.model.fit(X_train, y_train, batch_size=batchSize, nb_epoch=1, verbose=1)

                if reward == self.GAME_OVER_REWARD or new_state is None: #if game over
                    status = 0

                self.state = new_state
                self.currentPiece = self.nextPiece
                self.piecesPlaced += 1
                self.nextPiece = self.nextNextPiece
                self.nextNextPiece = self.board.generate_next_piece(init=True)
                self.board.updateSingleScore(self.score)
                self.board.set_matrix_tetris(self.state)
                self.board.draw()
                print self.board.epsilon

            if self.board.epsilon > 0.1 and len(replay) > 49990: #decrement epsilon over time
                if self.board.epsilon == 1:
                    self.board.epsilon = 0.6
                self.board.epsilon -= (1/float(epochs))

            #update single game stats
            self.board.updateSinglePiecesPlaced(self.piecesPlaced)
            self.board.updateSingleGameLines(self.linesCleared_x1, self.linesCleared_x2, self.linesCleared_x3,
                                             self.linesCleared_x4)
            self.board.updateScore(self.score)
            #self.save_model(len(replay))


    def get_high_state(self, state, currentPiece, nextPiece):
        high_state = np.full(12,-1)
        if state is not None:
            high_state[0] = self.board.get_piece_index(currentPiece)
            high_state[1] = self.board.get_piece_index(nextPiece)
            min_height = 9
            for i in xrange(2,12):
                column = i - 2
                column_height = high_states._columnHeight(state, column)
                high_state[i] = column_height
                if column_height < min_height:
                    min_height = column_height
            for i in xrange(2,12):
                high_state[i] = high_state[i] - min_height
        return high_state

    def make_move(self, action):
        action_name = self.high_actions.get_action_name(action)
        print action_name
        current_piece_array = getattr(self.board, self.currentPiece)()
        #Call the action method with the name action_name that returns the best state for that action
        new_state = getattr(self.high_actions, action_name)(self.state, current_piece_array)
        return new_state

    def get_reward(self, state, column):
        if self.board.game_over(state):
            return self.GAME_OVER_REWARD
        lines_cleared = self.high_actions.number_of_lines_cleared(state)
        if lines_cleared > 0:
            self.boardLevel = high_states.max_height(state)
            self.burriedHoles = high_states.numberOfBurriedHoles(state)
            if lines_cleared == high_states.max_height(state): # board cleared
                return 20000
            else:
                score = [0,50,150,350,1200]
                return score[lines_cleared]
        else:
            new_board_level = high_states.max_height(state)
            new_burried_holes = high_states.numberOfBurriedHoles(state)
            burried_holes_diff = self.burriedHoles - new_burried_holes
            level_diff = self.boardLevel - new_board_level
            self.boardLevel = new_board_level
            self.burriedHoles = new_burried_holes
            if new_board_level < 5:
                if level_diff == 0 and burried_holes_diff == 0:
                    return 3
                elif level_diff == -1 and burried_holes_diff == 0:
                    return 1
                elif level_diff == -2 and burried_holes_diff == 0:
                    return 0.5
                elif level_diff < -2 and burried_holes_diff == 0:
                    return -0.5
                else:
                    return 0.5 * burried_holes_diff + 0.2 * level_diff
            else:
                if level_diff == 0 and burried_holes_diff == 0:
                    return 2
                elif level_diff == 0:
                    return 1
                else:
                    return level_diff + 0.4 * burried_holes_diff


    #modified the reward function so I had to use another method for the score, hence the duplicated code
    def get_score(self, state, column):
        if state is None:
            return 0
        lines_cleared = self.high_actions.number_of_lines_cleared(state)
        if lines_cleared > 0:
            if lines_cleared == high_states.max_height(state):
                return 2000
            else:
                score = [0,50,150,350,1200]
                return score[lines_cleared] * self.currentGame_level
        else:
            column_height = high_states._columnHeight(state,column)
            column_burried_holes = high_states._BurriedHolesColumn(state, column)
            height_reward = 0.2 * (10 - column_height) #negative if it's past half
            burried_holes_reward = -1 * column_burried_holes #negative if there are burried holes
            if column_burried_holes == 0:
                burried_holes_reward = 1 #positive if no burried holes
            burried_holes_reward *= 0.3
            non_terminal_state_reward = height_reward + burried_holes_reward + 0.5 * (self.currentGame_level^2)
            return max(0,non_terminal_state_reward)

    def updateSingleLinesCleared(self, state):
        linesCleared = self.high_actions.number_of_lines_cleared(state)
        if linesCleared == 1:
            self.linesCleared_x1 += 1
        elif linesCleared == 2:
            self.linesCleared_x2 += 1
        elif linesCleared == 3:
            self.linesCleared_x3 += 1
        elif linesCleared == 4:
            self.linesCleared_x4 += 1

        #increase game level every 10 lines cleared
        total_lines_cleared = self.linesCleared_x1 + self.linesCleared_x2 + self.linesCleared_x3 + self.linesCleared_x4
        if total_lines_cleared >= 10 * self.currentGame_level:
            self.currentGame_level += 1

    def save_model(self, piecesPlaced):
        if piecesPlaced > 49900:
            self.iterations += 1
            if self.iterations % 50 == 0:
                tetris_nn.NeuralNetwork.save_model(self.model)
