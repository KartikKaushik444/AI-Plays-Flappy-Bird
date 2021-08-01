import random   # For generating random numbers
import sys      # For closing the game
import pygame    
import os
from pygame.locals import *  # For keys

import neat

# Globals variables for the game
FPS = 32         # Frames per second

screenwidth = 1112
screenheight = 627

screen = pygame.display.set_mode((screenwidth, screenheight))

groundy = screenheight * 0.8
game_sprites = {}
game_sounds = {}
player = "gallery/Sprites/bird.png"
background ="gallery/Sprites/background.png"
pipe = "gallery/Sprites/pipe.png"
pygame.init()

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.BirdVely = -9       # it is -ve  to make bird jump automatically whwn game starts
        self.BirdFlapAccv = -8    # velocity while flapping
        self.BirdFlapped = True
        self.BirdAccY = 1        # For increasing velocity
        self.BirdMaxVelY = 10

    def jump(self):
        if self.y > 0 :
            self.BirdVely = self.BirdFlapAccv
            self.BirdFlapped = True

    def move(self):
        if self.BirdVely < self.BirdMaxVelY and not self.BirdFlapped:
            self.BirdVely += self.BirdAccY

        if self.BirdFlapped:
            self.BirdFlapped = False
        #BirdHeight = game_sprites['player'].get_height()
        
        self.y = self.y + self.BirdVely


    



# Functions

def welcomeScreen():     # Shows welcome Screen
    
    messagex = int((screenwidth - game_sprites['message'].get_width())/2)
    messagey = int (screenheight * 0.001)

    font = pygame.font.SysFont("Times New Roman", 30, bold=True, italic=True)
    guide_message = font.render(" Press 's' to Start", True, (0, 0, 0))
    basex = 0
    while True:
        for event in pygame.event.get():
            # If user clicks cross button than close the game

            if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key== K_ESCAPE):
                pygame.quit()
                sys.exit()
                quit()

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key == pygame.K_s or event.key== K_UP):
                return

            else:
                # screen.blit(game_sprites['background'], (0,0))
                # screen.blit(game_sprites['player'], (playerx, playery))
                screen.blit(game_sprites['message'], (messagex, messagey))
                screen.blit(guide_message, (0.1 * screenwidth, 0.6 *screenheight))
                # screen.blit(game_sprites['base'], (basex, groundy))
                pygame.display.update()     # VERY IMP: Without this no  update
                FPSclock.tick(FPS)

