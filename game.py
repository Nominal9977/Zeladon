# Imports
import pygame
import random


# Window settings
GRID_SIZE = 64
WIDTH = 29 * GRID_SIZE
HEIGHT = 14 * GRID_SIZE
TITLE = "Game Title"
FPS = 60


# Create window
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (0, 150, 255)
GRAY = (175,175,175)

#Stages
Start = 0
Playing = 1
Lose = 2
# Load fonts
font_xl = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 96)
font_lg = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 64)
font_md = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 32)
font_sm = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 24)
font_xs = pygame.font.Font(None, 14)

# Load images
hero_img = pygame.image.load('assets/images/characters/player_idle.png').convert_alpha()
stoneBlock_img = pygame.image.load('assets/images/tiles/stone.png').convert_alpha()
grassBlock_img = pygame.image.load('assets/images/tiles/grass_dirt.png').convert_alpha()
gems_img = pygame.image.load('assets/images/items/gem.png')
orangeblade_img = pygame.image.load('assets/Items/images/characters/enemy2a.png').convert_alpha()
barnacle_img = pygame.image.load('assets/Items/Enemies/barnacle.png').convert_alpha()
mouse_img = pygame.image.load('assets/Items/Enemies/mouse.png').convert_alpha()
saw_img = pygame.image.load('assets/Items/Enemies/saw.png').convert_alpha()
greenworm_img = pygame.image.load('assets/Items/Enemies/wormGreen.png').convert_alpha()
heart_img = pygame.image.load('assets/images/items/heart.png')



# Load sounds


#Settings
gravity = 1.0
terminal_velocity = 24

# Game classes

