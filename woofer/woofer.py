import pygame

# Confirm code is running
print("Program didn't crash. Yay!")

# Initialize pygame
pygame.init()

# Setup for sounds
pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.mixer.init()
  
# Load all sound files
outside_sound = pygame.mixer.Sound("outside.wav")
starwars_sound = pygame.mixer.Sound("StarWars60.wav")

#Play Outside Sound
# outside_sound.play()
starwars_sound.play()
