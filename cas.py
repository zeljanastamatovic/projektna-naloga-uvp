def is_int(val):
    try:
        int(val)
        return True
    except ValueError:
        return False
    

class Cas:
    def __init__(self, niz):
        if niz is None:
            self.ura = 25
            self.minuta = 25
        if ':' in str(niz):
            i = niz.find(':')
            self.ura = int(niz[i-2:i])
            self.minuta = int(niz[i+1:i+3])
        else:
            if is_int(str(niz)):
                self.ura = int(str(niz)) % 24
                self.minuta = 0
            else:
                self.ura = 25
                self.minuta = 25
                

    def __str__(self):
        return f'Cas({self.ura:02d}:{self.minuta:02d})'

    def __eq__(self, other):
        if self.ura == other.ura and self.minuta == other.minuta:
            return True
        return False

    def __add__(self, other):
        if self.minuta + other.minuta >= 60:
            if self.ura + other.ura >= 23:
                return Cas(f'{self.ura + other.ura + 1 - 24}:{self.minuta +
                           other.minuta - 60}')
            return Cas(f'{self.ura + other.ura + 1}:{self.minuta +
                       other.minuta - 60}')
        else:
            if self.ura + other.ura >= 24:
                return Cas(f'{self.ura + other.ura - 24}:{self.minuta +
                           other.minuta}')
            return Cas(f'{self.ura + other.ura}:{self.minuta + other.minuta}')

    def __gt__(self, other):
        if self.ura > other.ura:
            return True
        if self.ura < other.ura:
            return False
        if self.minuta > other.minuta:
            return True
        return False
