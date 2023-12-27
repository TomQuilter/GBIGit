import random
import itertools
import csv
import math
random.seed(9)  ##41
import math

def insert_commas(s):
    return ",".join(s)

string = "hello"
print(insert_commas(string))  # Output: h,e,l,l,o

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9
                 , epsilon=0.8, TotalNumberOfGamesToPlay=100):
        self.Q = {}     ## Initiate Q table 
        self.alpha = alpha 
        self.gamma = gamma 
        self.epsilon = epsilon
        self.TotalNumberOfGamesToPlay = TotalNumberOfGamesToPlay
        self.OptimalTrajectory = []     ## Initiate OptimalTrajectory

    def get_Q(self, state, action):

       #r#print("action = ", action)
       #r#print("state = ", state)
        # print("self.Q[(state, action)] = ", self.Q[(state, action)])

        ## IF State doesnt exist give it a random number, else do nothing###

        if (state, action) in self.Q:
          1==1
          #print("self.Q[(state, action)]", self.Q[(state, action)])
        else:
            self.Q[(state, action)] = 0 # random.uniform(4, 5)      ### Initialise with Random numbers - could be zero's     
          #r#print("No self.Q[(state, action)]")
          #r#print("self.Q[(state, action)] = ", self.Q[(state, action)])

            # print("self.Q", self.Q)


        #print("self.Q[(state, action)] = ", self.Q[(state, action)])
        # if hasattr(self.Q[(state, action)]):
        #p# print("action = ", action)
        #p# print("state = ", state)
        #p# print("self.Q[(state, action)] = ", self.Q[(state, action)])
        
        return self.Q[(state, action)]   ## starts q values randomly between 0 and 1

    def choose_action(self, state, available_actions, NumberOfGamesPlayedSoFar):
        print("#### CHOOSE ACTION ####")
        
        print("self.current_player",game.current_player)

        ExplorationProb = round(math.exp(math.log(0.01/self.epsilon) / self.TotalNumberOfGamesToPlay),2)  ## Set the final Exploration to be 0.01
        RandomNumber = random.uniform(0, 1)
        ExplorationThreshold = self.epsilon*pow(ExplorationProb, NumberOfGamesPlayedSoFar)  ##  300 and 0.985  ## 5000 and 0.9999 ## 1000 and 0.995
        onelessthanthetotalnumberofgames = agent.TotalNumberOfGamesToPlay - 1
        if NumberOfGamesPlayedSoFar >= onelessthanthetotalnumberofgames :
            ExplorationThreshold = 0   ## If its the penultimalte final game then play the optimal strategy with Zero exploration
      #r#print("/// Epsilon =", ExplorationThreshold , " ///")
        if RandomNumber < ExplorationThreshold:
          #r#print(RandomNumber,ExplorationThreshold,"###Randomly Explore!##", NumberOfGamesPlayedSoFar)
            #q_values = [random.uniform(0, 1) for action in available_actions]
            
            print("available actions for random play for ",available_actions)
            return random.choice(available_actions), 1
        else:    ### Selects the Maximum Q-value of all available actions
            
            print("available actions for max q value for", available_actions)

            #Creates Q values for all possible actions or finds current ones
            q_values = [self.get_Q(state, action) for action in available_actions]  
            ## Explains why some "winning moves are 0, they have not actually been played"
             
            #p# print("(4) self.get_Q(state, action[0]) ", self.get_Q(state, available_actions[0]))
            #p# print("(5) self.get_Q(state, action[1]) ", self.get_Q(state, available_actions[1]))
            #p# print("state",state)
            # print("action",action)   ### If not initialised then randomly initialise 

            #p# print("available_actions",available_actions)    ## Its doing available_actions correclty so far
            #p# print("q_values",q_values)
            MaxQValueFromAllPossibleActionsInTheCurrentState = max(q_values)
            return available_actions[q_values.index(MaxQValueFromAllPossibleActionsInTheCurrentState)], MaxQValueFromAllPossibleActionsInTheCurrentState

    def learn(self, PreviousState , current_state, action, reward, MaxQValueFromAllPossibleActionsInTheNEWState):
      #r#print("####Time to Learn! ####")
        #max_q_next = max([self.get_Q(next_state, next_action) for next_action in available_actions_in_next_state])
        if PreviousState == '  #   #O   X    ':   #    '|  # |  #O|  X |    |'                                                  
            1==1
                                                  #    '|  # |  #O|   X|    |'            
        # Best possible Q-value from current moves
        #### Q-Table Here #####
        #p# print("state",current_state)
        #p# print(insert_commas(current_state))
        #p# print("action",action)
      #r#print("PreviousState",PreviousState)
        print("Current state",current_state)
      #r#print("action",action)
      #r#print("reward",reward)
      #r#print("MaxQValueFromAllPossibleActionsInTheNEWState",MaxQValueFromAllPossibleActionsInTheNEWState)
      #r#print("self.gamma",self.gamma)
      #r#print("self.alpha",self.alpha)

        #if reward > 0:
        if MaxQValueFromAllPossibleActionsInTheNEWState > 3:
            1==1           
          #r#print("reward",reward)
            self.get_Q(PreviousState, action)     ##   Initiate Q values as wont have happened before when not winning
    
        #p# print("MaxQValueFromAllPossibleActionsInTheCurrentState",MaxQValueFromAllPossibleActionsInTheCurrentState)
        print("Q-val before", self.get_Q(PreviousState, action))

        ## Update based on the Different between Max Q-Value in NEW state and what u got in the last state + REWARD

        self.Q[(PreviousState, action)] = self.get_Q(PreviousState, action) + \
                                  self.alpha * (reward + self.gamma * MaxQValueFromAllPossibleActionsInTheNEWState - self.get_Q(PreviousState, action))
        
        # print("self.Q",self.Q)
        print("Q-val after", self.Q[(PreviousState, action)])
      #r#print("####Learnt! ####")
        #p##r#print("VS CODE!")
        
