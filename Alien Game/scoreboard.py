import pygame.font
import pygame.transform
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
	"""Class to report scoring info"""
	
	def __init__(self, ai_settings, screen, stats):
		"""Init scorekeeping attributs."""
		self.screen = screen
		self.screen_rect = screen.get_rect() #just grabing the hitbox
		self.ai_settings = ai_settings
		self.stats = stats
		
		#Font settings for scoring info
		self.text_color = (30,30,30)
		self.font = pygame.font.SysFont(None, 48)
		
		#prep score image.
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()
		
	def prep_ships(self):
		"""shows how many ship are left."""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_settings, self.screen)
				
			new_ship_size = (30,40)
			ship.image = pygame.transform.scale(ship.image, new_ship_size)
			ship.rect = ship.image.get_rect()
				
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship) #ADDINg to group ship
		
	def prep_level(self):
		"""Turnt he level into a rendered image"""
		self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)
		
		#position below the score
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right #mark the right as same as scoreboard
		self.level_rect.top = self.score_rect.bottom + 10 #right under the scoreboard
		
	def prep_score(self):
		"""Rendering score"""
		rounded_score = int(round(self.stats.score, -1)) #round to nearest 10s
		score_str = "{:,}".format(rounded_score) #turn into a string with ","s
		self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color) #pass through to render
		
		#Display the score at the top right of the screen.
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20 #adjusting 20 pixels from the right edge
		self.score_rect.top = 20
		
	def prep_high_score(self):
		"""Rendering Score"""
		high_score = int(round(self.stats.high_score, -1))
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)
		
		#display high score at top middle of screen
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.right = self.screen_rect.centerx #center x-axis
		self.high_score_rect.top = self.score_rect.top #match the score image
		
	def show_score(self):
		"""Draw score"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect) #drawing high_score
		self.screen.blit(self.level_image, self.level_rect) #drawing level
		self.ships.draw(self.screen) #drawing ships
