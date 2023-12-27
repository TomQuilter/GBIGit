import random
import itertools
import csv

random.seed(41)  

def insert_commas(s):
    return ",".join(s)

string = "hello"
print(insert_commas(string))  # Output: h,e,l,l,o
 
class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9
                 , epsilon=0.2, TotalNumberOfGamesToPlay=20):
        self.Q = {}     ## Initiate Q table 
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.TotalNumberOfGamesToPlay = TotalNumberOfGamesToPlay
        self.OptimalTrajectory = []     ## Initiate OptimalTrajectory

    def get_Q(self, state, action):

        print("action = ", action)
        print("state = ", state)
        # print("self.Q[(state, action)] = ", self.Q[(state, action)])

        if (state, action) in self.Q:
            print("self.Q[(state, action)]", self.Q[(state, action)])
        else:
            self.Q[(state, action)] = random.uniform(0, 1)         
            print("No self.Q[(state, action)]")
            print("self.Q[(state, action)] = ", self.Q[(state, action)])

            # print("self.Q", self.Q)


        #print("self.Q[(state, action)] = ", self.Q[(state, action)])
        # if hasattr(self.Q[(state, action)]):
        1==1
        #p# print("action = ", action)
        #p# print("state = ", state)
        #p# print("self.Q[(state, action)] = ", self.Q[(state, action)])

        2==2
        
        return self.Q[(state, action)]   ## starts q values randomly between 0 and 1
    
    def t_Q(self, money):
        money = money + 1
        #p# print("Money", money)
        return money

    def choose_action(self, state, available_actions, NumberOfGamesPlayedSoFar):
        print("#### CHOOSE ACTION ####")
        RandomNumber = random.uniform(0, 1)
        ExplorationThreshold = self.epsilon*pow(0.995, NumberOfGamesPlayedSoFar)
        ExplorationThreshold = self.epsilon*pow(0.995, NumberOfGamesPlayedSoFar)
        onelessthanthetotalnumberofgames = agent.TotalNumberOfGamesToPlay - 1
        if NumberOfGamesPlayedSoFar >= onelessthanthetotalnumberofgames :
            ExplorationThreshold = 0   ## If its the penultimalte final game then play the optimal strategy with Zero exploration
        print("/// Epsilon =", ExplorationThreshold , " ///")
        if RandomNumber < ExplorationThreshold:
            print(RandomNumber,ExplorationThreshold,"###Randomly Explore!##", NumberOfGamesPlayedSoFar)
            #q_values = [random.uniform(0, 1) for action in available_actions]
            return random.choice(available_actions), 1
        else:    ### Selects the Maximum Q-value of all available actions
            q_values = [self.get_Q(state, action) for action in available_actions]
            #p# print("(4) self.get_Q(state, action[0]) ", self.get_Q(state, available_actions[0]))
            #p# print("(5) self.get_Q(state, action[1]) ", self.get_Q(state, available_actions[1]))
            #p# print("state",state)
            # print("action",action)   ### If not initialised then randomly initialise 

            #p# print("available_actions",available_actions)    ## Its doing available_actions correclty so far
            #p# print("q_values",q_values)
            MaxQValueFromAllPossibleActionsInTheCurrentState = max(q_values)
            return available_actions[q_values.index(MaxQValueFromAllPossibleActionsInTheCurrentState)], MaxQValueFromAllPossibleActionsInTheCurrentState

    def learn(self, PreviousState , current_state, action, reward, MaxQValueFromAllPossibleActionsInTheNEWState):
        print("####Time to Learn! ####")
        #max_q_next = max([self.get_Q(next_state, next_action) for next_action in available_actions_in_next_state])

        # Best possible Q-value from current moves
        #### Q-Table Here #####
        #p# print("state",current_state)
        #p# print(insert_commas(current_state))
        #p# print("action",action)
        print("PreviousState",PreviousState)
        print("Current state",current_state)
        print("action",action)
        print("reward",reward)
        print("MaxQValueFromAllPossibleActionsInTheNEWState",MaxQValueFromAllPossibleActionsInTheNEWState)
        print("self.gamma",self.gamma)
        print("self.alpha",self.alpha)

        if reward > 0:
            print("reward",reward)
            self.get_Q(PreviousState, action)

        if action == (1,3):
            print("stop",reward)
     
        #p# print("MaxQValueFromAllPossibleActionsInTheCurrentState",MaxQValueFromAllPossibleActionsInTheCurrentState)
        print("Q-val before", self.get_Q(PreviousState, action))

        self.Q[(PreviousState, action)] = self.get_Q(PreviousState, action) + \
                                  self.alpha * (reward + self.gamma * MaxQValueFromAllPossibleActionsInTheNEWState - self.get_Q(PreviousState, action))
        
        # print("self.Q",self.Q)
        print("Q-val after", self.Q[(PreviousState, action)])
        print("####Learnt! ####")
        #p#  print("VS CODE!")
        