#def mainGame():
    print("In main Game")
    score = 0
    playerx = int(screenwidth/5)
    playery = int(screenheight/2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    newPipe3 = getRandomPipe()

    # List of upper pipes
    upperPipes = [
        {'x' : screenwidth+50, 'y' : newPipe1[0]['y']},
        {'x' : screenwidth+50+(screenwidth/3), 'y' : newPipe2[0]['y']},
        {'x' : screenwidth+50+2*(screenwidth/3)  , 'y' : newPipe3[0]['y']},
    ]

    # List of Lower pipes
    lowerPipes = [
        {'x' : screenwidth+50, 'y' : newPipe1[1]['y']},
        {'x' : screenwidth+50+(screenwidth/3), 'y' : newPipe2[1]['y']},
        {'x' : screenwidth+50+2*(screenwidth/3)  , 'y' : newPipe3[1]['y']},

    ]

    pipeVelx = -4
    playerVely = -9       # it is -ve  to make bird jump automatically whwn game starts
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1        # For increasing velocity

    playerFlapAccv = -8    # velocity while flapping
    playerFlapped = False  # It is true only when bird is flapping

    while True:
        # playerVely = -9
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0 :
                    playerVely = playerFlapAccv
                    playerFlapped = True
                    
                    #game_sounds[''].play()
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        
        if crashTest:       # If player is crashed
            return
        # Check for score
        playerMidpos = playerx + game_sprites['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + game_sprites['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidpos <pipeMidPos+4:
                score += 1
                print(f"Your score is {score}")
                # game_sounds['point'].play()
    
        if playerVely < playerMaxVelY and not playerFlapped:
            playerVely += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = game_sprites['player'].get_height()
        
        playery = playery + playerVely
        # + min(playerVely, groundy - playery - playerHeight)
        
        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelx
            lowerPipe['x'] += pipeVelx

        # Add a pipe just before left pipe is going to be removed

        if 0< upperPipes[0]['x']<4:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])
    
        # If the pipe is out of screen remove it
        if upperPipes[0]['x'] < -game_sprites['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)


        # Blit the sprites
        
        screen.blit(game_sprites['background'], (0, 0))

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            screen.blit(game_sprites['pipe'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(game_sprites['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
            
        screen.blit(game_sprites['base'], (basex, groundy))
        screen.blit(game_sprites['player'], (playerx, playery))

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digits in myDigits:
            width += game_sprites['numbers'][digits].get_width()
            
        xoffset = (screenwidth - width)/2

        for digit in myDigits:
            screen.blit(game_sprites['numbers'][digit], (xoffset, screenwidth*0.12))
            xoffset += game_sprites['numbers'][digit].get_width()+2

        pygame.display.update()
        FPSclock.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery >= groundy - 56 or playery<0:
        # game_sounds['hit'].play()
        return True
     
    for pipe in upperPipes:
        pipeHeight = game_sprites['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx -pipe['x'])+50 < game_sprites['pipe'][0].get_width()):
            return True

    for pipe in lowerPipes:
        if (playery + game_sprites['player'].get_height() > pipe['y'] and abs(playerx -pipe['x'])+50 < game_sprites['pipe'][0].get_width()):
            return True
    return False

def getRandomPipe():
    # generate positions of both pipes

    pipeHeight = game_sprites['pipe'][0].get_height()
    offset = screenheight/6
    y2 = offset + random.randrange(2, int(screenheight - game_sprites['base'].get_height() + 0.6*offset))
    pipex = screenwidth + 10
    # y1 = pipeHeight - y2 + offset    to make this work change y1 to -y1 on '192'
    y1 = y2 - offset - pipeHeight
    pipe = [
        {'x' : pipex, 'y' : y1} ,  # Upper Pipe
        {'x' : pipex, 'y' : y2}    # Lower Pipe
    ]
    return pipe


# if __name__ == "__main__":
    # It is the main function form where gamw will start
    #pygame.init()                 # Initialize all pygame modules
    FPSclock = pygame.time.Clock()       # For contolling FPS
    pygame.display.set_caption("Flappy Bird by KK")
    game_sprites['numbers'] = (
        pygame.image.load('gallery/Sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/Sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/Sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/Sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/Sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/Sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/Sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/Sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/Sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/Sprites/9.png').convert_alpha(),

   )

    # Game sprites
    game_sprites['base'] = pygame.image.load('gallery/Sprites/base.png').convert_alpha()
    game_sprites['message'] = pygame.image.load('gallery/Sprites/message.jpg').convert_alpha()
    game_sprites['pipe'] = (pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(),180),
    pygame.image.load(pipe).convert_alpha()
    )
    game_sprites['background'] = pygame.image.load(background).convert()
    game_sprites['player'] = pygame.image.load(player).convert_alpha()  



    # Game Sounds

    #    game_sounds['die'] = pygame.mixer.Sounds('')
    #    game_sounds['hit'] = pygame.mixer.Sounds('')
    #    game_sounds['point'] = pygame.mixer.Sounds('')
    #    game_sounds['swoosh'] = pygame.mixer.Sounds('')
    #    game_sounds['wing'] = pygame.mixer.Sounds('')
  
    while True:
        welcomeScreen()    # Shows welcome screen to the user untill he presses a button
        mainGame()         # This is the main game function


def main(genomes, config):
    score = 0
    nets = []
    ge = []
    birds = []

    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    newPipe3 = getRandomPipe()

    # List of upper pipes
    upperPipes = [
        {'x' : screenwidth+50, 'y' : newPipe1[0]['y']},
        {'x' : screenwidth+50+(screenwidth/3), 'y' : newPipe2[0]['y']},
        {'x' : screenwidth+50+2*(screenwidth/3)  , 'y' : newPipe3[0]['y']},
    ]

    # List of Lower pipes
    lowerPipes = [
        {'x' : screenwidth+50, 'y' : newPipe1[1]['y']},
        {'x' : screenwidth+50+(screenwidth/3), 'y' : newPipe2[1]['y']},
        {'x' : screenwidth+50+2*(screenwidth/3)  , 'y' : newPipe3[1]['y']},

    ]

    pipeVelx = -4

    run = True

    for _, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            nets.append(net)
            birds.append(Bird(int(screenwidth/5), int(screenheight/2)))
            g.fitness = 0
            ge.append(g)

    while run:
    

        for x,bird in enumerate(birds):
            if isCollide(bird.x, bird.y, upperPipes, lowerPipes) == True:
                ge[x].fitness -= 1
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

             # Check for score
            birdMidpos = bird.x + game_sprites['player'].get_width()/2
            i = 0
            for pipe in upperPipes:
                pipeMidPos = pipe['x'] + game_sprites['pipe'][0].get_width()
                if pipeMidPos<= birdMidpos <pipeMidPos+4:
                    # ge[x].fitness += 5
                    for g in ge:
                        g.fitness+=5
                    if i == 0:
                        score += 1
                        i += 1
                    #print(f"Your score is {score}")
                    # game_sounds['point'].play()

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelx
            lowerPipe['x'] += pipeVelx

        # Add a pipe just before left pipe is going to be removed

        if 0< upperPipes[0]['x']<4:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])
    
        # If the pipe is out of screen remove it
        if upperPipes[0]['x'] < -game_sprites['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # For finding the pipe in front of the birds
        for x,pipe in enumerate(upperPipes):
            if len(birds) != 0:
                if pipe['x'] >= birds[0].x - 50:
                    indexNextPipe = x
                    break
            else:
                return

        print("YO RA PIPE")
        print(indexNextPipe)

        pipeHeight = game_sprites['pipe'][0].get_height()
        # For moving bird
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y, (bird.y - (upperPipes[indexNextPipe]['y'] + pipeHeight) ), (bird.y - (lowerPipes[indexNextPipe]['y']) )  ))

            if output[0] > 0.5:
                bird.jump()

        # Blit the sprites
        
        screen.blit(game_sprites['background'], (0, 0))

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            screen.blit(game_sprites['pipe'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(game_sprites['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
            
        screen.blit(game_sprites['base'], (basex, groundy))

        for bird in birds:
            screen.blit(game_sprites['player'], (bird.x, bird.y))

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digits in myDigits:
            width += game_sprites['numbers'][digits].get_width()
            
        xoffset = (screenwidth - width)/2

        for digit in myDigits:
            screen.blit(game_sprites['numbers'][digit], (xoffset, screenwidth*0.12))
            xoffset += game_sprites['numbers'][digit].get_width()+2

        pygame.display.update()
        FPSclock.tick(FPS)

        # print("Yo h size")
        # print(len(birds))

        if len(birds) == 0:
            run = False
        

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                     neat.DefaultStagnation, config_path)
     
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    print("In run")

    winner = p.run(main,50)
        

if __name__ == "__main__":
    #print("THEEK HAI")
     # It is the main function form where gamw will start
    #pygame.init()                 # Initialize all pygame modules
    FPSclock = pygame.time.Clock()       # For contolling FPS
    pygame.display.set_caption("Flappy Bird by KK")
    game_sprites['numbers'] = (
        pygame.image.load('gallery/Sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/Sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/Sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/Sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/Sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/Sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/Sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/Sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/Sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/Sprites/9.png').convert_alpha(),

   )

    # Game sprites
    game_sprites['base'] = pygame.image.load('gallery/Sprites/base.png').convert_alpha()
    game_sprites['message'] = pygame.image.load('gallery/Sprites/message.jpg').convert_alpha()
    game_sprites['pipe'] = (pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(),180),
    pygame.image.load(pipe).convert_alpha()
    )
    game_sprites['background'] = pygame.image.load(background).convert()
    game_sprites['player'] = pygame.image.load(player).convert_alpha()  


  
    while True:
        welcomeScreen()    # Shows welcome screen to the user untill he presses a button
        break
       


    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)