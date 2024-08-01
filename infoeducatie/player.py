import pygame 
import numpy as np

class Player(pygame.sprite.Sprite):
    def __init__(self, color, screen_width, screen_height, x, y, width, height, velocity, alive, role, image):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image = pygame.image.load(image).convert()
        self.rect = self.image.get_rect()
        self.pos = np.array([x, y], dtype=np.float64)
        self.color = color
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width = width
        self.height = height
        self.vel = np.asarray(velocity, dtype=np.float64)
        self.alive = alive
        self.role = role
        self.room = -1
        self.idea = ""
        self.rooms = []
        self.neighbours = []
        self.killed = -1 # who the killer killed
        self.emotion = ""

    def update_rect(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.rect.width = self.width
        self.rect.height = self.height

    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, self.color, (self.pos[0], self.pos[1], self.width, self.height))
    
    def update(self):
        self.pos += self.vel
        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[1] < 0:
            self.pos[1] = 0
        
        if self.pos[0] + self.width > self.screen_width:
            self.pos[0] = self.screen_width - self.width
        if self.pos[1] + self.height > self.screen_height:
            self.pos[1] = self.screen_height - self.height