class GridWorldGame:
    def __init__(self, BarrierPositions):
        
        #self.instance_variable = BarrierPositions
        self.BarrierPositions = BarrierPositions
        print("Value =", BarrierPositions)

        self.NumberOfRows = 4
        self.NumberOfCols = 4
        # Initialize the 5x5 game board
        self.board = [[' ' for _ in range(self.NumberOfCols)] for _ in range(self.NumberOfRows)]

        self.add_BarrierPositions(BarrierPositions)

        #self.BarrierPositions()

        # Set the starting positions of the players
        self.board[0][0] = 'X' 
        agent.OptimalTrajectory.append((0,0))
        # self.board[self.NumberOfRows-1][self.NumberOfCols-1] = 'O'   ## Always start in the bottom right corner for now
 
        self.NumberofGamesPlayedSoFar = 1
        self.NumberofXVictoriesInTheGameSoFar = 0
        self.NumberofOVictoriesInTheGameSoFar = 0
        self.NumberofDrawsInTheGameSoFar = 0

        # Set the current player to 'X'
        self.current_player = 'X'
        # Define the winning rows for each player
        self.WinningColumnForX = self.NumberOfCols-1
        self.WinningColumnForO = 0
 
        self.current_state = ''.join([''.join(row) for row in self.board])
        print("## Current State at the start of the game = ", self.current_state)

        # Create a total move counter
        self.TheTotalNumberOfMovesPlayedSoFar = 0
        self.NumberofMovesInTheGameSoFar = -1
        self.counter = 0

    def add_BarrierPositions(self, BarrierPositions):
        for i in range(0, len(BarrierPositions), 2):
            row = BarrierPositions[i]
            col = BarrierPositions[i+1]
            # Check if the row and col are within the bounds of the board
            if 0 <= row < self.NumberOfRows and 0 <= col < self.NumberOfCols:
                self.board[row][col] = '#'
            else:
                print(f"Warning: BarrierPositions ({row}, {col}) is out of bounds.")

