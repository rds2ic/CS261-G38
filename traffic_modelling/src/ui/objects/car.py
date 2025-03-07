import pygame
import customtkinter as ctk
import tkinter as tk

class Car:
    def __init__(self, x, y, width, height, direction, destination, image_path="assets/car.png"):
        self.image_path = image_path
        self.original_width = 118
        self.original_height = 72
        self.direction = direction
        
        # Direction to rotation mapping (degrees)
        self.rotation_map = {
            'W': 180,   
            'S': 270,   
            'E': 0,  
            'N': 90   
        }

        self.destination = destination
        
        # Load original image
        self.original_image = pygame.image.load(image_path)
        
        self.width = width
        self.height = height

        # Store position
        self.x = x
        self.y = y
        
        # Initial scaling and rotation setup
        self.image = self.scale_and_rotate_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
    
    def scale_and_rotate_image(self):
        """Scale and rotate the car image based on direction"""
        # First rotate based on direction
        rotation_angle = self.rotation_map[self.direction]
        rotated_image = pygame.transform.rotate(self.original_image, rotation_angle)
        
        # Then scale the rotated image
        scale_factor = min(self.width / 1000, self.height / 1000)
        new_width = int(self.original_width * scale_factor)
        new_height = int(self.original_height * scale_factor)
        return pygame.transform.scale(rotated_image, (new_width, new_height))
    
    def update_position(self, x, y):
        """Update the car's position"""
        self.x = x
        self.y = y
        self.rect.center = (x, y)
    
    def move(self, dx, dy):
        """Move the car by the given delta values"""
        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)
    
    def go_destination(self, speed=5):
        """Handle car movement and turning based on current direction and destination"""
        speed = speed * self.width / self.height if self.direction in ['W', 'E'] else speed * self.height / self.width
        
        if self.direction == 'W':
            if self.destination == 'N' and self.x < self.width//2 - self.rect[2] - 15:
                self.direction = 'N'
                self.move(0, -speed)
            elif self.destination == 'S' and self.x < self.width//2 + 25:
                self.direction = 'S'
                self.move(0, speed)
            else:
                self.move(-speed, 0)

        elif self.direction == 'E':
            if self.destination == 'N' and self.x > self.width//2 - self.rect[2] - 25:
                self.direction = 'N'
                self.move(0, -speed)
            elif self.destination == 'S' and self.x > self.width//2 + 25:
                self.direction = 'S'
                self.move(0, speed)
            else:
                self.move(speed, 0)

        elif self.direction == 'S':
            if self.destination == 'E' and self.y > self.height//2 - 90:
                self.direction = 'E'
                self.move(speed, 0)
            elif self.destination == 'W' and self.y > self.height//2 + 50:
                self.direction = 'W'
                self.move(-speed, 0)
            else:
                self.move(0, speed)

        elif self.direction == 'N':
            if self.destination == 'E' and self.y < self.height//2 - 80:
                self.direction = 'E'
                self.move(speed, 0)
            elif self.destination == 'W' and self.y < self.height//2 + 50:
                self.direction = 'W'
                self.move(-speed, 0)
            else:
                self.move(0, -speed)
    
    def update_image(self):
        # Rescale and rotate image based on current frame dimensions
        self.image = self.scale_and_rotate_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
    
    def draw(self, surface):
        self.update_image()
        
        # Draw the car
        surface.blit(self.image, self.rect)
    
    def out_of_bounds(self):
        if self.x < 0 and self.destination == 'W':
            return True
        if self.x > 800 and self.destination == 'E':
            return True
        if self.y < 0 and self.destination == 'N':
            return True
        if self.y > 600 and self.destination == 'S':
            return True
        return False