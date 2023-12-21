import chess
import chess.engine
import random
import time
board=chess.Board()
count=0
ch=0
transpos={}
def istherecapture(board):
    l=list(board.legal_moves)
    for m in l:
        if board.iscapture(m):
            return(True)
    return(False)

def captureeval(board,m):
    eval=0
    board.push_san(m)
    lm=list(board.legal_moves)
    for l in lm:
        if board.is_capture(l):
            eval=captureeval(board,l)
    return(eval)

def boardaslist(board):
    l=""
    rows=""
    for r in range(0,8):
        for c in range(0,8):
            sq=r*8+c
            rows+=str(board.piece_at(sq))
        l+=rows
        rows=""
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
            nl=[j]+nl
        else:
            nl+=[j]
        board.pop()
    return(nl)

def points(board1,white):
    if board1.is_checkmate() and white:
        return(1000000000000000000000000)
    elif board1.is_checkmate() and white==False:
        return(-100000000000000000000000)
    s=0
    rookpos=[[0,0,0,0.2,0.2,0,0,0],[0,0,0.1,0.2,0.2,0.1,0,0],[0.1,0.1,0.2,0.3,0.3,0.2,0.1,0.1],[0.1,0.1,0.2,0.3,0.3,0.2,0.1,0.1],[0.1,0.1,0.2,0.3,0.3,0.2,0.1,0.1],[0.1,0.1,0.2,0.3,0.3,0.2,0.1,0.1],[0.1,0.1,0.2,0.3,0.3,0.2,0.1,0.1],[0.1,0.1,0.2,0.3,0.3,0.2,0.1,0.1]]
    kingpos=[[0.1,0.1,0.1,-0.1,-0.1,0.1,0.5,0.5],[-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1],[-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1],[-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1],[-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1],[-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1],[-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1],[-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1]]
    knightpos=[[-0.5,-0.4,-0.3,-0.3,-0.3,-0.3,-0.4,-0.5],[-0.4,-0.2,0,0.05,0.05,0,-0.2,-0.4],[-0.3,0.05,0.1,0.15,0.15,0.1,0.05,-0.3],[-0.3,0,0.1,0.15,0.15,0.1,0,-0.3],[-0.3,0.05,0.1,0.15,0.15,0.1,0.05,-0.3],[-0.3,0.05,0.1,0.15,0.15,0.1,0.05,-0.3],[-0.4,-0.2,0,0.05,0.05,0,-0.2,-0.4],[-0.5,-0.4,-0.3,-0.3,-0.3,-0.3,-0.4,-0.5]]
    pawnpos=[[0,0,0,0,0,0,0,0],[0.05,0.1,0.1,-0.2,-0.2,0.1,0.1,0.05],[0.05,-0.05,-0.1,0.2,0.2,-0.1,-0.05,0.05],[0,0,0,0.2,0.2,0,0,0],[0.05,0.05,0.1,0.25,0.25,0.1,0.05,0.05],[0.1,0.1,0.2,0.3,0.3,0.2,0.1,0.1],[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],[0,0,0,0,0,0,0,0]]
    bishoppos=[[-0.2,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.2],[-0.1,0.05,0,0,0,0,0.05,-0.1],[-0.1,0.1,0.1,0.1,0.1,0.1,0.1,-0.1],[-0.1,0,0.1,0.1,0.1,0.1,0.1,0,-0.1],[-0.1,0.05,0.05,0.1,0.1,0.05,0.05,0.05,-0.1],[-0.1,0,0.05,0.1,0.1,0.05,0.05,0.,-0.1],[-0.1,0.05,0,0,0,0,0.05,-0.1],[-0.2,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.2]]
    for row in range(0,8):
        for columns in range(0,8):
            si=row*8+columns
            sq=chess.SQUARES[si]
            p1=board1.piece_at(sq)
            p=str(p1)
            if p=='P':
                s+=10
            elif p=='B':
                s+=30
            elif p=='N':
                s+=30
            elif p=='R':
                s+=50
            elif p=='Q':
                s+=90
            elif p=='K':
                s+=9000
            elif p=='p':
                s-=10
            elif p=='n':
                s-=30
            elif p=='b':
                s-=30
            elif p=='r':
                s-=50
            elif p=='q':
                s-=90
            elif p=='k':
                s-=9000
            else:
                s+=0
            if p=='N':
                s+=knightpos[row][columns]
            if p=='P':
                s+=pawnpos[row][columns]
            if p=='B':
                s+=bishoppos[row][columns]
            if p=='n':
                s-=knightpos[7-row][7-columns]
            if p=='p':
                s-=pawnpos[7-row][7-columns]
            if p=='b':
                s-=bishoppos[7-row][7-columns]
            if p=='K':
                s+=kingpos[row][columns]
            if p=='k':
                s+=kingpos[7-row][7-columns]
            if p=='R':
                s+=rookpos[row][columns]
            if p=='r':
                s-=rookpos[7-row][7-columns]
    return(s)

