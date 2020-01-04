from random import randint
import random
import numpy as np
from copy import deepcopy


class Board:
    def __init__(self):
        self.board = [' ']*9
        self.won = False

    def reset(self):
        self.board = [' ']*9
        self.won = False

    def step(self, action, symbol):
        (x,y) = action
        self.board[y*3+x] = symbol
        self.CheckWinner()
        return (100 if self.won else 0)

    def GetPossibleActions(self):
        L = []
        for i in range(3):
            for j in range(3):
                if self.board[j*3+i] == ' ':
                    L.append((i,j))
        return L

    def Display(self):
        for i in range(3):
            print(" | ", end='')
            for j in range(3):
                print(str(self.board[i*3+j])+" | ",end='')
            print("\n")

    def CheckWinner(self):
        #Checking Horizontal lines
        for i in range(3):
            if self.board[i*3] !=' ' and self.board[i*3] == self.board[i*3+1] and self.board[i*3+1]==self.board[i*3+2]:
                self.won = True
                return True
        #Checking Vertical lines
        for i in range(3):
            if self.board[i] !=' ' and self.board[i] == self.board[i+3] and self.board[i+3]==self.board[i+6]:
                self.won = True
                return True
        #Cheking Diagonals
        self.won = self.board[4] != ' ' and ((self.board[0] == self.board[4] and self.board[4]==self.board[8]) or (self.board[2] == self.board[4] and self.board[4]==self.board[6]))
        return self.won

    def IsFinished(self):
        return self.won or not ' ' in self.board

class Player:
    def __init__(self,name, symbol, isHuman, isRandom):
        self.symbol = symbol
        self.isHuman = isHuman
        self.name = name
        self.ValueFunction = {}
        self.epsilon = 0.99
        self.game_history = []
        self.nbWin = 0
        self.isRandom = isRandom

    def HumanTurn(self, board):
        print(self.name + " it is your turn !")
        print("Please write valid coordinates like x,y.")
        user_in = input("Coordinates :")
        y = int(user_in[2])
        x = int(user_in[0])
        if board.board[y*3+x]!=' ':
            return self.HumanTurn(board)
        return (x,y)

    #Take a random action for a given board
    def RandomAction(self, board):
        x = randint(0,2)
        y = randint(0,2)
        if board.board[y*3+x] != ' ':
            return self.RandomAction(board)
        return (x,y)

    def OptimizedAction(self,board):
        possibleActions = board.GetPossibleActions()
        bestAction = None
        bestValue = None
        for action in possibleActions:
            tempBoard = deepcopy(board.board)
            tempBoard[action[1]*3+action[0]] = self.symbol
            hboard = hash(tuple(tempBoard))
            actionValue = (self.ValueFunction[hboard] if hboard in self.ValueFunction else 0)

            if bestValue == None or bestValue < actionValue:
                bestValue = actionValue
                bestAction = action
        return bestAction

    def IATurn(self,board):
        #Randon Action
        if self.isRandom or random.uniform(0, 1) < self.epsilon:
            return self.RandomAction(board)
        else: #Optimized Action
            return self.OptimizedAction(board)

    def Turn(self, board):
        if self.isHuman:
            return self.HumanTurn(board)
        else:
            return self.IATurn(board)

    #Going throught history to update value function
    def Train(self):
        if self.isHuman:
            return
        for transition in reversed(self.game_history):
            s,_, r, sp = transition
            if not s in self.ValueFunction:
                self.ValueFunction[s]=0
            #Happen when there is a draw
            #Reward is 0 and the last board can have not be seen
            if not sp in self.ValueFunction and r == 0:
                self.ValueFunction[sp] = 0
            if r == 0:
                self.ValueFunction[s] = self.ValueFunction[s] + 0.1*(self.ValueFunction[sp] - self.ValueFunction[s])
            else:
                self.ValueFunction[s] = self.ValueFunction[s] + 0.1*(r - self.ValueFunction[s])
        self.game_history = []

def PlayGame(board, p1,p2, train = True):
    board.reset()
    players = [p2,p1]
    random.shuffle(players)
    currentPlayer = 0
    reward = 0
    while not board.IsFinished():
        action = players[currentPlayer%2].Turn(board)
        reward = board.step(action, players[currentPlayer%2].symbol)

        if currentPlayer != 0:
            s, a, _,_ = players[(currentPlayer+1)%2].game_history[-1]
            players[(currentPlayer+1)%2].game_history[-1] = (s, a, reward * -1, hash(tuple(board.board)))

        if currentPlayer > 1:
            s, a, r,_ = players[currentPlayer%2].game_history[-1]
            players[currentPlayer%2].game_history[-1] = (s, a, r, hash(tuple(board.board)))

        players[currentPlayer%2].game_history.append((hash(tuple(board.board)), action, reward, None))

        if reward != 0:
            #Game is finished and current player has won (no draw)
            players[currentPlayer%2].nbWin+=1

        currentPlayer +=1

    if train:
        p1.Train()
        p2.Train()


def PlayGameHuman(board, p1,p2, train = True):
    board.reset()
    #No random anymore
    p1.epsilon = 0
    players = [p1,p2]
    random.shuffle(players)
    currentPlayer = 0
    reward = 0
    while not board.IsFinished():
        board.Display()
        action = players[currentPlayer%2].Turn(board)
        reward = board.step(action, players[currentPlayer%2].symbol)
        if reward != 0:
            #Game is finished
            board.won = True
            board.Display()
            print(players[currentPlayer%2].name + " won")
            return

        currentPlayer +=1
    board.Display()
    print("It's a draw !")


if __name__ == "__main__":
    p1 = Player("IA_1","X",False, False)
    p2 = Player("IA_2","O", False, False)
    board = Board()
    for i in range(10000):
        if i%10 == 0:
            p1.epsilon =max(p1.epsilon*0.996,0.05)
            p2.epsilon =max(p2.epsilon*0.996,0.05)
            print("Game : " + str(i))
        PlayGame(board,p1,p2)

    #Testing again full random player
    randomPlayer = Player("IA_2","O", False, True)
    p1.nbWin = 0
    nbTest = 1000
    for i in range(0, nbTest):
        PlayGame(board, p1, randomPlayer, train=False)

    print("IA win rate", p1.nbWin/nbTest)
    print("Random Player win rate", randomPlayer.nbWin/nbTest)

    #Playing against you
    p4 = Player("Human","O",True,False)
    PlayGameHuman(board,p1,p4,False)