import numpy as np
import pygame
import random
import pickle

# Importing game classes and constants
from flappy_bird import Bird, Pipe, FlappyBirdGame, PIPE_GAP, SCREEN_WIDTH, PIPE_WIDTH, SCREEN_HEIGHT, BIRD_SIZE

# RL settings
STATE_SPACE = 2  # distance to next pipe, height difference with next pipe's gap
ACTION_SPACE = 2  # flap or do nothing
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.99
EXPLORATION_RATE = 1.0
EXPLORATION_DECAY = 0.995
MIN_EXPLORATION_RATE = 0.01
EPISODES = 1000

class QLearningAgent:
    def __init__(self):
        self.q_table = np.zeros((500, 500, ACTION_SPACE))
        self.exploration_rate = EXPLORATION_RATE

    def get_state(self, game):
        bird_x = game.bird.x
        bird_y = game.bird.y
        pipe_x = game.pipes[0].x
        pipe_height = game.pipes[0].height
        distance_to_pipe = pipe_x - bird_x
        height_diff = pipe_height + PIPE_GAP // 2 - bird_y

        distance_to_pipe = min(max(distance_to_pipe // 10, 0), 499)
        height_diff = min(max(height_diff // 10, 0), 499)
        
        return (distance_to_pipe, height_diff)

    def choose_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice([0, 1])
        return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + DISCOUNT_FACTOR * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += LEARNING_RATE * td_error

    def train(self, game):
        for episode in range(EPISODES):
            game.reset()
            state = self.get_state(game)
            done = False
            total_reward = 0

            while not done:
                action = self.choose_action(state)
                if action == 1:
                    game.bird.flap()
                
                game.bird.update()
                for pipe in game.pipes:
                    pipe.update()
                    if not pipe.passed and pipe.x < game.bird.x:
                        game.score += 1
                        pipe.passed = True
                    if pipe.x + PIPE_WIDTH < 0:
                        game.pipes.remove(pipe)
                        game.pipes.append(Pipe(SCREEN_WIDTH))

                next_state = self.get_state(game)
                reward = 1
                done = game.check_collision()
                if done:
                    reward = -100
                
                self.update_q_table(state, action, reward, next_state)
                state = next_state
                total_reward += reward

                # Render the game screen
                game.screen.fill((255, 255, 255))  # Fill the screen with white
                game.bird.draw(game.screen)
                for pipe in game.pipes:
                    pipe.draw(game.screen)
                pygame.display.flip()

                # Limit the frame rate
                game.clock.tick(30)

            self.exploration_rate = max(self.exploration_rate * EXPLORATION_DECAY, MIN_EXPLORATION_RATE)
            print(f"Episode: {episode}, Total Reward: {total_reward}")

    def save_q_table(self, file_name):
        with open(file_name, "wb") as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, file_name):
        with open(file_name, "rb") as f:
            self.q_table = pickle.load(f)

if __name__ == "__main__":
    game = FlappyBirdGame()
    agent = QLearningAgent()
    agent.train(game)
    agent.save_q_table("q_table.pkl")
    pygame.quit()




