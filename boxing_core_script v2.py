import random
import time
import pygame
import threading
from threading import Event
import inquirer
# ~ from tqdm import tqdm

#Boxing Callout program

# Basic moves to .wav
move_1 = r'D:\Steven\Documents\Boxing Program\New Vocals\1.mp3' #jab
move_2 = r'D:\Steven\Documents\Boxing Program\New Vocals\2.mp3' #'straight/cross'
move_3 = r'D:\Steven\Documents\Boxing Program\New Vocals\3.mp3' #'lead hook'
move_4 = r'D:\Steven\Documents\Boxing Program\New Vocals\4.mp3' #'rear hook'
move_5 = r'D:\Steven\Documents\Boxing Program\New Vocals\5.mp3' #'lead uppercut'
move_6 = r'D:\Steven\Documents\Boxing Program\New Vocals\6.mp3' #'rear uppercut'
move_7 = r'D:\Steven\Documents\Boxing Program\New Vocals\slip_right.mp3' #'slip right'
move_8 = r'D:\Steven\Documents\Boxing Program\New Vocals\slip_left.mp3' #'slip left'
move_9 = r'D:\Steven\Documents\Boxing Program\New Vocals\duck_right.mp3' #'duck right'i
move_10 = r'D:\Steven\Documents\Boxing Program\New Vocals\duck_left.mp3' #'duck left'
move_11 = r'D:\Steven\Documents\Boxing Program\New Vocals\1 1.mp3'
move_12 = r'D:\Steven\Documents\Boxing Program\New Vocals\1 2.mp3'
move_13 = r'D:\Steven\Documents\Boxing Program\New Vocals\1 1 2.mp3'
move_14 = r'D:\Steven\Documents\Boxing Program\New Vocals\2 3 2.mp3'
move_15 = r'D:\Steven\Documents\Boxing Program\New Vocals\3 4.mp3'
move_16 = r'D:\Steven\Documents\Boxing Program\New Vocals\5 2.mp3'
move_17 = r'D:\Steven\Documents\Boxing Program\New Vocals\4 1.mp3'

# Replace with your wav filenames

stop_event = Event()

def countdown(total_duration, stop_event):
  """Displays countdown timer in a separate thread"""
  start_time = time.time()
  while True:
    elapsed_time = time.time() - start_time
    remaining_time = int(total_duration - elapsed_time)
    mins, secs = divmod(remaining_time, 60)
    timer = '{:02d}:{:02d}'.format(mins, secs)
    print(timer, end="\r")
    time.sleep(1)
    if remaining_time <= 0:
        stop_event.set()
        break

def play_mp3(filename):
  """Plays an mp3 file using pygame"""
  pygame.mixer.init()
  pygame.mixer.music.load(filename)
  pygame.mixer.music.play()
  # Wait for music to finish (can be improved for long sounds)
  while pygame.mixer.music.get_busy():
    time.sleep(1)
  pygame.mixer.quit()

def play_random_groups(mp3_files, group_size_min, group_size_max, min_interval, max_interval, stop_event):
  """Plays random groups of mp3 files with random intervals between groups"""
  while not stop_event.is_set():
    # Shuffle the list for random order
    random.shuffle(mp3_files)
    # Select a random group size
    group_size = random.randint(group_size_min, group_size_max)
    # Play the selected group of files
    for i in range(group_size):
	    if i < len(mp3_files):  # Avoid index out of bounds
	        play_mp3(mp3_files[i])
    # Generate random wait time in milliseconds between groups
    wait_time = random.randint(min_interval, max_interval)
    time.sleep(wait_time/1000)  # Convert to seconds

# Replace with your mp3 filenames
mp3_files = [move_1, move_2, move_3, move_4, move_5, move_6, move_7, move_8, move_9, move_10, move_11,
    move_12, move_13, move_14, move_15, move_16, move_17]
# Minimum and maximum group size
group_size_min = 2
group_size_max = 4
# Minimum and maximum interval between groups (in milliseconds)
min_interval = 200  # 1 second
max_interval = 1000 # 5 seconds

# Set the timer duration in seconds
print("Please Select Workout Duration: ")
questions = [
  inquirer.List('duration',
                message="Please Select Workout Duration (secs): ",
                choices=['10', '30', '60', '90', '120', '150', '180'],
            ),
]
answers = inquirer.prompt(questions)
total_duration = answers["duration"]
total_duration = int(total_duration)

# Start the countdown thread
countdown_thread = threading.Thread(target=countdown, args=(total_duration, stop_event))
countdown_thread.start()
# Wait for the countdown thread to finish (optional)

# Run the other function concurrently
play_random_groups(mp3_files, group_size_min, group_size_max, min_interval, max_interval, stop_event)
countdown_thread.join()

# Exit pygame
pygame.quit()
bell_mp3 = r'D:\Steven\Documents\Boxing Program\boxing-bell.mp3'
play_mp3(bell_mp3)