#    def BarrierPositions(self):
#        # Set the positions of the barriers
#        for i in [1]:  # Set barriers at C1, C2, C4, C5  [0, 1, 3, 4]
#            self.board[i][3] = '#'
#            # self.board[i][2] = '#'

    def ResetThePeicesAtTheEndOfTheGame(self):  
        print("The Game Just Ended! Reset the board guys and girls!")
        
        self.print_board()        
        
        if self.NumberofGamesPlayedSoFar > (agent.TotalNumberOfGamesToPlay - 9): 
            self.counter += 1
            self.TheTotalNumberOfMovesPlayedSoFar += self.NumberofMovesInTheGameSoFar 
            self.MeanNumberOfMovesPerGame = self.TheTotalNumberOfMovesPlayedSoFar/9
            print("self.counter",self.counter)
            print("MeanNumberOfMovesPerGameinthlast9games = ", self.MeanNumberOfMovesPerGame)
            
        self.NumberofMovesInTheGameSoFar = -1        
        self.NumberofGamesPlayedSoFar += 1 
        # Player X always starts
        self.current_player = 'X'
        print("##### GAME NUMBER", self.NumberofGamesPlayedSoFar)
        # Initialize the 5x5 game board
        self.board = [[' ' for _ in range(self.NumberOfCols)] for _ in range(self.NumberOfRows)]
        # Set the starting positions of the players
        self.board[0][0] = 'X'
        # self.board[self.NumberOfRows-1][self.NumberOfCols-1] = 'O'
        # Set the positions of the barriers
        self.add_BarrierPositions(self.BarrierPositions)
        self.current_state = ''.join([''.join(row) for row in self.board])
        print("## Current State after a reset of they game = ", self.current_state)
        print("f", self.NumberofGamesPlayedSoFar)           

        print("NumberofXVictoriesInTheGameSoFar",self.NumberofXVictoriesInTheGameSoFar)
        print("NumberofOVictoriesInTheGameSoFar",self.NumberofOVictoriesInTheGameSoFar)
        print("NumberofDrawsInTheGameSoFar",self.NumberofDrawsInTheGameSoFar)

        if self.NumberofGamesPlayedSoFar == agent.TotalNumberOfGamesToPlay:
            ##### Q-Table #####
            for key, value in agent.Q.items():
                agent.Q[key] = round(value, 2)
                print(key, agent.Q[key] )

        # print(agent.Q)

        # Reset the move counter
        self.NumberofMovesInTheGameSoFar = -1

    def print_numbers(self,n):
    # Create a string with numbers from 0 to n-1, separated by spaces
        number_string = "  "
        number_string = number_string + " ".join(str(i) for i in range(n))
        print(number_string)
    
    def print_board(self):
        self.print_numbers((self.NumberOfCols))
        # print("  0 1 2 3")
        for i in range(self.NumberOfRows):
            print(f"{i}", end=" ")
            for j in range(self.NumberOfCols):
                print(self.board[i][j], end=" ")
            print()

    def get_moves(self, row, col):
        moves = []
        opponent = 'X' if self.current_player == 'X' else 'X'
        opponent_row, opponent_col = None, None
        
        # Locate the opponent's position
        for i in range(self.NumberOfRows):
            for j in range(self.NumberOfCols):
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
                if 0 <= new_row < self.NumberOfRows and 0 <= new_col < self.NumberOfCols and self.board[new_row][new_col] == ' ':
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
            self.NumberofDrawsInTheGameSoFar += 1
            self.ResetThePeicesAtTheEndOfTheGame()
            self.NumberofMovesInTheGameSoFar = -1
    
    def pair_coordinates(self,coord_tuple):
    # Use list comprehension to create pairs
        return tuple((coord_tuple[i], coord_tuple[i + 1]) for i in range(0, len(coord_tuple), 2))

   
    def play(self, q_agent=None, training=True):   
        while self.NumberofGamesPlayedSoFar < agent.TotalNumberOfGamesToPlay:
            print("NumberofGamesPlayedSoFar = ",self.NumberofGamesPlayedSoFar)
            self.NumberofMovesInTheGameSoFar += 1
            print("self.NumberofMovesInTheGameSoFar = ",self.NumberofMovesInTheGameSoFar)
            self.Is_Draw()
            self.print_board()
            print(f"{self.current_player}'s turn")
            row, col = None, None
            for i in range(self.NumberOfRows):
                for j in range(self.NumberOfCols):
                    if self.board[i][j] == self.current_player:
                        row, col = i, j
                        break
            moves = self.get_moves(row, col)
            
            if not moves:
                print(f"{self.current_player} has no valid moves. The game is a draw!")
                self.ResetThePeicesAtTheEndOfTheGame()
                reward = 0

            else:  # O's random moves or manual gameplay
                if self.current_player == 'X':  # if it's X's turn and there's a Q agent
                        action, MaxQValueFromAllPossibleActionsInTheCurrentState  = q_agent.choose_action(self.current_state, moves, self.NumberofGamesPlayedSoFar)   
                        ## Select the maximum Q-value from available moves from the current state - and move to to that new state
                        print("MaxQValueFromAllPossibleActionsInTheCurrentState = ",MaxQValueFromAllPossibleActionsInTheCurrentState) # Max value From your CURRENT state 
                        # should then update the value of the state, action just taken based on how good it is in the NEW state 
                        # ... the value of your best move from your NEW state
                        ## Need a MaxQValueFromAllPossibleActionsInThe**NEW**State
                        print("current_state",self.current_state) 
                        print("X's NON-random move",action) 
                        reward = -10  ## To create quick optimal trajectories for X
           
                if self.current_player == 'O':
                    if training:
                        action = random.choice(moves)
                        print("O's random move",action)
                    else:
                        move_str = input("Enter your move (e.g. 0,3): ")
                        action = (int(move_str[0]), int(move_str[2]))

            if action not in moves:
                print("Invalid move!")
                continue

            #if self.NumberofMovesInTheGameSoFar == 0 and self.NumberofGamesPlayedSoFar == 1:   ### OVERIDE FOR DEBUGGING
            #    action = (1,4)
            #    print("action = ", action)

            if self.current_player == 'O':  ### OVERIDE FOR DEBUGGING
                action = (self.NumberOfRows-1,self.NumberOfRows-1)
                print("0's OVERIDE action = ", action)

            ###### Execute action AND update the NEW *State* and board ########
            self.PreviousState = self.current_state
            print("PreviousState = ", self.PreviousState)

            self.board[row][col] = ' '
            self.board[action[0]][action[1]] = self.current_player    ### Set the NEW co-ordinates of player X or player Y

            self.current_state = ''.join([''.join(row) for row in self.board])
            print("NEW STATE  = ", self.current_state)

            ## Obtain the best value from the NEW state
            newrow, newcol = None, None
            for i in range(self.NumberOfRows):
                for j in range(self.NumberOfCols):
                    if self.board[i][j] == self.current_player:
                        newrow, newcol = i, j
                        break
            movesInNewPosition = self.get_moves(newrow, newcol)
            Newaction, MaxQValueFromAllPossibleActionsInTheNEWState  = q_agent.choose_action(self.current_state, movesInNewPosition, self.NumberofGamesPlayedSoFar)

            print("MaxQValueFromAllPossibleActionsInTheNEWState = ",MaxQValueFromAllPossibleActionsInTheNEWState) # Max value From your CURRENT state 

            ###########################

            # Check for game over conditions and learn and then reset
            # reward = 0  ## By Defaut
            if self.current_player == 'X' and action[1] == self.WinningColumnForX:
                reward = 100               
                print("X is the winner!!")
                q_agent.learn(self.PreviousState , self.current_state, action, reward, MaxQValueFromAllPossibleActionsInTheNEWState) 
                self.ResetThePeicesAtTheEndOfTheGame()
                self.NumberofXVictoriesInTheGameSoFar += 1
                ## If last game record the move TotalNumberOfGamesToPlay
                if self.NumberofGamesPlayedSoFar == agent.TotalNumberOfGamesToPlay:
                    agent.OptimalTrajectory.append(action)
 
                # return 1  # return reward for X's win
            elif self.current_player == 'O' and action[1] == self.WinningColumnForO:
                reward = -100   
                print("O is the winner!!")
                q_agent.learn(self.PreviousState , self.current_state, action, reward, MaxQValueFromAllPossibleActionsInTheNEWState) 
                #ResetThePeicesAtTheEndOfTheGame(self): 
                self.NumberofOVictoriesInTheGameSoFar += 1
                self.ResetThePeicesAtTheEndOfTheGame()
                # return -1  # return reward for O's win

                ######   LEARN !! ######
            if self.current_player == 'X'and action[1] != self.WinningColumnForX:  # if it's X's turn and hasnt won then LEARN
                print("X's non-random move",action) 
                ## If last game record the move TotalNumberOfGamesToPlay
                onelessthanthetotalnumberofgames = agent.TotalNumberOfGamesToPlay - 1
                if self.NumberofGamesPlayedSoFar == onelessthanthetotalnumberofgames:
                    agent.OptimalTrajectory.append(action)

                print("Reward = ",reward) 
                q_agent.learn(self.PreviousState , self.current_state, action, reward, MaxQValueFromAllPossibleActionsInTheNEWState) 

            if self.NumberofMovesInTheGameSoFar != -1:  ## Unless we are starting a new game in which X should always start
                self.current_player = 'X' if self.current_player == 'X' else 'X'
            else:
                self.current_player = 'X'

            if agent.TotalNumberOfGamesToPlay == self.NumberofGamesPlayedSoFar:
               print("#######STOP!!! OptimalTrajectory = ##########")
               BarrierPositionCoords = self.pair_coordinates(self.BarrierPositions)
               print(BarrierPositionCoords)
               print(agent.OptimalTrajectory)
               randomnumb = random.randint(1, 10000)   ## 'combinations'+str(randomnumb)+'.csv'
               with open('combinations5.csv', 'a', newline='') as file:
                    writer = csv.writer(file) 
                    combination_str = '(' + ', '.join(map(str, BarrierPositionCoords)) + ')'
                    writer.writerow([BarrierPositionCoords,agent.OptimalTrajectory])


