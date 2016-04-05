# -*- coding: iso-latin-1 -*-
class LinesError(Exception): pass

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

def load_integers(file, size = None):
    "Carica una matrice di dimensione SIZE e di interi tra zero e MAX_VALUE"
    file = open(file)
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
    except:
        file.close()
        raise

def random_values(count, zeros):
    import random
    "Una lista di COUNT numeri random tra 0 e 8 di cui ZEROS nulli"   
    ii = [random.choice(range(1,8)) for i in range(count-zeros)]
    ii.extend([0] * zeros)
    random.shuffle(ii)
    return ii
    
