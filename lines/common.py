# -*- coding: iso-latin-1 -*-

import os, crypt, game, random
from subprocess import call

class LinesError(Exception): pass
class FileError(Exception): pass ## added

MAX_VALUE = 8

about_message = "Python clone of Lines - by Luke"

def is_pos_in_size(pos, size):
    # print "is_pos_in_size - pos:%s size:%s" % (pos, size)
    r, c = pos
    return r >= 0 and r < size[0] and c >= 0 and c < size[1]
    
def check_pos_in_size(pos, size):
    "Solleva una eccesione se POS è fuori dai limiti di SIZE"
    if not is_pos_in_size(pos, size):
        r,c = size
        s = "Posizione %s non valida: indici ammessi [0:%d,0:%d]" % \
            (pos, r-1, c-1)
        raise LinesError, s

def check_data(ss, size = (9,9)):
	try:
		data = eval('/n'.join(ss)) # type(ss) = list
		story_point, history, next_values, matrix, score = data		

		for move in history:
			if move[0] == game.UT_MOVE:
				check_pos_in_size(move[1], size)
				check_pos_in_size(move[2], size)
				if move[1] == move[2]: raise Exception, "not a valid move"
			elif move[0] == game.PC_MOVE:
				check_pos_in_size(move[1], size)
				if not (move[2] > 0 and move[2] <= MAX_VALUE and type(move[2]) == int):
					raise Exception, "not a valid stone"
			elif move[0] == game.GROUP_DEL:
				if not (move[2] > 0 and move[2] <= MAX_VALUE and type(move[2]) == int):
					raise Exception, "not a valid stone"
				for c in move[1]:
					check_pos_in_size(c, size)
					for c2 in move[1]:
						if c == c2: raise Exception, "2 cells equals in group deletion"
			elif move[0] == game.SCORE_ADD:
				if type(move[1]) != int or move[1] <= 0:
					raise Exception, "bad score to add"
			elif move[0] == game.NEXT_STONES:
				if type(move[1]) != tuple:
					raise Exception, "bad stones generated"
				if len(move[1]) != 3:
					raise Exception, "bad stones generated"
				for stone in move[1]:
					if not (stone > 0 and stone <= MAX_VALUE and type(stone) == int):
						raise Exception, "not a valid stone"
			elif move[0] == game.RANDOM_STATE:
				pass ## controlli per il seed random?
			else:
				raise Exception, "not a valid move."

		if type(story_point) != int or story_point < 0 or story_point > len(history):
			raise Exception, "bad story point"

		for v in next_values:
			if not (v > 0 and v <= MAX_VALUE) or type(v) != int:
				raise Exception, "bad stone"

		if score < 0 or type(score) != int:
			raise Exception, "bad score"

		check_grid(matrix, size)

		return data
	except Exception as e:
	 	print(e)
	 	print("error log function check_data in common package")
	 	return None

def check_grid(rows, size):
    "Carica una matrice di dimensione SIZE e di interi tra zero e MAX_VALUE"

    try:
        rc = len(rows)
        cc = len(rows[0])
        for r in rows:
            if len(r) != cc:
                raise LinesError, "Le righe non sono tutte della stessa lunghezza"
        if size and (rc,cc) != size:
            raise LinesError, "I dati hanno dimensione %s diversa da quella richiesta %s" \
                  % ((rc,cc), size)

        for i, r in enumerate(rows):
            if min(r) < 0:
                raise LinesError, "La riga %d contiene numeri negativi" \
                      % (i + 1)
            if max(r) > MAX_VALUE:
                raise LinesError, "La riga %d contiene numeri maggiori di %d" \
                      % (i + 1, MAX_VALUE)

            for c in r:
            	if type(c) != int:
            		raise Exception, "La riga %d contiene valori non interi"%i

    except Exception as e:
    	print(e)
    	raise FileError, "Not correct data: " + e.message

def check_scores(ss): ## controllo validità dati score
	return True

def random_values(count, zeros):
    "Una lista di COUNT numeri random tra 0 e 8 di cui ZEROS nulli"
    oldstate = random.getstate()

    ii = [random.choice(range(1,8)) for i in range(count-zeros)]
    ii.extend([0] * zeros)
    random.shuffle(ii)
    return ii, oldstate

def set_random_state(oldstate):
	random.setstate(oldstate)   


def read_file(file, crypting=True):
	if not (os.path.exists(file) and os.path.isfile(file)):
		#raise FileError, "File '%s' don't exists."%file
		return []

	try:
		f = open(file)
	except Exception as e:
		raise FileError, "Error to open file '%s'."%file

	try:
		ll = f.readlines()

		if crypting:
			ss = [crypt.decrypt(l) for l in ll]
			return ss
		else:
			return ll
	except Exception as e:
		raise FileError, "Error to read data from file '%s'."%file
	finally:
		f.close()

def write_file(file, ss, crypting=True):
	path, _ = os.path.split(file)
	if not (os.path.exists(path) and os.path.isdir(path)):
		try:
			os.mkdir(path)
		except Exception as e:
			raise FileError, "Error to create directory '%s'."%path

	try:
		f = open(file, "w")
	except Exception as e:
		raise FileError, "Can't create file '%s'\n"%file

	try:
		if crypting:			
			ll = [crypt.encrypt(s) for s in ss]
		else:
			ll = list(ss)
		f.writelines(ll)
	except Exception as e:
		print e
		raise FileError, "Error to write data to file '%s'\n"%file
	finally:
		f.close()

def get_home_dir():
	try:
		return os.path.expanduser("~") ## forse sotto windows non funziona?
	except:
		return ""


HOME_DIR = get_home_dir()+"/"
GAME_DIR = HOME_DIR+".five/"
SAVE_DIR = GAME_DIR+"saves/"
TMP_DIR = SAVE_DIR+".tmp/"
SETTINGS_DIR = GAME_DIR+"settings/"


def init_game_dir():	
	if not (os.path.exists(GAME_DIR) and os.path.isdir(GAME_DIR)):
		try:
			os.mkdir(GAME_DIR)
		except Exception as e:
			raise FileError, "Error to create directory '%s'."%GAME_DIR

	if not (os.path.exists(SAVE_DIR) and os.path.isdir(SAVE_DIR)):
		try:
			os.mkdir(SAVE_DIR)
		except Exception as e:
			raise FileError, "Error to create directory '%s'."%SAVE_DIR

	if not (os.path.exists(SETTINGS_DIR) and os.path.isdir(SETTINGS_DIR)):
		try:
			os.mkdir(SETTINGS_DIR)
		except Exception as e:
			raise FileError, "Error to create directory '%s'."%SETTINGS_DIR

	if not (os.path.exists(TMP_DIR) and os.path.isdir(TMP_DIR)):
		try:
			os.mkdir(TMP_DIR)
		except Exception as e:
			raise FileError, "Error to create directory '%s'."%TMP_DIR

def delete_tmp():
	if (os.path.exists(TMP_DIR) and os.path.isdir(TMP_DIR)):
		ff = os.listdir(TMP_DIR)
		for f in ff:
			if os.path.isfile(TMP_DIR+f):
				os.remove(TMP_DIR+f)

def get_tmp():
	if (os.path.exists(TMP_DIR) and os.path.isdir(TMP_DIR)):
		ff = os.listdir(TMP_DIR)
		for f in ff:
			if os.path.isfile(TMP_DIR+f):
				try:
					return read_file(TMP_DIR+f)
				except:
					continue
	return None

		