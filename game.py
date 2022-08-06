import pygame, sys, time, random
from pygame.sprite import Sprite
from pygame.sprite import Group

clock = pygame.time.Clock ()
pygame.font.init ()

font_type = pygame.font.SysFont ('comicsans', 30)
font_typebig = pygame.font.SysFont ('comicsans', 50)

# images
upperbg = pygame.image.load ('images/upper_bg.png')
lowerbg = pygame.image.load ('images/base.png')

bird_up = pygame.image.load ('images/upflap.png')
bird_mid = pygame.image.load ('images/midflap.png')
bird_down = pygame.image.load ('images/downflap.png')

bird_up = pygame.transform.scale (bird_up, (37, 37))
bird_mid = pygame.transform.scale (bird_mid, (37, 37))
bird_down = pygame.transform.scale (bird_down, (37, 37))

birdgif = [bird_up, bird_mid, bird_down]

# define
screen = pygame.display.set_mode ((336, 624))
pygame.display.set_caption ('Flappy Bird')

def movingbg(screen, background, x_pos, y_pos, ):
    screen.blit (background, (x_pos, y_pos))


class Bird ():
    def __init__(self, screen, slice):
        self.screen = screen
        self.screen_rect = self.screen.get_rect ()

        self.bird_image = birdgif[slice]
        self.bird_rect = self.bird_image.get_rect ()

        self.bird_rect.y = self.screen_rect.centery
        self.bird_rect.x = self.screen_rect.centerx - 130
        self.bird_rect.y = self.bird_rect.y

    def draw_bird(self):
        screen.blit (self.bird_image, self.bird_rect)


class Pipes (Sprite):
    def __init__(self, screen, image, y_pos):
        super ().__init__ ()
        self.screen = screen
        self.screen_rect = self.screen.get_rect ()

        self.image = image
        self.pipe_rect = self.image.get_rect ()

        self.pipe_rect.x = self.screen_rect.right
        self.pipe_rect.y = y_pos

    def draw_pipe(self):
        screen.blit (self.image, self.pipe_rect)


def run():
    pygame.init ()

    # sound
    #hit = pygame.mixer.Sound ('sound/sfx_hit.wav')
   # bouns = pygame.mixer.Sound ('sound/sfx_point.wav')
    #music = pygame.mixer.music.load ('sound/music.mp3')
   # pygame.mixer.music.play (-1)
    pipe_bottom = pygame.image.load ('images/pipe.png')
    pipe_top = pygame.transform.rotate (pipe_bottom, 180)
    pipe_groupbottom = Group ()
    pipe_groupsec = Group ()
    FPS = 135
    run = True
    slice = 1
    # background variables
    x_pos_upper = 0
    x_pos_lower = -336
    y_pos_upper = 0
    y_pos_lower = 512

    # bird variables
    bird = Bird (screen, slice)
    vel = 90
    print("s")

    while run:
        current_time = pygame.time.get_ticks ()
        # score and lives
        score = int (current_time / 100)
        score_label = font_type.render (f'Score: {str (score)}', 1, (255, 255, 255))
        y_pos = random.randint (250, 420)
        pipe_down = Pipes (screen, pipe_bottom, y_pos)
        pipe_sec = Pipes (screen, pipe_top, y_pos - 480)

        # drawing moving background
        movingbg (screen, upperbg, x_pos_upper, y_pos_upper)
        x_pos_upper -= 1
        x_pos_lower += 1

        if x_pos_upper + 336 == 0:
            x_pos_upper = 0
        if x_pos_lower == 0:
            x_pos_lower = - 336

        # bird animation
        bird.bird_image = birdgif[int (slice)]
        bird.draw_bird ()
        slice += 0.05
        if int (slice) > 2:
            slice = 0

        # pipes
        if len (pipe_groupbottom) == 0 and len (pipe_groupbottom) < 2:
            pipe_groupbottom.add (pipe_down)
            pipe_groupsec.add (pipe_sec)

        for event in pygame.event.get ():
            if event.type == pygame.QUIT:
                sys.exit ()

            if event.type == pygame.MOUSEBUTTONDOWN and bird.bird_rect.y > 30:
                bird.bird_rect.y -= vel

                slice = 0

        if bird.bird_rect.y < 475:
            bird.bird_rect.y += 1
        if bird.bird_rect.y < 0:
            bird.bird_rect.y = bird.bird_rect.y + 10

        # drawing pipes
        for pipe_down in pipe_groupbottom.sprites ():
            pipe_down.draw_pipe ()
            pipe_down.pipe_rect.x -= 2

        for pipe_sec in pipe_groupsec.sprites ():
            pipe_sec.draw_pipe ()
            pipe_sec.pipe_rect.x -= 2

        if pipe_down.pipe_rect.x < 5:
            pipe_down.kill ()
        if pipe_sec.pipe_rect.x < 5:
            pipe_sec.kill ()
#            bouns.play ()

        if bird.bird_rect.colliderect (pipe_down.pipe_rect) or bird.bird_rect.colliderect (pipe_sec.pipe_rect):
           # hit.play ()
            pipe_down.kill ()
            pipe_sec.kill ()
            run = 0
            return score

        # showing score and lives
        screen.blit (score_label, (5, 10))
        pipe_groupsec.update ()
        pipe_groupbottom.update ()
        movingbg (screen, lowerbg, x_pos_lower, y_pos_lower)
        clock.tick (FPS)
        pygame.display.update ()


def start():
    pygame.init ()
    run2 = True
    msg = pygame.image.load ('images/message.png')
    msg = pygame.transform.scale (msg, (336, 624))
    while run2:
        screen.fill ((255, 255, 255))
        screen.blit (msg, (0, 0))
        for event in pygame.event.get ():
            if event.type == pygame.QUIT:
                sys.exit ()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run2 = False
        pygame.display.update ()


def gameover():
    pygame.init()
    run3 = True
    score = run()
    msg = pygame.image.load ('images/gameover.png')
    score_labelbig = font_typebig.render (f'Score: {str (score)}', 1, (0, 0, 0))

    while run3:
        screen.fill ((255, 255, 255))
        screen.blit (msg, (74, 250))
        screen.blit (score_labelbig, (74, 314))

        for event in pygame.event.get ():
            if event.type == pygame.QUIT:
                sys.exit ()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run3 = False

        pygame.display.update ()


start ()
run ()
gameover ()

