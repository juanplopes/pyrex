def rex(pattern):
    tokens = Tokens(pattern)

    def option():
        e = sequence()
        for token in tokens.walk('|'):
            e2 = sequence()
            e = [(1, len(e)+2)] + e + [(len(e2)+1,)] + e2
        return e        

    def sequence():
        e = []
        while tokens.peek('|)', negate=True):
            e += repetition()
        return e
        
    def repetition():
        e = primary()
        for token in tokens.walk('?*+'):
            if token == '?': e = [(1, len(e)+1)] + e
            if token == '+': e = e + [(1, -len(e))]
            if token == '*': e = [(1, len(e)+2)] + e + [(-len(e)-1,)]
        return e
        
    def primary():
        token = next(tokens.walk('', negate=True))
        if token == '.':
            return [None]
        elif token == '(':
            return (option(), next(tokens.walk(')')))[0]
        else:
            return [token]

    return Machine(option())

class Tokens:
    def __init__(self, pattern):    
        self.pattern = pattern
        self.i = 0

    def peek(self, chars, negate=False):
        if self.i < len(self.pattern) and (self.pattern[self.i] in chars) ^ negate:
            return self.pattern[self.i]

    def walk(self, chars, negate=False):
        while self.peek(chars, negate):
            self.i += 1
            yield self.pattern[self.i-1]
                
class Machine(object):
    def __init__(self, states):
        self.states = states
        
    def match(self, string):
        P, Q, V = [], [], [-1] * len(self.states)
        
        def best(a, b):
            if a is None: return b
            if b is None: return a
            return a if (a[0] < b[0] if a[0] != b[0] else a[1] > b[1]) else b
            
        def add(start, i, j):
            if j==len(self.states): return (start, i-start)
            if V[j] == i: return
            V[j] = i

            state = self.states[j]
            if isinstance(state, tuple):
                return reduce(best, (add(start, i, j+incr) for incr in state))
            else:
                Q.append((start, j))
        
        match = None
        add(0, 0, 0)
        for i, c in enumerate(string):
            P, Q = Q, []
            
            for start, j in P:
                state = self.states[j]
                if state is None or c == state:
                    match = best(match, add(start, i+1, j+1))
            add(i+1, i+1, 0)
        return match
    
           
