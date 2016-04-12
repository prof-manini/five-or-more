# -*- coding: iso-latin-1 -*-

import os

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

## changed exceptions raised
def load_integers(file, size = None):
    "Carica una matrice di dimensione SIZE e di interi tra zero e MAX_VALUE"
    try:
    	file = open(file)
    except:
        raise FileError, "Unable to open '%s'."%file
    try:
        rows = [s.strip().split() for s in file]
        rc = len(rows)
        cc = len(rows[0])
        for r in rows:
            if len(r) <> cc:
                raise LinesError, "Le righe del file %s non sono tutte della stessa lunghezza" \
                      % file
        if size and (rc,cc) <> size:
            raise LinesError, "I dati del file %s ha dimensione %s diversa da quella richiesta %s" \
                  % (file, (rc,cc), size)
        ss = []
        for i, r in enumerate(rows):
            try:
                s = map(int, r)
            except ValueError:
                raise LinesError, "La riga %d del file %s non contiene solo numeri interi" \
                      % (i + 1, file)
            if min(s) < 0:
                raise LinesError, "La riga %d del file %s contiene numeri negativi" \
                      % (i + 1, file)
            if max(s) > MAX_VALUE:
                raise LinesError, "La riga %d del file %s contiene numeri maggiori di %d" \
                      % (i + 1, file, MAX_VALUE)
            ss.append(s)
        return ss
    except Exception as e:
    	raise FileError, "Not correct data in file: " + e.message
    finally:
    	file.close()

def random_values(count, zeros):
    import random
    "Una lista di COUNT numeri random tra 0 e 8 di cui ZEROS nulli"   
    ii = [random.choice(range(1,8)) for i in range(count-zeros)]
    ii.extend([0] * zeros)
    random.shuffle(ii)
    return ii
    

def read_file(file):
	if not (os.path.exists(file) and os.path.isfile(file)):
		#raise FileError, "File '%s' don't exists."%file
		return []

	try:
		f = open(file)
	except Exception as e:
		raise FileError, "Error to open file '%s'."%file

	ss = []
	try:
		ss = f.readlines()
	except Exception as e:
		raise FileError, "Error to read data from file '%s'."%file
	finally:
		f.close()

	return ss

def write_file(file, ss):
	path, _ = os.path.split(file)
	if not (os.path.exists(path) and os.path.isdir(path)):
		try:
			os.mkdir(path)
		except Exception as e:
			raise common.FileError, "Error to create directory '%s'."%path

	try:
		f = open(file, "w")
	except Exception as e:
		raise common.FileError, "Can't create file '%s'\n"%file

	try:        	
		f.writelines(ss)
	except Exception as e:
		raise common.FileError, "Error to write data to file '%s'\n"%file
	finally:
		f.close()
