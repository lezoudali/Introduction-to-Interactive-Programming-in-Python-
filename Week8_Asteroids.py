#Follow link to play game
#http://www.codeskulptor.org/#user33_59LAPAtLqYk1rmy.py
#
# program template for Spaceship
import simplegui
import math
import random
from random import randrange 

# globals for user interface

WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
    
    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
#soundtrack = simplegui.load_sound("https://dl-web.dropbox.com/get/August%20Alsina%20-%20Testimony%20%28Deluxe%20Version%29%20AlbumKings.com/15%20Numb%20%28Ft.%20B.o.B%20%26%20Yo%20Gotti%29%20%5BBonus%20Track%5D.mp3?_subject_uid=33803597&w=AADyA4qEZtPr9mzvJzet_sxTgmHK8g0syb35OKKU1FjkgA") 
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def update_angle(self, ang):
        if ang:
            self.angle_vel += 0.05
        else:
            self.angle_vel -= 0.05
            
    def update_thrust(self, flag):
        self.thrust = flag
        ship_thrust_sound.play() if flag else ship_thrust_sound.rewind()
        

    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)   
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)  
    def update(self):
        
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        if self.thrust:
            accel = angle_to_vector(self.angle)
            self.vel[0] += (accel[0]*.05)
            self.vel[1] += (accel[1]*.05)
        
        self.vel[0] *= .99
        self.vel[1] *= .99
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius    
    
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        
        missile_vel = [self.vel[0] + 5*forward[0], self.vel[1] + 5*forward[1]]
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        
        a_missile = Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
            
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
   
    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + (self.age * self.image_size[0]), self.image_center[1]], self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.age += 1
        flag = True if self.age == self.lifespan else False
        return flag
            
        
    def collide(self, sprite):
        return True if dist(self.get_position(), sprite.get_position()) < (self.get_radius() + sprite.get_radius()) else False
  
def group_collide(group, obj):
    num_collisions = 0
    for sprite in set(group):
        if sprite.collide(obj):
            num_collisions += 1
            explosion = Sprite(sprite.get_position(),[0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(explosion)
            group.remove(sprite)      
    return num_collisions


def group_group_collide(group1, group2):
    num_collisions = 0
    for sprite in set(group1):
        if group_collide(group2, sprite):
            group1.remove(sprite)
            num_collisions += 1
    return num_collisions
            
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        soundtrack.play()
        
def process_sprite_group(group, canvas):
    for sprite in set(group):
        if sprite.update():
            group.remove(sprite)
        sprite.draw(canvas)
        
def draw(canvas):
    global time,lives, score, started, rock_group
    
    if lives == 0:
        soundtrack.rewind()
        started = False
        lives = 3
        score = 0
        rock_group = set([])
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # update ship and sprites
    my_ship.update()
    
    #draw score and lives
    lives -= group_collide(rock_group, my_ship)
    score += group_group_collide(rock_group, missile_group)
    canvas.draw_text('Lives: ' + str(lives), [20, 20], 20, 'White')
    canvas.draw_text('Score: ' + str(score), [700, 20], 20, 'White')
    
      
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.update_angle(False)
    if key == simplegui.KEY_MAP['right']:
        my_ship.update_angle(True)
    if key == simplegui.KEY_MAP['up']:
        my_ship.update_thrust(True)
    if key == simplegui.KEY_MAP['space']:
        my_ship.shoot()

def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.update_angle(True)
    if key == simplegui.KEY_MAP['right']:
        my_ship.update_angle(False)
    if key == simplegui.KEY_MAP['up']: 
        my_ship.update_thrust(False)
        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, started
    
    if len(rock_group) < 10 and started:
        a_rock = Sprite([randrange(0, WIDTH), randrange(0, HEIGHT)], [random.random() * 1.5 - .3, random.random() * 1.5 - .3], 
                    0, random.random() * -.2 + .1, asteroid_image, asteroid_info)
        if dist(a_rock.get_position(), my_ship.get_position()) > 200: 
            rock_group.add(a_rock)
            
    if frame.get_canvas_textwidth("test",50) < 10:
        soundtrack.pause()
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set ([])
explosion_group = set()


# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)


# get things rolling
timer.start()
frame.start()
