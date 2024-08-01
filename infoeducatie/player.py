import pygame 
import numpy as np

class Player(pygame.sprite.Sprite):
    def __init__(self, color, screen_width, screen_height, x, y, width, height, velocity, alive, role):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
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