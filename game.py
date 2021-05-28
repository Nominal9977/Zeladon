#hell yea
# Imports
import pygame
import random
import json 

# Window settings
GRID_SIZE = 64
WIDTH = 25 * GRID_SIZE
HEIGHT = 16 * GRID_SIZE
TITLE = "Zeladon"
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
Level_complete = 3
win = 4
# Load fonts
font_xl = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 96)
font_lg = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 64)
font_md = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 32)
font_sm = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 24)
font_xs = pygame.font.Font(None, 14)

# Load images
hero_imgs_rt = [pygame.image.load('assets/Items/Players/Variable sizes/Blue/alienBlue_walk1.png').convert_alpha(),
                pygame.image.load('assets/Items/Players/Variable sizes/Blue/alienBlue_walk2.png').convert_alpha()]

hero_jump_rt = [pygame.image.load('assets/Items/Players/Variable sizes/Blue/alienBlue_jump.png').convert_alpha()]

hero_climb_rt = [pygame.image.load('assets/Items/Players/Variable sizes/Blue/alienBlue_climb1.png').convert_alpha(),
                 pygame.image.load('assets/Items/Players/Variable sizes/Blue/alienBlue_climb2.png').convert_alpha()]


hero_imgs_lt = [pygame.transform.flip(img, True, False)for img in hero_imgs_rt]
hero_jump_lt = [pygame.transform.flip(img, True, False)for img in hero_jump_rt]
hero_climb_lt = [pygame.transform.flip(img, True, False)for img in hero_climb_rt]

Block_img = pygame.image.load('assets/images/tiles/block.png').convert_alpha()
stoneBlock_img = pygame.image.load('assets/images/tiles/stone.png').convert_alpha()
grassBlock_img = pygame.image.load('assets/images/tiles/grass_dirt.png').convert_alpha()
gems_img = pygame.image.load('assets/images/items/gem.png').convert_alpha()
heart_img = pygame.image.load('assets/images/items/heart.png').convert_alpha()
chain_img = pygame.image.load('assets/Items/Tiles/signExit.png').convert_alpha()

bee_imgs = [pygame.image.load('assets/Items/Enemies/bee.png').convert_alpha(),
            pygame.image.load('assets/Items/Enemies/bee_move.png').convert_alpha()]

barnacle_imgs = [pygame.image.load('assets/Items/Enemies/barnacle.png').convert_alpha(),
                 pygame.image.load('assets/Items/Enemies/barnacle_attack.png').convert_alpha()]
                 
mouse_imgs_rt = [pygame.image.load('assets/Items/Enemies/mouse.png').convert_alpha(),
              pygame.image.load('assets/Items/Enemies/mouse_move.png').convert_alpha()]
mouse_imgs_lt = [pygame.transform.flip(img, True, False)for img in mouse_imgs_rt ]

saw_imgs = [pygame.image.load('assets/Items/Enemies/saw.png').convert_alpha(),
            pygame.image.load('assets/Items/Enemies/saw_move.png').convert_alpha()]

greenworm_imgs = [pygame.image.load('assets/Items/Enemies/wormGreen.png').convert_alpha(),
                  pygame.image.load('assets/Items/Enemies/wormGreen_move.png').convert_alpha()] 



# Load sounds


#load levels

Levels = ["assets/levels/World-1.json",
          "assets/levels/World-2 .json",
          "assets/levels/World-3.json"]

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
class AminatedEntity(Entity):
     def __init__(self, x, y, images):
         super().__init__(x,y, images[0])

         self.images = images
         self.image_index = 0
         self.ticks = 0
         self.animation_speed = 10

     def set_img_list(self):
         self.images = self.images 
     def animate(self):
         self.set_img_list()
         self.ticks += 1

         if self.ticks % self.animation_speed == 0:
              self.image_index += 1

              if self.image_index >= len(self.images):
                  self.image_index = 0
                          
              self.image = self.images[self.image_index]            
         
class Hero(AminatedEntity):
    
    def __init__(self, x, y, images):
        super().__init__(x, y, images)
        
       

        self.speed = 5
        self.jump_power = 22

        self.vx = 0 
        self.vy = 0
        self.hurt_timer = 0 

        self.hearts = 400
        self.gems = 0
        self.score = 0
       
    def move_right(self):
    	self.vx = self.speed
    
    def move_to(self,x, y):
        self.rect.centerx = x * GRID_SIZE + GRID_SIZE//2
        self.rect.centery = y * GRID_SIZE + GRID_SIZE//2
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
        elif self.rect.right > world_width:
            self.rect.right = world_width


        
        
    def reached_goal(self):
        return pygame.sprite.spritecollideany(self, goal)

    
    def update(self):
        self.apply_gravity()
        self.move_and_check_blocks()
        self.check_world_edges()
        self.check_items()
        self.check_enemy()
        self.animate()
    	
    	 
