from collections import deque
from functools import reduce

def rex(pattern):
    tokens = deque(pattern)

    def walk(chars):
        while tokens and tokens[0] in chars:
            yield tokens.popleft()

    def option():
        e = sequence()
        for token in walk('|'):
            e2 = sequence()
            e = [(1, len(e)+2)] + e + [(len(e2)+1,)] + e2
        return e        

    def sequence():
        e = []
        while tokens and tokens[0] not in '|)':
            e += repetition()
        return e
        
    def repetition():
        e = primary()
        for token in walk('?*+'):
            if token in '+*': e = e + [(1, -len(e))]
            if token in '?*': e = [(1, len(e)+1)] + e
        return e
        
    def primary():
        token = tokens.popleft()
        if token == '.': return [None]
        if token == '(': return (option(), tokens.popleft())[0]
        return [token]

    return Machine(option())
                
class Machine(object):
    def __init__(self, states):
        self.states = states
        
    def match(self, string):
        A, B = deque(), deque()
        V = [-1] * len(self.states)
             
        def best(a, b):
            if a is None: return b
            if b is None: return a
            return a if a[0] < b[0] or a[0] == b[0] and a[1] > b[1] else b
                
        def add(start, i, j):
            if j==len(self.states): return (start, i-start)
            if V[j] == i: return
            V[j] = i

            state = self.states[j]
            if isinstance(state, tuple):
                return reduce(best, (add(start, i, j+incr) for incr in state))
            else:
                B.append((start, j))
        
        def advance(i, c):
            while A:
                start, j = A.popleft()
                if self.states[j] in (None, c):
                    yield add(start, i+1, j+1)
        
        answer = None
        for i, c in enumerate(string):
            add(i, i, 0)
            A, B = B, A
            answer = reduce(best, advance(i, c), answer)
            
        return answer
