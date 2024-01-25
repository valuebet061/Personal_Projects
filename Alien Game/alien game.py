import sys
import pygame
from pygame.sprite import Group
from button import Button

from settings import Settings
from ship import Ship
from game_stats import GameStats
from scoreboard import Scoreboard
import game_functions as gf

def run_game():
	#creating screen
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width,
		ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")	
	
	#create play button
	play_button = Button(ai_settings, screen, "Play")
	
	#create instance to store game statistics
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
	
	#make a ship and group of aliens 
	ship = Ship(ai_settings, screen)	
	#make group to store bullets in.
	bullets = Group()
	#making Alien
	aliens = Group() #this holds all aliens
	
	#Create the fleet of aliens
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	#main loop for the game
	while True:
		#watch for keyboard and mouse events (from gf module)
		gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button) #adding each one, so each function updates
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets) #aliens + bullets (for collision) 
			gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets) #need ai_setings because it calls on someting from it, ship because of collision
			#need stats (in turn everything else)
			#removing disappeared bullets

		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)
			
run_game()
