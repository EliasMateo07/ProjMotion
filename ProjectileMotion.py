import math
import pygame
import sys

g = 9.8
theta = math.degrees(45)
difference = 0

class Circle(pygame.sprite.Sprite):
    def __init__(self, radius, color, position, thickness=None):
        super().__init__()
        self.radius = radius
        self.color = color
        self.thickness = thickness
        self.position = position
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=position)
        self.draw_circle()
    def draw_circle(self):
        if self.thickness is not None:
            pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius, self.thickness)
        else:
            pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
class BlockSprite(pygame.sprite.Sprite):
    def __init__(self, surface_size, color, position):
       super().__init__()
       self.image = pygame.Surface(surface_size)
       self.rect = self.image.get_rect()
       self.image.fill(color)
       self.rect.x, self.rect.y = position[0], position[1]
    def update(self, color):
        self.image.fill(color)
class Line(pygame.sprite.Sprite):
    def __init__(self, start_pos, end_pos, color, thickness=2):
        super().__init__()
        self.color = color
        self.thickness = thickness
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.image = pygame.Surface((abs(end_pos[0] - start_pos[0]) + thickness, abs(end_pos[1] - start_pos[1]) + thickness), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1])
        self.draw_line()
    def draw_line(self):
        self.image = pygame.Surface((abs(self.end_pos[0] - self.start_pos[0]) + self.thickness, abs(self.end_pos[1] - self.start_pos[1]) + self.thickness), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = min(self.start_pos[0], self.end_pos[0]), min(self.start_pos[1], self.end_pos[1])
        pygame.draw.line(self.image, self.color, (self.start_pos[0] - self.rect.x, self.start_pos[1] - self.rect.y), (self.end_pos[0] - self.rect.x, self.end_pos[1] - self.rect.y), self.thickness)
class ArcSprite(pygame.sprite.Sprite):
    def __init__(self, surface, color, rect, start_angle, stop_angle, thickness):
        super().__init__()
        self.surface = surface
        self.color = color
        self.rect = rect
        self.start_angle = start_angle
        self.stop_angle = stop_angle
        self.thickness = thickness
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.draw_arc()
    def draw_arc(self):
        # Draw the empty arc on the surface
        pygame.draw.arc(self.image, self.color, self.image.get_rect(), self.start_angle, self.stop_angle, self.thickness)
    def update(self):
        # Blit the image onto the surface
        self.surface.blit(self.image, self.rect.topleft)
class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text, font, color, position):
        super().__init__()
        self.font = font
        self.color = color
        self.text = text
        self.update_text(self.text)
        self.rect = self.image.get_rect()
        self.rect.center = position
    def update_text(self, text):
        self.image = self.font.render(text, True, self.color)

def calculate_trajectory(t):
    x = vxi * t + ball.position[0]
    y = 540 - (vyi * t - 0.5 * g * t ** 2)
    return x, y

def calculate_angle(t, origin_x, origin_y):
    vx = vxi
    vy = vyi - g * t
    adjusted_vx = vx - origin_x
    adjusted_vy = vy - origin_y
    return math.atan2(adjusted_vy, adjusted_vx)

def simple_calculate_angle(pos, origin):
    adjusted_x = pos[0] - origin[0]
    adjusted_y = pos[1] - origin[1]
    return math.atan2(adjusted_y, adjusted_x)

def radius_size(size, radius, origin=(50, 550)):
    x, y = size
    x_origin, y_origin = origin
    adjusted_x = x - x_origin
    adjusted_y = y - y_origin
    r = math.sqrt(math.pow(adjusted_x, 2) + math.pow(adjusted_y, 2))
    if r <= radius:
        return False
    return True

BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
origin = (50, 550)

pygame.init()
screen = pygame.display.set_mode((1200, 600)) # 800
pygame.display.set_caption("Projectile Motion")
text_font = pygame.font.SysFont("arial", 30)
screen.fill(WHITE)

