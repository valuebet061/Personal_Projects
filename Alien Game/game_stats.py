import pygame

class GameStats():
	"""Tracking stats for Alien Invasion"""
	
	def __init__(self, ai_settings):
		"""Initialize"""
		#start game in an active state.
		self.game_active = False #just a flag to keep game "is going" will go down to loss (wait until start button)
		self.ai_settings = ai_settings
		self.reset_stats() #reset if player starts a new game
		self.high_score = 0 #high score does not reset, so keep outside of reset function
		
	def reset_stats(self):
		"""Initialize statistics taht can change during the game."""
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0 #put here because we want to make sure it resets
		self.level = 1
		
	
