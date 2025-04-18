import random
import time
from colorama import init, Fore, Style, Back
import sys
import seaborn as sns 
import matplotlib.pyplot as plt



init(autoreset=True)



SUIT_SYMBOLS = {
    'Hearts':   Fore.RED + '♥' + Style.RESET_ALL,
    'Diamonds': Fore.RED + '♦' + Style.RESET_ALL,
    'Clubs':    Fore.GREEN + '♣' + Style.RESET_ALL,
    'Spades':   Fore.GREEN + '♠' + Style.RESET_ALL
}



CARD_ART_TEMPLATE = """\
┌───────┐
| {rank:<2}    |
|       |
|   {suit}   |
|       |
|    {rank:>2} |
└───────┘
"""



def card_ascii(card):
    rank_symbol = card.rank if card.rank != '10' else '10'
    if card.rank == '10':
        top_rank = card.rank
        bottom_rank = card.rank
    else:
        top_rank = card.rank[0]
        bottom_rank = card.rank[0]

    return CARD_ART_TEMPLATE.format(rank=top_rank, suit=SUIT_SYMBOLS[card.suit]).split('\n')



def display_hand_ascii(cards, role):
    card_lines = [card_ascii(card) for card in cards]
    transposed = list(zip(*card_lines))
    role_color = Fore.GREEN if role == "Player" else Fore.RED if role == "Dealer" else Fore.CYAN
    print(role_color + f"{role}'s Cards:" + Style.RESET_ALL)
    for line_tuple in transposed:
        print("  ".join(line_tuple))
    print()



class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit



    def __str__(self):
        return f"{self.rank} of {self.suit}"



    @property
    def value(self):
        
        if self.rank in ['Jack', 'Queen', 'King']:
            return 10
        elif self.rank == 'Ace':
            return 1
        else:
            return int(self.rank)



class Deck:
    def __init__(self, num_decks=6):
        self.card_categories = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
        self.num_decks = num_decks
        self.reset_deck()



    def reset_deck(self):
        self.deck = [Card(rank, suit)
                     for _ in range(self.num_decks)
                     for suit in self.card_categories
                     for rank in self.cards_list]
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

    def needs_reshuffle(self):
       
        return len(self.deck) < (self.num_decks * 52 * 0.2) or len(self.deck) < 20



class Participant:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def receive_card(self, card):
        self.cards.append(card)

    def clear_hand(self):
        self.cards = []

    def compute_score(self):
        total = 0
        aces = 0

        for c in self.cards:
            if c.rank == 'Ace':
                aces += 1
            else:
                total += c.value

        total += aces

        if aces > 0 and total + 10 <= 21:
            total += 10
        return total

    def is_blackjack(self):
        if len(self.cards) == 2:
            ranks = [c.rank for c in self.cards]
            if 'Ace' in ranks and any(r in ['10', 'Jack', 'Queen', 'King'] for r in ranks):
                return True
        return False

    def is_busted(self):
        return self.compute_score() > 21





class Player(Participant):
    pass



class Dealer(Participant):
    def should_hit(self):
        return self.compute_score() < 17



