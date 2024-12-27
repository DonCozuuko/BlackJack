import pygame as pg
from button import Button
import os
import random as r
import time as t
PATH = r"c:\Users\J1R\Documents\Personal\Code Projects\Projects\Python Projects"
os.chdir(PATH)
# Window stuff
pg.init()
pg.font.init()
WIN_SIZE = (1280, 720)
WIDTH, HEIGHT = WIN_SIZE
SCREEN = pg.display.set_mode(WIN_SIZE)
bg = pg.image.load("BlackJack/black_felt_table.jpg")
BG = pg.transform.scale(bg, (1280, 720))

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (125, 125, 125)

# Resources
CARDS = []
for card in os.listdir("BlackJack/Cards"):
    CARDS.append(card)

BACK_OF_CARD = pg.image.load("BlackJack/Cards/d.png")
BACK_OF_CARD_RECT = BACK_OF_CARD.get_rect(center = (WIDTH // 2 + 90, HEIGHT // 2 - 200))

FAIL_SOUND = pg.mixer.Sound("BlackJack/fail_sound.mp3")
WIN_SOUND = pg.mixer.Sound("BlackJack/pvz_jingle.mp3")
# Variables
BET_AMNT = 0
PLAYERS_HAND = 0
DEALERS_HAND = 0

# Helper functions
def get_font(size):
    return pg.font.SysFont(None, size)


class Game:
    def __init__(self, start_menu):
        self.start_menu = start_menu

        self.display_hand = None
        self.Pcard1_chosen = None
        self.Pcard2_chosen = None
        self.Dcard1_chosen = None
        self.Dcard2_chosen = None
        self.new_card = None
        self.Pcard1_x = WIDTH
        self.Pcard2_x = WIDTH
        self.Dcard1_x = WIDTH
        self.Dcard2_x = WIDTH
        self.new_card_x = WIDTH
        self.max_dist = WIDTH
        self.end_of_drawing_seq = None
        self.animation_speed = 16
        self.Pcards_chosen = [self.Pcard1_chosen, self.Pcard2_chosen]
        self.Dcards_chosen = [self.Dcard1_chosen, self.Dcard2_chosen]
        self.countdown = False
        self.show_bust = False
        self.show_win = False
        self.show_lose = False
        self.player_init = False
        self.dealer_init = False
        self.dealer_stand = False
    
    def reset_game_state(self):
        global BET_AMNT, PLAYERS_HAND, DEALERS_HAND
        BET_AMNT = 0
        PLAYERS_HAND = 0
        DEALERS_HAND = 0
        self.display_hand = None
        self.Pcard1_chosen = None
        self.Pcard2_chosen = None
        self.Dcard1_chosen = None
        self.Dcard2_chosen = None
        self.new_card = None
        self.Pcard1_x = WIDTH
        self.Pcard2_x = WIDTH
        self.Dcard1_x = WIDTH
        self.Dcard2_x = WIDTH
        self.new_card_x = WIDTH
        self.max_dist = WIDTH
        self.end_of_drawing_seq = None
        self.animation_speed = 16
        self.Pcards_chosen = [self.Pcard1_chosen, self.Pcard2_chosen]
        self.Dcards_chosen = [self.Dcard1_chosen, self.Dcard2_chosen]
        self.countdown = False
        self.show_bust = False
        self.show_win = False
        self.show_lose = False
        self.player_init = False
        self.dealer_init = False
        self.dealer_stand = False

    def draw_bet_state(self):
        onek = pg.image.load("BlackJack/1k_chip.png")
        onek_chip = pg.transform.scale(onek, (160, 160))
        self.onek_rect = onek_chip.get_rect()
        self.onek_rect.center = (150, HEIGHT // 2)

        fiveh = pg.image.load("BlackJack/5h_chip.png")
        fiveh_chip = pg.transform.scale(fiveh, (160, 160))
        self.fiveh_chip_rect = fiveh_chip.get_rect()
        self.fiveh_chip_rect.center = (395, HEIGHT // 2)

        oneh = pg.image.load("BlackJack/1h_chip.png")
        oneh_chip = pg.transform.scale(oneh, (160, 160))
        self.oneh_chip_rect = oneh_chip.get_rect()
        self.oneh_chip_rect.center = (WIDTH // 2, HEIGHT // 2)

        vingt_five = pg.image.load("BlackJack/25_chip.png")
        vingt_five_chip = pg.transform.scale(vingt_five, (160, 160))
        self.vingt_five_chip_rect = vingt_five_chip.get_rect()
        self.vingt_five_chip_rect.center = (885, HEIGHT // 2)

        five = pg.image.load("BlackJack/5_chip.png")
        five_chip = pg.transform.scale(five, (160, 160))
        self.five_chip_rect = five_chip.get_rect()
        self.five_chip_rect.center = (1130, HEIGHT // 2)

        text1 = get_font(60).render("Place your bet:", True, WHITE)
        text1_rect = text1.get_rect()
        text1_rect.center = (WIDTH // 2, HEIGHT // 2)
        text1_rect.top = 30

        text2 = get_font(60).render("Lock in bet", True, WHITE)
        self.text2_rect = text2.get_rect()
        self.text2_rect.center = (WIDTH // 2, HEIGHT // 2)
        self.text2_rect.top = 200

        SCREEN.blit(text2, self.text2_rect)
        SCREEN.blit(text1, text1_rect)
        SCREEN.blit(five_chip, self.five_chip_rect)
        SCREEN.blit(vingt_five_chip, self.vingt_five_chip_rect)
        SCREEN.blit(oneh_chip, self.oneh_chip_rect)
        SCREEN.blit(fiveh_chip, self.fiveh_chip_rect)
        SCREEN.blit(onek_chip, self.onek_rect)


    def display_bet_amnt(self):
        amount = get_font(60).render(f"{BET_AMNT}", True, WHITE)
        rect = amount.get_rect()
        rect.center = (WIDTH // 2, HEIGHT // 2)
        rect.top = 100
        SCREEN.blit(amount, rect)


    def bet_state(self):
        global BET_AMNT
        while True:
            
            SCREEN.blit(BG, (0, 0))
            MOUSE_POS = pg.mouse.get_pos()
            X_POS, Y_POS = MOUSE_POS

            Game.draw_bet_state(self)
            Game.display_bet_amnt(self)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                if event.type == pg.MOUSEBUTTONDOWN and X_POS in range(self.onek_rect.left, self.onek_rect.right) and Y_POS in range(self.onek_rect.top, self.onek_rect.bottom):
                    BET_AMNT += 1000
                elif event.type == pg.MOUSEBUTTONDOWN and X_POS in range(self.fiveh_chip_rect.left, self.fiveh_chip_rect.right) and Y_POS in range(self.fiveh_chip_rect.top, self.fiveh_chip_rect.bottom):
                    BET_AMNT += 500
                elif event.type == pg.MOUSEBUTTONDOWN and X_POS in range(self.oneh_chip_rect.left, self.oneh_chip_rect.right) and Y_POS in range(self.oneh_chip_rect.top, self.oneh_chip_rect.bottom):
                    BET_AMNT += 100
                elif event.type == pg.MOUSEBUTTONDOWN and X_POS in range(self.vingt_five_chip_rect.left, self.vingt_five_chip_rect.right) and Y_POS in range(self.vingt_five_chip_rect.top, self.vingt_five_chip_rect.bottom):
                    BET_AMNT += 25
                elif event.type == pg.MOUSEBUTTONDOWN and X_POS in range(self.five_chip_rect.left, self.five_chip_rect.right) and Y_POS in range(self.five_chip_rect.top, self.five_chip_rect.bottom):
                    BET_AMNT += 5
                elif event.type == pg.MOUSEBUTTONDOWN and X_POS in range(self.text2_rect.left, self.text2_rect.right) and Y_POS in range(self.text2_rect.top, self.text2_rect.bottom):
                    return

            pg.display.update()

    
    def drawing_cards_scene(self):
        if self.Pcard1_chosen == None and self.Pcard2_chosen == None:
            shuffle1 = r.randint(0, 51)
            shuffle2 = r.randint(0, 51)
            shuffle3 = r.randint(0, 51)
            shuffle4 = r.randint(0, 51)
            self.Pcard1_chosen = CARDS[shuffle1]
            self.Pcard2_chosen = CARDS[shuffle2]
            self.Dcard1_chosen = CARDS[shuffle3]
            self.Dcard2_chosen = CARDS[shuffle4]
            self.Pcard1_x = WIDTH
            self.Pcard2_x = WIDTH
            self.Dcard1_x = WIDTH
            self.Dcard2_x = WIDTH
            self.blank_card_x = WIDTH

        self.card_images = [
            pg.image.load(f"BlackJack/Cards/{self.Pcard1_chosen}"),
            pg.image.load(f"BlackJack/Cards/{self.Dcard1_chosen}"),
            pg.image.load(f"BlackJack/Cards/{self.Pcard2_chosen}"),
            pg.image.load(f"BlackJack/Cards/{self.Dcard2_chosen}")
        ]

        self.card_rects = [ 
            self.card_images[0].get_rect(center = (WIDTH // 2 - 90, HEIGHT // 2 + 200)),
            self.card_images[1].get_rect(center = (WIDTH // 2 - 90, HEIGHT // 2 - 200)),
            self.card_images[2].get_rect(center = (WIDTH // 2 + 90, HEIGHT // 2 + 200)),
            self.card_images[3].get_rect(center = (WIDTH // 2 + 90, HEIGHT // 2 - 200))
        ]

        self.positions = [
            self.Pcard1_x, self.Dcard1_x, self.Pcard2_x, self.Dcard2_x
        ]

        self.destinations = [
            self.card_rects[0].x, self.card_rects[1].x, self.card_rects[2].x, self.card_rects[3].x
        ]


    def first_card(self):
        dist = abs(self.positions[0] - self.destinations[0])
        speed = max(2, 500 * (dist / self.max_dist) ** 2 + 60 * (dist / self.max_dist))
        if self.positions[0] > self.destinations[0]:
            self.positions[0] -= speed
        
        else:
            self.positions[0] = self.destinations[0]
        
        SCREEN.blit(self.card_images[0], (self.positions[0], self.card_rects[0].y))
        
        return self.positions[0] == self.destinations[0]


    def second_card(self):
        dist = abs(self.positions[1] - self.destinations[1])
        speed = max(2, 500 * (dist / self.max_dist) ** 2 + 60 * (dist / self.max_dist))
        if self.positions[1] > self.destinations[1]:
            self.positions[1] -= speed
        
        else:
            self.positions[1] = self.destinations[1]
        
        SCREEN.blit(self.card_images[1], (self.positions[1], self.card_rects[1].y))

        return self.positions[1] == self.destinations[1]


    def third_card(self):
        dist = abs(self.positions[2] - self.destinations[2])
        speed = max(2, 500 * (dist / self.max_dist) ** 2 + 60 * (dist / self.max_dist))
        if self.positions[2] > self.destinations[2]:
            self.positions[2] -= speed
        else:
            self.positions[2] = self.destinations[2]
        
        SCREEN.blit(self.card_images[2], (self.positions[2], self.card_rects[2].y))

        return self.positions[2] == self.destinations[2]


    def blank_card(self):
        dist = abs(self.blank_card_x - BACK_OF_CARD_RECT.x)
        speed = max(2, 500 * (dist / self.max_dist) ** 2 + 60 * (dist / self.max_dist))
        if self.blank_card_x > BACK_OF_CARD_RECT.x:
            self.blank_card_x -= speed
        
        else:
            self.blank_card_x = BACK_OF_CARD_RECT.x
        
        SCREEN.blit(BACK_OF_CARD, (self.blank_card_x, BACK_OF_CARD_RECT.y))

        return self.blank_card_x == BACK_OF_CARD_RECT.x


    def get_card_value(self, card, face_value, face_cards):
        if card is None:  # Safeguard against NoneType
            raise ValueError("Card is None. Ensure it is properly initialized before calling get_card_value.")
        
        card_value = card[-5]
        if card_value in face_value:
            if card_value == '0':
                return int(10)
            return int(card_value)
        elif card_value in face_cards:
            return 10
        elif card_value == 'A':
            return 11


    def calc_hand_value(self):
        global PLAYERS_HAND
        global DEALERS_HAND

        PLAYERS_HAND = 0
        DEALERS_HAND = 0
        self.face_value = ['2', '3', '4', '5', '6', '7', '8', '9', '0']
        self.face_cards = ['J', 'Q', 'K']

        PLAYERS_HAND += self.get_card_value(self.Pcard1_chosen, self.face_value, self.face_cards)
        PLAYERS_HAND += self.get_card_value(self.Pcard2_chosen, self.face_value, self.face_cards)

        DEALERS_HAND += self.get_card_value(self.Dcard1_chosen, self.face_value, self.face_cards)



    def draw_new_card(self, num_cards):
        # Shuffle a card (random index)
        n_shuffle = r.randint(0, 51)
        
        # Get card name and initialize the image
        self.new_card_name = CARDS[n_shuffle]  # Store the name for reference
        self.new_card_img = pg.image.load(f"BlackJack/Cards/{self.new_card_name}")
        
        # Define the card's position (adjust position based on `num_cards`)
        self.new_card_x = WIDTH  # Set initial position off the screen
        self.new_card_rect = self.new_card_img.get_rect(center = (WIDTH // 2 + (90 * num_cards), HEIGHT // 2 + 200))
        
        # Append the new card's data to the respective lists
        self.player_positions.append(self.new_card_x)  # Add the new card's initial position
        self.player_card_images.append(self.new_card_img)  # Add the new card's image
        self.player_card_rects.append(self.new_card_rect)  # Add the new card's rect

    def hit_update_elements(self):
        text = get_font(40).render("Your Bet:", True, WHITE)
        text_rect = text.get_rect()
        text_rect.bottomleft = (0, 320)

        self.p_hand = get_font(40).render(f"{PLAYERS_HAND}", True, WHITE)
        SCREEN.blit(self.p_hand, self.p_hand_rect)

        amount = get_font(40).render(f"{BET_AMNT}", True, WHITE)
        amount_rect = amount.get_rect()
        amount_rect.bottomleft = (0, 360)
        SCREEN.blit(amount, amount_rect)
        SCREEN.blit(text, text_rect)
        SCREEN.blit(self.d_hand, self.d_hand_rect)
        SCREEN.blit(self.card_images[1], (self.positions[1], self.card_rects[1].y))
        SCREEN.blit(BACK_OF_CARD, (self.blank_card_x, BACK_OF_CARD_RECT.y))
  
    def hit(self):
        global PLAYERS_HAND
        # Ensure player_positions and related lists are initialized only once
        if not self.player_init:
            # Set the initial player positions when the game starts
            self.player_positions = [480, 660]  # Starting positions
            self.player_card_images = [self.card_images[0], self.card_images[2]]
            self.player_card_rects = [self.card_rects[0], self.card_rects[2]]
            self.new_card = None
            self.player_init = True

        run = True
        while run:
            SCREEN.blit(BG, (0, 0))
            self.hit_update_elements()
            
            # Animate all cards with dynamic spacing
            for i in range(len(self.player_positions)):
                # Adjust target position based on the number of cards and 180-pixel spacing
                target_x = self.player_card_rects[0].x + (i * 180)

                if self.player_positions[i] > target_x:
                    self.player_positions[i] = max(self.player_positions[i] - self.animation_speed, target_x)
                else:
                    self.player_positions[i] = min(self.player_positions[i] + self.animation_speed, target_x)

                SCREEN.blit(self.player_card_images[i], (self.player_positions[i], self.player_card_rects[i].y))

            # Add a new card if needed
            if self.new_card is None:
                self.draw_new_card(len(self.player_positions))
                self.new_card = True
                self.Pcards_chosen.append(self.new_card_name)
                PLAYERS_HAND += self.get_card_value(self.new_card_name, self.face_value, self.face_cards)


            # Check for animation completion
            all_cards_aligned = True
            for i in range(len(self.player_positions)):
                target_x = self.player_card_rects[0].x + (i * 180)
                if abs(self.player_positions[i] - target_x) > self.animation_speed:
                    all_cards_aligned = False
                    break

            if all_cards_aligned:
                # print("Player positions:", self.player_positions)
                # print("rects:", self.player_card_rects)
                # print("Number of cards:", len(self.player_positions) - 2)
                # print("Updated Player Hand Value:", PLAYERS_HAND)
                self.new_card = None
                run = False

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            pg.display.update()


    def stand_update_elements(self):
        text = get_font(40).render("Your Bet:", True, WHITE)
        text_rect = text.get_rect()
        text_rect.bottomleft = (0, 320)

        self.p_hand = get_font(40).render(f"{PLAYERS_HAND}", True, WHITE)
        SCREEN.blit(self.p_hand, self.p_hand_rect)

        amount = get_font(40).render(f"{BET_AMNT}", True, WHITE)
        amount_rect = amount.get_rect()
        amount_rect.bottomleft = (0, 360)
        SCREEN.blit(amount, amount_rect)
        SCREEN.blit(text, text_rect)
        SCREEN.blit(self.d_hand, self.d_hand_rect)
        
    
    def draw_new_card2(self, num_cards):
        n_shuffle = r.randint(0, 51)

        self.new_card_name = CARDS[n_shuffle]  
        self.new_card_img = pg.image.load(f"BlackJack/Cards/{self.new_card_name}")

     
        new_x = 640 + (90 * num_cards)  
        new_y = HEIGHT // 2 - 200 
        self.new_card_rect = self.new_card_img.get_rect(center=(new_x, new_y))

        self.dealer_positions.append(new_x)  
        self.dealer_card_images.append(self.new_card_img)
        self.dealer_card_rects.append(self.new_card_rect)

    def stand_update_elements(self):
        text = get_font(40).render("Your Bet:", True, WHITE)
        text_rect = text.get_rect()
        text_rect.bottomleft = (0, 320)

        self.p_hand = get_font(40).render(f"{PLAYERS_HAND}", True, WHITE)
        SCREEN.blit(self.p_hand, self.p_hand_rect)

        amount = get_font(40).render(f"{BET_AMNT}", True, WHITE)
        amount_rect = amount.get_rect()
        amount_rect.bottomleft = (0, 360)
        SCREEN.blit(amount, amount_rect)
        SCREEN.blit(text, text_rect)
        SCREEN.blit(self.d_hand, self.d_hand_rect)

    def stand(self):
        global DEALERS_HAND
        if not self.player_init:
            # Set the initial player positions when the game starts
            self.player_positions = [480, 660]  # Starting positions
            self.player_card_images = [self.card_images[0], self.card_images[2]]
            self.player_card_rects = [self.card_rects[0], self.card_rects[2]]
            self.new_card = None
            self.player_init = True

            self.dealer_positions = [480, 660]  # Dealer cards row
            self.dealer_card_images = [self.card_images[1], self.card_images[3]]
            self.dealer_card_rects = [self.card_rects[1], self.card_rects[3]]
            DEALERS_HAND = 0  # Initialize dealer's hand value

        if not hasattr(self, 'dealer_init'):
            self.dealer_init = False
        if not hasattr(self, 'd_hand'):
            self.d_hand = None
        if not hasattr(self, 'd_hand_rect'):
            self.d_hand_rect = None

        run = True
        while run:
            SCREEN.blit(BG, (0, 0))

            # Reveal the upside card (first dealer card)
            if not self.dealer_init:
                DEALERS_HAND += self.get_card_value(
                    self.Dcard2_chosen, self.face_value, self.face_cards
                )
                self.d_hand = get_font(40).render(f"{DEALERS_HAND}", True, WHITE)
                self.d_hand_rect = self.d_hand.get_rect()
                self.d_hand_rect.bottomright = (1220, 320)
                SCREEN.blit(self.d_hand, self.d_hand_rect)
                self.dealer_init = True

            self.stand_update_elements()
            for i in range(len(self.player_positions)):
                SCREEN.blit(self.player_card_images[i], (self.player_positions[i], self.player_card_rects[i].y))

            # Display dealer's current cards
            for i in range(len(self.dealer_card_images)):
                SCREEN.blit(self.dealer_card_images[i], self.dealer_card_rects[i])

            # Dealer draws until reaching 17 or higher
            if DEALERS_HAND < 17:
                self.draw_new_card2(len(self.dealer_card_images))
                self.Dcards_chosen.append(self.new_card_name)
                # Add the value of the new card to DEALERS_HAND
                DEALERS_HAND += self.get_card_value(
                    self.new_card_name, self.face_value, self.face_cards
                )
                self.d_hand = get_font(40).render(f"{DEALERS_HAND}", True, WHITE)
                self.d_hand_rect = self.d_hand.get_rect()
                self.d_hand_rect.bottomright = (1220, 320)

            else:
                run = False  # Stop once dealer reaches 17 or higher

            # Update screen
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            pg.display.update()


    def move_options(self):
        global DEALERS_HAND, FAIL_SOUND, WIN_SOUND
        self.run = True
        while self.run:
            SCREEN.blit(self.p_hand, self.p_hand_rect)
            SCREEN.blit(self.d_hand, self.d_hand_rect)

            if not self.check_player_bust_round() or not self.check_player_win_round1() or not self.check_dealer_win_round():
                MOUSE_POS = pg.mouse.get_pos()
                HIT_BTN_TXT = "HIT"
                STAND_BTN_TXT = "STAND"
                # DD_BTN_TXT = "DOUBLE DOWN"

                HIT_BTN_POS = (WIDTH // 2 + 150, 360)
                STAND_BTN_POS = (WIDTH // 2 - 150, 360)
                # DD_BTN_POS = (950, 360)

                HIT_BTN = Button(None, HIT_BTN_POS, HIT_BTN_TXT, get_font(60), WHITE, GREY)
                STAND_BTN = Button(None, STAND_BTN_POS, STAND_BTN_TXT, get_font(60), WHITE, GREY)
                # DD_BTN = Button(None, DD_BTN_POS, DD_BTN_TXT, get_font(60), BLACK, GREY)

                for button in [HIT_BTN, STAND_BTN]: #This just loops over the buttons to see if we are hovering them
                    button.changeColour(MOUSE_POS)
                    button.update(SCREEN)

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        exit()

                    if event.type == pg.MOUSEBUTTONDOWN:
                        if HIT_BTN.checkForInput(MOUSE_POS):
                            self.hit()
                        if STAND_BTN.checkForInput(MOUSE_POS):
                            self.stand()
                        # if DD_BTN.checkForInput(MOUSE_POS):
                        #     self.dd()
            
            if self.check_player_bust_round():
                if not self.show_bust:
                    text = get_font(300).render("BUST", True, WHITE)
                    # text.set_alpha(13)
                    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    SCREEN.blit(text, text_rect)
                    FAIL_SOUND.play()
                    self.show_bust = True
                    self.bust_time = pg.time.get_ticks()

                if self.show_bust and not self.countdown:
                    if pg.time.get_ticks() - self.bust_time >= 500:
                        text = get_font(45).render("Returning to bet screen in . . .", None, WHITE)
                        text_rect = text.get_rect(center=(230, 600))
                        SCREEN.blit(text, text_rect)

                        self.countdown_draw()

            if self.check_player_win_round1():
                if not self.show_win:
                    text = get_font(300).render("WIN!!!", True, WHITE)
                    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    SCREEN.blit(text, text_rect)
                    WIN_SOUND.play()
                    self.show_win = True
                    self.win_time = pg.time.get_ticks()

                if self.show_win and not self.countdown:
                    if pg.time.get_ticks() - self.win_time >= 500:
                        text = get_font(45).render("Returning to bet screen in . . .", None, WHITE)
                        text_rect = text.get_rect(center=(230, 600))
                        SCREEN.blit(text, text_rect)

                        self.countdown_draw()

            if self.check_dealer_win_round():
                if not self.show_lose:
                    text = get_font(300).render("Lose :(", True, WHITE)
                    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    SCREEN.blit(text, text_rect)
                    FAIL_SOUND.play()
                    self.show_lose = True
                    self.lose_time = pg.time.get_ticks()

                if self.show_lose and not self.countdown:
                    if pg.time.get_ticks() - self.lose_time >= 500:
                        text = get_font(45).render("Returning to bet screen in . . .", None, WHITE)
                        text_rect = text.get_rect(center=(230, 600))
                        SCREEN.blit(text, text_rect)

                        self.countdown_draw()

            if self.check_dealer_bust_round():
                if not self.show_win:
                    text = get_font(300).render("WIN!!!", True, WHITE)
                    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    SCREEN.blit(text, text_rect)
                    WIN_SOUND.play()
                    self.show_win = True
                    self.win_time = pg.time.get_ticks()

                if self.show_win and not self.countdown:
                    if pg.time.get_ticks() - self.win_time >= 500:
                        text = get_font(45).render("Returning to bet screen in . . .", None, WHITE)
                        text_rect = text.get_rect(center=(230, 600))
                        SCREEN.blit(text, text_rect)

                        self.countdown_draw()

            if self.countdown:
                self.reset_game_state()
                self.run = False
                self.start_menu.play()

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        exit()

            pg.display.update()


    def check_player_win_round1(self):
        if PLAYERS_HAND == 21 and DEALERS_HAND < 21 or DEALERS_HAND > 21:
            return True

    def check_player_bust_round(self):
        if PLAYERS_HAND > 21:
            return True
    
    def check_dealer_win_round(self):
        if DEALERS_HAND in range(17, 22) and abs(PLAYERS_HAND - 21) > abs(DEALERS_HAND - 21):
            return True
        
    def check_dealer_bust_round(self):
        if DEALERS_HAND > 21:
            return True
    
    def countdown_draw(self):
        cd1 = get_font(50).render("3", True, WHITE)
        cd2 = get_font(50).render("2", True, WHITE)
        cd3 = get_font(50).render("1", True, WHITE)

        cd1_rect = cd1.get_rect(center=(200, 650))
        cd2_rect = cd2.get_rect(center=(250, 650))
        cd3_rect = cd3.get_rect(center=(300, 650))

        SCREEN.blit(cd1, cd1_rect)
        pg.display.update()
        pg.time.delay(1000)
        
        SCREEN.blit(cd2, cd2_rect)
        pg.display.update()
        pg.time.delay(1000)

        SCREEN.blit(cd3, cd3_rect)
        pg.display.update()
        pg.time.delay(1000)
        self.countdown = True
        

    def game_state_display(self):
        self.calc_hand_value()

        text = get_font(40).render("Your Bet:", True, WHITE)
        text_rect = text.get_rect()
        text_rect.bottomleft = (0, 320)

        amount = get_font(40).render(f"{BET_AMNT}", True, WHITE)
        amount_rect = amount.get_rect()
        amount_rect.bottomleft = (0, 360)

        self.p_hand = get_font(40).render(f"{PLAYERS_HAND}", True, WHITE)
        self.p_hand_rect = self.p_hand.get_rect()
        self.p_hand_rect.bottomright = (1220, 400)

        self.d_hand = get_font(40).render(f"{DEALERS_HAND}", True, WHITE)
        self.d_hand_rect = self.d_hand.get_rect()
        self.d_hand_rect.bottomright = (1220, 320)

        SCREEN.blit(amount, amount_rect)
        SCREEN.blit(text, text_rect)


        if self.first_card():
            self.second_card()
            if self.second_card():
                self.third_card()
                if self.third_card():
                    self.blank_card()
                    if self.blank_card():
                        self.end_of_drawing_seq = True
        
        if self.end_of_drawing_seq:
            self.move_options()

    
    def game_state(self):
        self.drawing_cards_scene()
        while True:
            SCREEN.blit(BG, (0, 0))

            Game.game_state_display(self)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            pg.display.update()


class Start_Menu:
    def __init__(self):
        exit_icon = pg.image.load("BlackJack/black_x.png")
        self.exit_icon_t = pg.transform.scale(exit_icon, (70, 70))
        self.exit_btn_rect = self.exit_icon_t.get_rect()
        self.exit_btn_rect.topright = (1280, 0)
        
        self.Game = Game(self)


    def draw(self):
        text1 = get_font(150).render("BlackJack", True, BLACK)
        text2 = get_font(50).render("by", True, GREY)
        text3 = get_font(50).render("James Rim", True, GREY)

        text1_rect = text1.get_rect()
        text2_rect = text2.get_rect()
        text3_rect = text3.get_rect()
        text1_rect.center = (WIDTH // 2, HEIGHT // 2)
        text2_rect.center = (WIDTH // 2, HEIGHT // 2)
        text3_rect.center = (WIDTH // 2, HEIGHT // 2)
        text1_rect.top = 30
        text2_rect.top = 180
        text3_rect.top = 220

        SCREEN.blit(text1, text1_rect)
        SCREEN.blit(text2, text2_rect)
        SCREEN.blit(text3, text3_rect)


    def htp(self):
        while True:
            
            HTP_MOUSE_POS = pg.mouse.get_pos()
            X_POS, Y_POS = HTP_MOUSE_POS
            SCREEN.fill(WHITE)

            text = get_font(60).render("How To Play BlackJack?", True, BLACK)
            text_rect = text.get_rect()
            text_rect.topleft = (0, 0)

            SCREEN.blit(text, text_rect)
            SCREEN.blit(self.exit_icon_t, self.exit_btn_rect)
            # Finish the htp section another time


            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if X_POS in range(self.exit_btn_rect.left, self.exit_btn_rect.right) and Y_POS in range(self.exit_btn_rect.top, self.exit_btn_rect.bottom):
                        SCREEN.fill(WHITE)
                        self.draw()
                        self.menu()

            pg.display.update()


    def options(self):
        while True:
            
            O_MOUSE_POS = pg.mouse.get_pos()
            X_POS, Y_POS = O_MOUSE_POS
            SCREEN.fill(WHITE)

            text = get_font(60).render("Options", True, BLACK)
            text_rect = text.get_rect()
            text_rect.topleft = (0, 0)

            SCREEN.blit(text, text_rect)
            SCREEN.blit(self.exit_icon_t, self.exit_btn_rect)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if X_POS in range(self.exit_btn_rect.left, self.exit_btn_rect.right) and Y_POS in range(self.exit_btn_rect.top, self.exit_btn_rect.bottom): 
                        SCREEN.fill(WHITE)
                        self.draw()
                        self.menu()

            pg.display.update()


    def play(self):
        while True:

            SCREEN.blit(BG, (0, 0))

            self.Game.bet_state()
            self.Game.game_state()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            pg.display.update()
     

    def menu(self): # Will cycle through the three buttons to initiate their respective functions when clicked
        
        while True:
            MOUSE_POS = pg.mouse.get_pos()
            HTP_TXT = "How To Play"
            OPTIONS_TXT = "Options"
            PLAY_TXT = "START GAME"

            HTP_BTN_POS = (350, 360)
            OPTIONS_BTN_POS = (900, 360)
            PLAY_BTN_POS = (640, 550)

            HTP_BTN = Button(None, HTP_BTN_POS, HTP_TXT, get_font(90), BLACK, GREY)
            OPTIONS_BTN = Button(None, OPTIONS_BTN_POS, OPTIONS_TXT, get_font(90), BLACK, GREY)
            PLAY_BTN = Button(None, PLAY_BTN_POS, PLAY_TXT, get_font(110), BLACK, GREY)

            for button in [HTP_BTN, OPTIONS_BTN, PLAY_BTN]: #This just loops over the buttons to see if we are hovering them
                button.changeColour(MOUSE_POS)
                button.update(SCREEN)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if PLAY_BTN.checkForInput(MOUSE_POS):
                        self.play()
                    if OPTIONS_BTN.checkForInput(MOUSE_POS):
                        self.options()
                    if HTP_BTN.checkForInput(MOUSE_POS):
                        self.htp()

            pg.display.update()


class App:
    def __init__(self):
        self.Start_Menu = Start_Menu()


    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

    def run(self):
        while True:
            pg.display.set_caption("BlackJack")

            SCREEN.fill(WHITE)
            self.Start_Menu.draw()
            self.Start_Menu.menu()

            self.check_events()
            pg.display.update()


if __name__ == "__main__":
    game = App()
    game.run()