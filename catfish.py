import chess
import chess.engine
import random
import time
import sys
import pandas as pd
import numpy as np
board=chess.Board()
count=0
ch=0
transposW={}
transposB={}
#transpos={}

# Define the custom values for pieces
piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 90,
}

def boardaslist(board):
    l=[]
    rows=[]
    for r in range(0,8):
        for c in range(0,8):
            sq=r*8+c
            rows+=[str(board.piece_at(sq))]
        l+=[rows]
        rows=[]
    return(l)

def boardlist(board):
    l=[]
    for row in range(0,8):
        for columns in range(0,8):
            si=row*8+columns
            sq=chess.SQUARES[si]
            p1=board.piece_at(sq)
            p=str(p1)
            if p=='P':
                l+=[10]
            elif p=='B':
                l+=[30]
            elif p=='N':
                l+=[30]
            elif p=='R':
                l+=[50]
            elif p=='Q':
                l+=[90]
            elif p=='K':
                l+=[9000]
            elif p=='p':
                l+=[-10]
            elif p=='n':
                l+=[-30]
            elif p=='b':
                l+=[-30]
            elif p=='r':
                l+=[-50]
            elif p=='q':
                l+=[-90]
            elif p=='k':
                l+=[-9000]
            else:
                l+=[0]
    return(l)

def movesortedlist(board):
    l=list(board.legal_moves)
    nl=[]
    c=0
    for j1 in l:
        board.push_san(str(j1))
        if board.is_checkmate():
            c=1
            cm=j1
        board.pop()
    if c==1:
        return([cm]) 
    for j in l:
        board.push_san(str(j))
        if board.is_capture(j):
            nl=nl+[j]
        else:
            nl+=[j]
        board.pop()
    return(nl)

