import random

def insert_commas(s):
    return ",".join(s)

string = "hello"
print(insert_commas(string))  # Output: h,e,l,l,o

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.001):
        self.Q = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_Q(self, state, action):
        return self.Q.get((state, action), random.random())   ## starts q values randomly between 0 and 1
    
    def t_Q(self, money):
        money = money + 1
        print("Money", money)
        return money

    def choose_action(self, state, available_actions):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(available_actions)
        else:    ### Selects the Maximum Q-value of all available actions
            q_values = [self.get_Q(state, action) for action in available_actions]
            print(" self.get_Q(state, action[0]) ", self.get_Q(state, available_actions[0]))
            print(" self.get_Q(state, action[1]) ", self.get_Q(state, available_actions[1]))
            print("state",state)
            # print("action",action)   ### If not initialised then randomly initialise 

            print("available_actions",available_actions)    ## Its doing available_actions correclty so far
            print("q_values",q_values)
            MaxQValueFromAllPossibleActionsInTheCurrentState = max(q_values)
            return available_actions[q_values.index(MaxQValueFromAllPossibleActionsInTheCurrentState)], MaxQValueFromAllPossibleActionsInTheCurrentState

    def learn(self, current_state, action, reward, MaxQValueFromAllPossibleActionsInTheCurrentState):
        print("####Time to Learn! ####")
        #max_q_next = max([self.get_Q(next_state, next_action) for next_action in available_actions_in_next_state])

        # Best possible Q-value from current moves
        #### Q-Table Here #####
        print("state",current_state)
        print(insert_commas(current_state))
        print("action",action)
        print("reward",reward)
        if reward > 0:
            print("reward",reward)
        print("MaxQValueFromAllPossibleActionsInTheCurrentState",MaxQValueFromAllPossibleActionsInTheCurrentState)
        print("Q-val before"), self.get_Q(current_state, action)

        self.Q[(current_state, action)] = self.get_Q(current_state, action) + \
                                  self.alpha * (reward + self.gamma * MaxQValueFromAllPossibleActionsInTheCurrentState - self.get_Q(current_state, action))

        print("state",current_state)
        print("action",action)
        print("Q-val after"), self.Q[(current_state, action)]
        print("VS CODE!")
        
