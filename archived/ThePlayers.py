import numpy as np

class GridWorldGame:
    def __init__(self):
        # Initialize the 5x5 game board
        self.board = [[' ' for _ in range(5)] for _ in range(5)]
        # Set the positions of the barriers
        for i in [0, 1, 3, 4]:
            self.board[i][2] = '#'
        # Define the goal position
        self.goal = (0, 4)

    def is_goal_reached(self, state):
        return state == self.goal

    def get_moves(self, state):
        row, col = state
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_row, new_col = row + i, col + j
                if 0 <= new_row < 5 and 0 <= new_col < 5 and self.board[new_row][new_col] == ' ':
                    moves.append((new_row, new_col))
        return moves

    def step(self, state, action):
        # Define the possible actions
        actions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        new_state = (state[0] + actions[action][0], state[1] + actions[action][1])
        if new_state in self.get_moves(state):
            if new_state == self.goal:
                return new_state, 1  # Return a reward of 1 for reaching the goal
            else:
                return new_state, -0.1  # Return a reward of -0.1 to incentivize faster paths
        else:
            return state, -1  # Return a reward of -1 for invalid moves

    def q_learning(self, episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.1):
        # Initialize the Q-table with zeros
        q_table = np.zeros((5, 5, 8))
        for episode in range(episodes):
            state = (0, 0)
            while not self.is_goal_reached(state):
                if np.random.uniform(0, 1) < epsilon:
                    action = np.random.choice(8)  # Explore action space
                else:
                    action = np.argmax(q_table[state[0], state[1]])  # Exploit learned values
                new_state, reward = self.step(state, action)
                future_max = np.max(q_table[new_state[0], new_state[1]])
                q_table[state[0], state[1], action] = q_table[state[0], state[1], action] + alpha * (reward + gamma * future_max - q_table[state[0], state[1], action])
                state = new_state

            # Display the current optimal policy and Q-table every 100 episodes
            if (episode + 1) % 100 == 0:
                print(f"Episode: {episode + 1}")
                self.display_policy(q_table)
                # print("Q-table:")
                # print(q_table)
                print("\n")
        return q_table

    def display_policy(self, q_table):
        policy = np.chararray((5, 5), itemsize=2, unicode=True)
        policy[:] = ' '
        for i in range(5):
            for j in range(5):
                action = np.argmax(q_table[i, j])
                policy[i, j] = ['U', 'D', 'L', 'R', 'UL', 'UR', 'DL', 'DR'][action]
        
        row_labels = ['A', 'B', 'C', 'D', 'E']
        print("  1 2 3 4 5")
        for idx, row in enumerate(policy):
            print(row_labels[idx], ' '.join(row))
        print("\n")

    def optimal_path(self, q_table):
        state = (0, 0)
        path = [state]
        while not self.is_goal_reached(state):
            action = np.argmax(q_table[state[0], state[1]])
            state = self.step(state, action)[0]
            path.append(state)
        return path

if __name__ == "__main__":
    game = GridWorldGame()
    q_table = game.q_learning()
    path = game.optimal_path(q_table)
    print("Optimal path from A1 to E1:", path)
