import colors
import high_actions as action

actions = action.HighActions()

def getMatrix(file='matrix.txt'):
    color = colors.Colors()
    newState = [[[1, color.GREY] for i in xrange(0, 10)] for j in xrange(0, 20)]
    i=0
    j=0
    try:
        with open(file) as f:
            while True:
                c = f.read(1)
                if not c:
                    break
                if j == 10:
                    j = 0
                    i += 1
                else:
                    if c.upper() == 'X':
                        newState[i][j][0]=0
                    j += 1
        return newState
    except Exception:
        return