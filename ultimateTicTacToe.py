import numpy as np; 
from copy import deepcopy



class UT3State:

	def __init__(self,s=None):

		if(s is None):
			self.board =  np.zeros(shape=(81)) #row\col macro, row\col micro
			self.macroBoard = np.zeros(shape=9); 
			self.winner = 0; 
		else:
			self.board = deepcopy(s.board); 
			self.macroBoard = deepcopy(s.macroBoard); 
			self.winner = deepcopy(s.winner); 


	def resetBoard(self):
		self.board = np.zeros(shape=(81)); 

	def isWon(self,micInd):
		#if 9, test macroboard

		#if 0-8, test microboard
		testInd = np.arange(0,9) + micInd*9; 
		
		if(micInd < 9):
			bv = self.board[testInd]; 
		else:
			bv = self.macroBoard;  

		winner = 0; 

		#wins
		if(bv[0]!=0 and bv[0]==bv[1] and bv[1]==bv[2]):
			if(micInd < 9):
				self.macroBoard[micInd] = bv[0]
			winner = bv[0]; 
		elif(bv[3]!=0 and bv[3]==bv[4] and bv[4]==bv[5]):
			if(micInd < 9):
				self.macroBoard[micInd] = bv[3]
			if(winner != 0 and bv[3] != winner):
				winner = 3
			else:
				winner = bv[3]
		elif(bv[6]!=0 and bv[6]==bv[7] and bv[7]==bv[8]):
			if(micInd < 9):
				self.macroBoard[micInd] = bv[6]
			if(winner != 0 and bv[6] != winner):
				winner = 3
			else:
				winner = bv[6]
		elif(bv[0]!=0 and bv[0]==bv[3] and bv[3]==bv[6]):
			if(micInd < 9):
				self.macroBoard[micInd] = bv[0]
			if(winner != 0 and bv[0] != winner):
				winner = 3
			else:
				winner = bv[0] 
		elif(bv[1]!=0 and bv[1]==bv[4] and bv[4]==bv[7]):
			if(micInd < 9):
				self.macroBoard[micInd] = bv[1]
			if(winner != 0 and bv[1] != winner):
				winner = 3
			else:
				winner = bv[1]
		elif(bv[2]!=0 and bv[2]==bv[5] and bv[5]==bv[8]):
			if(micInd < 9):
				self.macroBoard[micInd] = bv[2]
			if(winner != 0 and bv[2] != winner):
				winner = 3
			else:
				winner = bv[2]
		elif(bv[0]!=0 and bv[0]==bv[4] and bv[4]==bv[8]):
			if(micInd < 9):
				self.macroBoard[micInd] = bv[0]
			winner = bv[0]
		elif(bv[2]!=0 and bv[2]==bv[4] and bv[4]==bv[6]):
			if(micInd < 9):
				self.macroBoard[micInd] = bv[2]
			if(winner != 0 and bv[2] != winner):
				winner = 3
			else:
				winner = bv[2]
		else:
			winner = 0;

		return winner

	def ind2Board(self,ind):
		mac = ind//9; 
		macRow = mac//3; 
		macCol = mac%3; 

		mic = ind-9*mac; 
		micRow = mic//3; 
		micCol = mic%3; 

		return [macRow,macCol,micRow,micCol]; 

	def board2Ind(self,board):
		return board[0]*27 + board[1]*9 + board[2]*3 + board[3];  

	def makeMove(self,ind,player):
		self.board[ind] = player; 
		b = self.ind2Board(ind); 
		macInd = b[0]*3+b[1]; 
		minWin = self.isWon(macInd); 
		if(minWin != 0):
			for i in range(0,3):
				for j in range(0,3):
					tmpInd = self.board2Ind([b[0],b[1],i,j]); 
					self.board[tmpInd] = minWin; 

		winner = self.isWon(9); 
		if(winner != 0):
			if(winner == 1):
				pl = 1; 
			else:
				pl = 2; 
			for i in range(0,len(self.board)):
				self.board[i] = winner; 
			print("Game Over! Player {} wins!".format(pl))

	def displayBoard(self):
		boardString = ['','','','------------','','','','------------','','','']; 
		playerMap = {1:'X',-1:'O',0:'*'};

		shifts = [0,3,6,-1,27,30,33,-1,54,57,60]; 
		for j in range(0,len(shifts)):

			s=shifts[j]; 
			if(s==-1):
				continue; 
			for i in range(0+s,3+s):
				boardString[j] += playerMap[self.board[i]]; 
			boardString[j]+='|'; 

			for i in range(9+s,12+s):
				boardString[j] += playerMap[self.board[i]]; 
			boardString[j]+='|'; 

			for i in range(18+s,21+s):
				boardString[j] += playerMap[self.board[i]]; 



		for b in boardString:
			print(b); 
		print("");
		print("");  



def testIndexing():
	a = UT3State(); 

	board = [0,1,2,1]; #should be 16 
	c = a.board2Ind(board); 
	print(c); 
	print(a.ind2Board(c)); 


def testWon():
	a = UT3State(); 

	negs = [12,13,14]; 
	pos = [9,16,17]; 

	for n in negs:
		a.board[n] = -1; 
	for p in pos:
		a.board[p] = 1; 

	print(a.isWon(1)); 

def testDisplay():
	a = UT3State(); 

	negs = [12,13,14,27,33]; 
	pos = [9,16,17,30,54,65]; 

	for n in negs:
		a.board[n] = -1; 
	for p in pos:
		a.board[p] = 1; 

	a.displayBoard();

	a.board[64] = 1; 
	a.displayBoard(); 
	



if __name__ == '__main__':

	#testIndexing(); 
	#testWon(); 
	testDisplay(); 