class GridWorldGame:
    def __init__(self):
        # Initialize the 5x5 game board
        self.board = [[' ' for _ in range(5)] for _ in range(5)]
        # Set the starting positions of the players
        self.board[0][0] = 'X'
        self.board[4][4] = 'O'

        # Set the positions of the barriers
        for i in [0, 1, 3, 4]:  # Set barriers at C1, C2, C4, C5
            self.board[i][2] = '#'
        # Set the current player to 'X'
        self.current_player = 'X'
        # Define the winning rows for each player
        self.WinningColumnForX = 4
        self.WinningColumnForO = 0

        # Create a total move counter
        self.NumberofMovesInTheGameSoFar = -1

    def ResetThePeicesAtTheEndOfTheGame(self):  
        print("The Game Just Ended! Reset the board guys and girls!")      
        # Initialize the 5x5 game board
        self.board = [[' ' for _ in range(5)] for _ in range(5)]
        # Set the starting positions of the players
        self.board[0][0] = 'X'
        self.board[4][4] = 'O'

        # Set the positions of the barriers
        for i in [0, 1, 3, 4]:  # Set barriers at C1, C2, C4, C5
            self.board[i][2] = '#'

        # Set the current player to 'X'
        self.current_player = 'X'
        # Reset the move counter
        self.NumberofMovesInTheGameSoFar = -1
    
    def print_board(self):
        # print("  A B C D E")
        print("  0 1 2 3 4")
        for i in range(5):
            print(f"{i}", end=" ")
            for j in range(5):
                print(self.board[i][j], end=" ")
            print()

    def get_moves(self, row, col):
        moves = []
        opponent = 'O' if self.current_player == 'X' else 'X'
        opponent_row, opponent_col = None, None
        
        # Locate the opponent's position
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == opponent:
                    opponent_row, opponent_col = i, j
                    print("opponent_row",opponent_row,"opponent_col",opponent_col)
                    break

        # Check if players are horizontally adjacent
        horizontally_adjacent = opponent_row == row and abs(opponent_col - col) == 1

        for i in range(-1, 2):
            for j in range(-1, 2):
                new_row, new_col = row + i, col + j
                
                # Skip if it's the current position
                if new_row == row and new_col == col:
                    continue

                # Conditions to add the move
                if 0 <= new_row < 5 and 0 <= new_col < 5 and self.board[new_row][new_col] == ' ':
                    # Block moves based on horizontal adjacency
                    if horizontally_adjacent:
                        if self.current_player == 'X' and new_col > col:  # If 'X' is to move right
                            continue
                        if self.current_player == 'O' and new_col < col:  # If 'O' is to move left
                            continue
                    # Block forward diagonal moves when blocked by the opponent
                    if self.current_player == 'X' and new_row > row and self.board[row][new_col] == opponent:
                        continue
                    if self.current_player == 'O' and new_row < row and self.board[row][new_col] == opponent:
                        continue

                    moves.append((new_row, new_col))

                    # print("legal moves",moves)
                    
        return moves
    
    def Is_Draw(self):     ## Declare a draw if the game has gone on too long, this is a shortcut for 3 fold repition for now - could make it one fold ...
        # print(" A B C D E")
        print("NumberofMovesInTheGameSoFar = ", self.NumberofMovesInTheGameSoFar)
        if self.NumberofMovesInTheGameSoFar > 16:
            print("We Declare this game a draw!")
            self.ResetThePeicesAtTheEndOfTheGame()
            self.NumberofMovesInTheGameSoFar = -1
            return 0  # return reward for draw
            # exit() 
            

    def play(self, q_agent=None, training=True):   
        while True:
            self.NumberofMovesInTheGameSoFar += 1
            self.Is_Draw()
            self.print_board()
            print(f"{self.current_player}'s turn")
            row, col = None, None
            for i in range(5):
                for j in range(5):
                    if self.board[i][j] == self.current_player:
                        row, col = i, j
                        break
            moves = self.get_moves(row, col)
            
            if not moves:
                print(f"{self.current_player} has no valid moves. The game is a draw!")
                self.NumberofMovesInTheGameSoFar = -1
                reward = 0
                return 0  # return reward for draw

            else:  # O's random moves or manual gameplay
                if training:
                    action = random.choice(moves)
                    print("O's random move",action)
                    print("O's random move",action)
                else:
                    move_str = input("Enter your move (e.g. 0,3): ")
                    action = (int(move_str[0]), int(move_str[2]))

            if action not in moves:
                print("Invalid move!")
                continue

            # Execute action
            self.board[row][col] = ' '
            self.board[action[0]][action[1]] = self.current_player

            # Check for game over conditions
            reward = 0  ## By Defaut
            if self.current_player == 'X' and action[1] == self.WinningColumnForX:
                print("X is the winner!!")
                self.ResetThePeicesAtTheEndOfTheGame()
                self.NumberofMovesInTheGameSoFar = -1
                reward = 10
                # return 1  # return reward for X's win
            elif self.current_player == 'O' and action[1] == self.WinningColumnForO:
                print("O is the winner!!")
                #ResetThePeicesAtTheEndOfTheGame(self): 
                self.NumberofMovesInTheGameSoFar = -1
                self.ResetThePeicesAtTheEndOfTheGame()
                print("hi")
                reward = -10
                # return -1  # return reward for O's win

            if self.current_player == 'X':  # if it's X's turn and there's a Q agent
                current_state = ''.join([''.join(row) for row in self.board]) + 'X'
                action, MaxQValueFromAllPossibleActionsInTheCurrentState  = q_agent.choose_action(current_state, moves)   ## Select the maximum Q-value from available moves - and move state
                print("MaxQValueFromAllPossibleActionsInTheCurrentState = ",MaxQValueFromAllPossibleActionsInTheCurrentState) 
                print("current_state",current_state) 
                print("X's non-random move",action) 
                print("Reward = ",reward) 
                if reward > 0:
                    print("Reward = ",reward) 
                # reward = 0.1 
                q_agent.t_Q(55)
                q_agent.learn(current_state, action, reward, MaxQValueFromAllPossibleActionsInTheCurrentState)

            self.current_player = 'O' if self.current_player == 'X' else 'X'

print("HEREEEEEEE")

if __name__ == "__main__":
    agent = QLearningAgent()
    game = GridWorldGame()
    num_episodes = 1
    for episode in range(num_episodes):
        print("#######  Episode = ", episode )
        reward = game.play(q_agent=agent, training=True) ## Create a q_agent instance of the q learning class, training = true is an alternative to manual play
        if episode % 100 == 0:
            game.print_board()