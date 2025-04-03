import pygame
import random
import os
import webbrowser

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
JUMP_STRENGTH = -7
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

try:
    BACKGROUND = pygame.image.load(os.path.join('assets', 'gameobjects', 'background-day.png')).convert()
    BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    BASE = pygame.image.load(os.path.join('assets', 'gameobjects', 'base.png')).convert_alpha()
    BASE = pygame.transform.scale(BASE, (SCREEN_WIDTH, 70))
    BASE_Y = SCREEN_HEIGHT - 70
    BASE_RECT = pygame.Rect(0, BASE_Y, SCREEN_WIDTH, 70)
    
    PIPE_IMG = pygame.image.load(os.path.join('assets', 'gameobjects', 'pipe-green.png')).convert_alpha()
    PIPE_IMG = pygame.transform.scale(PIPE_IMG, (50, SCREEN_HEIGHT + 100))

    BIRD_SPRITES = [
        pygame.image.load(os.path.join('assets', 'gameobjects', 'yellowbird-downflap.png')).convert_alpha(),
        pygame.image.load(os.path.join('assets', 'gameobjects', 'yellowbird-midflap.png')).convert_alpha(),
        pygame.image.load(os.path.join('assets', 'gameobjects', 'yellowbird-upflap.png')).convert_alpha()
    ]

    GAMEOVER_IMG = pygame.image.load(os.path.join('assets', 'UI', 'gameover.png')).convert_alpha()
    GAMEOVER_RECT = GAMEOVER_IMG.get_rect()
    GAMEOVER_RECT.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

    NUMBER_SPRITES = []
    for i in range(10):
        number_img = pygame.image.load(os.path.join('assets', 'UI', 'Numbers', f'{i}.png')).convert_alpha()
        NUMBER_SPRITES.append(number_img)

    try:
        DIE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Sound Efects', 'die.ogg'))
        HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Sound Efects', 'hit.ogg'))
        POINT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Sound Efects', 'point.ogg'))
        WING_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Sound Efects', 'wing.ogg'))
    except:
        print("Could not load sound effects")
        DIE_SOUND = None
        HIT_SOUND = None
        POINT_SOUND = None
        WING_SOUND = None

except Exception as e:
    print(f"Error loading images: {e}")
    BACKGROUND = None
    BASE = None
    PIPE_IMG = None
    BIRD_SPRITES = None
    GAMEOVER_IMG = None
    NUMBER_SPRITES = None
    DIE_SOUND = None
    HIT_SOUND = None
    POINT_SOUND = None
    WING_SOUND = None

class Bird:
    def __init__(self):
        self.x = SCREEN_WIDTH // 3
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.animation_index = 0
        self.animation_speed = 0.1
        self.animation_timer = 0
        if BIRD_SPRITES:
            self.image = BIRD_SPRITES[0]
            self.rect = self.image.get_rect(center=(self.x, self.y))
        else:
            self.rect = pygame.Rect(self.x, self.y, 30, 30)
        self.update()

    def jump(self):
        self.velocity = JUMP_STRENGTH
        if WING_SOUND:
            WING_SOUND.play()

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y
        
        if BIRD_SPRITES:
            self.animation_timer += self.animation_speed
            self.animation_index = int(self.animation_timer) % 3
            self.image = BIRD_SPRITES[self.animation_index]

    def draw(self):
        if BIRD_SPRITES:
            angle = max(-30, min(self.velocity * 3, 30))
            rotated_bird = pygame.transform.rotate(self.image, -angle)
            rotated_rect = rotated_bird.get_rect(center=self.rect.center)
            screen.blit(rotated_bird, rotated_rect)
        else:
            pygame.draw.rect(screen, WHITE, self.rect)

