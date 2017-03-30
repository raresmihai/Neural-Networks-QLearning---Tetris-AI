import tetris_nn
import tetris_ai

def main():
    nn = tetris_nn.NeuralNetwork()

    #Load the model from combination23.save
    #Possible to work only on Windows. See methods save_model and load_model from tetris_nn.py
    #board.epsilon is 0 => test mode
    model = nn.load_model()


    #Uncomment this line to create a model from 0
    #Also you need to modify board.epsilon from 0 to 1 in board.py
    #model = nn.create_model()


    #Keys
    #Left arrow: decrement epsilon with 0.1
    #Right arrow: increment epsilon with 0.1
    #Down arrow: Slow speed
    #Up arrow: Increase speed
    #P : pause
    # 1,2,3,4,5,6 (when on pause) : Simulate high actions from high_actiony.py
    tetris_ai.TetrisAI(model)

main()