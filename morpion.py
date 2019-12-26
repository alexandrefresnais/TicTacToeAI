class Board:
    def __init__(self):
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

    def HumanTurn(self, board):
        print(self.name + " it is your turn !")
        print("Please write valid coordinates like (x,y).")
        user_in = input("Coordinates :")
        while(not board.Play(int(user_in[1]), int(user_in[3]), self.symbol)):
            continue

    def Turn(self, board):
        if self.isHuman:
            self.HumanTurn(board)

game = Board()
p1 = Player("Human","X",True)
p1.HumanTurn(game)
game.Display()
game.CheckWinner()
print(game.IsFinished())