class Pipe:
    def __init__(self):
        self.gap_y = random.randint(150, SCREEN_HEIGHT - 150)
        self.x = SCREEN_WIDTH
        if PIPE_IMG:
            self.image = PIPE_IMG
            self.upper_rect = PIPE_IMG.get_rect(bottomleft=(self.x, self.gap_y - PIPE_GAP // 2))
            self.lower_rect = PIPE_IMG.get_rect(topleft=(self.x, self.gap_y + PIPE_GAP // 2))
        else:
            self.upper_rect = pygame.Rect(self.x, 0, 50, self.gap_y - PIPE_GAP // 2)
            self.lower_rect = pygame.Rect(self.x, self.gap_y + PIPE_GAP // 2, 50, SCREEN_HEIGHT)
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED
        self.upper_rect.x = self.x
        self.lower_rect.x = self.x

    def draw(self):
        if PIPE_IMG:
            upper_pipe = pygame.transform.flip(self.image, False, True)
            screen.blit(upper_pipe, self.upper_rect)
            screen.blit(self.image, self.lower_rect)
        else:
            pygame.draw.rect(screen, GREEN, self.upper_rect)
            pygame.draw.rect(screen, GREEN, self.lower_rect)

def draw_score(score, x, y):
    if NUMBER_SPRITES:
        score_str = str(score)
        width = NUMBER_SPRITES[0].get_width()
        total_width = width * len(score_str)
        start_x = x - total_width // 2
        
        for i, digit in enumerate(score_str):
            digit_img = NUMBER_SPRITES[int(digit)]
            screen.blit(digit_img, (start_x + i * width, y))

def main():
    bird = Bird()
    pipes = []
    last_pipe = pygame.time.get_ticks()
    score = 0
    running = True
    game_over = False

    while running:
        clock.tick(60)
        current_time = pygame.time.get_ticks()

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        bird = Bird()
                        pipes = []
                        last_pipe = current_time
                        score = 0
                        game_over = False
                    else:
                        bird.jump()
                elif event.key == pygame.K_n:
                    score += 10
                    if POINT_SOUND:
                        POINT_SOUND.play()
        
        if not game_over and keys[pygame.K_SPACE]:
            bird.jump()

        if not game_over:
            bird.update()

            if bird.rect.colliderect(BASE_RECT):
                game_over = True
                if DIE_SOUND:
                    DIE_SOUND.play()

            if current_time - last_pipe > PIPE_FREQUENCY:
                pipes.append(Pipe())
                last_pipe = current_time

            for pipe in pipes[:]:
                pipe.update()
                
                hit_pipe = bird.rect.colliderect(pipe.upper_rect) or bird.rect.colliderect(pipe.lower_rect)
                hit_bounds = bird.y < 0
                
                if hit_pipe:
                    game_over = True
                    if HIT_SOUND:
                        HIT_SOUND.play()
                elif hit_bounds:
                    game_over = True
                    if DIE_SOUND:
                        DIE_SOUND.play()
                
                if not game_over and not pipe.passed and pipe.x < bird.x:
                    score += 1
                    pipe.passed = True
                    if POINT_SOUND:
                        POINT_SOUND.play()
                    if score > 100:
                        webbrowser.open('https://youtu.be/XeiZD3ve-fI?si=U2cl40ATeIX14Dh6')
                        running = False

                if pipe.x < -60:
                    pipes.remove(pipe)

        if BACKGROUND:
            screen.blit(BACKGROUND, (0, 0))
        else:
            screen.fill(BLACK)
            
        for pipe in pipes:
            pipe.draw()
        bird.draw()
        
        if BASE:
            screen.blit(BASE, (0, BASE_Y))

        if NUMBER_SPRITES:
            draw_score(score, SCREEN_WIDTH//2, 50)
        else:
            font = pygame.font.Font(None, 36)
            score_text = font.render(str(score), True, WHITE)
            screen.blit(score_text, (SCREEN_WIDTH//2, 50))

        if game_over:
            if GAMEOVER_IMG:
                screen.blit(GAMEOVER_IMG, GAMEOVER_RECT)
            else:
                font = pygame.font.Font(None, 36)
                game_over_text = font.render("Game Over - Space to Restart", True, WHITE)
                text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                screen.blit(game_over_text, text_rect)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
