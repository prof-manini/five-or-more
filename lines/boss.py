# -*- coding: iso-latin-1 -*-
import game
from datetime import datetime
import common
from common import SAVE_DIR, SETTINGS_DIR, TMP_DIR


class Boss:

	"""Boss fornisce una interfaccia unica, di alto livello, verso le GUI.

	Alcune delle funzionalità sono implementate da altre classi (es:
	Game, Board) e vengono delegate, altre sono implementate
	direttamente da Boss."""

	def __init__(self):
		common.init_game_dir()		
		self.new_empty_game()
		# non posso salvare tmp -> salvo in gui

	# command
	def new_empty_game(self, size = (9,9)):
		self._game  = game.Game(size = size)
		self._board = self._game.get_board()

	def move(self, fc, tc):
	    self._game.move(fc, tc)
	    self.save_tmp()

	def load_game(self, file):
		ss = common.read_file(file)

		data = common.check_data(ss, size = (9,9))
		if data:
			self._game  = game.Game(size = (9,9), data = data)
			self._board = self._game.get_board()
			return True
		else:
			return False

	def save_game(self, file=None):
	    common.write_file(file, [repr(self._game.get_data())])
	    return file

	def save_tmp(self):
		common.delete_tmp()
		date = datetime.now().timetuple()[0:6]
		file = TMP_DIR+"tmp%04d.%02d.%02d.%02d.%02d.%02d"%date
		_,__, next_values, grid, score = self._game.get_data() # salvo solo situazione finale, altrimenti troppi dati
		common.write_file(file, [repr([0,[], next_values, grid, score])])

	def get_tmp_data(self):
		data_tmp = common.get_tmp()
		if not data_tmp:
			return None

		data = common.check_data(data_tmp, size = (9,9))
		if not data:
			common.delete_tmp()
			return None
		return data

	def load_tmp(self, data=None): # gli passo data già da gui-gui
		if not data: # se non passo data provo a vedere se c'è
			data = self.get_tmp_data()
		if data:
			self._game  = game.Game(size = (9,9), data = data)
			self._board = self._game.get_board()
			return True
		return False

	def finalize_game(self):
		common.delete_tmp()

	def save_score(self, file=None):
		if not file:
			file = SAVE_DIR+"scores"

		scores = common.read_file(file)

		date = datetime.now().timetuple()[0:6]
		scores.append("%d %04d.%02d.%02d.%02d.%02d.%02d"%tuple([self.get_score()]+list(date)))
		
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