
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *; 
from PyQt5.QtGui import *;
from PyQt5.QtCore import *;
import sys,os

import numpy as np

from ultimateTicTacToe import UT3State
from copy import deepcopy

from matplotlib.backends.backend_qt4agg import FigureCanvas
from matplotlib.figure import Figure, SubplotParams
import matplotlib.pyplot as plt

from UT3ControllerRandom import RandController;

class UT3Window(QWidget):

	def __init__(self):

		super(UT3Window,self).__init__()

		self.computerPlaying = [True,True]; 
		self.currentPlayer = 1; 

		self.setGeometry(800,800,23*26,23*26)
		self.layout = QGridLayout(); 
		self.setLayout(self.layout);

		self.state = UT3State(); 
		self.prevState = self.state.board; 

		self.controller=RandController(self); 

		#self.populateLayout(); 
		

		self.makeViews(); 
		self.setFixedSize(self.size())
		self.show(); 

		if(self.computerPlaying[0]):
			self.controller.makeMove(); 


	def makeViews(self):

		# for i in range(0,81):
		# 	tmp = np.random.randint(-1,2); 
		# 	if(tmp != 0):
		# 		self.state.makeMove(i,tmp); 

		self.imageView = QGraphicsView(self); 
		self.imageScene = QGraphicsScene(self); 

		#use grid layout
		#0,2,4,6,,8,10,12,14,,16,18,20,22 very thin, for micros
		#7,15 somewhat thin, for macros
		veryThin = [0,2,4,6,8,10,12,14,16,18,20,22]; 
		sortOfThin = [7,15]; 
		notThin = [1,3,5,9,11,13,17,19,21]; 

		for v in veryThin:
			self.layout.setColumnStretch(v,1); 
			self.layout.setRowStretch(v,1); 
		for s in sortOfThin:
			self.layout.setColumnStretch(s,2);
			self.layout.setRowStretch(s,2); 
		for n in notThin:
			self.layout.setColumnStretch(n,5); 
			self.layout.setRowStretch(n,5); 

		
		pix = QPixmap(1,1); 
		pix.fill(QtCore.Qt.transparent); 
		painter = QPainter(pix); 
		pen = QPen(QColor(0,255,0,100)); 
		painter.setPen(pen); 
		painter.drawPoint(0,0)
		painter.end(); 
		pix = pix.scaledToWidth(23*25); 
		pix = pix.scaledToHeight(23*25); 
		self.backgroundIndicator = self.imageScene.addPixmap(pix); 


		grids = QLabel(); 
		pix = QPixmap(23,23); 
		pix.fill(QtCore.Qt.transparent); 
		painter = QPainter(pix); 
		pen = QPen(QColor(0,0,0,255)); 
		painter.setPen(pen); 
		for s in sortOfThin:
			for i in range(0,23):
				painter.drawPoint(s,i);
				painter.drawPoint(i,s); 
		painter.end(); 
		pix = pix.scaledToWidth(23*25); 
		pix = pix.scaledToHeight(23*25); 
		#print(pix.size()); 
		#grids.setPixmap(pix)
		#self.layout.addWidget(grids,0,0,23,22)
		self.imageScene.addPixmap(pix); 

		self.imageView.setScene(self.imageScene); 
		self.layout.addWidget(self.imageView,0,0,23,23); 



		self.boardMap = [[],[],[],[],[],[],[],[],[]]; 
		self.buttons = [[],[],[],[],[],[],[],[],[]]; 

		shifts = [0,3,6,27,30,33,54,57,60]; 
		for j in range(0,len(shifts)):

			s=shifts[j]; 
			if(s==-1):
				continue; 
			for i in range(0+s,3+s):
				self.boardMap[j].append(self.state.board[i]); 

			for i in range(9+s,12+s):
				self.boardMap[j].append(self.state.board[i]); 

			for i in range(18+s,21+s):
				self.boardMap[j].append(self.state.board[i]); 

		shifts = {0:1,1:3,2:5,3:9,4:11,5:13,6:17,7:19,8:21}

		for i in range(0,9):
			for j in range(0,9):
				b = QPushButton("");
				ind = [i,j]; 
				b.clicked.connect(lambda ind,x=ind:self.buttonPush(x));
				if(self.boardMap[i][j] == 1):
					b.setStyleSheet("background-color: blue");
				elif(self.boardMap[i][j] == -1):
					b.setStyleSheet("background-color: red"); 
				elif(self.boardMap[i][j] == 3):
					b.setStyleSheet("background-color: purple")
				else:
					b.setStyleSheet("background-color: gray");
				self.buttons[i].append(b); 

				self.layout.addWidget(b,shifts[i],shifts[j]);


	def allowableMoves(self):
		moves = []; 
		for i in range(0,9):
			for j in range(0,9):
				if(self.buttons[i][j].isEnabled()==True):
					moves.append([i,j]); 
		return moves; 

	def keyPressEvent(self,event):
		if(event.key() == (Qt.Key_Control and Qt.Key_Z)):
			self.undo(); 

	def undo(self):
		print("Undoing"); 
		self.state.board = deepcopy(self.prevState);  
		self.remapBoard(); 
		self.currentPlayer = -self.currentPlayer; 
		print("Undone")

	def remapBoard(self):
		self.boardMap = [[],[],[],[],[],[],[],[],[]]; 
		shifts = [0,3,6,27,30,33,54,57,60]; 
		for j in range(0,len(shifts)):

			s=shifts[j]; 
			if(s==-1):
				continue; 
			for i in range(0+s,3+s):
				self.boardMap[j].append(self.state.board[i]); 

			for i in range(9+s,12+s):
				self.boardMap[j].append(self.state.board[i]); 

			for i in range(18+s,21+s):
				self.boardMap[j].append(self.state.board[i]); 
		for i in range(0,9):
			for j in range(0,9):
				if(self.boardMap[i][j] == 1):
					self.buttons[i][j].setStyleSheet("background-color: blue");
					#self.buttons[i][j].setEnabled(False); 
				elif(self.boardMap[i][j] == -1):
					self.buttons[i][j].setStyleSheet("background-color: red");
					#self.buttons[i][j].setEnabled(False); 
				elif(self.boardMap[i][j] == 3):
					self.buttons[i][j].setStyleSheet("background-color: purple")
					#self.buttons[i][j].setEnabled(False);
				else:
					self.buttons[i][j].setStyleSheet("background-color: gray"); 
					#self.buttons[i][j].setEnabled(True); 

	def buttonPush(self,inds):
		self.prevState = deepcopy(self.state.board); 

		#print(inds); 
		if(not self.buttons[inds[0]][inds[1]].isEnabled()):
			return; 

		macRow = inds[0]//3; 
		macCol = inds[1]//3; 
		micRow = inds[0] - macRow*3; 
		micCol = inds[1] - macCol*3; 


		#print([macRow,macCol,micRow,micCol])
		index = self.state.board2Ind([macRow,macCol,micRow,micCol]); 
		self.state.makeMove(index,self.currentPlayer); 
		if(self.currentPlayer == 1):
			self.buttons[inds[0]][inds[1]].setStyleSheet("background-color: blue");
		else:
			self.buttons[inds[0]][inds[1]].setStyleSheet("background-color: red"); 
		#self.buttons[inds[0]][inds[1]].setEnabled(False); 
		self.currentPlayer = -self.currentPlayer; 
		
		#self.state.displayBoard();

		if(self.state.macroBoard[micRow*3+micCol] == 0):
			#print(macRow,macCol)
			for i in range(0,9):
				for j in range(0,9):
					self.buttons[i][j].setEnabled(False); 
			for i in range(0,9):
				for j in range(0,9):
					macRow2 = i//3; 
					macCol2 = j//3; 
					micRow2 = i - macRow2*3; 
					micCol2 = j - macCol2*3; 
					index = self.state.board2Ind([macRow2,macCol2,micRow2,micCol2]); 
					if(macRow2 == micRow and macCol2 == micCol and self.state.board[index] == 0):
						self.buttons[i][j].setEnabled(True); 
		else:
			for i in range(0,9):
				for j in range(0,9):
					self.buttons[i][j].setEnabled(False);
			for i in range(0,9):
				for j in range(0,9):
					macRow2 = i//3; 
					macCol2 = j//3; 
					micRow2 = i - macRow2*3; 
					micCol2 = j - macCol2*3; 
					index = self.state.board2Ind([macRow2,macCol2,micRow2,micCol2]); 
					if(self.state.board[index] == 0 and self.state.macroBoard[macRow2*3+macCol2] == 0):
						self.buttons[i][j].setEnabled(True); 

		pix = self.backgroundIndicator.pixmap(); 
		pix.fill(QColor(0,0,0,0)); 
		painter = QPainter(pix); 
		pen = QPen(QColor(0,255,0,100)); 
		painter.setPen(pen);
		if(self.state.macroBoard[micRow*3+micCol] == 0): 
			for i in range(0,int(23*26/3)):
				for j in range(0,int(23*26/3)):
					painter.drawPoint((micCol*int(23*26/3) + i),(micRow*int(23*26/3) + j))
		else:
			for k in range(0,3):
				for l in range(0,3):
					if(self.state.macroBoard[k*3+l] == 0):
						for i in range(0,int(23*26/3)):
							for j in range(0,int(23*26/3)):
								painter.drawPoint((l*int(23*26/3) + i),(k*int(23*26/3) + j))
		painter.end(); 
		pix = pix.scaledToHeight(23*25); 
		pix = pix.scaledToWidth(23*25); 
		self.backgroundIndicator.setPixmap(pix); 

		self.remapBoard(); 

		if((self.computerPlaying[0] and self.currentPlayer==1) or (self.computerPlaying[1] and self.currentPlayer==-1) and self.state.winner == 0):
			self.controller.makeMove(); 

if __name__ == '__main__':
	app = QApplication(sys.argv); 
	ex = UT3Window(); 
	sys.exit(app.exec_()); 