class Entity (pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x* GRID_SIZE
        self.rect.y = y* GRID_SIZE

        self.vx = 0
        self.vy = 0 

    def apply_gravity(self):
         self.vy += gravity
         if self.vy > terminal_velocity:
            self.vy = terminal_velocity
    
class Hero(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        
       

        self.speed = 5
        self.jump_power = 22

        self.vx = 0 
        self.vy = 0
        self.hurt_timer = 0 

        self.hearts = 3
        self.gems = 0
        self.score = 0
       
    def move_right(self):
    	self.vx = self.speed
    	
    def move_left(self):
    	self.vx = -1 * self.speed

    def stop(self):
        self.vx = 0 
    def jump(self):
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, blocks, False)
        self.rect.y -= 1

        if len(hits) > 0:
            self.vy = -1 * self.jump_power

    

    def move_and_check_blocks(self):
        self.rect.x += self.vx
        hits = pygame.sprite.spritecollide(self, blocks, False)

        for block in hits:
            if self.vx > 0:
                self.rect.right = block.rect.left
            elif self.vx < 0:
                self.rect.left = block.rect.right

        self.rect.y +=self.vy
        hits = pygame.sprite.spritecollide(self, blocks, False)
        
        for block in hits:
            if self.vy > 0:
                self.rect.bottom = block.rect.top
            elif self.vy < 0:
                self.rect.top = block.rect.bottom


    def check_items(self):
        hits = pygame.sprite.spritecollide(self, items, True)

        for item in hits:
            item.apply(self)
    def check_enemy(self):
        hits = pygame.sprite.spritecollide(self, emenys, False)

        for enemy in hits:
            if self.hurt_timer == 0:
                self.hearts -= 1
                self.hurt_timer = 1.0 * FPS
                print(self.hearts)
                print("Oof!!")# play a sound

            if self.rect.x < enemy.rect.x:
                self.vx = -15
            elif self.rect.x > enemy.rect.x:
                self.vx = 15

            if self.rect.y < enemy.rect.y:
                self.vy = -5
                enemy.kill()
            elif self.rect.y > enemy.rect.y:
                self.vy = 5
                
        else:
            self.hurt_timer -= 1

            if self.hurt_timer < 0:
                self.hurt_timer = 0


                
             


    def check_world_edges(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH


        
        
    
    def update(self):
        self.apply_gravity()
        self.move_and_check_blocks()
        self.check_world_edges()
        self.check_items()
        self.check_enemy()
    	
    	 
class Platform(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        
class Item(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        
    def apply(self, character):
        character.gems +=1
        character.score +=10
        print(character.score)

class Enemy(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        
        self.vx = -2
        self.vy = 0

    def reverse(self):
        self.vx*=-1
    def move_and_check_blocks(self):
        self.rect.x += self.vx
        hits = pygame.sprite.spritecollide(self, blocks, False)

        for block in hits:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.vx = -1 
                self.reverse()
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.reverse() 

        self.rect.y +=self.vy

        
        hits = pygame.sprite.spritecollide(self, blocks, False)
        
        for block in hits:
            if self.vy > 0:
                self.rect.bottom = block.rect.top
            elif self.vy < 0:
                self.rect.top = block.rect.bottom

    def check_world_edges(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.reverse()
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.reverse()
    def check_platform_edges(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, blocks, False)
        self.rect.y -=2

        must_reverse = True

        for platform in hits:
            if self.vx < 0 and platform.rect.left <= self.rect.left:
                must_reverse = False
            elif self.vx > 0 and platform.rect.right >= self.rect.right:
                must_reverse = False

            if must_reverse:
                self.reverse()

class Saw(Enemy):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def update(self):
        self.move_and_check_blocks()
        self.apply_gravity()
        self.check_world_edges()


class Mouse(Enemy):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def update(self):
        self.move_and_check_blocks()
        self.apply_gravity()
        self.check_world_edges()        
        self.check_platform_edges()
class Worm(Enemy):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def update(self):
        self.move_and_check_blocks()
        self.check_world_edges()        
        


# Helper functoins
def show_start_screen():
    text = font_xl.render(TITLE, True, WHITE)
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)
    
    text = font_sm.render(" press any key to start", True, WHITE)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)
def show_lose_screen():
        text = font_xl.render('Game over', True, WHITE)
        rect = text.get_rect()
        rect.midbottom = WIDTH // 2, HEIGHT // 2
        screen.blit(text, rect)
        
        text = font_sm.render("Press 'r' to play again", True, WHITE)
        rect = text.get_rect()
        rect.midtop = WIDTH // 2, HEIGHT // 2
        screen.blit(text, rect)
def show_hud():
    text = font_md.render(str(hero.score), True, WHITE)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, 16
    screen.blit(text, rect)

    screen.blit(gems_img, [WIDTH - 128, 17])
    text = font_md.render("x" + str(hero.gems), True, WHITE)
    rect = text.get_rect()
    rect.topleft = WIDTH - 70, 33
    screen.blit(text, rect)

    for i in range(hero.hearts):
        x = i * 36 + 16
        y = 16
        screen.blit(heart_img, [x,y])
    
def draw_grid(offset_x=0, offset_y=0):
    for x in range(0, WIDTH + GRID_SIZE, GRID_SIZE):
        adj_x = x - offset_x % GRID_SIZE
        pygame.draw.line(screen, GRAY, [adj_x, 0], [adj_x, HEIGHT], 1)

    for y in range(0, HEIGHT + GRID_SIZE, GRID_SIZE):
        adj_y = y - offset_y % GRID_SIZE
        pygame.draw.line(screen, GRAY, [0, adj_y], [WIDTH, adj_y], 1)

    for x in range(0, WIDTH + GRID_SIZE, GRID_SIZE):
        for y in range(0, HEIGHT + GRID_SIZE, GRID_SIZE):
            adj_x = x - offset_x % GRID_SIZE + 4
            adj_y = y - offset_y % GRID_SIZE + 4
            disp_x = x // GRID_SIZE + offset_x // GRID_SIZE
            disp_y = y // GRID_SIZE + offset_y // GRID_SIZE
            
            point = '(' + str(disp_x) + ',' + str(disp_y) + ')'
            text = font_xs.render(point, True, GRAY)
            screen.blit(text, [adj_x, adj_y])

   
# Game loop
def setup():
    global player, emenys, items, blocks, stage, hero
    
    blocks = pygame.sprite.Group()
    items = pygame.sprite.Group()
    emenys = pygame.sprite.Group()
    player = pygame.sprite.GroupSingle()

    item_locs = [[11,7], [16,0], [8,3]]
    block_locs =  [[0,13], [1,13], [2,13], [3,13], [4,13], [5,13],
                   [6,13], [7,13], [8,13], [9,13], [10,13], [11,13],
                   [12,13], [13,13], [14,13], [15,13], [16,13], [17,13],
                   [18,13], [19,13], [20,13], [21,13], [22,13], [23,13],
                   [24,13], [25,13], [26,13], [27,13], [28,13]]

    platform_locs = [[11,6], [12,6], [13,6], [4,10], [5,10], 
                     [8, 4], [7,4], [9,4], [8,7], [6,10],
                     [7,10], [11,1], [16,1], [16,11], [17,11],
                     [18,11], [20,8], [22,5], [20,3], [19,8]]
    saw_locs = [(11,7)]
    mouse_locs = [(7,2)]
    greenworm_locs = [(8,0)]


                     
    for loc in platform_locs:
        x = loc[0]
        y = loc[1]
        b = Platform(x,y,stoneBlock_img)
        blocks.add(b)               
    for loc in block_locs:
        x = loc[0]
        y = loc[1]
        b = Platform(x,y,grassBlock_img)
        blocks.add(b)
    for loc in item_locs:
        x = loc[0]
        y = loc[1]
        b = Item(x,y,gems_img)
        items.add(b)

    for loc in saw_locs:
        x = loc[0]
        y = loc[1]
        e = Saw(x,y,saw_img)
        emenys.add(e)
    for loc in mouse_locs:
        x = loc[0]
        y = loc[1]
        e = Mouse(x,y,mouse_img)
        emenys.add(e)

    for loc in greenworm_locs:
        x = loc[0]
        y = loc[1]
        e = Worm(x,y,greenworm_img)
        emenys.add(e)

    
    start_x = 0
    start_y = 0

    hero = Hero(start_x, start_y, hero_img)
    player.add(hero)
        

    stage = Start
# Input handling
grid_on = False
running = True
setup()

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if stage  == Start:
                stage = Playing
                
            if stage == Playing:
                  if event.key == pygame.K_SPACE:
                        hero.jump()
            if stage == Lose:
                if event.key == pygame.k_r:
                        setup()
                
            if event.key == pygame.K_g:
                  grid_on = not grid_on
            

    pressed = pygame.key.get_pressed()
    if stage == Playing:
        
        if pressed[pygame.K_LEFT]:
            hero.move_left()
        elif pressed[pygame.K_RIGHT]:
            hero.move_right()
        else:
            hero.stop()

    
    # Game logic
    if stage == Playing:
     player.update()
     emenys.update()
    if hero.hearts == 0:
            stage = Lose 
        
    # Drawing code
    screen.fill(SKY_BLUE)
    player.draw(screen)
    blocks.draw(screen)
    emenys.draw(screen)
    items.draw(screen)
    show_hud()
    if grid_on:
         draw_grid(offset_x=0)
       

    if stage == Start:
        show_start_screen()

    elif stage == Lose:
        show_lose_screen()
        
    # Update screen
    pygame.display.update()


    # Limit refresh rate of game loop 
    clock.tick(FPS)


# Close window and quit
pygame.quit()

