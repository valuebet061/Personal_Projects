import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""A Class to represent a single alien in the fleet."""
	
	def __init__(self, ai_settings, screen):
		"""Initialize the alien and set its starting position."""
		super(Alien, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		#Load the alien image and set its rect attribute.
		self.image = pygame.image.load('D:\Program Files\Geany\Alien Game\Alien.bmp')
		alien_size = (70,60)
		self.image = pygame.transform.scale(self.image, alien_size)
		self.rect = self.image.get_rect()
		
		#start new alien near the top of the screen
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		
		#store exact position
		self.x = float(self.rect.x)
		
	def blitme(self):
		"""Actually drawing alien at current location."""
		self.screen.blit(self.image, self.rect)
	
	def check_edges(self):
		"""Return True if alien is at edge of the screen"""
		screen_rect = self.screen.get_rect() #grabs the "hitbox" of the entire screen
		if self.rect.right >= screen_rect.right: #if the alien's rect right is > than the hitbox
			return True
		elif self.rect.left <= 0: #checks if at left value?
			return True
		
	def update(self): #incremental updates each tick
		"""Move the alien right."""
		self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
		self.rect.x = self.x	
	
	