class GridWorldGame:
    def __init__(self, BarrierPositions):
        
        #self.instance_variable = BarrierPositions
        self.BarrierPositions = BarrierPositions
      #r#print("Value =", BarrierPositions)

        self.NumberOfRows = 4
        self.NumberOfCols = 4
        # Initialize the 5x5 game board
        self.board = [[' ' for _ in range(self.NumberOfCols)] for _ in range(self.NumberOfRows)]

        self.add_BarrierPositions(BarrierPositions)

        #self.BarrierPositions()

        # Set the starting positions of the players
        self.board[0][0] = 'X' 
        agent.OptimalTrajectory.append((0,0))
        self.board[self.NumberOfRows-1][self.NumberOfCols-1] = 'O'   ## Always start in the bottom right corner for now
 
        self.NumberofGamesPlayedSoFar = 1
        self.NumberofXVictoriesInTheGameSoFar = 0
        self.NumberofOVictoriesInTheGameSoFar = 0
        self.NumberofDrawsInTheGameSoFar = 0

        # Set the current player to 'X'
        self.current_player = 'X'
        # Define the winning rows for each player
        # self.WinningColumnForX = self.NumberOfCols-1
        self.WinningColumnForX = 3
        #self.WinningRowForX = 0
        self.WinningColumnForO = 0
        #self.WinningRowForO = 0
 
        self.current_state = ''.join([''.join(row) for row in self.board])
      #r#print("## Current State at the start of the game = ", self.current_state)

        # Create a total move counter
        self.TheTotalNumberOfMovesPlayedSoFar = 0
        self.NumberofMovesInTheGameSoFar = -1    ## Initially before the game has begun
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
        print("Final Position of Last Game")
        self.print_board()        
        
        if self.NumberofGamesPlayedSoFar > (agent.TotalNumberOfGamesToPlay - 9): 
            self.counter += 1
            self.TheTotalNumberOfMovesPlayedSoFar += self.NumberofMovesInTheGameSoFar 
            self.MeanNumberOfMovesPerGame = self.TheTotalNumberOfMovesPlayedSoFar/9
          #r#print("self.counter",self.counter)
          #r#print("MeanNumberOfMovesPerGameinthlast9games = ", self.MeanNumberOfMovesPerGame)
            
        self.NumberofMovesInTheGameSoFar = -1    ### Reset the numberofMovesPlayedina game to 0    
        self.NumberofGamesPlayedSoFar += 1 
        # Player X always starts
        self.current_player = 'X'
        print("##### GAME NUMBER", self.NumberofGamesPlayedSoFar)
        if(self.NumberofGamesPlayedSoFar == 599):
            1==1
        # Initialize the 5x5 game board
        self.board = [[' ' for _ in range(self.NumberOfCols)] for _ in range(self.NumberOfRows)]
        # Set the starting positions of the players
        self.board[0][0] = 'X'
        self.board[self.NumberOfRows-1][self.NumberOfCols-1] = 'O'
        # Set the positions of the barriers
        self.add_BarrierPositions(self.BarrierPositions)
        self.current_state = ''.join([''.join(row) for row in self.board])
      #r#print("## Current State after a reset of they game = ", self.current_state)
      #r#print("f", self.NumberofGamesPlayedSoFar)           

        print("NumberofXVictoriesInTheGameSoFar",self.NumberofXVictoriesInTheGameSoFar)
        print("NumberofOVictoriesInTheGameSoFar",self.NumberofOVictoriesInTheGameSoFar)
        print("NumberofDrawsInTheGameSoFar",self.NumberofDrawsInTheGameSoFar)



        if self.NumberofGamesPlayedSoFar == agent.TotalNumberOfGamesToPlay:
            print("##### Q-Table #####")
            for key, value in agent.Q.items():
                agent.Q[key] = round(value, 2)
                #print(key, agent.Q[key] )
            print("##### Ordered Q-Table #####")
            q_items = [(key, round(value, 2)) for key, value in agent.Q.items()]
            # Sort the list of tuples by the second item in each tuple (the Q-value)
            q_items_sorted = sorted(q_items, key=lambda x: x[1], reverse=True)  # Use reverse=False to sort in ascending order
            # Print the sorted Q-table
            print("##### Q-Table #####")
            for key, value in q_items_sorted:
                print(key, value)

        # print(agent.Q)

        # Reset the move counter
        #28Nov2023 self.NumberofMovesInTheGameSoFar = -1
 
    def print_numbers(self,n):
    # Create a string with numbers from 0 to n-1, separated by spaces
        number_string = "  "
        number_string = number_string + " ".join(str(i) for i in range(n))
      #r#print(number_string)
    
    def print_board(self):
        self.print_numbers((self.NumberOfCols))
        print("  0 1 2 3")
        for i in range(self.NumberOfRows):
            print(f"{i}", end=" ")
            for j in range(self.NumberOfCols):
                print(self.board[i][j], end=" ")
            print()

    def get_moves(self, row, col):
        moves = []
        opponent = 'O' if self.current_player == 'X' else 'X'
        opponent_row, opponent_col = None, None
        
        # Locate the opponent's position
        for i in range(self.NumberOfRows):
            for j in range(self.NumberOfCols):
                if self.board[i][j] == opponent:
                    opponent_row, opponent_col = i, j
                  #r#print("opponent_row",opponent_row,"opponent_col",opponent_col)
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

                    if not moves:  # Check if q_values list is empty
                       1==1
                    else:
                       2==2

                    # print("legal moves",moves)
                    
        return moves
    
    def Is_Draw(self):     ## Declare a draw if the game has gone on too long, this is a shortcut for 3 fold repition for now - could make it one fold ...
        # print(" A B C D E")
      #r#print("NumberofMovesInTheGameSoFar = ", self.NumberofMovesInTheGameSoFar)
        if self.NumberofMovesInTheGameSoFar > 16:   ## always been 16, Dec 5th
            print("We Declare this game a draw!")
            self.NumberofDrawsInTheGameSoFar += 1
            self.ResetThePeicesAtTheEndOfTheGame()
            #self.NumberofMovesInTheGameSoFar = -1
    
    def pair_coordinates(self,coord_tuple):
    # Use list comprehension to create pairs
        return tuple((coord_tuple[i], coord_tuple[i + 1]) for i in range(0, len(coord_tuple), 2))

   
    def play(self, q_agent=None, training=True):   
        while self.NumberofGamesPlayedSoFar < (agent.TotalNumberOfGamesToPlay+1):
          #r#print("NumberofGamesPlayedSoFar = ",self.NumberofGamesPlayedSoFar)
            self.NumberofMovesInTheGameSoFar += 1
            print("self.NumberofMovesInTheGameSoFar = ",self.NumberofMovesInTheGameSoFar)
            self.Is_Draw()
            self.print_board()
          #r#print(f"{self.current_player}'s turn")
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
                if self.current_player == 'X':  # if it's X's turn SELECT THEIR ACTUAL MOVE
                        action, MaxQValueFromAllPossibleActionsInTheCurrentState  = q_agent.choose_action(self.current_state, moves, self.NumberofGamesPlayedSoFar)   
                        ## THis is updating Q-values of all possible moves from the current position
                        ## Select the maximum Q-value from available moves from the current state - and move to to that new state
                        if action == (1,3):
                            1==1
                       #r#print("MaxQValueFromAllPossibleActionsInTheCurrentState = ", MaxQValueFromAllPossibleActionsInTheCurrentState) # Max value From your CURRENT state 
                        # should then update the value of the state, action just taken based on how good it is in the NEW state 
                        # ... the value of your best move from your NEW state
                        ## Need a MaxQValueFromAllPossibleActionsInThe**NEW**State
                      #r#print("current_state",self.current_state) 
                      #r#print("X's NON-random move",action) 
                        ## Add a reward for 'direct' trajectories to the goal
                        #EuclidianDistanceFromGoal =  math.sqrt(pow((action[0]-0),2)+pow((action[1]-3),2))
                        #print(action[0])
                        #print(action[1])
                        #print("EuclidianDistanceFromGoal",EuclidianDistanceFromGoal)
                        # reward = -100*(EuclidianDistanceFromGoal)  ## To create quick optimal trajectories for X 
                        # reward = -5-100*(EuclidianDistanceFromGoal-(action[1]-3))  ## To create quick optimal trajectories for X 
                        reward = -1 ## Penalty for playing a move
                if self.current_player == 'O':
                    if training:
                        action = random.choice(moves)
                      #r#print("O's random move",action)
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
                #action = (2,2)
                 #action = random.choice(moves)
                action = (self.NumberOfRows-1,self.NumberOfCols-1)

                 # print("0's action = ", action)

            ###### Execute action AND UPDATE the NEW *State* and board ########
            self.PreviousState = self.current_state
          #r#print("PreviousState = ", self.PreviousState)

            self.board[row][col] = ' '
            self.board[action[0]][action[1]] = self.current_player    ### Set the NEW co-ordinates of player X or player Y

            self.current_state = ''.join([''.join(row) for row in self.board])
          #r#print("NEW STATE  = ", self.current_state)

            ## Obtain the best value from the NEW state so that the agent can learn - MaxQValueFromAllPossibleActionsInTheNEWState
            newrow, newcol = None, None
            for i in range(self.NumberOfRows):
                for j in range(self.NumberOfCols):
                    if self.board[i][j] == self.current_player:
                        newrow, newcol = i, j
                        break
            movesInNewPosition = self.get_moves(newrow, newcol)

            ## THis is updating Q-values from the winning position :(
            NewactionWhichWeDontUse, MaxQValueFromAllPossibleActionsInTheNEWState  = q_agent.choose_action(self.current_state, movesInNewPosition, self.NumberofGamesPlayedSoFar)
            print("NewactionWhichWeDontUse",NewactionWhichWeDontUse)
          #r#print("MaxQValueFromAllPossibleActionsInTheNEWState = ",MaxQValueFromAllPossibleActionsInTheNEWState) # Max value From your CURRENT state 

            ###########################

            # Check for game over conditions and learn and then reset
            # reward = 0  ## By Defaut
            if self.current_player == 'X' and action[1] == self.WinningColumnForX:
            # if self.current_player == 'X' and (action[0],action[1]) == (self.WinningRowForX,self.WinningColumnForX):
                reward = 100               
                print("X is the winner!!") ### Learn only when you win
                q_agent.learn(self.PreviousState , self.current_state, action, reward, MaxQValueFromAllPossibleActionsInTheNEWState) 
                self.ResetThePeicesAtTheEndOfTheGame()
                self.NumberofXVictoriesInTheGameSoFar += 1
                ## If last game record the FINAL move TotalNumberOfGamesToPlay
                onelessthanthetotalnumberofgames = agent.TotalNumberOfGamesToPlay - 1
                if self.NumberofGamesPlayedSoFar == onelessthanthetotalnumberofgames:
                    agent.OptimalTrajectory.append(action)

                # return 1  # return reward for X's win
            elif self.current_player == 'O' and action[1] == self.WinningColumnForO:
                # reward = -100   
                print("O is the winner!!")
                # q_agent.learn(self.PreviousState , self.current_state, action, reward, MaxQValueFromAllPossibleActionsInTheNEWState) 
                #ResetThePeicesAtTheEndOfTheGame(self): 
                self.NumberofOVictoriesInTheGameSoFar += 1
                self.ResetThePeicesAtTheEndOfTheGame()
                # return -1  # return reward for O's win

                ######   LEARN after every X move !? ######
            if self.current_player == 'X' and action[1] != self.WinningColumnForX:    
            # if self.current_player == 'X'and (action[0],action[1]) != (self.WinningRowForX,self.WinningColumnForX):  # if it's X's turn and hasnt won then LEARN
                print("X's non-random move",action) 
                ## If last game record the move TotalNumberOfGamesToPlay
                onelessthanthetotalnumberofgames = agent.TotalNumberOfGamesToPlay - 1
                if self.NumberofGamesPlayedSoFar == onelessthanthetotalnumberofgames and self.NumberofMovesInTheGameSoFar > -1: #Dont include last games victorious move
                    agent.OptimalTrajectory.append(action)

                print("Reward = ",reward) 
                q_agent.learn(self.PreviousState , self.current_state, action, reward, MaxQValueFromAllPossibleActionsInTheNEWState) 

            # Switch Whose Turn it is #
            if self.NumberofMovesInTheGameSoFar != -1:  ## Unless we are starting a new game in which X should always start
                self.current_player = 'O' if self.current_player == 'X' else 'X'   ## Issue
            else:
                self.current_player = 'X'

            if agent.TotalNumberOfGamesToPlay == self.NumberofGamesPlayedSoFar:
               print("#######STOP!!! OptimalTrajectory = ##########")
               BarrierPositionCoords = self.pair_coordinates(self.BarrierPositions)
               print(BarrierPositionCoords)
               print(agent.OptimalTrajectory)
               randomnumb = random.randint(1, 10000)   ## 'combinations'+str(randomnumb)+'.csv'
               #with open('combinations5.csv', 'a', newline='') as file:
               #     writer = csv.writer(file) 
               #     combination_str = '(' + ', '.join(map(str, BarrierPositionCoords)) + ')'
               #     writer.writerow([BarrierPositionCoords,agent.OptimalTrajectory])