class BlackjackGame:
    def __init__(self, initial_capital):
        self.deck_obj = Deck(num_decks=6)
        self.capital = initial_capital
        self.capital_history = [self.capital]

        sns.set_theme(style="whitegrid")
        plt.ion()
        self.fig, self.ax = plt.subplots()
        sns.lineplot(x=range(len(self.capital_history)), y=self.capital_history, marker='o', color='blue', ax=self.ax)
        self.ax.set_title("Capital Trend")
        self.ax.set_xlabel("Number of Hands Played")
        self.ax.set_ylabel("Capital (Euro)")
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        self.player = Player("Player")
        self.dealer = Dealer("Dealer")
        self.round_number = 0
        self.results_log = []



    def deal_card_animated(self, recipient):
        spinner = ['|', '/', '-', '\\']
        for i in range(4):
            sys.stdout.write(Fore.CYAN + "\rDealing card " + spinner[i] + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write("\r" + " " * 20 + "\r")
        sys.stdout.flush()

        card = self.deck_obj.deal_card()
        recipient.receive_card(card)
        time.sleep(0.3)  

    def deal_initial_cards(self):
        self.player.clear_hand()
        self.dealer.clear_hand()

        self.deal_card_animated(self.player)
        self.deal_card_animated(self.player)

        self.deal_card_animated(self.dealer)
        self.deal_card_animated(self.dealer)

    def can_split(self, cards):
        if len(cards) == 2:
            def card_basic_value(card):
                if card.rank in ['Jack','Queen','King']:
                    return 10
                elif card.rank == 'Ace':
                    return 11
                else:
                    return int(card.rank)
            return card_basic_value(cards[0]) == card_basic_value(cards[1])
        return False

    def display_all_information(self, bet):
        dealer_show_card = self.dealer.cards[0]

        print(Fore.CYAN + "\n────────────────────────────────────────────────" + Style.RESET_ALL)
        print(Fore.CYAN + f"Dealer shows: {str(dealer_show_card)} (one card hidden)" + Style.RESET_ALL)
        print(Fore.CYAN + "────────────────────────────────────────────────" + Style.RESET_ALL + "\n")

        display_hand_ascii(self.player.cards, "Player")

        player_score = self.player.compute_score()
        score_color = Fore.GREEN if player_score <= 21 else Fore.RED
        print(score_color + f"Player's Score: {player_score}" + Style.RESET_ALL)
        print(Fore.CYAN + "────────────────────────────────────────────────\n" + Style.RESET_ALL)

    def player_turn(self, bet):
        player_busted = False
        first_action = True
        while True:
            if self.player.is_busted():
                player_busted = True
                break

            if first_action and self.capital >= bet:
                print(Fore.YELLOW + 'Options: ["play" to hit, "stop" to stand, "double" to double down]' + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + 'Options: ["play" to hit, "stop" to stand]' + Style.RESET_ALL)

            choice = input(Fore.YELLOW + "Your choice: " + Style.RESET_ALL).lower()

            if choice == "play":
                self.deal_card_animated(self.player)
                print("\n" + Fore.CYAN + "──────────────────────────" + Style.RESET_ALL)
                display_hand_ascii(self.player.cards, "Player")
                player_score = self.player.compute_score()
                score_color = Fore.GREEN if player_score <= 21 else Fore.RED
                print(score_color + f"Player's Score: {player_score}" + Style.RESET_ALL)
                print(Fore.CYAN + "──────────────────────────" + Style.RESET_ALL + "\n")
                first_action = False

            elif choice == "stop":
                break

            elif choice == "double" and first_action and self.capital >= bet:
                self.capital -= bet
                bet = bet * 2
                self.deal_card_animated(self.player)
                print(Fore.MAGENTA + "Player doubled down!" + Style.RESET_ALL)
                display_hand_ascii(self.player.cards, "Player")
                player_score = self.player.compute_score()
                print("Player's Score:", player_score)
                player_busted = self.player.is_busted()
                break
            else:
                print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)



        return bet, player_busted



    def dealer_turn(self):
        print(Fore.CYAN + "Dealer's turn..." + Style.RESET_ALL)
        time.sleep(0.5)
        while self.dealer.should_hit():
            self.deal_card_animated(self.dealer)

    def determine_winner(self, bet):
        player_score = self.player.compute_score()
        dealer_score = self.dealer.compute_score()

        print("\n" + Fore.CYAN + "========================================" + Style.RESET_ALL)
        display_hand_ascii(self.dealer.cards, "Dealer")
        print(Fore.RED + f"Dealer's Score: {dealer_score}" + Style.RESET_ALL)
        print(Fore.CYAN + "========================================" + Style.RESET_ALL + "\n")

        outcome = ""
        if dealer_score > 21:
            self.capital += bet * 2
            print(Fore.GREEN + "Dealer busts! Player wins." + Style.RESET_ALL)
            outcome = "Win"
        elif player_score > dealer_score and player_score <= 21:
            self.capital += bet * 2
            print(Fore.GREEN + "Player beats the Dealer. Player wins." + Style.RESET_ALL)
            outcome = "Win"
        elif dealer_score > player_score and dealer_score <= 21:
            print(Fore.RED + "Dealer outscores Player. Dealer wins." + Style.RESET_ALL)
            outcome = "Lose"
        else:
            self.capital += bet
            print(Fore.YELLOW + "It's a tie! No one loses money." + Style.RESET_ALL)
            outcome = "Tie"

        print(f"Final capital: {self.capital} euros.")
        self.capital_history.append(self.capital)
        self.update_chart()
        return outcome

    def handle_blackjack(self, bet):
        player_blackjack = self.player.is_blackjack()
        dealer_blackjack = self.dealer.is_blackjack()

        if player_blackjack or dealer_blackjack:
            print("\n" + Fore.CYAN + "========================================" + Style.RESET_ALL)
            display_hand_ascii(self.dealer.cards, "Dealer")
            dealer_score = self.dealer.compute_score()
            print(Fore.RED + f"Dealer's Score: {dealer_score}" + Style.RESET_ALL)
            print(Fore.CYAN + "========================================" + Style.RESET_ALL + "\n")

            if player_blackjack and dealer_blackjack:
                self.capital += bet
                print(Fore.YELLOW + "Both have blackjack! It's a tie." + Style.RESET_ALL)
                print(f"Final capital: {self.capital} euros.")
                self.capital_history.append(self.capital)
                self.update_chart()
                return "Tie"

            if player_blackjack:
                self.capital += int(bet * 2.5)
                print(Fore.GREEN + "Blackjack! Player wins." + Style.RESET_ALL)
                print(f"Final capital: {self.capital} euros.")
                self.capital_history.append(self.capital)
                self.update_chart()
                return "Win"

            if dealer_blackjack:
                print(Fore.RED + "Dealer has blackjack! Dealer wins." + Style.RESET_ALL)
                print(f"Final capital: {self.capital} euros.")
                self.capital_history.append(self.capital)
                self.update_chart()
                return "Lose"

        return None



    def update_chart(self):
        self.ax.clear()
        sns.lineplot(x=range(len(self.capital_history)), y=self.capital_history, marker='o', color='blue', ax=self.ax)
        self.ax.set_title("Capital Trend")
        self.ax.set_xlabel("Number of Hands Played")
        self.ax.set_ylabel("Capital (Euro)")
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()



    def play_single_hand(self, bet):
        blackjack_result = self.handle_blackjack(bet)
        if blackjack_result is not None:
            return blackjack_result

        bet, player_busted = self.player_turn(bet)

        if player_busted:
            player_score = self.player.compute_score()
            dealer_score = self.dealer.compute_score()
            print(Fore.RED + "Player busted!" + Style.RESET_ALL)
            display_hand_ascii(self.player.cards, "Player")
            print("Player's Score:", player_score)
            display_hand_ascii(self.dealer.cards, "Dealer")
            print("Dealer's Score:", dealer_score)
            print(Fore.RED + "Dealer wins." + Style.RESET_ALL)
            print(f"Final capital: {self.capital} euros.")
            self.capital_history.append(self.capital)
            self.update_chart()


            return "Lose"



        self.dealer_turn()
        return self.determine_winner(bet)



    def print_banner(self, text):
        print(Fore.MAGENTA + "******************************************" + Style.RESET_ALL)
        print(Fore.MAGENTA + f"*           {text.center(30)}           *" + Style.RESET_ALL)
        print(Fore.MAGENTA + "******************************************" + Style.RESET_ALL)



    def play_round(self):
        self.round_number += 1



        if self.deck_obj.needs_reshuffle():
            print(Fore.MAGENTA + "\nReshuffling the deck..." + Style.RESET_ALL)
            self.deck_obj.reset_deck()
            time.sleep(1)

        self.print_banner(f"ROUND {self.round_number}")
        print(Fore.BLUE + f"Your current capital: {self.capital} euros." + Style.RESET_ALL)

       
       
        while True:
            try:
                bet = int(input(Fore.CYAN + "How much do you want to bet? " + Style.RESET_ALL))
                if bet <= 0:
                    print(Fore.RED + "The bet must be a positive number." + Style.RESET_ALL)
                elif bet > self.capital:
                    print(Fore.RED + "You cannot bet more than your current capital." + Style.RESET_ALL)
                else:
                    break
            except ValueError:
                print(Fore.RED + "Please enter a valid number." + Style.RESET_ALL)

        self.capital -= bet
        self.deal_initial_cards()
        self.display_all_information(bet)



        if self.can_split(self.player.cards):
            if self.capital >= bet:
                choice = input(Fore.YELLOW + "You have two cards of the same value. Do you want to split? [y/n]: " + Style.RESET_ALL).lower()
                if choice == 'y':
                    self.capital -= bet
                    original_bet = bet
                    first_hand = [self.player.cards[0]]
                    second_hand = [self.player.cards[1]]

                    self.player.cards = first_hand
                    self.deal_card_animated(self.player)
                    print("\n" + Fore.MAGENTA + "--- FIRST HAND AFTER SPLIT ---" + Style.RESET_ALL)
                    outcome1 = self.play_single_hand(original_bet)

                    print("\n" + Fore.MAGENTA + "--- SECOND HAND AFTER SPLIT ---" + Style.RESET_ALL)
                    self.player.cards = second_hand
                    self.deal_card_animated(self.player)
                    outcome2 = self.play_single_hand(original_bet)

                    self.results_log.append((self.round_number, outcome1 + " (hand1)", outcome2 + " (hand2)", self.capital))
                    return
                else:
                    outcome = self.play_single_hand(bet)
                    self.results_log.append((self.round_number, outcome, self.capital))
                    return
            else:
                print(Fore.RED + "You don't have enough capital to split." + Style.RESET_ALL)
                outcome = self.play_single_hand(bet)
                self.results_log.append((self.round_number, outcome, self.capital))
        else:
            outcome = self.play_single_hand(bet)
            self.results_log.append((self.round_number, outcome, self.capital))



    def run(self):


        self.display_welcome()
        while self.capital > 0:
            self.play_round()
            if self.capital <= 0:
                print(Fore.RED + "You have no more capital. Game over." + Style.RESET_ALL)
                break
            choice = input(Fore.YELLOW + "Do you want to play another hand? [y/n]: " + Style.RESET_ALL).lower()
            if choice != 'y':
                print(Fore.GREEN + "Thanks for playing!" + Style.RESET_ALL)
                break



        self.show_final_summary()
        print(Fore.BLUE + "Press Enter to close..." + Style.RESET_ALL)
        input()
        plt.ioff()
        plt.show()

    def display_welcome(self):


        print(Fore.MAGENTA + "******************************************" + Style.RESET_ALL)
        print(Fore.MAGENTA + "*          Welcome to Mario's            *" + Style.RESET_ALL)
        print(Fore.MAGENTA + "*              Blackjack!                *"      + Style.RESET_ALL)
        print(Fore.MAGENTA + "******************************************" + Style.RESET_ALL)



    def show_final_summary(self):
        print(Fore.CYAN + "\n=== Final Summary ===" + Style.RESET_ALL)
        print(f"Starting Capital: {self.capital_history[0]} euros")
        print(f"Ending Capital:   {self.capital} euros\n")

        print(Fore.CYAN + "Results log: (Round, Outcome(s), Capital after)" + Style.RESET_ALL)
        for entry in self.results_log:
            if len(entry) == 4:
                print(f"Round {entry[0]}: {entry[1]}, {entry[2]} | Capital: {entry[3]}")
            else:
                print(f"Round {entry[0]}: {entry[1]} | Capital: {entry[2] if len(entry)>2 else 'N/A'}")




if __name__ == "__main__":
    while True:
        try:
            initial_capital = int(input(Fore.CYAN + "Enter your initial capital: " + Style.RESET_ALL))
            if initial_capital <= 0:
                print(Fore.RED + "Initial capital must be a positive number." + Style.RESET_ALL)
            else:
                break
        except ValueError:
            print(Fore.RED + "Please enter a valid number." + Style.RESET_ALL)



    game = BlackjackGame(initial_capital=initial_capital)
    game.run()
