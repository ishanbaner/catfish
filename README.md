# Catfish
Catfish is a simple chess engine in Python.
I have used the Minimax algorithm with alpha-beta pruning (with move-ordering). A small opening database is added, which the bot accesses at the beginning of the game.
Evaluation is based on material, a piece-square table, and whether there is a checkmate or stalemate. 
The code uses PyChess and uses its board representation.

 #Against Stockfish
 Towards the end of the code, I have added a snippet where the bot can play against various levels of Stockfish as white. Changes can be made to make the bot play as black. You are free to make changes in the level of Stockfish, but as of now, the bot performs decently against level 2. 

# Requirements
``` pip install chess ```
