from random import randint
import random
import numpy as np

class Board:
    def __init__(self):
        self.board = [' ']*9
        self.won = False

    def reset(self):
        self.board = [' ']*9
        self.won = False

    def Display(self):
        for i in range(3):
            print(" | ", end='')
            for j in range(3):
                print(str(self.board[i*3+j])+" | ",end='')
            print("\n")

    def Play(self, x, y, symbol):
        if(x > 2 or y> 2 or x<0 or y <0):
            print("Out Of Bounds")
            return False
        if(self.board[y*3+x]!=' '):
            return False
        self.board[y*3+x] = symbol
        return True

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
    def __init__(self,name, symbol, isHuman):
        self.symbol = symbol
        self.isHuman = isHuman
        self.name = name
        self.ValueFunction = {}
        self.epsilon = 0.99
        self.game_history = []

    def HumanTurn(self, board):
        print(self.name + " it is your turn !")
        print("Please write valid coordinates like (x,y).")
        user_in = input("Coordinates :")
        y = int(user_in[3])
        x = int(user_in[1])
        if board.board[y*3+x]!=' ':
            return HumanTurn(board)
        return (x,y)

    #Take a random action for a given board
    def RandomAction(self, board):
        played = False
        #While has played in a full position
        x = randint(0, 2)
        y = randint(0,2)
        if board.board[y*3+x]!=' ':
            return RandomAction(board)
        return (x,y)

    def OptimizedAction(self,board):
        #I do not want to give the possible actions to the IA
        #It has to learn by itself to not play on a full position
        #It means that all position are possible
        possibleActions = []
        for i in range(3):
            for j in range(3):
                possibleActions.append((i,j))

        bestAction = None
        bestValue = None
        for action in possibleActions:
            actionValue = (self.ValueFunction[board] if board in self.ValueFunction else 0)
            if bestValue ==None or bestValue>actionValue:
                bestValue = actionValue
                bestAction = action
        return bestAction

    def IATurn(self,board):
        #Randon Action
        if random.uniform(0, 1) < self.epsilon:
            self.RandomAction(board)
        else: #Optimized Action
            self.OptimizedAction(board)

    def Turn(self, board):
        if self.isHuman:
            self.HumanTurn(board)
        else:
            self.IATurn(board)

def Train(p1,p2):
    i=1

def PlayGame(board, p1,p2, train = True):
    players = [p1,p2]
    currentPlayer = 0
    while not board.IsFinished():
        action = players[currentPlayer%2]
        currentPlayer +=1
        board.CheckWinner()

def main():
    p1 = Player("IA_1","X",False)
    p2 = Player("IA_2","O", False)

    for i in range(10000):
        if i%10 == 0:
            p1.epsilon =max(p1.epsilon*0.996,0.05)
            p2.epsilon =max(p2.epsilon*0.996,0.05)
        Train(p1,p2)

game = Board()
p1 = Player("Human","X",True)
p1.HumanTurn(game)
game.Display()
game.CheckWinner()
print(game.IsFinished())
