import tkinter as tk
from tkinter import messagebox
import random

# --- Core Logic & Constants ---
SUITS = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUIT_COLORS = {'Hearts': '#e74c3c', 'Diamonds': '#e74c3c', 'Clubs': '#2c3e50', 'Spades': '#2c3e50'}

# Color palette
C = {
    'felt':       '#1a6b3a',
    'felt_dark':  '#145730',
    'felt_edge':  '#0f4225',
    'panel':      '#1a1a2e',
    'panel2':     '#16213e',
    'gold':       '#f0c040',
    'cyan':       '#00d4ff',
    'pink':       '#ff69b4',
    'orange':     '#ff7043',
    'red':        '#ef5350',
    'blue':       '#42a5f5',
    'green':      '#66bb6a',
    'white':      '#f5f5f5',
    'grey':       '#9e9e9e',
    'card_bg':    '#fafafa',
    'card_shadow':'#333',
}

def calculate_total(cards):
    total, aces = 0, 0
    for rank, suit in cards:
        if rank in ['J', 'Q', 'K']: total += 10
        elif rank == 'A': aces += 1; total += 11
        else: total += int(rank)
    while total > 21 and aces:
        total -= 10; aces -= 1
    return total

def get_card_value(rank):
    if rank in ['J', 'Q', 'K', '10']: return 10
    if rank == 'A': return 11
    return int(rank)

def update_count(card, current_count):
    rank = card[0]
    if rank in ['2', '3', '4', '5', '6']: return current_count + 1
    elif rank in ['10', 'J', 'Q', 'K', 'A']: return current_count - 1
    return current_count

def ml_advisor_reasoning(player_cards, dealer_upcard):
    player_total = calculate_total(player_cards)
    dealer_val = get_card_value(dealer_upcard[0])
    is_soft = any(rank == 'A' for rank, suit in player_cards) and player_total <= 21

    if is_soft:
        if player_total <= 17: return "HIT", "Hitting is optimal, but the house edge remains negative."
        if player_total == 18:
            if dealer_val in [2, 7, 8]: return "STAND", "Stand. You are statistically likely to lose money long-term regardless."
            else: return "HIT", "Hit. You are fighting a mathematical disadvantage."
        return "STAND", "Stand. Enjoy the illusion of safety; the math will catch up."
    else:
        if player_total <= 11: return "HIT", "Hit. You can't bust, but the house still has the statistical upper hand."
        if player_total == 12:
            if dealer_val in [4, 5, 6]: return "STAND", "Stand. Hoping the dealer busts is a negative EV strategy over time."
            return "HIT", "Hit. You are forced to risk busting just to survive the hand."
        if 13 <= player_total <= 16:
            if dealer_val <= 6: return "STAND", "Stand. Let the dealer play. Note: The casino built its wealth on players in this situation."
            return "HIT", "Hit. You are heavily disadvantaged here. The math is against you."
        return "STAND", "Stand. You have a strong hand, but the casino's rules ensure they win 51% of the time."


