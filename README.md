This Python code simulates a Blackjack game where the player competes against the dealer, following standard Blackjack rules. The program is interactive and allows the player to bet, hit, stand, double down, and split hands.

Beyond the basic gameplay, the script also tracks the player’s capital over time and provides statistical insights by plotting a capital trend.


🎮 How the Game Works
- The game starts with the player entering an initial capital (e.g., 1000 euros).
- The player places a bet before each round.
- The player and dealer receive two initial cards.
- The player can choose to:
   - Hit (take another card)
   - Stand (keep the current hand)
   - Double down (double the bet & take only one more card)
   - Split (if the two starting cards have the same value)
- The dealer must hit until their total score is at least 17.
- The winner is determined:
   - The closest to 21 wins.
   - A score over 21 results in a bust (automatic loss).
   - Blackjack (Ace + 10-point card) wins instantly.
- The player’s capital is updated based on the round outcome.
- The game continues until the player chooses to stop or runs out of money.

  
📊 Statistical & Risk Analysis
1️⃣ Capital Trend Analysis
- Each round’s capital is saved and plotted as a line chart.
- This helps visualize how different betting strategies impact earnings.
- Uses Seaborn and Matplotlib to generate real-time graphs.
2️⃣ Blackjack Probabilities
- The script uses 6 decks (312 total cards)
- Aces are dynamically valued as 1 or 11 based on the best outcome.
- Splitting is allowed only if the player has two identical-value cards.
- The dealer follows the standard rule of hitting until 17.
3️⃣ Testing Strategies
- Players can experiment with different betting styles:
   - Aggressive (high bets, frequent doubling/splitting) → Higher risk but potential for big wins.
   - Conservative (small bets, fewer risky moves) → More consistent but slower capital growth.
   - Card Counting (in future improvements) → The script could be extended to track deck composition and adjust bets accordingly.
📦 Required Python Libraries
- To run this script, install the following dependencies:
```bash
pip install colorama seaborn matplotlib
```

🧠 Insights Gained From Playing
- How often does a Blackjack occur?
- What happens if you always double down?
- Does splitting pairs improve your chances of winning?
- How does capital fluctuate over multiple rounds?
- What is the expected profit/loss per round?
- 
🎉 Conclusion
- This Blackjack game is not just for fun but also a tool for statistical and financial analysis. By tracking capital and applying different strategies, players can understand the mathematics behind Blackjack and improve their decision-making.
