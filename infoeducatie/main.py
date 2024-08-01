import pygame
import sys
from game import Game
import numpy as np
import pygame.gfxdraw
from openaitest import *  # Import gfxdraw for drawing antialiased circles

# Initialize Pygame
pygame.init()

# Set up the screen
window_width = 800
window_height = 800
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("AMOGUS")

# Load the background image
background = pygame.image.load("map.png").convert()

# Initialize the game
game = Game(screen, window_width, window_height)

# Game variables
clock = pygame.time.Clock()
running = True
game_phase = "playing"  # Game phases: "playing", "discussion", "voting"
phase_duration = 10  # 10 seconds for demo purposes
phase_start_time = pygame.time.get_ticks()
krange = 10000
vision_radius = 100  # Radius of the vision circle
move_var = 1
discussion_var = 1

def ai_movement():
    for i in range(1, 6):
        output = np.random.randint(0,5)
        cnt = 0
        for player in game.players:
            if player.room == output:
                cnt += 1
        game.move_to_room(i, output, cnt)

def ai_discussion(i):
    # for i in range(1, 6):
    output = "wtf-nigger"
    game.players[i].idea = output
    if output != "":
        game.add_chat_message(i, output)

def ai_voting(i):
    # AI players decide whom to vote for
    output="2"
    game.players[i].vote=output
    for i in range(1, 6):  # Assuming player 0 is the user
        if game.players[i].alive:
            game.ai_vote(i,output)



def closest(player):
    x, y = game.players[player].pos
    min_distance = np.inf
    closest_index = -1
    for i in range(0, 6):
        if player != i and game.players[i].alive:
            xx, yy = game.players[i].pos
            distance = (x - xx) * 2 + (y - yy) * 2
            if distance < min_distance:
                min_distance = distance
                closest_index = i

    if min_distance > krange:
        closest_index = -1
    return closest_index

def draw_vision_mask(player):
    # Create a new surface with SRCALPHA for transparency
    mask = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 255))  # Fill the mask with opaque black

    # Center of the player
    player_center = player.pos + np.array([player.width // 2, player.height // 2])

    # Draw a transparent circle around the player to represent their vision
    pygame.gfxdraw.filled_circle(mask, int(player_center[0]), int(player_center[1]), vision_radius, (0, 0, 0, 0))
    pygame.gfxdraw.aacircle(mask, int(player_center[0]), int(player_center[1]), vision_radius, (0, 0, 0, 0))

    # Blit the mask onto the screen
    screen.blit(mask, (0, 0))

while running:
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - phase_start_time) / 1000  # Convert to seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.KEYDOWN:
            if game_phase == "discussion":
                if event.key == pygame.K_RETURN:
                    game.add_chat_message(0, game.chat_input)  # Assuming Player 1 is the user
                elif event.key == pygame.K_BACKSPACE:
                    game.chat_input = game.chat_input[:-1]
                else:
                    game.chat_input += event.unicode
                if event.key == pygame.K_UP:
                    game.chat_scroll_offset = max(0, game.chat_scroll_offset - 40)
                elif event.key == pygame.K_DOWN:
                    game.chat_scroll_offset = min(len(game.chat_messages) * 40 - game.chat_window_height, game.chat_scroll_offset + 40)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_phase == "voting":
                mouse_pos = pygame.mouse.get_pos()
                game.handle_voting(mouse_pos)

    keys = pygame.key.get_pressed()
    if game_phase == "playing":
        if keys[pygame.K_w]:
            game.players[0].vel[1] = -5
        elif keys[pygame.K_s]:
            game.players[0].vel[1] = 5
        else:
            game.players[0].vel[1] = 0

        if keys[pygame.K_a]:
            game.players[0].vel[0] = -5
        elif keys[pygame.K_d]:
            game.players[0].vel[0] = 5
        else:
            game.players[0].vel[0] = 0

        if game.players[0].role == 0:
            var = closest(0)
            if keys[pygame.K_k] and game.kill_runda == 0 and var != -1:
                game.kill(var)
                game.kill_runda = 1

        # ai_movements()

    if elapsed_time >= phase_duration:
        if game_phase == "playing":
            game_phase = "discussion"
            for i in game.list_of_deaths:
                game.players[i].alive = 0
        elif game_phase == "discussion":
            game_phase = "voting"
            discussion_var = 1
        elif game_phase == "voting":
            maxi = 0
            ok = -1
            for i in range(0, 6):
                if game.votes[i] > maxi:
                    maxi = game.votes[i]
                    ok = i
                elif game.votes[i] == maxi:
                    ok = -1
            if ok != -1:
                game.players[ok].alive = 0

            game_phase = "playing"
            game.restart_game_phase()
            move_var = 1
        
        phase_start_time = pygame.time.get_ticks()

    remaining_time = phase_duration - elapsed_time
    
    if game_phase == "discussion" and discussion_var:
        ai_discussion(1)
        discussion_var = 0

    # Draw the background image
    if game_phase == "playing":
        screen.blit(background, (0, 0))
        if int(remaining_time) == 5 and move_var:
            ai_movement()
            move_var = 0
            print(int(remaining_time))
    else:
        screen.fill(Game.BACKGROUND)
    

    # Update and render the game
    game.loop(game_phase)

    # Draw the vision mask for player 0
    if game_phase == "playing":
        draw_vision_mask(game.players[0])
    game.display_timer(remaining_time)

    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()