# Convert board to 2D input with custom piece values
def board_to_input(board):
    board_state = np.zeros((8, 8), dtype=float)  # 2D array for board representation
    piece_map = board.piece_map()
    
    for square, piece in piece_map.items():
        value = piece_values[piece.piece_type]  # Get value for the piece
        if piece.color == chess.BLACK:
            value = -value  # Negate for black pieces
        board_state[square // 8, square % 8] = value

    # Add turn indicator; 1 for White's turn, 0 for Black's turn
    turn_indicator = 1 if board.turn == chess.WHITE else 0
    board_state = np.expand_dims(board_state, axis=-1)  # Add channel dimension
    turn_indicator_array = np.full((8, 8, 1), turn_indicator)  # Create turn indicator array
    board_state = np.concatenate((board_state, turn_indicator_array), axis=-1)  # Combine board state with turn indicator
    
    return board_state

def count_attacked_squares(fen, piece_square):
    
    board = chess.Board(fen)
    
    # Convert the square notation (e.g., "e4") to a square index
    square_index = chess.parse_square(piece_square)
    
    # Get the squares attacked by the piece on the given square
    attacked_squares = board.attacks(square_index)
    
    return len(attacked_squares)

def king_safety(board,white):
    if white:
        posw=board.king(chess.WHITE)
        if posw in [1,2,6] and (board.piece_at(posw+7) == 'P' and board.piece_at(posw+8) == 'P' and (board.piece_at(posw+9) == 'P' or board.piece_at(posw+17) == 'P')):
            return 1
        elif posw == 0 and board.piece_at(posw+8) == 'P' and board.piece_at(posw+9) == 'P':
            return 1
        elif posw == 7 and board.piece_at(posw+7) == 'P' and board.piece_at(posw+8) == 'P':
            return 1
    else:
        posb=board.king(chess.BLACK)
        if posb in [62,57,58] and (board.piece_at(posb-7) == 'p' and board.piece_at(posb-8) == 'p' and (board.piece_at(posb-9) == 'p' or board.piece_at(posb-17) == 'p')):
            return 1
        elif posb == 56 and board.piece_at(posb-8) == 'p' and board.piece_at(posb-7) == 'p':
            return 1
        elif posb == 63 and board.piece_at(posb-8) == 'p' and board.piece_at(posb-9) == 'p':
            return 1
    return(0)

def points(board1,white):
    
    if board1.is_checkmate() and white:
        return(1000000000000000000000000)
    elif board1.is_checkmate() and white==False:
        return(-100000000000000000000000)
    #if board1.fen() in df['FEN']:
    #    return()
    s=0
    piece_countw=0
    piece_countb=0
    
    rookpos=[[0,0,0,0.2,0.2,0,0,0],[0,0,0.1,0.2,0.2,0.1,0,0],[0.1,0.1,0.2,0.3,0.3,0.2,0.1,0.1],[0.1,0.1,0.2,0.3,0.3,0.2,0.1,0.1],[0.1,0.1,0.2,0.3,0.3,0.2,0.1,0.1],[0.1,0.1,0.2,0.3,0.3,0.2,0.1,0.1],[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]]
    kingpos=[[0.7,0.7,0.1,-0.1,-0.1,0.1,0.7,0.7],[-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1],[-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1],[-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1],[-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1],[-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1],[-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1],[-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1]]
    knightpos=[[-0.5,-0.4,-0.3,-0.3,-0.3,-0.3,-0.4,-0.5],[-0.4,-0.2,0,0.05,0.05,0,-0.2,-0.4],[-0.3,0.05,0.1,0.15,0.15,0.1,0.05,-0.3],[-0.3,0,0.1,0.15,0.15,0.1,0,-0.3],[-0.3,0.05,0.1,0.15,0.15,0.1,0.05,-0.3],[-0.3,0.05,0.1,0.15,0.15,0.1,0.05,-0.3],[-0.4,-0.2,0,0.05,0.05,0,-0.2,-0.4],[-0.5,-0.4,-0.3,-0.3,-0.3,-0.3,-0.4,-0.5]]
    pawnpos=[[0,0,0,0,0,0,0,0],[0.05,0.1,0.1,-0.2,-0.2,0.1,0.1,0.05],[0.05,-0.05,-0.1,0.2,0.2,-0.1,-0.05,0.05],[0,0,0,0.3,0.3,0,0,0],[0.05,0.05,0.1,0.25,0.25,0.1,0.05,0.05],[0.1,0.1,0.2,0.3,0.3,0.2,0.1,0.1],[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],[0,0,0,0,0,0,0,0]]
    bishoppos=[[-0.2,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.2],[-0.1,0.05,0,0,0,0,0.05,-0.1],[-0.1,0.1,0.1,0.1,0.1,0.1,0.1,-0.1],[-0.1,0,0.1,0.1,0.1,0.1,0.1,0,-0.1],[-0.1,0.05,0.05,0.1,0.1,0.05,0.05,0.05,-0.1],[-0.1,0,0.05,0.1,0.1,0.05,0.05,0.,-0.1],[-0.1,0.05,0,0,0,0,0.05,-0.1],[-0.2,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.2]]
    
    pawnposend=[[0,0,0,0,0,0,0,0],
             [0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05],
             [0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06],
             [0.08,0.08,0.08,0.08,0.08,0.08,0.08,0.08],
             [0.09,0.09,0.09,0.09,0.09,0.09,0.09,0.09],
             [0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3],
             [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
             [0,0,0,0,0,0,0,0]]

    for row in range(0,8):
        for columns in range(0,8):
            si=row*8+columns
            sq=chess.SQUARES[si]
            p1=board1.piece_at(sq)
            p=str(p1)
            #piece_square = chess.square_name(2)  # Square where the piece is located
            #ns = count_attacked_squares(board1.fen(), piece_square)
            if p=='P':
                s+=10
                piece_countw+=1
            elif p=='B':
                s+=30
            elif p=='N':
                s+=30
                piece_countw+=1
            elif p=='R':
                s+=50
                piece_countw+=1
            elif p=='Q':
                s+=90
                piece_countw+=1
            elif p=='p':
                s-=10
                piece_countb+=1
            elif p=='n':
                s-=30
                piece_countb+=1
            elif p=='b':
                s-=30
                piece_countb+=1
            elif p=='r':
                s-=50
                piece_countb+=1
            elif p=='q':
                s-=90
                piece_countb+=1
            elif p=='K':
                s+=9000
                piece_countw+=1
            elif p=='k':
                s-=9000
                piece_countb+=1
            else:
                s+=0
            piece_count=piece_countw+piece_countb
            
            if p=='N':
                s+=knightpos[row][columns]
            if p=='P':
                if piece_countb>5: s+=pawnpos[row][columns]
                else:
                    s+=pawnposend[row][columns]
            if p=='B':
                s+=bishoppos[row][columns]
            if p=='n':
                s-=knightpos[7-row][7-columns]
            if p=='p':
                if piece_countw>5: s-=pawnpos[7-row][7-columns]
                else: s-pawnposend[7-row][7-columns]
            if p=='b':
                s-=bishoppos[7-row][7-columns]
            if p=='K':
                if piece_count>7: s+=kingpos[row][columns]
            if p=='k':
                if piece_count>7: s-=kingpos[7-row][7-columns]
            if p=='R':
                s+=rookpos[row][columns]
            if p=='r':
                s-=rookpos[7-row][7-columns]
            '''
            ns=len(board.attacks(si))
            if p=='N':
                s+=0.01*3*ns
            if p=='P':
                s+=0.01*ns
            if p=='B':
                s+=0.01*3*ns
            if p=='n':
                s-=0.01*3*ns
            if p=='p':
                s-=0.01*ns
            if p=='b':
                s-=0.01*3*ns
            if p=='R':
                s+=0.01*5*ns
            if p=='r':
                s-=0.01*5*ns 
            '''
            s+=king_safety(board1,white)
    return(s)

'''
   if p=='N':
                s+=0.01*3*ns
            if p=='P':
                s+=0.01*ns
            if p=='B':
                s+=0.01*3*ns
            if p=='n':
                s-=0.01*3*ns
            if p=='p':
                s-=0.01*ns
            if p=='b':
                s-=0.01*3*ns
            if p=='K':
                if piece_count>7: s+=kingpos[row][columns]
            if p=='k':
                if piece_count>7: s-=kingpos[7-row][7-columns]
            if p=='R':
                s+=0.01*5*ns
            if p=='r':
                s-=0.01*5*ns         
'''

def bestmove(board1,depth,white,alpha,beta,positions,evaluations):
    global count
    global ct
    maxi=-99999
    mini=99999
    ma=-99999
    mi=99999
    if depth==1 and white:
        l1=list(board1.legal_moves)
        best=l1[random.randint(0,len(l1)-1)]
        for j in l1:
            board1.push_san(str(j))
            count+=1
            bl=str(board1)
            if board1.is_checkmate():
                best=j
                ma=999999
            elif points(board1,True)>ma:
                ma=points(board1,True)
                best=j
            board1.pop()
        #transpos[bl]=ma

        return([ma,best,positions,evaluations])
    
    elif depth==1 and white==False:
        l2=list(board1.legal_moves)
        best=l2[random.randint(0,len(l2)-1)]
        for j1 in l2:
            board1.push_san(str(j1))
            count+=1
            bl=str(board1)
            if board1.is_checkmate():
                best=j1
                mi=-999999
            elif points(board1,False)<mi:
                mi=points(board1,False)
                best=j1
            board1.pop()
        #transpos[bl]=mi

        #print(best)
        return([mi,best,positions,evaluations])    

    elif white and depth>1:
        l3=movesortedlist(board1)
        #l3=list(board1.legal_moves)
        best=best=l3[random.randint(0,len(l3)-1)]
        for k in l3:
            #if time.time()-ct>=10:
            #   break
            if beta<=alpha:
                break
            board1.push_san(str(k))
            count+=1
            #bl=boardaslist(board1)
            bl=str(board1)
            d=depth-1
            if board1.is_game_over()==False:
                if bl in transposW.keys() and d>=1:
                    eval=transposW[bl]
                    #print('Hi')
                else:
                    bmm=bestmove(board1,d,False,alpha,beta,positions,evaluations)
                    preval=bmm[0]
                    eval=preval
                    if d>=3: transposW[bl]=eval
                if d==1: 
                    #print(k,'-',eval)
                    positions.append(boardlist(board1))
                    evaluations.append(eval)
                    
                if board1.is_checkmate():
                    best=k
                elif eval>maxi:
                    maxi=eval
                    best=k            
                    alpha=max(alpha,eval)
            
            else:
                best=k
                maxi=999999
                eval=maxi
            
            
            #transpos[bl]=eval
            board1.pop()
            #if depth==4:
            #    transpos[bl]=eval
        #transpos[boardaslist(board1)]=maxi
        return([maxi,best,positions,evaluations])

    elif white==False and depth>1:
        l4=movesortedlist(board1)
        #l4=list(board1.legal_moves)
        best=l4[random.randint(0,len(l4)-1)]
        for m in l4:
            #if time.time()-ct>=10:
            #   break
            if beta<=alpha:
                break
            
            board1.push_san(str(m))
            count+=1
            #bl=boardaslist(board1)
            bl=str(board1)
            d=depth-1
            if board1.is_game_over()==False:
                if bl in transposB.keys() and d>=1:
                    eval2=transposB[bl]           
                    #print("Hi")
                else:
                    bmm=bestmove(board1,d,True,alpha,beta,positions,evaluations)
                    preval=bmm[0]
                    eval2=preval
                    if d>=2: transposB[bl]=eval2
                if d==1: 
                    #print(m,"-",eval2)
                    positions.append(boardlist(board1))
                    evaluations.append(eval2)
                    
                if board1.is_checkmate():
                    best=m

                elif eval2<mini:
                    mini=eval2
                    best=m
                    beta=min(beta,eval2)
                
            else:
                best=m
                mini=-999999
                eval2=mini
                #print(m,"-",mini," Mate")
            
            
            #transpos[bl]=eval2
            board1.pop()
            #if depth==3:
            #    transpos[bl]=eval2
        #print(best)
        #transpos[boardaslist(board1)]=mini
        return([mini,best,positions,evaluations])

import chess
from stockfish import Stockfish
from IPython.display import clear_output

# Initialize Stockfish with the path to your Stockfish engine
# Make sure to replace '/path/to/stockfish' with the actual path
stockfish = Stockfish(path="/usr/games/stockfish")

# Set Stockfish skill level (0-20) - for example, level 10
stockfish.set_skill_level(2)

# Function to play a game between Stockfish and `bestmove`
def play_game(w,d,l):
    moves_list = []  # List to store the moves
    board = chess.Board()  # Initialize the chess board
    run=True
    while not board.is_game_over():
        if board.turn == chess.BLACK:  
            stockfish.set_fen_position(board.fen())
            stockfish_move = stockfish.get_best_move()
            moves_list.append(board.san(chess.Move.from_uci(stockfish_move)))
            board.push_uci(stockfish_move)
            clear_output(wait=True)
            print(board)
            print(w,d,l)
            
        else:  
            if run: bestmove_move1 = aswhite(moves_list)
            if bestmove_move1==None: 
                bestmove_move = bestmove(board, 4, board.turn, -99999, 99999, [], [])[1]
                run=False
            else:
                bestmove_move = bestmove_move1
            moves_list.append(bestmove_move)
            board.push_san(str(bestmove_move))
            clear_output(wait=True)
            print(board)
            print(w,d,l)
            if bestmove_move1!=None:
                print('Opening book')
        
    # Return the list of moves and the game result
    return moves_list, board.result()
import pandas as pd
import chess
import random
# Load the CSV file with openings
openings = pd.read_csv("/home/ishan/Documents/openings.csv")  # Ensure the CSV has a column named "Moves". Also, change the path
bl=list(openings['Moves'])
bl=[x.split() for x in bl]
buff=[]
bln=[]
for i in range(len(bl)):
    for j in range(len(bl[i])):
        if bl[i][j][0] in ['1','2','3','4','5','6']:
            buff+=[bl[i][j][2:]]
        else:
            buff+=[bl[i][j]]
    bln+=[buff]
    buff=[]
bl=bln
print(bl)

def asblack(moves):
    k=len(moves)
    mb=None
    ml=[x[0:k] for x in bl]
        
    if moves in ml:
        ind = ml.index(moves)
        print("Index",ind)
        if k<len(bln[ind]):
            mb = bln[ind][k]
    
    return(mb)

def aswhite(moves):
    k=len(moves)
    mw=None
    rd=random.randint(0,len(bl))
    if k==0: 
        mw=bl[rd][k]
        
    else:

        ml=[x[0:k] for x in bl]
        
        if moves in ml:
            ind = ml.index(moves)
            print("Index",ind)
            if k<len(bln[ind]):
                mw = bln[ind][k]

    return(mw)

        
# Run the game and retrieve moves
wins=0
draws=0
losses=0
for i in range(1):
    game_moves, result = play_game(wins,draws,losses)
    if result == '1-0':
        #losses+=1
        wins+=1
    elif result == '1/2-1/2':
        draws+=1
    elif result == '0-1':
        #wins+=1
        losses+=1
#print("Moves played:", game_moves)
print("Game result:")
print('wins:',wins)
print('draws:',draws)
print('losses',losses)

#Note that I have made the bot play as white in this code and arranged the wins and losses accordingly. Make the changes to make it play as black
