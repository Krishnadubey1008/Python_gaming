import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game settings
BIRD_SIZE = 70  # Increased bird size
PIPE_WIDTH = 70
PIPE_GAP = 200
GRAVITY = 1
FLAP_STRENGTH = 15
PIPE_SPEED = 3

# Load bird image
BIRD_IMG = pygame.image.load("bird.png")
BIRD_IMG = pygame.transform.scale(BIRD_IMG, (BIRD_SIZE, BIRD_SIZE))

# Create a class for the bird
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def flap(self):
        self.velocity = -FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self, screen):
        screen.blit(BIRD_IMG, (self.x, self.y))

# Create a class for pipes
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT))

# Create a class for the game
class FlappyBirdGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.bird = Bird()
        self.pipes = [Pipe(SCREEN_WIDTH + i * 300) for i in range(3)]
        self.score = 0

    def reset(self):
        self.bird = Bird()
        self.pipes = [Pipe(SCREEN_WIDTH + i * 300) for i in range(3)]
        self.score = 0

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.bird.flap()

            self.bird.update()
            for pipe in self.pipes:
                pipe.update()
                if not pipe.passed and pipe.x < self.bird.x:
                    self.score += 1
                    pipe.passed = True
                if pipe.x + PIPE_WIDTH < 0:
                    self.pipes.remove(pipe)
                    self.pipes.append(Pipe(SCREEN_WIDTH))

            self.screen.fill(WHITE)
            self.bird.draw(self.screen)
            for pipe in self.pipes:
                pipe.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(30)

            if self.check_collision():
                self.reset()

    def check_collision(self):
        if self.bird.y > SCREEN_HEIGHT or self.bird.y < 0:
            return True
        for pipe in self.pipes:
            if pipe.x < self.bird.x < pipe.x + PIPE_WIDTH:
                if self.bird.y < pipe.height or self.bird.y > pipe.height + PIPE_GAP:
                    return True
        return False

if __name__ == "__main__":
    game = FlappyBirdGame()
    game.run()
    pygame.quit()