########################## Generate Barriers #####################################

# Initialize an empty set to store the unique coordinate combinations
unique_coordinate_combinations = set()

# Create a list of all possible single coordinates in a 5x5 grid, excluding (0, 0)
single_coordinates = [(i, j) for i in range(4) for j in range(3) if (i, j) != (0, 0)]
print("single_coordinates",single_coordinates)
print("Length",len(single_coordinates))
# Generate combinations of increasing length
for r in range(1, 12):  # This will generate combinations of lengths 1 to to last number, 3 gives max combo (2, 1, 2, 2)
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
# print("sorted_combinations", sorted_combinations)

print("Number Pre cleaninging",len(sorted_combinations))  
# sorted_combinations = [(1,2,2,0)]
# print("sorted_combinations", sorted_combinations)

######## REMOVE IMPOSSIBLE BARRIERS for speed efficieny and sanity checking #########

def split_into_pairs(lst):
    new_list = []
    for item in lst:
        # Split each tuple into pairs and add them to the new list
        new_list.append([item[i:i+2] for i in range(0, len(item), 2)])
    return new_list

def flatten_pairs(lst):
    new_list = []
    for sublist in lst:
        # Flatten each sublist of tuples into a single tuple
        flattened_tuple = tuple(item for pair in sublist for item in pair)
        new_list.append(flattened_tuple)
    return new_list

