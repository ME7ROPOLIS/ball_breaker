# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 14:02:04 2016
Ball Breaker! (Clone of Breakout)
@author: Jake Fortner
"""

import sys, time, pygame
from pygame.locals import *
from ball_breaker.game_objects import Player, Ball, Wall


#=============================================================================#
#                               GAME VARIABLES                                #
#=============================================================================#

# Window #
fps = 30
win_width = 800
win_height = 600
half_winwidth = int(win_width/2)
half_winheight = int(win_height/2)

# Colors #
white =            (255, 255, 255)
black =            (  0,   0,   0)
wall_color_start = (255,   0,   0)
bg_color = black

# Directions #
left = False
right = False

# Wall Variables #
wall_rows = 10
wall_columns = 10
wall_width = int(win_width / wall_columns)
wall_height = int(half_winheight / wall_rows)
row_color_change = int(255/wall_rows) # rate the wall color will change from row to row
col_color_change = int(255/wall_columns)

# Ball Variables
ball_coords = (half_winwidth, win_height - int(win_height/4)) # centered
ball_width = 30
ball_radius = ball_width / 2
ball_velocity = 10
max_speed = 25
respawn_rate = 0.5
ball_time = 0

# Paddle Variables #
paddle_rate = 15
paddle_size = (160, 15)

max_lives = 3
lives_color = white
lives_coords = (20, win_height - 20) # where the lives show up on screen
lives_size = (40, 10)

#=============================================================================#
#                                  GAME BODY                                  #
#=============================================================================#


class Main():
    """
    Main() holds the game together. It is the skeleton, or brain of the game
    that uses it's methods to make the various pieces move, and calculates
    circumstances depending on what values have been changed. 
    """
    
    def __init__(self):
        # Basic Setup
        pygame.init()
        pygame.display.set_caption('Ball Breaker!')
        self.fpsclock = pygame.time.Clock()
        self.window = pygame.display.set_mode((win_width, win_height))
        self.basicfont = pygame.font.Font('freesansbold.ttf', 100)
        self.subfont = pygame.font.Font('freesansbold.ttf', 32)
        self.left = False
        self.right = False
    
                
    def start(self):
        
        self.start_screen()
        
        # Game Loop #
        while True:
            result = self.run_game()
            
            if result == 'won':
                self.win_screen()
                
            elif result == 'lost':
                self.game_over()
            
    def terminate(self):
        pygame.quit()
        sys.exit()

    def run_game(self):
        
        # Create Game Objects
        paddle = Player(paddle_size, (half_winwidth, win_height - 20)) # paddle is 10 pixels above bottom of screen
        ball_in_play = Ball(ball_coords, ball_velocity)
        
        # Create the Walls
        global temp_x, temp_y
        walls = [] 
        temp_x = 0
        wall_color = wall_color_start
        for x in range(wall_columns):
            walls.append([])
            wall_color = (wall_color_start[0], wall_color_start[1], wall_color[2] + col_color_change)
            temp_y = 0
            for y in range(wall_rows):
                walls[x].append(Wall((wall_width, wall_height), (temp_x, temp_y), wall_color))
                wall_color = (wall_color[0] - row_color_change, wall_color[1] + row_color_change, wall_color[2])
                temp_y += wall_height
            temp_x += wall_width
        
        
        # Main Game Loop #
        while True:
            
                                                   
            # Draw Window #
            self.window.fill(bg_color)
            
            # Draw Ball if it is Live
            if ball_in_play.ball_live:
                self.draw_obj(ball_in_play.coords, ball_width, white, rect=False)
            else: 
                if time.time() - ball_time >= respawn_rate:
                    ball_in_play = Ball(ball_coords, ball_velocity)
            
            # Draw Paddle
            self.draw_obj(paddle.coords, paddle.size, white)
            
            # Draw Walls
            wall_exists = False
            for x in range(wall_columns):
                for y in range(wall_rows):
                    if walls[x][y] != '.':
                        self.draw_obj(walls[x][y].coords, walls[x][y].size, walls[x][y].color, color2=black)
                        wall_exists = True # If this is never set to True, no
                                           # walls exist and the game is won.
            # Draw Lives
            life = lives_coords
            for i in range(paddle.lives):
                self.draw_obj(life, lives_size, white, color2=black)
                life = (life[0] + lives_size[0], life[1]) # Move over by size of lives rectangle
                
            # Check If Lost
            if paddle.lives <= 0:
                # Set Values Back #
                self.left = False
                self.right = False
                return 'lost'
            
            # Check if Won
            if not wall_exists:
                # Set Values Back #
                self.left = False
                self.right = False
                return 'won'
        
            # Event Checking #
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                
                # On Keydown, set it so we can hold keys to move
                elif event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.left = True
                        self.right = False
                    elif event.key == K_RIGHT:
                        self.right = True
                        self.left = False
                    
                elif event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        self.terminate()
                    elif event.key == K_LEFT:
                        self.left = False
                    elif event.key == K_RIGHT:
                        self.right = False
                    elif event.key == K_p:
                        self.pause_screen()
            
            # Move Paddle #
            paddle_x, paddle_y = paddle.coords           
            if self.left:
                paddle_x -= paddle_rate
            if self.right:
                paddle_x += paddle_rate
            paddle.coords = (paddle_x, paddle_y)
            
            # Move Ball #
            if ball_in_play.ball_live:
                ball_x, ball_y = ball_in_play.coords
                ball_x += ball_in_play.velocity[0]
                ball_y += ball_in_play.velocity[1]
                ball_in_play.coords = (ball_x, ball_y)
                
            # Check if ball is Live
            elif not ball_in_play.ball_live:
                if time.time() - ball_time >= respawn_rate:
                    ball_in_play.ball_live = True
            
            # Check if the ball has hit anything #
            self.check_window_bounce(ball_in_play, paddle)
            self.check_obj_bounce(ball_in_play, paddle)
            
            for x in range(wall_columns):
                for y in range(wall_rows):
                    # If there is a wall there.
                    if walls[x][y] != '.':
                        # If the ball bounces on a wall, delete wall 
                        if self.check_obj_bounce(ball_in_play, walls[x][y]):
                            walls[x][y] = '.'
                            
           
            pygame.display.update()
            self.fpsclock.tick(fps)            
                        
            
    # The Screen Functions #
    def start_screen(self):
        text = ('Ball Breaker!', 'Press any key to play.')
        self.create_screen(text)
        return
    
    def win_screen(self):
        text = ('You Won!', 'Press any key to play again.')
        self.create_screen(text)
        return
    
    def game_over(self):
        text = ('Game Over', 'Press any key to play again.')
        self.create_screen(text)
        return
        
    def pause_screen(self):
        text = ('Paused.', 'Press any key to continue.')
        self.create_screen(text)
        return
    
    def create_screen(self, text):
        big_text = self.basicfont.render(text[0], True, white)
        big_rect = big_text.get_rect()
        big_rect.center = (int(win_width/2), int(win_height/2))
        self.window.blit(big_text, big_rect)
        
        sub_text = self.subfont.render(text[1], True, white)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (int(win_width/2), int(win_height/2) + 100)
        self.window.blit(sub_text, sub_rect)
        
        quit_text = self.subfont.render('Press Esc to Quit.', True, white)
        quit_rect = quit_text.get_rect()
        quit_rect.center = (int(win_width/2), int(win_height/2) + 150)
        self.window.blit(quit_text, quit_rect)
        
        while True:
            
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    return
            pygame.display.update()
            self.fpsclock.tick(fps)
    
    def draw_obj(self, coords, size, color, color2=None, rect=True):
        if rect:
            pygame.draw.rect(self.window, color, (coords[0], coords[1], size[0] + 1, size[1] + 1))
            if color2:
                pygame.draw.rect(self.window, color2, (coords[0], coords[1], size[0], size[1]), 1)
        if not rect:
            pygame.draw.circle(self.window, color, coords, int(size / 2), 0)
    
    def check_obj_bounce(self, ball, obj):
        """
        Checks to see if the ball has hit an object, and bounces off of it. The
        function resets the ball velocity values if it has hit, and returns True
        so that destructible objects (like walls) can change. Otherwise, it returns
        False.
        """
        
        vx, vy = ball.velocity
        
        ball_x, ball_y = ball.coords
        obj_x, obj_y = obj.coords
        
        # Ball Bounces On Paddle #
        # Adjust ball center coords with the radius for outer edge of circle collision
        # Then adjust paddle coords to adjust for paddle size
        if (ball_x + ball_radius) >= (obj_x) and \
            (ball_x - ball_radius) <= (obj_x + obj.size[0]) and \
            (ball_y + ball_radius) >= (obj_y) and \
            (ball_y - ball_radius) <= (obj_y + obj.size[1]): 
            vx = vx * -1
            vy = vy * -1
            
            # Change Velocity of X depending on where on the paddle it hits
            if ball_x + ball_radius or ball_x - ball_radius >= (obj.center[0] + 20):
                vx += 10
                # Make sure the ball isn't moving too fast
                if vx > max_speed:
                    vx -= 10
                    
            elif ball_x + ball_radius or ball_x - ball_radius <= (obj.center[0] - 20):
                vx -= 10
                # Make sure the ball isn't moving too fast
                if vx < (-1 * max_speed):
                    vx += 10
                    
            ball.velocity = (vx, vy)
            return True
            
        return False
        
    def check_window_bounce(self, ball, paddle): 
        """
        Checks to see if the ball has hit the top, left, or right side of the window,
        or if the ball has fallen below the bottom edge, in which paddle loses one
        life and the ball is no longer live.
        """          
        vx, vy = ball.velocity
        
        ball_x, ball_y = ball.coords
        global ball_time
        
        # Ball Bounces Off Edge
        if (ball_x + ball_radius) > (win_width - 1) or (ball_x - ball_radius) < 0:
            vx = -1 * vx
        elif (ball_y - (ball_radius)) > (win_height) and ball.ball_live:
            # Lose a life since it has fallen past the bottom. Ball is no longer
            # live.
            paddle.lives -= 1
            ball.ball_live = False
            vx = ball_velocity
            vy = 0
            ball_time = time.time()
        elif (ball_y + ball_radius) < 0:
            vy = -1 * vy
    
        ball.velocity = (vx, vy)
                
            

def play():
    game = Main()
    game.start()    