##### Generate Barriers ######

# Initialize an empty set to store the unique coordinate combinations
unique_coordinate_combinations = set()

# Create a list of all possible single coordinates in a 5x5 grid, excluding (0, 0)
single_coordinates = [(i, j) for i in range(3) for j in range(3) if (i, j) != (0, 0)]
print("single_coordinates",single_coordinates)
print("Length",len(single_coordinates))
# Generate combinations of increasing length
for r in range(1, 3):  # This will generate combinations of lengths 1 to to last number, 3 gives max combo (2, 1, 2, 2)
    # itertools.combinations will create all **unique** combinations of the coordinates with length r
    for combination in itertools.combinations(single_coordinates, r):
        # Flatten the combination and add to the set
        flattened_combination = tuple(coord for pair in combination for coord in pair)
        unique_coordinate_combinations.add(flattened_combination)

# Convert the set to a list and sort it for display purposes
sorted_combinations = sorted(unique_coordinate_combinations, key=lambda x: (len(x), x))

# Now, sorted_combinations contains all unique combinations of coordinates without repeats and excluding (0, 0)
# Display some of the combinations
for combination in sorted_combinations:  # Print all combinations
    print(combination)

number_of_combinations = len(sorted_combinations)

# Display the count
print(f"The number of unique coordinate combinations excluding (0, 0) is: {number_of_combinations}")

#for combination in sorted_combinations:
#    print("combination", combination)
#    for i in range(0, len(combination), 2):
#        row = combination[i]
#        col = combination[i+1]
#        print("row", row)
#        print("col", col)

###### Train RL agent for each Barrier Position ######
print("sorted_combinations", sorted_combinations)

# sorted_combinations = [(1,2,2,0)]
# print("sorted_combinations", sorted_combinations)

if __name__ == "__main__":
        NumberOfDifferentGamesWithDifferentBarriersToPlay = 5
        ## For each 
        # for episode in range(NumberOfDifferentGamesWithDifferentBarriersToPlay):
        for combination in sorted_combinations:
            agent = QLearningAgent()   ## Create an instance of a Q-Learning Agent
            # BoardPositionForThisGame = (1,2,4,0)
            BoardPositionForThisGame = (combination)
            game = GridWorldGame(BoardPositionForThisGame)     ## Create an instance of a GridWorldGame
            print("#######  Episodee = ", combination )
            game.play(q_agent=agent, training=True) ## Create a q_agent instance of the q learning class, training = true is an alternative to manual play  reward = 