def create_graph(combination, grid_size=4):
    """ Create a graph representation of the grid. """
    graph = {}
    for x in range(grid_size):
        for y in range(grid_size):
            if (x, y) not in combination:
                graph[(x, y)] = []
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < grid_size and 0 <= ny < grid_size and (nx, ny) not in combination:
                            graph[(x, y)].append((nx, ny))
    return graph
 
def can_reach_target(graph, start, target):
    """ Check if the target is reachable from start using DFS. """
    visited = set()
    stack = [start]
 
    while stack:
        node = stack.pop()
        if node == target:
            return True
        if node not in visited:
            visited.add(node)
            stack.extend(graph[node])
 
    return False

# sorted_combinations = [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2), (0, 1, 0, 2), (0, 1, 1, 0), (0, 1, 1, 1), (0, 1, 1, 2), (0, 1, 2, 0), (0, 1, 2, 1), (0, 1, 2, 2), (0, 2, 1, 0), (0, 2, 1, 1), (0, 2, 1, 2), (0, 2, 2, 0), (0, 2, 2, 1), (0, 2, 2, 2), (1, 0, 1, 1), (1, 0, 1, 2), (1, 0, 2, 0), (1, 0, 2, 1), (1, 0, 2, 2), (1, 1, 1, 2), (1, 1, 2, 0), (1, 1, 2, 1), (1, 1, 2, 2), (1, 2, 2, 0), (1, 2, 2, 1), (1, 2, 2, 2), (2, 0, 2, 1), (2, 0, 2, 2), (0, 1), (1, 1), (1, 2), (2, 1), (1, 3)]
# print(sorted_combinations)
sorted_combinations = split_into_pairs(sorted_combinations)

