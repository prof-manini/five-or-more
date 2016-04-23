# -*- coding: iso-latin-1 -*-
import game
from datetime import datetime
import common
from common import SAVE_DIR, SETTINGS_DIR


class Boss:

	"""Boss fornisce una interfaccia unica, di alto livello, verso le GUI.

	Alcune delle funzionalitą sono implementate da altre classi (es:
	Game, Board) e vengono delegate, altre sono implementate
	direttamente da Boss."""

	def __init__(self):
		common.init_game_dir()
		self.new_empty_game()

	# command
	def new_empty_game(self, size = (9,9)):
	    self._game  = game.Game(size = size)
	    self._board = self._game.get_board()

	def move(self, fc, tc):
	    self._game.move(fc, tc)

	def load_game(self, file):
		ss = common.read_file(file)

		data = common.check_data(ss, size = self.get_size())
		if data:
			self._game  = game.Game(size = self.get_size(), data = data)
			self._board = self._game.get_board()
			return True
		else:
			return False

	def save_game(self, file=None):
	    if not file:
	    	date = datetime.now().timetuple()[0:7]
	    	file = SAVE_DIR+"data%d.%d.%d.%d.%d.%d.%d"%date

	    common.write_file(file, repr(self._game.get_data()))
	    return file

	def save_score(self, file=None):
		if not file:
			file = SAVE_DIR+"scores"

		scores = common.read_file(file)

		date = datetime.now().timetuple()[0:7]
		scores.append("%d %d.%d.%d.%d.%d.%d.%d"%tuple([self.get_score()]+list(date)))
		
		common.write_file(file, scores)
		return file

	def load_score(self, file=None):
		if not file:
			file = SAVE_DIR+"scores"
		
		ss = common.read_file(file)
		scores = dict()

		if common.check_scores(ss):
			for line in ss:
				points, date = line.strip().split()
				scores[date] = int(points)

		return scores

	def load_records(self, file=None):
		scores = self.load_score(file)
		records = scores.values()
		records.sort(reverse=True)
		return records

	def undo(self):
		result = self._game.undo()
		self._board = self._game.get_board()
		return result # result tell us if you can undo or not

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
	    return self._board.get_raw_data()
	    
	def is_there_free_cells(self):
		return len(self._board.get_all_empty())>0

	def get_paths(self, fc, tc):
		return self._game.get_paths(fc, tc)