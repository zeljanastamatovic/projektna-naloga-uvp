import re


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
        niz = re.sub(r'[^0-9:]', '', niz)
        if ':' in str(niz):
            i = niz.find(':')
            try:
                self.ura = int(niz[i-2:i])
            except:
                self.ura = int(niz[i-1:i])
            self.minuta = int(niz[i+1:i+3])
        else:
            if is_int(str(niz)):
                self.ura = int(str(niz)) % 24
                self.minuta = 0
            else:
                self.ura = 25
                self.minuta = 25

    def __str__(self):
        return f'{self.ura:02d}:{self.minuta:02d}'

    def __eq__(self, other):
        if self.ura == other.ura and self.minuta == other.minuta:
            return True
        return False

    def __add__(self, other):
        if self.minuta + other.minuta >= 60:
            return Cas(f'{(self.ura + other.ura + 1):02d}: \
                       {(self.minuta + other.minuta - 60):02d}')
        else:
            return Cas(f'{(self.ura + other.ura):02d}: \
                       {(self.minuta + other.minuta):02d}')

    def __sub__(self, other):
        kon = (self.ura * 60 + self.minuta) - (other.ura * 60 + other.minuta)
        if kon < 0:
            kon = - kon
        ura = kon // 60
        minuta = kon - ura * 60
        return Cas(f'{ura:02d}:{minuta:02d}')

    def __gt__(self, other):
        if self.ura > other.ura:
            return True
        if self.ura < other.ura:
            return False
        if self.minuta > other.minuta:
            return True
        return False


def into_minutes(cas):
    if is_int(str(cas)):
        return cas
    return cas.ura * 60 + cas.minuta
