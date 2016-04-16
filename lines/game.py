# -*- coding: iso-latin-1 -*-
import common
import board
import walker
import grouper

# types of moves for history
PC_MOVE = 1
UT_MOVE = 2
GROUP_DEL = 3
SCORE_ADD = 4

class Game:

    _NEXT_VALUES_COUNT = 3

    def __init__(self, size = (9,9), data = None):
    	self.size = size

        self.board = board.Board(self.size)
        self.walker = walker.Walker()
        self.grouper = grouper.Grouper()

        self._score = 0

        self._stone_added    = []
        self._groups_removed = []

        self._history = []
        self._story_point = 0 # segna la posizione rispetto history

        if not data:
        	self._update_next_values()
        	self._add_random_stones()
        else:
	    	story_point, history, next_values, matrix, score = data
	    	self._score = score
	    	self._story_point = story_point
	    	self._history = history
	    	self._next_values = next_values
	    	self.board.load_data(matrix)    	

    # commands
    def move(self, fc, tc):
        self._check_can_move(fc, tc)
        v = self.board.get_value(fc)
        self.board.set_value(fc, 0)

        if self._story_point != len(self._history):
        	self._history = self._history[:self._story_point]
        self._history.append( (UT_MOVE, fc, tc) ) # save move ut
        self._story_point += 1

        self._fill_pos(tc, v)
        if not self.are_groups_removed():
        	self._add_random_stones()
        
    def _add_random_stones(self):
        vv = self._take_next_values()
        cc = self.board.get_all_empty()[:len(vv)] ## se non ci sono abbastanza celle libere dovrebbe dare errore
        # print "free:", cc
        if len(cc) == 0:
            raise common.LinesError, "Non ci sono celle libere!"

        # print "__add_random_stones: zip: %s", zip(cc,vv)
        ss = zip(cc,vv)
        self._stone_added = ss[:]
        for c,v in zip(cc,vv):
            self._fill_pos(c,v)
            self._history.append( (PC_MOVE, tuple(c), v) ) # save move pc
            self._story_point += 1

    def undo(self):
    	mossa_utente_trovata = False
    	for mossa in self._history[self._story_point-1::-1]:
    		if mossa[0] == UT_MOVE:
    			mossa_utente_trovata = True
    			break
    	if not mossa_utente_trovata:
    		return False

    	for move in self._history[self._story_point-1::-1]:
    		if move[0] == UT_MOVE:
    			self.board.set_value(move[1], self.board.get_value(move[2]))
    			self.board.set_value(move[2], 0)
    			self._story_point -= 1
    			break

    		elif move[0] == PC_MOVE:
    			self.board.set_value(move[1], 0)
    		elif move[0] == GROUP_DEL:
    			for c in move[1]:
    				self.board.set_value(c, move[2])
    		else: # score
    			self._score -= move[1]

    		self._story_point -= 1

    	assert self._story_point > 0

    	self._update_next_values() ## genero casualmente, senza ripristinare quelle precedenti?
    	return True

    def redo(self):
    	if len(self._history) == self._story_point:
    		return False # sono gi� alla fine della storia di gioco

    	assert self._history[self._story_point][0] == UT_MOVE

    	mossa_ut_trovata = False
    	for move in self._history[self._story_point:]:
    		if move[0] == UT_MOVE:
    			if mossa_ut_trovata:
    				break
    			mossa_ut_trovata = True
    			self.board.set_value(move[2], self.board.get_value(move[1]))
    			self.board.set_value(move[1], 0)    			

    		elif move[0] == PC_MOVE:
    			self.board.set_value(move[1], move[2])
    		elif move[0] == GROUP_DEL:
    			for c in move[1]:
    				self.board.set_value(c, 0)
    		else: # score
    			self._score += move[1]

    		self._story_point += 1

    	self._update_next_values() ## genero casualmente, senza ripristinare quelle precedenti?    	
    	return True

    # comoda nel debugging!
    def debug_add_random_stones(self):
        self._add_random_stones()
        
    # queries
    def get_size(self):
        return self.size

    def can_move(self, fc, tc):
        try:
            self._check_can_move(fc, tc)
            return True
        except common.LinesError:
            return False

    def get_board(self):
        return self.board
    
    def get_next_values(self):
        return self._next_values

    def get_score(self):
        return self._score

    def get_paths(self, fc, tc):
        return self.walker.get_paths(self.board, fc, tc)

    def get_raw_data(self):
        return self.board.get_raw_data()

    def are_groups_removed(self):
    	return len(self._groups_removed) > 0

    # private
    def _take_next_values(self):
        vv = self.get_next_values()
        self._update_next_values()
        return vv

    def _check_can_move(self, fc, tc):
        fe = te = pe = ""               # from, to, path errors
        if self.board.is_free(fc):
            fe = "la cella %s non contiene una pedina" % str(fc)
        if not self.board.is_free(tc):
            te = "la cella %s non � libera" % str(tc)
        if len(self.get_paths(fc, tc)) == 0:
            pe = "non esiste un percorso da %s a %s" % (str(fc), str(tc))
        if fe or te or pe:
            ee = ", ".join( (fe, te, pe) ) + '.'
            raise common.LinesError, ee
        
    def get_some_random_values(self, count):
        "COUNT interi positivi non nulli"
        return common.random_values(count, 0)

    def _fill_pos(self, pos, value):
        """Assegna il valore VALUE alla posizione POS e rimouve gli
        eventuali gruppi formatisi; aggiorna i punti"""        

        self.board.set_value(pos, value)
        self._groups_removed = [] # tolgo gruppi rimossi precedentemente
        gg = self.grouper.groups_for_pos_in_board(pos, self.board)
        if not gg: return
        
        for g in gg:
            for c in g:
                # print "__fill_pos group:", g
                self.board.set_value(c, 0)
            self._history.append( (GROUP_DEL, tuple(g), value) ) # save group deleting
            self._story_point += 1

        self._score += self._get_points_for_groups(gg)
        self._history.append( (SCORE_ADD, self._get_points_for_groups(gg)) ) # save score adding
        self._story_point += 1
       	self._groups_removed.extend(gg)
        
    def _get_points_for_groups(self, gg):
        #return sum(map(len, gg))
        import math
        return sum([l**(len(gg)+1) for l in map(len, gg)])

    def _update_next_values(self):
        self._next_values = common.random_values(self._NEXT_VALUES_COUNT, 0)
    
    def get_data(self):
    	return self._story_point, self._history, self._next_values, self.board.get_raw_data(), self._score

   #  def _restore_history(self):
   #  	for move in self._history:
			# if move[0] == UT_MOVE:
   #  			self.board.set_value(move[1], self.board.get_value(move[2]))
   #  			self.board.set_value(move[2], 0)
   #  			del self._history[i]
   #  			return

   #  		else if move[0] == PC_MOVE:
   #  			self.board.set_value(move[1], 0)
   #  		else if move[0] == GROUP_DEL:
   #  			for c in move[1]:
   #  				self.board.set_value(c, move[2])
   #  		else: # score
   #  			self._score -= move[1]


#     def add_some_random(self, count = 3):
#         "Aggiunge COUNT pietre con valori random (non nulli)"
#         pp = self.board.get_all_empty()
#         if not pp:
#             raise common.LinesError, "Non ci sono celle libere"
#         pp = pp[:count]
#         print pp
#         vv = self.get_some_random_values(len(pp))
#         cc = zip(pp,vv)
#         for c,v in cc:
#             self._fill_pos(c,v)
#         return cc

