# -*- coding: iso-latin-1 -*-
import game
from datetime import datetime

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
        f = open(file)
        # controllare file
        data = eval(f.readline())
        self._game  = game.Game(size = self.get_size(), data = data)
        self._board = self._game.get_board()


    def save_game(self, file=None):
        if not file:
        	date = datetime.now().timetuple()[0:7]
        	file = "saves/data%d.%d.%d.%d.%d.%d.%d"%date

        f = open(file, "w")
        try:        	
        	f.writelines(repr(self._game.get_data()))
        except:
        	pass
        finally:
        	f.close()
        return file

    def save_score(self, file=None):
    	if not file:
    		file = "saves/scores"

    	scores = []
    	try:
    		f = open(file)
    		scores = f.readlines()
    		f.close()
    	except:
    		pass

    	date = datetime.now().timetuple()[0:7]
    	scores.append("%d %d.%d.%d.%d.%d.%d.%d"%tuple([self.get_score()]+list(date)))
    	
    	f = open(file, "w") ## controllare che cartella di salvataggio esista, altrimenti crearla
    	f.writelines(scores)
    	f.close()

    def load_score(self, file=None):
    	if not file:
    		file = "saves/scores"

    	scores = []
    	try:
    		with open(file) as f:
    			for line in f.readlines():
    				points, date = line.strip().split()
    				scores.append(int(points))
    	except Exception as e:
    		print(e)
    	return scores

    def load_records(self, file=None):
    	scores = self.load_score(file)
    	scores.sort(reverse=True)
    	return scores

    def undo(self):
    	result = self._game.undo()
    	self._board = self._game.get_board()
    	return result


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