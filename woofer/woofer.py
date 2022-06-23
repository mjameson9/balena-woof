import pygame
print("Program didn't crash. Yay!")

# Initialize pygame
pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init()

# Setup for sounds
pygame.mixer.init()
  
# Load all sound files
outside_sound = pygame.mixer.Sound("/data/my_data/sounds/outside.wav")

#Play Outside Sound
outside_sound.play()