# --- GUI Application ---
class BlackjackEducationalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("The Reality of Blackjack")
        self.root.geometry("1200x780")
        self.root.configure(bg=C['felt_edge'])
        self.root.resizable(False, False)
        self._reset_state()
        self.setup_ui()

    def _reset_state(self):
        self.bankroll = 1000.0
        self.total_wagered = 0.0
        self.hands_played = 0
        self.current_bet = 0
        self.deck = []
        self.running_count = 0
        self.player_hand = []
        self.dealer_hand = []
        self.game_over = True
        self.loan_taken = False
        self.init_deck()

    def init_deck(self):
        self.deck = [(r, s) for r in RANKS for s in SUITS.keys()] * 6
        random.shuffle(self.deck)
        self.running_count = 0

    # ------------------------------------------------------------------ #
    #  UI BUILD                                                            #
    # ------------------------------------------------------------------ #
    def setup_ui(self):
        """Build (or rebuild) all widgets from scratch."""
        for w in self.root.winfo_children():
            w.destroy()

        # ── outer border ring ──────────────────────────────────────────
        outer = tk.Frame(self.root, bg=C['felt_edge'], padx=6, pady=6)
        outer.pack(fill=tk.BOTH, expand=True)

        # ── two-column layout ─────────────────────────────────────────
        self.left_panel = tk.Frame(outer, bg=C['panel'], width=340, padx=18, pady=18)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.left_panel.pack_propagate(False)

        self.table_panel = tk.Frame(outer, bg=C['felt'])
        self.table_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._build_left_panel()
        self._build_table()

    def _section_header(self, parent, icon, text, color):
        f = tk.Frame(parent, bg=C['panel'])
        f.pack(fill=tk.X, pady=(14, 4))
        tk.Label(f, text=icon, font=("Segoe UI Emoji", 13), bg=C['panel'], fg=color).pack(side=tk.LEFT)
        tk.Label(f, text=f"  {text}", font=("Arial", 13, "bold"), bg=C['panel'], fg=color).pack(side=tk.LEFT)
        tk.Frame(parent, bg=color, height=1).pack(fill=tk.X, pady=(0, 6))

    def _build_left_panel(self):
        lp = self.left_panel

        # Title
        tk.Label(lp, text="BLACKJACK", font=("Arial", 20, "bold"), bg=C['panel'],
                 fg=C['gold'], lettersp=2 if hasattr(tk.Label, 'lettersp') else 0).pack(anchor="w")
        tk.Label(lp, text="Educational Reality Simulator", font=("Arial", 9),
                 bg=C['panel'], fg=C['grey']).pack(anchor="w")

        # ── The Math section ─────────────────────────────────────────
        self._section_header(lp, "📉", "THE MATH", C['gold'])
        rules = (
            "• Casino edge: ~0.5 – 2% built-in.\n"
            "• Perfect play only slows losses.\n"
            "• Even card counting can't save you\n"
            "  from variance-driven bankruptcy."
        )
        tk.Label(lp, text=rules, font=("Arial", 10), bg=C['panel'], fg=C['white'],
                 justify=tk.LEFT, wraplength=295).pack(anchor="w")

        # ── Count section ─────────────────────────────────────────────
        self._section_header(lp, "🧠", "THE ILLUSION (TUTOR)", C['cyan'])
        self.count_var = tk.StringVar(value="Running Count: 0\nTrue Count: 0.0")
        tk.Label(lp, textvariable=self.count_var, font=("Courier New", 11),
                 bg=C['panel'], fg=C['white'], justify=tk.LEFT).pack(anchor="w")
        self.bet_advice_var = tk.StringVar(
            value="Reality: Even at +2 True Count your edge is <1 %. A single\nbad streak will ruin you.")
        tk.Label(lp, textvariable=self.bet_advice_var, font=("Arial", 9, "italic"),
                 bg=C['panel'], fg=C['orange'], wraplength=295, justify=tk.LEFT).pack(anchor="w", pady=(4, 0))

        # ── AI Advisor section ────────────────────────────────────────
        self._section_header(lp, "🤖", "REALITY CHECK ADVISOR", C['pink'])
        self.ai_action_var = tk.StringVar(value="Optimal Move: —")
        tk.Label(lp, textvariable=self.ai_action_var, font=("Arial", 13, "bold"),
                 bg=C['panel'], fg=C['white']).pack(anchor="w")
        self.ai_reason_var = tk.StringVar(value="Truth: Awaiting your wager…")
        tk.Label(lp, textvariable=self.ai_reason_var, font=("Arial", 9),
                 bg=C['panel'], fg=C['grey'], wraplength=295, justify=tk.LEFT).pack(anchor="w")

        # ── Stats (bottom-pinned) ─────────────────────────────────────
        stats_frame = tk.Frame(lp, bg=C['panel2'], padx=12, pady=10)
        stats_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        tk.Label(stats_frame, text="SESSION STATS", font=("Arial", 10, "bold"),
                 bg=C['panel2'], fg=C['grey']).pack(anchor="w")
        self.stats_var = tk.StringVar(value="Hands: 0    Wagered: £0.00    P/L: £0.00")
        tk.Label(stats_frame, textvariable=self.stats_var, font=("Arial", 10, "bold"),
                 bg=C['panel2'], fg=C['red'], justify=tk.LEFT, wraplength=295).pack(anchor="w")

    def _build_table(self):
        tp = self.table_panel

        # ── table rim decoration ──────────────────────────────────────
        rim = tk.Frame(tp, bg=C['felt_dark'], padx=20, pady=14)
        rim.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        # Dealer zone
        dealer_zone = tk.Frame(rim, bg=C['felt_dark'])
        dealer_zone.pack(fill=tk.X, pady=(0, 6))
        self.dealer_score_var = tk.StringVar(value="Dealer")
        tk.Label(dealer_zone, textvariable=self.dealer_score_var,
                 font=("Arial", 14, "bold"), bg=C['felt_dark'], fg=C['grey']).pack()
        self.dealer_cards_frame = tk.Frame(dealer_zone, bg=C['felt_dark'])
        self.dealer_cards_frame.pack(pady=6)

        # Divider
        tk.Frame(rim, bg=C['felt_edge'], height=2).pack(fill=tk.X, pady=6)

        # Status / bankroll
        centre = tk.Frame(rim, bg=C['felt_dark'])
        centre.pack(fill=tk.X)
        self.status_var = tk.StringVar(value="The house always wins.  Place your wager.")
        self.status_label = tk.Label(centre, textvariable=self.status_var,
                                     font=("Arial", 16, "bold"), bg=C['felt_dark'], fg=C['gold'],
                                     wraplength=680)
        self.status_label.pack(pady=(4, 2))
        self.bankroll_var = tk.StringVar(value=f"Bankroll: £{self.bankroll:.2f}")
        self.bankroll_label = tk.Label(centre, textvariable=self.bankroll_var,
                                       font=("Arial", 26, "bold"), bg=C['felt_dark'], fg=C['white'])
        self.bankroll_label.pack()

        # Player zone
        player_zone = tk.Frame(rim, bg=C['felt_dark'])
        player_zone.pack(fill=tk.X, pady=(6, 0))
        tk.Frame(rim, bg=C['felt_edge'], height=2).pack(fill=tk.X, pady=6)
        self.player_score_var = tk.StringVar(value="Player")
        tk.Label(player_zone, textvariable=self.player_score_var,
                 font=("Arial", 14, "bold"), bg=C['felt_dark'], fg=C['grey']).pack()
        self.player_cards_frame = tk.Frame(player_zone, bg=C['felt_dark'])
        self.player_cards_frame.pack(pady=6)

        # ── Controls ─────────────────────────────────────────────────
        self.controls_frame = tk.Frame(rim, bg=C['felt_dark'])
        self.controls_frame.pack(pady=10)
        self._build_controls()

    def _build_controls(self):
        cf = self.controls_frame

        # Chip-style bet row
        bet_row = tk.Frame(cf, bg=C['felt_dark'])
        bet_row.pack(pady=(0, 8))
        tk.Label(bet_row, text="BET £", font=("Arial", 13, "bold"),
                 bg=C['felt_dark'], fg=C['gold']).pack(side=tk.LEFT)
        self.bet_entry = tk.Entry(bet_row, font=("Arial", 14, "bold"), width=7,
                                  bg=C['panel'], fg=C['white'], insertbackground=C['white'],
                                  relief=tk.FLAT, justify=tk.CENTER,
                                  highlightbackground=C['gold'], highlightthickness=1)
        self.bet_entry.pack(side=tk.LEFT, padx=6)
        self.bet_entry.insert(0, "50")

        # Quick-bet chips
        for amt in (10, 25, 50, 100):
            tk.Button(bet_row, text=f"£{amt}", font=("Arial", 10, "bold"),
                      bg=C['panel2'], fg=C['gold'], relief=tk.FLAT,
                      activebackground=C['gold'], activeforeground=C['panel'],
                      padx=6, pady=2,
                      command=lambda a=amt: (self.bet_entry.delete(0, tk.END),
                                             self.bet_entry.insert(0, str(a)))
                      ).pack(side=tk.LEFT, padx=3)

        # Action buttons
        btn_row = tk.Frame(cf, bg=C['felt_dark'])
        btn_row.pack()

        self.btn_deal = self._make_btn(btn_row, "DEAL", C['green'],  self.deal)
        self.btn_hit  = self._make_btn(btn_row, "HIT",  C['red'],    self.hit,  disabled=True)
        self.btn_stand = self._make_btn(btn_row, "STAND", C['blue'],  self.stand, disabled=True)

    def _make_btn(self, parent, text, color, cmd, disabled=False):
        btn = tk.Button(parent, text=text, font=("Arial", 13, "bold"),
                        bg=color, fg="white", relief=tk.FLAT,
                        activebackground=color, activeforeground="white",
                        padx=22, pady=8, cursor="hand2",
                        state=tk.DISABLED if disabled else tk.NORMAL,
                        command=cmd)
        btn.pack(side=tk.LEFT, padx=8)
        btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=self._lighten(c)))
        btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
        return btn

    @staticmethod
    def _lighten(hex_color):
        r = int(hex_color[1:3], 16); g = int(hex_color[3:5], 16); b = int(hex_color[5:7], 16)
        r = min(255, r + 40); g = min(255, g + 40); b = min(255, b + 40)
        return f"#{r:02x}{g:02x}{b:02x}"

    # ------------------------------------------------------------------ #
    #  CARD DRAWING                                                        #
    # ------------------------------------------------------------------ #
    def draw_card(self, parent, card, hidden=False):
        shadow = tk.Frame(parent, bg=C['card_shadow'], width=78, height=118)
        shadow.pack(side=tk.LEFT, padx=(4, 6), pady=4)
        shadow.pack_propagate(False)

        card_frame = tk.Frame(shadow, bg=C['card_bg'], width=76, height=116)
        card_frame.place(x=0, y=0)
        card_frame.pack_propagate(False)

        if hidden:
            inner = tk.Frame(card_frame, bg="#1a237e", width=76, height=116)
            inner.place(x=0, y=0)
            tk.Label(inner, text="🂠", font=("Segoe UI Emoji", 36), bg="#1a237e",
                     fg=C['gold']).place(relx=0.5, rely=0.5, anchor="center")
        else:
            rank, suit = card
            color = SUIT_COLORS[suit]
            sym   = SUITS[suit]
            tk.Label(card_frame, text=f"{rank}", font=("Arial", 11, "bold"),
                     bg=C['card_bg'], fg=color).place(x=4, y=2)
            tk.Label(card_frame, text=sym, font=("Arial", 10),
                     bg=C['card_bg'], fg=color).place(x=4, y=18)
            tk.Label(card_frame, text=sym, font=("Arial", 32),
                     bg=C['card_bg'], fg=color).place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(card_frame, text=f"{rank}", font=("Arial", 11, "bold"),
                     bg=C['card_bg'], fg=color).place(relx=1.0, rely=1.0, anchor="se", x=-4, y=-2)
            tk.Label(card_frame, text=sym, font=("Arial", 10),
                     bg=C['card_bg'], fg=color).place(relx=1.0, rely=1.0, anchor="se", x=-4, y=-18)

    def clear_table(self):
        for w in self.dealer_cards_frame.winfo_children(): w.destroy()
        for w in self.player_cards_frame.winfo_children(): w.destroy()

    # ------------------------------------------------------------------ #
    #  TUTOR / AI / STATS UPDATES                                         #
    # ------------------------------------------------------------------ #
    def update_tutor(self):
        decks_remaining = max(1, len(self.deck) // 52)
        true_count = self.running_count / decks_remaining
        self.count_var.set(f"Running Count: {self.running_count:+d}\nTrue Count: {true_count:+.1f}")
        if true_count >= 2:
            self.bet_advice_var.set("Reality Check: Count is high — slight edge, but\none bad streak still wipes you out.")
        elif true_count <= -1:
            self.bet_advice_var.set("Reality Check: Count is low. House is aggressively\ncrushing you. You should walk away.")
        else:
            self.bet_advice_var.set("Reality Check: Neutral deck. Standard house edge\nin effect. You are losing money over time.")

    def update_ai(self):
        if self.game_over:
            self.ai_action_var.set("Optimal Move: —")
            self.ai_reason_var.set("Truth: Awaiting your wager…")
            return
        action, reasoning = ml_advisor_reasoning(self.player_hand, self.dealer_hand[0])
        self.ai_action_var.set(f"Optimal Move: {action}")
        self.ai_reason_var.set(f"Truth: {reasoning}")

    def update_stats(self):
        net = self.bankroll - 1000.0
        sign = "+" if net >= 0 else ""
        self.stats_var.set(
            f"Hands: {self.hands_played}    "
            f"Wagered: £{self.total_wagered:.2f}    "
            f"P/L: {sign}£{net:.2f}"
        )

    def _set_bankroll_label(self):
        suffix = "  ⚠ IN DEBT" if self.loan_taken else ""
        color  = C['red'] if self.loan_taken else C['white']
        self.bankroll_var.set(f"Bankroll: £{self.bankroll:.2f}{suffix}")
        self.bankroll_label.config(fg=color)

    # ------------------------------------------------------------------ #
    #  GAME FLOW                                                           #
    # ------------------------------------------------------------------ #
    def deal(self):
        try:
            bet = float(self.bet_entry.get())
            if bet <= 0 or bet > self.bankroll: raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Wager", "Enter a valid bet amount (greater than 0 and within bankroll).")
            return

        self.hands_played  += 1
        self.total_wagered += bet

        if self.hands_played % 10 == 0:
            messagebox.showinfo(
                "Reality Check",
                f"Hands played: {self.hands_played}\n"
                f"Money risked: £{self.total_wagered:.2f}\n\n"
                "The casino is designed to keep you sitting here until it's all gone."
            )

        if len(self.deck) < 52:
            self.init_deck()
            self.status_var.set("Deck reshuffled. The house edge resets.")

        self.current_bet = bet
        self.bankroll -= bet
        self._set_bankroll_label()
        self.update_stats()

        self.game_over = False
        self.btn_deal.config(state=tk.DISABLED)
        self.btn_hit.config(state=tk.NORMAL)
        self.btn_stand.config(state=tk.NORMAL)
        self.status_var.set("Make your move.")

        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]

        for c in self.player_hand: self.running_count = update_count(c, self.running_count)
        self.running_count = update_count(self.dealer_hand[0], self.running_count)
        self.update_tutor()
        self.refresh_table(hide_dealer=True)
        self.update_ai()

        if calculate_total(self.player_hand) == 21:
            self.stand()

    def hit(self):
        self.btn_hit.config(state=tk.DISABLED)
        self.btn_stand.config(state=tk.DISABLED)
        new_card = self.deck.pop()
        self.player_hand.append(new_card)
        self.running_count = update_count(new_card, self.running_count)
        self.refresh_table(hide_dealer=True)
        self.update_tutor()
        self.update_ai()
        total = calculate_total(self.player_hand)
        if total > 21:
            self.end_game("You Busted. The math always wins.", lose=True)
        elif total == 21:
            self.stand()
        else:
            self.btn_hit.config(state=tk.NORMAL)
            self.btn_stand.config(state=tk.NORMAL)

    def stand(self):
        self.btn_hit.config(state=tk.DISABLED)
        self.btn_stand.config(state=tk.DISABLED)
        self.running_count = update_count(self.dealer_hand[1], self.running_count)
        self.refresh_table(hide_dealer=False)
        self.root.after(800, self.dealer_play)

    def dealer_play(self):
        while calculate_total(self.dealer_hand) < 17:
            new_card = self.deck.pop()
            self.dealer_hand.append(new_card)
            self.running_count = update_count(new_card, self.running_count)
            self.refresh_table(hide_dealer=False)
            self.root.update()
            self.root.after(700)
        self.update_tutor()
        self.resolve_winner()

    def resolve_winner(self):
        p = calculate_total(self.player_hand)
        d = calculate_total(self.dealer_hand)
        if   d > 21:   self.end_game("Dealer Busts. A temporary victory against the odds.", win=True)
        elif p > d:    self.end_game("You won this hand. Don't mistake luck for skill.", win=True)
        elif d > p:    self.end_game("Dealer Wins. The statistical norm.", lose=True)
        else:          self.end_game("Push. You survived to lose money on the next hand.", push=True)

    def end_game(self, message, win=False, lose=False, push=False):
        self.game_over = True
        self.status_var.set(message)
        self.refresh_table(hide_dealer=False)
        self.update_ai()

        if win:
            if calculate_total(self.player_hand) == 21 and len(self.player_hand) == 2:
                self.bankroll += self.current_bet * 2.5
            else:
                self.bankroll += self.current_bet * 2
        elif push:
            self.bankroll += self.current_bet

        self._set_bankroll_label()
        self.update_stats()
        self.btn_deal.config(state=tk.NORMAL)
        self.btn_hit.config(state=tk.DISABLED)
        self.btn_stand.config(state=tk.DISABLED)

        # ── LOAN / ENDGAME LOGIC ──────────────────────────────────────
        if self.bankroll <= 0:
            if not self.loan_taken:
                take_loan = messagebox.askyesno(
                    "Bankrupt",
                    "You have lost everything.\n\n"
                    "A shadowy figure at the bar offers you a £1,000 loan to keep playing.\n\n"
                    "Do you take it?"
                )
                if take_loan:
                    self.loan_taken = True
                    self.bankroll = 1000.0
                    self._set_bankroll_label()
                    self.status_var.set("You are playing with borrowed money…")
                else:
                    self.trigger_cautionary_tale()
            else:
                self.trigger_educational_end()

    def refresh_table(self, hide_dealer=True):
        self.clear_table()
        if hide_dealer:
            self.draw_card(self.dealer_cards_frame, self.dealer_hand[0])
            self.draw_card(self.dealer_cards_frame, self.dealer_hand[1], hidden=True)
            self.dealer_score_var.set(f"Dealer: {get_card_value(self.dealer_hand[0][0])} + ?")
        else:
            for card in self.dealer_hand:
                self.draw_card(self.dealer_cards_frame, card)
            self.dealer_score_var.set(f"Dealer: {calculate_total(self.dealer_hand)}")
        for card in self.player_hand:
            self.draw_card(self.player_cards_frame, card)
        self.player_score_var.set(f"Player: {calculate_total(self.player_hand)}")

    # ------------------------------------------------------------------ #
    #  END SCREENS                                                         #
    # ------------------------------------------------------------------ #
    def _build_end_screen(self, bg, heading_color, heading, body):
        """Generic end-screen builder with a Play Again button."""
        for w in self.root.winfo_children():
            w.destroy()
        self.root.configure(bg=bg)

        wrapper = tk.Frame(self.root, bg=bg)
        wrapper.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(wrapper, text=heading, font=("Arial", 28, "bold"),
                 bg=bg, fg=heading_color, justify=tk.CENTER).pack(pady=(0, 20))

        tk.Label(wrapper, text=body, font=("Courier New", 13),
                 bg=bg, fg=C['white'], justify=tk.CENTER, wraplength=820).pack(pady=(0, 30))

        # ── session stats recap ───────────────────────────────────────
        net  = self.bankroll - 1000.0
        sign = "+" if net >= 0 else ""
        stats = (
            f"Hands played: {self.hands_played}   "
            f"Total wagered: £{self.total_wagered:.2f}   "
            f"Net: {sign}£{net:.2f}"
        )
        tk.Label(wrapper, text=stats, font=("Arial", 11),
                 bg=bg, fg=C['grey'], justify=tk.CENTER).pack(pady=(0, 30))

        # ── Play Again button ─────────────────────────────────────────
        play_again_btn = tk.Button(
            wrapper, text="▶  PLAY AGAIN",
            font=("Arial", 15, "bold"),
            bg=C['green'], fg="white", relief=tk.FLAT,
            activebackground=self._lighten(C['green']), activeforeground="white",
            padx=30, pady=10, cursor="hand2",
            command=self.restart_game
        )
        play_again_btn.pack(side=tk.LEFT, padx=12)

        quit_btn = tk.Button(
            wrapper, text="✕  QUIT",
            font=("Arial", 15, "bold"),
            bg=C['red'], fg="white", relief=tk.FLAT,
            activebackground=self._lighten(C['red']), activeforeground="white",
            padx=30, pady=10, cursor="hand2",
            command=self.root.destroy
        )
        quit_btn.pack(side=tk.LEFT, padx=12)

    def trigger_cautionary_tale(self):
        self._build_end_screen(
            bg="#0a0a0a",
            heading_color=C['red'],
            heading="A CAUTIONARY TALE",
            body=(
                "You refused the loan, but the damage was already done.\n\n"
                "You go home with empty pockets.  Your family falls apart.\n"
                "Years of chasing losses leave nothing behind.\n\n"
                "One bad night became one bad week became one bad life.\n\n"
                "If you or someone you know is struggling with gambling,\n"
                "please reach out.\n\n"
                "UK: BeGambleAware  —  0808 8020 133  |  begambleaware.org"
            )
        )

    def trigger_educational_end(self):
        self._build_end_screen(
            bg="#1a1a1a",
            heading_color=C['gold'],
            heading="YOU HAVE LOST EVERYTHING. TWICE.",
            body=(
                "The math worked exactly as it was designed to.\n\n"
                "The casino built its chandeliers with money from players\n"
                "who believed they could beat the system.\n\n"
                "If you or someone you know is struggling with gambling,\n"
                "please reach out.\n\n"
                "UK: BeGambleAware  —  0808 8020 133  |  begambleaware.org"
            )
        )

    def restart_game(self):
        """Reset all state and rebuild the full UI."""
        self._reset_state()
        self.setup_ui()


if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackEducationalApp(root)
    root.mainloop()
