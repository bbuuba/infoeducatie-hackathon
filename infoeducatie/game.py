import pygame
import numpy as np
from player import Player

BLACK = (0, 0, 0)
rooms = [[200, 200], [400, 200], [600, 200], [200, 400], [400, 400], [600, 400]]

class Game:
    BACKGROUND = (0, 0, 0)

    def __init__(self, screen, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.players = []
        self.screen = screen
        self.killer = np.random.randint(0, 6)
        for i in range(6):
            x = window_width / 2 + i * 25
            y = window_height / 2
            w = 20
            h = 20
            role = 0
            color = (255, 255, 255)
            if i == self.killer:
                role = 1
                color = (255, 0, 0)
            player = Player(color, window_width, window_height, x, y, w, h, (0, 0), 1, role)
            self.players.append(player)
        self.font = pygame.font.Font(None, 36)
        self.chat_messages = []
        self.chat_input = ""
        self.chat_scroll_offset = 0
        self.chat_window_height = 500  # Height of the chat window
        self.votes = {i: 0 for i in range(len(self.players))}  # Track votes for each player
        self.voted = [False] * len(self.players)  # Track which players have voted
        self.kill_runda = 0
        self.list_of_deaths = []

    def kill(self, victim):
        self.players[victim].color = (200, 200, 50)
        self.list_of_deaths.append(victim)

    def restart_game_phase(self):
        # Reset players' positions and statuses for the next round
        for i in range(0, 6):
            self.players[i].pos = np.array([self.window_width / 2 + i * 25, self.window_height / 2], dtype=np.float64)
            self.players[i].vel = np.array([0, 0], dtype=np.float64)
            self.players[i].room = -1
            self.players[i].idea = ""
        self.votes = {i: 0 for i in range(len(self.players))}
        self.voted = [False] * len(self.players)
        self.kill_runda = 0
        

    def display_chat(self):
        # Render chat messages within a scrollable area
        chat_box = pygame.Rect(0, 0, self.window_width, self.chat_window_height)
        pygame.draw.rect(self.screen, (0, 0, 0), chat_box)
        pygame.draw.rect(self.screen, (255, 255, 255), chat_box, 2)

        # Render chat messages within the visible chat window
        y_offset = chat_box.y + self.chat_window_height - 40
        for message in reversed(self.chat_messages):
            text = self.font.render(message, True, (255, 255, 255))
            text_rect = text.get_rect(midleft=(chat_box.x + 10, y_offset))
            if y_offset < chat_box.y:
                break
            self.screen.blit(text, text_rect)
            y_offset -= 40
        
        # Render chat input box
        input_box = pygame.Rect(50, 50 + self.chat_window_height, 700, 50)
        pygame.draw.rect(self.screen, (255, 255, 255), input_box, 2)
        input_text = self.font.render(self.chat_input, True, (255, 255, 255))
        self.screen.blit(input_text, (input_box.x + 10, input_box.y + 5))

    def display_voting(self):
        # Render voting interface
        self.vote_rects = [] 
        y_offset = 50
        for i, player in enumerate(self.players):
            if player.alive:
                player_rect = pygame.Rect(50, y_offset, 700, 30)
                pygame.draw.rect(self.screen, (0, 0, 255), player_rect)
                text = self.font.render(f"Player{i+1}     {self.votes[i]}", True, (255, 255, 255))
                self.screen.blit(text, (player_rect.x + 10, player_rect.y + 5))
                self.vote_rects.append((player_rect, i))
                y_offset += 40

    def display_timer(self, remaining_time):
        timer_text = self.font.render(f"Time left: {int(remaining_time)}", True, (255, 255, 255))
        self.screen.blit(timer_text, (self.window_width - 200, 50))

    def add_chat_message(self, player, message):
        if message:
            self.chat_messages.append(f"Player{player}: {message}")
            message = ""
            if player == 0:
                self.chat_input = ""
            self.chat_scroll_offset = max(0, len(self.chat_messages) * 40 - self.chat_window_height)

    # Game Class

def ai_vote(self, player_index, vote_for):
    # Make sure the player has not already voted
    if not self.voted[player_index]:
        # Convert the vote_for to an integer, assuming it was passed as a string
        vote_for = int(vote_for)

        # Check if the chosen player is alive
        if self.players[vote_for].alive:
            # Register the vote
            self.votes[vote_for] += 1
            self.voted[player_index] = True  # Mark this player as having voted


    def handle_voting(self, mouse_pos):
        if not self.voted[0]:  # Assuming player 0 is the one voting
            for rect, player_index in self.vote_rects:
                if rect.collidepoint(mouse_pos):
                    self.votes[player_index] += 1
                    self.voted[0] = True  # Mark player 0 as voted
                    break
    def move_to_room(self, i, ind, cnt):
        self.players[i].pos[0] = rooms[ind][0] + cnt * 25
        self.players[i].pos[1] = rooms[ind][1]
        self.players[i].room = ind

    def loop(self, game_phase):
        if game_phase == "playing":
            for player in self.players:
                if player.alive:
                    player.update()
            for player in self.players:
                if player.alive: 
                    player.draw(self.screen)
        elif game_phase == "discussion":
            self.display_chat()
        elif game_phase == "voting":
            self.display_voting()