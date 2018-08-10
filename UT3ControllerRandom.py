import numpy as np

class RandController:

	def __init__(self,game):
		self.game = game; 

	def makeMove(self):
		moves = self.game.allowableMoves(); 
		x = [i for i in range(0,len(moves))]; 
		self.game.buttonPush(moves[np.random.choice(x)]); 