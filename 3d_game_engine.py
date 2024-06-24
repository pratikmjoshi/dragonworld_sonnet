import pygame
from pygame.math import Vector3
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math
import models
import cProfile

class Dragon:
    def __init__(self, position, is_friendly):
        self.position = position
        self.is_friendly = is_friendly

class Player:
    def __init__(self):
        self.position = Vector3(0, 1.7, 0)  # Eye level
        self.yaw = 0
        self.pitch = 0

    def update_rotation(self, dx, dy):
        sensitivity = 0.1
        self.yaw -= dx * sensitivity
        self.pitch += dy * sensitivity
        self.pitch = max(-89, min(89, self.pitch))  # Clamp pitch

    def move(self, forward, right):
        # Calculate forward and right vectors based on yaw
        yaw_rad = math.radians(self.yaw)
        forward_vec = Vector3(math.sin(yaw_rad), 0, -math.cos(yaw_rad))
        right_vec = Vector3(math.cos(yaw_rad), 0, math.sin(yaw_rad))

        # Move the player
        self.position += forward * forward_vec + right * right_vec
        self.position.y = 1.7  # Keep the player at a constant height

class GameEngine:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption("3D Magical World")
        self.clock = pygame.time.Clock()
        self.is_running = True

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (width / height), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Set to black or another dark color

        self.setup_lighting()

        self.player = Player()
        self.friendly_dragons = []
        self.hostile_dragons = []
        self.init_dragons()
        models.create_dragon_display_lists()

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

    def init_dragons(self):
        for _ in range(5):  # 5 friendly dragons
            position = Vector3(
                random.uniform(-10, 10),
                1.0,  # Floating 0.5 units above the ground
                random.uniform(-10, 10)
            )
            self.friendly_dragons.append(Dragon(position, True))

        for _ in range(5):  # 5 hostile dragons
            position = Vector3(
                random.uniform(-10, 10),
                1.0,  # Floating 0.5 units above the ground
                random.uniform(-10, 10)
            )
            self.hostile_dragons.append(Dragon(position, False))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False

        # Mouse movement for camera control
        dx, dy = pygame.mouse.get_rel()
        self.player.update_rotation(dx, dy)

        # Keyboard input for movement
        keys = pygame.key.get_pressed()
        move_speed = 0.1
        forward = (keys[pygame.K_w] - keys[pygame.K_s]) * move_speed
        right = (keys[pygame.K_d] - keys[pygame.K_a]) * move_speed
        self.player.move(forward, right)

    def update(self):
        pass

    def setup_lighting(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        
        # Set up a bright white light
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.4, 0.4, 0.4, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
        
        # Position the light above and slightly behind the viewer
        glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 10.0, 5.0, 1.0))

        # Add some global ambient light
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.2, 0.2, 0.2, 1.0))

        # Disable lighting for ground
        glDisable(GL_LIGHTING)
        glDisable(GL_COLOR_MATERIAL)


    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Apply player rotation and position
        glRotatef(self.player.pitch, 1, 0, 0)
        glRotatef(self.player.yaw, 0, 1, 0)
        glTranslatef(-self.player.position.x, -self.player.position.y, -self.player.position.z)

        # Render ground
        glBegin(GL_QUADS)
        glColor3f(0.0, 0.5, 0.0)
        glVertex3f(-10, 0, -10)
        glVertex3f(-10, 0, 10)
        glVertex3f(10, 0, 10)
        glVertex3f(10, 0, -10)
        glEnd()

        # Enable lighting for dragons
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        # Disable lighting for dragons temporarily
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)

        # Render dragons
        for dragon in self.friendly_dragons + self.hostile_dragons:
            glPushMatrix()
            glTranslatef(dragon.position.x, dragon.position.y, dragon.position.z)
            glScalef(0.3, 0.3, 0.3)
            if dragon.is_friendly:
                glCallList(models.friendly_dragon_list)
            else:
                glCallList(models.hostile_dragon_list)
            glPopMatrix()

        pygame.display.flip()

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = GameEngine()
    game.run()
    # cProfile.run('game.run()')