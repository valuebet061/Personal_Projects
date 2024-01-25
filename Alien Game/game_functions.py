import sys

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	"""Respond to keypresses."""
	if event.key == pygame.K_RIGHT:
		#moving ship to the right
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
		#Create a new bullet and add to group
	elif event.key == pygame.K_q:
		sys.exit()
		
def fire_bullet(ai_settings, screen, ship, bullets):
	"""Fire a bullet if limit not reached yet."""
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)
		
#turing check event to Kup + Kdown
def check_keyup_events(event, ship):
	"""Respond to Key releases"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets): #adding stats + play_button because stats needed to run play_button
	"""Respond to keypresses and mouse events."""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos() #create tuple of x,y coordinates
			check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
	"""Start a new game when the player clicks Play."""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y) #collide point to see if tuple of x/y is on the button
	if button_clicked and not stats.game_active: #if the game is active, then won't do anything if you click on the play button! SMART!
		#reset game settings
		ai_settings.initialize_dynamic_settings()
		#hide the mouse cursor.
		pygame.mouse.set_visible(False)
		#reset game stats
		stats.reset_stats()
		stats.game_active = True

		#reset scoreboard images.
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		
		#empty aliens + bullets list
		aliens.empty()
		bullets.empty()
		
		#create a new fleet and center the ship
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
	"""Update images on the screen and flip to the new screen."""
	screen.fill(ai_settings.bg_color)
	#Redraw all bullets behind ship and aliens.
	for bullet in bullets:
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	
	#Draw scoreboard
	sb.show_score()
	
	#Draw the play button if game is inactive.
	if not stats.game_active:
		play_button.draw_button()
	
	#displaying screen
	pygame.display.flip()
 
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Update position of bullets and get rid of old bullets."""
	#Update bullet positions
	bullets.update()
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	
	if len(aliens) == 0:
		bullets.empty() #destory bullets on screen
		ai_settings.increase_speed() #speed up game
		create_fleet(ai_settings, screen, ship, aliens) #create a new fleet
		
		#increase level
		stats.level += 1
		sb.prep_level()
		
	
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
	"""Check to see if there's a new high score."""
	if stats.score > stats.high_score: #check if score beat high_score
		stats.high_score = stats.score #overwriting old high score
		sb.prep_high_score()

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Respond to bullet/alien collisions"""
	#check for bullets that have hit aliens.
	# If so, get rid of bullet + alien.
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True) #True is to delete (pygame method)
	if collisions:
		for aliens in collisions.values(): #for each alien that has collision
			stats.score += ai_settings.alien_points * len(aliens) #so you get all the points if you hit more than one at a time
			sb.prep_score() #run prep score; to update scoreboard
		check_high_score(stats, sb) #check everytime you kill an alien
	
def get_number_aliens_x(ai_settings, alien_width): #how many fit in a row"
	"""Determine the number of aliens that fit in a row"""
	avaliable_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(avaliable_space_x / (2 * alien_width))
	return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
	"""Determine the number of rows of aliens that fit on the screen"""
	available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height) #determines space(y) avalibel to fit rows
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	alien.rect.x = alien.x
	aliens.add(alien)		

def check_fleet_edges(ai_settings, aliens):
	"""Resopnd appropriately if any aliens have reached an edge."""
	for alien in aliens.sprites(): #for each alien, we check if it hits edge
		if alien.check_edges():
			change_fleet_directions(ai_settings, aliens) # if we do, go to change_direction
			break #and break this loop at last alien

def change_fleet_directions(ai_settings, aliens):
	"""Drop the entire fleet and change the fleet's direction"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed #drop down
	ai_settings.fleet_direction *= -1 #changes fleet direction by *-1

def create_fleet(ai_settings, screen, ship, aliens):
	#create an alien and find number of aliens in a row.
	#spacing between each alien = 1 alien width
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
	
	#first row
	for row_number in range(number_rows): #for each number of rows calculated
		for alien_number in range(number_aliens_x): #add number = for each number of alien's per row calculated
		# Create an alien and place in the row
			create_alien(ai_settings, screen, aliens, alien_number, row_number)

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Respond to ship being hit by alien."""
	# Decrement ships_left.
	if stats.ships_left > 0:
		stats.ships_left -= 1 #decrease lives in increments of 1
		
		sb.prep_ships() #update sb
		
		#empty list of aliens and bullets when hit
		aliens.empty()
		bullets.empty()
		
		#create new fleet + ship in center
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		
		#Pause
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True) #mouse vsible, wherever end game switch is

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Check if hit bottom to screen"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			#treat same as ship hit
			ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
			break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets): #ai_settings for settings, aliens for the sprite
	"""Update the positions of all aliens in the fleet."""
	check_fleet_edges(ai_settings, aliens) #adding function to alien update
	aliens.update()

	#ship/alien collision
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

	check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
