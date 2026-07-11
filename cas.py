class cas:
    def __init__(self, niz):
        i = niz.find(':')
        self.ura = int(niz[i-2:i])
        self.minuta = int(niz[i+1:i+3])

    def __str__(self):
        return f'{self.ura:02d}:{self.minuta:02d}'

    def __eq__(self, other):
        if self.ura == other.ura and self.minuta == other.minuta:
            return True
        return False

    def __add__(self, other):
        if self.minuta + other.minuta >= 60:
            if self.ura + other.ura >= 23:
                return cas(f'{self.ura + other.ura + 1 - 24}:{self.minuta + other.minuta - 60}')
            return cas(f'{self.ura + other.ura + 1}:{self.minuta + other.minuta - 60}')
        else:
            if self.ura + other.ura >= 24:
                return cas(f'{self.ura + other.ura - 24}:{self.minuta + other.minuta }')
            return cas(f'{self.ura + other.ura}:{self.minuta + other.minuta}')
        
    def __gt__(self, other):
        if self.ura > other.ura:
            return True
        if self.ura < other.ura:
            return False
        if self.minuta > other.minuta:
            return True
        return False
