#creating a place to store all settings for game

class Settings():
	def __init__(self):
		"""Initialzie the game's static settings"""
		#screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)
		
		#alien settings
		self.alien_speed_factor = 0.4
		self.fleet_drop_speed = 15
		#fleet direction of 1 represents right; -1 represents left
		self.fleet_direction = 1

		#ship settings
		self.ship_speed_factor = 0.50
		self.ship_limit = 3
		
		#bullet settings
		self.bullet_speed_factor = 1
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 60, 60, 60
		self.bullets_allowed = 3

		#speed up
		self.speedup_scale = 1.1
		
		#alien point values increase
		self.score_scale = 1.5
	
		self.initialize_dynamic_settings()
	
	def initialize_dynamic_settings(self): #mehod sets initial values for the ship
		"""Init settings taht change throughout the game"""
		self.ship_speed_factor = 0.5
		self.bullet_speed_factor = 1
		self.alien_speed_factor = 0.4
		self.fleet_direction = 1 #1 = right, -1 = left
		
		#scoring
		self.alien_points = 50 #how much each alien is worth; here because poitns when we reset
		
	def increase_speed(self):
		"""Increase speed settings + score"""
		self.ship_speed_factor *= self.speedup_scale #multiply everything by scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)