def bestmove(board1,depth,white,alpha,beta):
    global count
    global ct
    maxi=-99999
    mini=99999
    ma=-99999
    mi=99999
    if depth==1 and white:
        l1=list(board1.legal_moves)
        best=l1[0]
        for j in l1:
            board1.push_san(str(j))
            count+=1
            bl=boardaslist(board1)
            if board1.is_checkmate():
                best=j
                ma=999999999
            elif points(board1,True)>ma:
                ma=points(board1,True)
                best=j
            board1.pop()
        #transpos[bl]=ma
        return([ma,best])
    elif depth==1 and white==False:
        l2=list(board1.legal_moves)
        best=l2[0]
        for j1 in l2:
            board1.push_san(str(j1))
            count+=1
            bl=boardaslist(board1)
            if board1.is_checkmate():
                best=j1
                mi=-999999999
            elif points(board1,False)<mi:
                mi=points(board1,False)
                best=j1
            board1.pop()
        #transpos[bl]=mi

        #print(best)
        return([mi,best])    

    elif white and depth>1:
        l3=movesortedlist(board1)
        best=l3[0]
        for k in l3:
            #if time.time()-ct>=10:
            #   break
            if beta<=alpha:
                break
            board1.push_san(str(k))
            count+=1
            bl=boardaslist(board1)
            d=depth-1
            if board1.is_checkmate()==False:
                if bl in transpos.keys():
                    eval=transpos[bl]
                else:
                    bmm=bestmove(board1,d,False,alpha,beta)
                    preval=bmm[0]
                    eval=preval
                if board1.is_checkmate():
                    best=k
                elif eval>maxi:
                    maxi=eval
                    best=k            
                    alpha=max(alpha,eval)
            else:
                best=k
                maxi=999999999999999999
            board1.pop()
        #transpos[boardaslist(board1)]=maxi
        return([maxi,best])
    
    elif white==False and depth>1:
        l4=movesortedlist(board1)
        best=l4[0]
        for m in l4:
            #if time.time()-ct>=10:
            #   break
            if beta<=alpha:
                break
            board1.push_san(str(m))
            count+=1
            bl=boardaslist(board1)
            d=depth-1
            if board1.is_checkmate()==False:
                if bl in transpos.keys():
                    eval2=transpos[bl]
                else:
                    bmm=bestmove(board1,d,True,alpha,beta)
                    preval=bmm[0]
                    eval2=preval
                #print(m,"-",eval2)
                if board1.is_checkmate():
                    best=m
                elif eval2<mini:
                    mini=eval2
                    best=m
                    beta=min(beta,eval2)
            else:
                best=m
                mini=-99999999999999
                #print(m,"-",mini," Mate")
                
            board1.pop()
        #print(best)
        transpos[boardaslist(board1)]=mini
        return([mini,best])

c=0
wh=input()
if wh=="B":
    c=1
if c==1:
    board.push_san(str("e4"))

    print("--------------------------------------")
    print(board)
    print("e4")
    
    print("--------------------------------------")
    inp=input()
    board.push_san(inp)
    print("--------------------------------------")
    print(board)
    print("--------------------------------------") 
if c==1:
    while((board.is_checkmate()==False or board.is_stalemate()==False)):
        movelist=[]
        moves=list(board.legal_moves)
        boardlist=boardaslist(board)
        if boardlist in transpos.keys():
            move=transpos[board] 
        else:
            movem=bestmove(board,3,True,-99999,99999)
            move=movem[1]
        board.push_san(str(move))
        movelist+=[move]
        print("--------------------------------------")
        print(board)
        print(move)
        print("Positions:",count)
        transpos[boardlist]=movem[0]
        print("--------------------------------------")
        inp=input()
        board.push_san(inp)
        movelist+=[move]
        print("--------------------------------------")
        print(board)
        print("--------------------------------------") 
else:
    while((board.is_checkmate()==False or board.is_stalemate()==False)):
        print("--------------------------------------")
        print(board)
        print("--------------------------------------")
        movelist=[]
        inp=input()
        board.push_san(inp)
        movelist+=[inp]
        print("--------------------------------------")
        print(board)
        print("--------------------------------------")
        moves=list(board.legal_moves)
        boardlist=boardaslist(board)
        if boardlist in transpos.keys():
            move=transpos[board] 
        else:   
            movem=bestmove(board,3,False,-99999,99999)
            move=movem[1]
        board.push_san(str(move))
        movelist+=[move]
        print("--------------------------------------")
        print(board)
        print(move)
        print("Positions:",count)
        transpos[boardlist]=movem[0]
        print("--------------------------------------")
