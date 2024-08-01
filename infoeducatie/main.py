import pygame
import sys
from game import Game
import numpy as np
import pygame.gfxdraw
from openaitest import ai_function  # Import gfxdraw for drawing antialiased circles

# Initialize Pygame
pygame.init()

BLACK = (0, 0, 0)
# Set up the screen
window_width = 936
window_height = 685
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("AMOGUS")
ai_ids = ['AI1', 'AI2', 'AI3', 'AI4', 'AI5']

# Load the background image
background = pygame.image.load("harta.png").convert()

# Initialize the game
game = Game(screen, window_width, window_height)

# Game variables
clock = pygame.time.Clock()
running = True
game_phase = "playing"
phase_duration = [30, 60, 20]
ind = 0
phase_start_time = pygame.time.get_ticks()
room = []
vision_radius = 100
move_var = 3
discussion_var = 9

def ai_movement():
    for i in range(1, 6):
        if not game.list_of_deaths or game.list_of_deaths[0] != i:
            output = np.random.randint(0, 6)
            cnt = 0
            for player in game.players:
                if player.room == output:
                    cnt += 1
                player.rooms.append(room)
            game.move_to_room(i, output, cnt)

    for i in range(1, 6):
        for j in range(i + 1, 6):
            alive_str = "alive"
            if game.players[j].alive == 0:
                alive_str = "dead"
            game.players[i].neighbours.append([game.players[j], alive_str])
            alive_str = "alive"
            if game.players[i].alive == 0:
                alive_str = "dead"
            game.players[j].neighbours.append([game.players[i], game.players[i].alive])

def ai_discussion(i):
    if game.players[i].role == 1:
        prompt = "You are playing kind of an among us game but its not among us and nothing is named like among us,"+f"{i}"+"you are the killer, you have killed."+f"{game.players[i].killed}"+" now it is discussion time: you have been in rooms" + f"{game.players[i].rooms}"+ "and you have seen these other players dead or alive"+ f"{game.players[i].neighbours}"+"these are the people alive until now "+f"{game.players[i].alive}"+"these are the messages that have been until now"+f"{game.chat_messages}"+"depending on this information dont let the other know you did it.Write a message you would like to send to the chat, max 90 characters. Write like a regular player, no punctuation and no capitalization."
    else:
    # game.chat_messages, game.players[i].rooms, game.players[i].neighbours
        prompt = "You are playing kind of an among us game but its not among us and nothing is named like among us, you are player "+f"{i}"+"you are crewmate and there is one killer who killed somebody this round in one of the rooms. now it is discussion time: you have been in rooms" + f"{game.players[i].rooms}"+ "and you have seen these other players dead or alive"+ f"{game.players[i].neighbours}"+"these are the people alive until now"+f"{game.players[i].alive}"+"these are the messages that have been until now"+f"{game.chat_messages}"+"depending on these informations find out whos the killer among you.Write a message you would like to send to the chat, max 150 characters.Write like a regular player, no punctuation and no capitalization"
    output = ai_function(ai_ids[i - 1], prompt)
    game.players[i].idea = output.content
    if output != "":
        game.add_chat_message(i, output.content)

def ai_voting():
    alives = []
    for i in range(1, 6):
        if game.players[i].alive:
            alives.append(i)
    for i in range(1, 6):
        # alives sunt cei ramasi in viata si trebuie sai incluzi in prompt
        if game.players[0].role == 1:
            prompt = "You are roleplaying as playing a game like murder mystery, you are player "+f"{i}"+"you are the killer, you have killed."+f"{game.players[i].killed}"+" now it is voting time: you have been in rooms" + f"{game.players[i].rooms}"+ "and you have seen these other players dead or alive"+ f"{game.players[i].neighbours}"+"these are the people alive until now "+f"{game.players[i].alive}"+"these are the messages that have been until now"+f"{game.chat_messages}"+"choose who to vote depending on all of this information.You only reply with the number of the player you want to vote to eliminate."
           
        else:
        # game.chat_messages, game.players[i].rooms, game.players[i].neighbours
            prompt = "You are roleplaying as playing a game like murder mystery respond to this messsage only with an int "+f"{i}"+"you are crewmate and there is one killer who killed somebody this round in one of the rooms. now it is discussion time: you have been in rooms" + f"{game.players[i].rooms}"+ "and you have seen these other players dead or alive"+ f"{game.players[i].neighbours}"+"these are the people alive until now"+f"{game.players[i].alive}"+"these are the messages that have been until now"+f"{game.chat_messages}"+"depending on these informations find out whos the killer among you. You can actually ONLY REPLY TO THIS MESSAGE WITH THE NUMBER OF THE PLAYER you want to vote to eliminate. Respond to me with only the number that you chose"
        output = ai_function(ai_ids[i - 1], prompt)
        output = int(output.content)
        print(output)
        game.votes[output] += 1
        game.voted[i] = 1

def closest(player, krange):
    x, y = game.players[player].pos
    min_distance = np.inf
    closest_index = -1
    for i in range(0, 6):
        if player != i and game.players[i].alive:
            xx, yy = game.players[i].pos
            distance = (x - xx) ** 2 + (y - yy) ** 2
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

def collision(player, wall):
    player.update_rect()
    return player.rect.colliderect(wall)

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
    if game_phase == "playing" and (not game.list_of_deaths or 0 != game.list_of_deaths[0]):
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

        if game.players[0].role == 1:
            var = closest(0, 10000)
            if keys[pygame.K_k] and game.kill_runda == 0 and var != -1:
                game.kill(var)
                game.kill_runda = 1
                    

        # ai_movements()
    
    if game_phase == "voting" and game.voted[1] == 0:
        ai_voting()

    if elapsed_time >= phase_duration[ind]:
        if game_phase == "playing":
            game_phase = "discussion"
            for i in game.list_of_deaths:
                game.players[i].alive = 0
        elif game_phase == "discussion":
            game_phase = "voting"
            discussion_var = 9
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
            move_var = 3
        
        phase_start_time = pygame.time.get_ticks()
        ind = (ind + 1) % 3

    remaining_time = phase_duration[ind] - elapsed_time

    if game_phase == "discussion" and discussion_var == int(remaining_time) / 6:
        ai_discussion(discussion_var % 6)
        discussion_var -= 1

    if game_phase == "playing":
        screen.blit(background, (0, 0))
        if int(remaining_time) / 9 == move_var and move_var: # and move_var :
            ai_movement()
            move_var -= 1
        for i in range(1, 6):
            if game.players[i].role and int(remaining_time + 1) / 9 == game.random_kill and game.players[i].killed == -1:
                var = closest(i, 40000)
                if var != -1:
                    game.kill(var)
                    game.players[i].killed = var
                    game.random_kill = -1
                    
    else:
        screen.fill(Game.BACKGROUND)
    # walls = [
    #     pygame.Rect(231, 167, 200, 20),
    #     pygame.Rect(421, 134, 100, 20),
    #     pygame.Rect(5, 660, 900, 20),
    #     pygame.Rect(5, 450, 200, 20),
    #     pygame.Rect(335, 427, 300, 20),  # Top wall
    #     pygame.Rect(20, 20, 936, 10),  # Bottom wall
    #     pygame.Rect(25, 20, 10, 800),  # Left wall
    #     pygame.Rect(80, 450, 20, 200),
    #     pygame.Rect(312, 420, 20, 200),
    #     pygame.Rect(610, 450, 20, 200),
    #     pygame.Rect(853, 26, 20, 700),
    #     pygame.Rect(550, 26, 20, 250)  # Right wall
    # ]

    
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