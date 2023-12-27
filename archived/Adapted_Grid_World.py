import numpy as np

ROWS = 5
COLS = 5
S = (4, 0)
G = (4, 4)

class Cliff:

    def __init__(self):
        self.end = False
        self.pos = S
        self.board = np.zeros([5, 5])
        # add cliff marked as -1 at C1, C2, and C3
        self.board[2, 1:4] = -1

    def nxtPosition(self, action):
        if action == "up":
            nxtPos = (self.pos[0] - 1, self.pos[1])
        elif action == "down":
            nxtPos = (self.pos[0] + 1, self.pos[1])
        elif action == "left":
            nxtPos = (self.pos[0], self.pos[1] - 1)
        else:
            nxtPos = (self.pos[0], self.pos[1] + 1)
        # check legitimacy
        if nxtPos[0] >= 0 and nxtPos[0] <= 4:
            if nxtPos[1] >= 0 and nxtPos[1] <= 4:
                # Check if the next position is on the cliff
                if self.board[nxtPos] != -1:
                    self.pos = nxtPos

        if self.pos == G:
            self.end = True
            print("Game ends reaching goal")

        return self.pos

    def giveReward(self):
        # give reward
        if self.pos == G:
            return -1
        if self.board[self.pos] == 0:
            return -1
        return -100

    def show(self):
        for i in range(0, ROWS):
            print('---------------------------------')
            out = '| '
            for j in range(0, COLS):
                token = '0'
                if self.board[i, j] == -1:
                    token = '*'
                if (i, j) == self.pos:
                    token = 'S'
                if (i, j) == G:
                    token = 'G'
                out += token + ' | '
            print(out)
        print('---------------------------------')

# ... [rest of the Agent class and other functions remain unchanged]

if __name__ == "__main__":
    print("sarsa training ... ")
    ag = Agent(exp_rate=0.1, sarsa=True)
    
    # Initial journey
    print("Initial journey:")
    ag.play(rounds=1)
    showRoute(ag.states)

    # Middle journey
    print("Middle journey after 250 rounds:")
    ag.play(rounds=249)
    ag_op = Agent(exp_rate=0)
    ag_op.state_actions = ag.state_actions
    states = []
    while 1:
        curr_state = ag_op.pos
        action = ag_op.chooseAction()
        states.append(curr_state)
        print("current position {} |action {}".format(curr_state, action))
        ag_op.cliff.pos = ag_op.cliff.nxtPosition(action)
        ag_op.pos = ag_op.cliff.pos
        if ag_op.cliff.end:
            break
    showRoute(states)

    # Final journey
    print("Final journey after 500 rounds:")
    ag.play(rounds=250)
    ag_op = Agent(exp_rate=0)
    ag_op.state_actions = ag.state_actions
    states = []
    while 1:
        curr_state = ag_op.pos
        action = ag_op.chooseAction()
        states.append(curr_state)
        print("current position {} |action {}".format(curr_state, action))
        ag_op.cliff.pos = ag_op.cliff.nxtPosition(action)
        ag_op.pos = ag_op.cliff.pos
        if ag_op.cliff.end:
            break
    showRoute(states)
