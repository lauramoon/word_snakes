# Word snakes

How many words can you find in this 5x5 grid of randomly selected letters?

With Flask on the backend and JavaScript out front, your high score is saved in your browser.

## Note on game name

The code implies that this game is like the game Boggle, but the two games differ in several key ways:
- In Boggle, the letter distribution is closer to the actual distribution of letters in English words; Word Snakes picks from the 26 letters with equal probability
- Boggle is played on a 4x4 grid; this game is 5x5
- Plural words are acceptable in Boggle but don't seem to be included in the dictionary for this game
- One- and two-letter words are not acceptable in Boggle but are here
- Boggle scores words differently than here (here, it is one point per letter)