x_line = Line((0, origin[1]), (1200, origin[1]), BLACK)
y_line = Line((origin[0], 600), (origin[0], 00), BLACK)
ball = Circle(8, BLUE, (origin[0], origin[1]))
x_bord = BlockSprite((50,1200), WHITE, (0,0))
y_bord = BlockSprite((1200, 50), WHITE, (0, 550))
x_text = TextSprite("Distance: ", text_font, BLACK, (700, 50))
y_text = TextSprite("Height: ", text_font, BLACK, (700, 100))

cover = Circle(1300, WHITE , (origin[0], origin[1]), 1000)
bordstop = Circle(301, BLACK, (origin[0], origin[1]), 3)

follow_line = Line(origin, (500,10), BLACK)
follow_arc = ArcSprite(screen, BLACK, pygame.Rect(origin[0], 500, 200, 200), 4, 8, 2)

angle_sprite = TextSprite("θ = ", text_font, BLACK, (100, 575))
velocity_sprite = TextSprite("Enter Velocity:", text_font, BLACK, (300, 575))
recomended = TextSprite("Recomended Velocity: 100", text_font, BLACK, (900, 575))
sprites = pygame.sprite.Group( bordstop, follow_line, x_bord, y_bord, cover, x_line, y_line, ball, angle_sprite)

start_time = 0
typing = False
animation = False
running = True
moving = True

x,y = 0,0
while running:
    time = pygame.time.get_ticks()/1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                moving = False
                sprites.add(velocity_sprite, recomended)
                typing = True
                
            elif event.button == 3:
                if not animation:
                    moving = True   
                    typing = False
                    velocity_sprite.text = "Enter Velocity:"
                    velocity_sprite.update_text(velocity_sprite.text)
                    ball.rect.centerx , ball.rect.centery = origin
                    sprites.remove(velocity_sprite, recomended, x_text, y_text)
        elif event.type == pygame.KEYDOWN:
            if typing:
                if event.key == pygame.K_RETURN:
                    if velocity_sprite.text != "Enter Velocity:":
                        typing = False
                        sprites.remove(velocity_sprite, recomended)

                        vi = int(velocity_sprite.text.split(":")[-1])
                        vyi = vi * math.sin(math.radians(theta))
                        vxi = vi * math.cos(math.radians(theta))
                        height = (vyi**2)//(2*g)
                        difference = time
                        time = (2 * vyi) / g
                        distance = vxi * time
                        animation = True

                        sprites.add(x_text, y_text)
                        velocity_sprite.text = "Enter Velocity:"
                        velocity_sprite.update_text(velocity_sprite.text)

                elif event.key == pygame.K_BACKSPACE:
                    velocity_sprite.text = velocity_sprite.text[:-1]
                    velocity_sprite.update_text(velocity_sprite.text)
                else:
                    if event.unicode.isdigit():
                        velocity_sprite.text += event.unicode
                        velocity_sprite.update_text(velocity_sprite.text)

    mouse_pos = pygame.mouse.get_pos()    
    if moving:     
        follow_line.end_pos = mouse_pos
        if radius_size(follow_line.end_pos, radius=300):
            follow_line.draw_line()
            angle = simple_calculate_angle(follow_line.end_pos, origin)
            if angle_sprite != "θ = ":
                angle_sprite.text = "θ = "
            if not x_bord.rect.collidepoint(mouse_pos) and not y_bord.rect.collidepoint(mouse_pos):
                theta = int(math.degrees(abs(angle)))
                angle_sprite.text += str(theta)
                angle_sprite.update_text(angle_sprite.text)

    if animation:
        start_time = time - difference
        x, y = calculate_trajectory(start_time)  
        x_text.text = "Distance: " + str(int(x)//1) + "m"
        y_text.text = "Height: " + str(abs((int(y)//1)-550)) + "m"
        x_text.update_text(x_text.text)
        y_text.update_text(y_text.text)
        ball.rect.x, ball.rect.y =  int(x), int(y) 
        ball.draw_circle()
        calculate_angle(start_time, ball.rect.x, ball.rect.y)
        
    if abs((int(y)//1)-550) == 0:
        animation = False
    screen.fill(WHITE)
    sprites.draw(screen)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()