class Platform(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        
class Blocks(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
                              
class Chain(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        
class Item(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        
    def apply(self, character):
        character.gems +=1
        character.score +=10
        print(character.score)

class Enemy(AminatedEntity):
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

        
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
        elif self.rect.right > world_width:
            self.rect.right = world_width
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
    
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

    def update(self):
        self.move_and_check_blocks()
        self.apply_gravity()
        self.check_world_edges()
        self.check_platform_edges()
        self.animate()

class Mouse(Enemy):
    
    def __init__(self, x, y, images):
        super().__init__(x, y, images)
        
    def set_image_list(self):
        if self.vx > 0:
            self.images = Mouse_imgs_rt

        else:
            self.images = spick_man_imgs_lt
    def update(self):
        self.move_and_check_blocks()
        self.apply_gravity()
        self.check_world_edges()        
        self.check_platform_edges()
        self.animate()                  
class Bee(Enemy):
    
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

    def update(self):
        self.move_and_check_blocks()
        self.check_world_edges()        
        self.animate()


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
def show_win_screen():
        text = font_xl.render('Level complete!', True, WHITE)
        rect = text.get_rect()
        rect.midbottom = WIDTH // 2, HEIGHT // 2
        screen.blit(text, rect)

       
def show_wins_screen():
        text = font_xl.render('You winnnnnnn!', True, WHITE)
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
def start_game():
    global hero, stage, current_level
    
    hero = Hero(0, 0, hero_imgs_rt)
    stage = Start
    current_level = 2
def setup():
    global player, emenys, items, blocks, goal, gravity, terminal_velocity, world_width,  world_height, all_sprites
    
    blocks = pygame.sprite.Group()
    items  = pygame.sprite.Group()
    emenys = pygame.sprite.Group()
    player = pygame.sprite.Group()
    goal   = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    with open(Levels[current_level]) as f:
        data = json.load(f)
  
    goal.add(Chain(data["chain_locs"][0], data["chain_locs"][1], chain_img))

    
             
    for loc in data ["platform_locs"]:
        x = loc[0]
        y = loc[1]
        b = Platform(x,y,stoneBlock_img)
        blocks.add(b)               
    for loc in data ["block_locs"]:
        x = loc[0]
        y = loc[1]
        b = Platform(x,y,grassBlock_img)
        blocks.add(b)
    for loc in data ["item_locs"]:
        x = loc[0]
        y = loc[1]
        b = Item(x,y,gems_img)
        items.add(b)

    for loc in data ["saw_locs"]:
        x = loc[0]
        y = loc[1]
        e = Saw(x,y,saw_imgs)
        emenys.add(e)
    for loc in data ["mouse_locs"]:
        x = loc[0]
        y = loc[1]
        e = Mouse(x,y,mouse_imgs_lt)
        emenys.add(e)

    for loc in data ["bee_locs"]:
        x = loc[0]
        y = loc[1]
        e = Bee(x,y,bee_imgs)
        emenys.add(e)

    
    for loc in data ["grayBlocks_locs"]:
        x = loc[0]
        y = loc[1]
        b = Blocks(x,y,Block_img)
        blocks.add(b)
        
    world_width = data['width'] * GRID_SIZE
    world_height = data['height'] * GRID_SIZE
    print(world_width)
    hero.move_to(data ["start"][0],data ["start"][1])
    player.add(hero)

    gravity = data["gravity"]
    terminal_velocity = data["terminal_velocity"]


    all_sprites.add(player,emenys, items, blocks, goal)

# Input handling
grid_on = False
running = True
start_game()
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
            if stage == Lose or stage == win:
                if event.key == pygame.K_r:
                        start_game()
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
         elif hero.reached_goal():
            stage = Level_complete
            countdown = 2 *FPS
    elif stage == Level_complete:
        countdown -= 1
        if countdown <=0:
            current_level += 1
            if current_level <len(Levels):
                setup()
                stage = Playing
            else:
                stage = win 
    if hero.rect.centerx < WIDTH // 2:
        offset_x = 0
    elif hero.rect.centerx > world_width - WIDTH //2:
        offset_x = world_width - WIDTH
    else:
        offset_x = hero.rect.centerx - WIDTH // 2

        
    if hero.rect.centery < HEIGHT :
        offset_y =0
   
    else:
        offset_y = hero.rect.centery - HEIGHT //2
    # Drawing code
    screen.fill(SKY_BLUE)
    

    for sprite in all_sprites:
        screen.blit(sprite.image, [sprite.rect.x - offset_x, sprite.rect.y-offset_y])
        
    

    show_hud()
    if grid_on:
         draw_grid(offset_x)
    if stage == Start:
        show_start_screen()

    elif stage == Lose:
        show_lose_screen()
    elif stage == Level_complete:
        show_win_screen()
    elif stage == win:
        show_wins_screen()
    # Update screen
    pygame.display.update()


    # Limit refresh rate of game loop 
    clock.tick(FPS)


# Close window and quit
pygame.quit()

