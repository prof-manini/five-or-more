# -*- coding: iso-latin-1 -*-
import game
from datetime import datetime
import common

HOME_DIR = common.get_home_dir()+"/" ## forse sotto windows non funziona?

class Boss:

	"""Boss fornisce una interfaccia unica, di alto livello, verso le GUI.

	Alcune delle funzionalità sono implementate da altre classi (es:
	Game, Board) e vengono delegate, altre sono implementate
	direttamente da Boss."""

	def __init__(self):
	    self.new_empty_game()

	# command
	def new_empty_game(self, size = (9,9)):
	    self._game  = game.Game(size = size)
	    self._board = self._game.get_board()

	def move(self, fc, tc):
	    self._game.move(fc, tc)

	def load_game(self, file):
		ss = common.read_file(file)
		## controllare validità dati

		if ss:
			data = eval("\n".join(ss))
			self._game  = game.Game(size = self.get_size(), data = data)
			self._board = self._game.get_board()

	def save_game(self, file=None):
	    if not file:
	    	date = datetime.now().timetuple()[0:7]
	    	file = HOME_DIR+".saves/data%d.%d.%d.%d.%d.%d.%d"%date

	    common.write_file(file, repr(self._game.get_data()))
	    return file

	def save_score(self, file=None):
		if not file:
			file = HOME_DIR+".saves/scores"

		scores = common.read_file(file)

		date = datetime.now().timetuple()[0:7]
		scores.append("%d %d.%d.%d.%d.%d.%d.%d"%tuple([self.get_score()]+list(date)))
		
		common.write_file(file, scores)
		return file

	def load_score(self, file=None):
		if not file:
			file = HOME_DIR+".saves/scores"
		
		ss = common.read_file(file)

		scores = []
		for line in ss:
			## controllare dati
			points, date = line.strip().split()
			scores.append(int(points))

		return scores

	def load_records(self, file=None):
		scores = self.load_score(file)
		scores.sort(reverse=True)
		return scores

	def undo(self):
		result = self._game.undo()
		self._board = self._game.get_board()
		return result # result tell us if you can go undo or not

	def redo(self):
		result = self._game.redo()
		self._board = self._game.get_board()
		return result # result tell us if you can redo or not


	# query
	def get_size(self):
	    return self._game.get_size()

	def can_move(self, fc, tc):
	    return self._game.can_move(fc, tc)

	def is_free(self, pos):
	    return self._board.is_free(pos)

	def get_next_values(self):
	    return self._game.get_next_values()

	def get_score(self):
	    return self._game.get_score()

	def get_data(self):
	    for rcv in self._board:
	        yield rcv

	def get_raw_data(self):
	    return self._board.get_raw_data() # restituisce la matrice dei colori delle celle
	    
	def is_there_free_cells(self):
		return len(self._board.get_all_empty())>0

	def get_paths(self, fc, tc):
		return self._game.get_paths(fc, tc)