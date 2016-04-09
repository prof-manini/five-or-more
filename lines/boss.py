# -*- coding: iso-latin-1 -*-
import game

class Boss:

    """Boss fornisce una interfaccia unica, di alto livello, verso le GUI.

    Alcune delle funzionalità sono implementate da altre classi (es:
    Game, Board) e vengono delegate, altre sono implementate
    direttamente da Boss."""

    def __init__(self):
        self.new_empty_game()
    
    # command
    def new_empty_game(self, size = (9,9)):
        self._game  = game.Game(size)
        self._board = self._game.get_board()

    def move(self, fc, tc):
        self._game.move(fc, tc)

    def load_from_file(self, file):
        # check file ....
        # game.set_data...
        pass

    def save_to_file(self, file):
        # data = game.get_data ...
        # save data to file
        pass

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
        
