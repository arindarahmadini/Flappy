# pygame.org/docs/ref/draw.html

import pygame, sys, random

# initiate game
pygame.init()

#1.1 draw to floor horizontally so that it covers double screen width
def draw_floor():
	SCREEN.blit(floor_surface,(floor_x_pos,450)) 
	SCREEN.blit(floor_surface,(floor_x_pos + 288,450))
#end2.1

#1.2 create pipe in random position
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (350, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (350, random_pipe_pos - 150))
    return bottom_pipe, top_pipe

#1.3 draw pipe upside down
def draw_pipes(pipes) :
    for pipe in pipes:
        if pipe.bottom >= 512:
            SCREEN.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            SCREEN.blit(flip_pipe, pipe)

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    visible_pipes = [pipe for pipe in pipes if pipe.right > -25]
    return visible_pipes

# scoring
score = 0
high_score = 0
game_font = pygame.font.Font('04B_19__.ttf', 20)

def score_display():
    if start:
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (144, 30))
        SCREEN.blit(score_surface, score_rect)
    else:
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (144, 30))
        SCREEN.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center= (144, 450))
        SCREEN.blit(high_score_surface, high_score_rect)


can_score = True
def pipe_score_check():
    global score, can_score

    if pipe_list:
        for pipe in pipe_list:
            if 45 < pipe.centerx < 55 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
        
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
            death_sound.play()
            return False
    
    return True


# Window.screen
SCREEN = pygame.display.set_mode((288, 512))
pygame.display.set_caption("Flappy Bird")
FPS = 120 # frame per second
clocks = pygame.time.Clock()

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

init_surface = pygame.image.load('assets/message.png').convert_alpha()
init_rect = init_surface.get_rect(center = (144, 256))

#load image
bg_surface = pygame.image.load('assets/background-day.png').convert()
bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (50,256))

BIRDFLAP = pygame.USEREVENT
pygame.time.set_timer(BIRDFLAP, 200)

# 2 set the flow surface    
floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0
#end2

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_height = [200, 300, 400]
pipe_list = []
# create event for pipe
SPAWNPIPE = pygame.USEREVENT + 1 # +1 is ID to difference with birdflap
pygame.time.set_timer(SPAWNPIPE, 2000)

gravity = 0.1 # 0.1 pixel FPS
start = False
bird_movement = 0

while True:
    clocks.tick(FPS) #maksimal 120fps
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # detect event quit
            pygame.quit()
            sys.exit()
        clicked = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                clicked = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                clicked = True

        if clicked and not start:
            can_score = True
            pipe_list = []
            bird_rect.center = (50,256)
            score = 0
            start = True

        if clicked and start:
            flap_sound.play()
            bird_movement = -5
            
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

        if event.type == SPAWNPIPE and start:
            pipe_list.extend(create_pipe())

    SCREEN.blit(bg_surface, (0,0))

    if start:
        bird_surface = bird_frames[bird_index]
        bird_movement += gravity
        bird_rect.centery += bird_movement
        SCREEN.blit(bird_surface, bird_rect)
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        pipe_score_check()

        start = check_collision(pipe_list)
        
        if not start:
            death_sound.play()
            if high_score < score:
                high_score = score
            
    else :
        SCREEN.blit(init_surface, init_rect)


    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0

    score_display()

    pygame.display.update() # update render