#print(sorted_combinations)
# Remove combinations that block the path from (0,0) to (0,3)
sorted_combinations = [combo for combo in sorted_combinations 
                       if can_reach_target(create_graph(combo), (0, 0), (0, 3))]  ### INSERT THE GOAL

sorted_combinations = flatten_pairs(sorted_combinations)

#print(sorted_combinations)

print("Number post cleaninging",len(sorted_combinations))  

#################################################################################
########################## END OF CREATE BARRIERS ###########################
#################################################################################

## Overide
sorted_combinations = [(0, 2 , 1, 2)]
# sorted_combinations = [(0, 1 , 1, 1, 1, 2, 2, 2)]  - too blocked up for X to win
# sorted_combinations = [(0, 2 , 1, 1 , 2, 2)] #  - working
#sorted_combinations = [(0, 2 , 2, 2)]  - "working"
# sorted_combinations = [(0, 2 , 1, 2, 2, 2)]
#sorted_combinations = [(0, 2 , 2, 2)]
# sorted_combinations = [(0, 2 , 1, 2, 2, 2)]
 
print("sorted final combos", sorted_combinations)

if __name__ == "__main__":
        # NumberOfDifferentGamesWithDifferentBarriersToPlay =         ## For each 
        # for episode in range(NumberOfDifferentGamesWithDifferentBarriersToPlay):
        for combination in sorted_combinations:
            agent = QLearningAgent()   ## Create an instance of a Q-Learning Agent
            # BoardPositionForThisGame = (1,2,4,0)
            BoardPositionForThisGame = (combination)
            game = GridWorldGame(BoardPositionForThisGame)     ## Create an instance of a GridWorldGame
            print("#######  Episodee = ", combination )
            game.play(q_agent=agent, training=True) ## Create a q_agent instance of the q learning class, training = true is an alternative to manual play  reward = 
