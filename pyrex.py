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
        ms = self.matches(string)
        if not ms: return None
        return min(ms, key=lambda x:(x[0], -x[1]))
        
    def matches(self, string):
        P, Q, V = [], [], [-1] * len(self.states)
        answers = []
        
        def add(start, i, j):
            if j==len(self.states): return answers.append((start, i-start))
            if V[j] == i: return
            V[j] = i

            state = self.states[j]
            if isinstance(state, tuple):
                for incr in state:
                    add(start, i, j+incr)
            else:
                Q.append((start, j))
        
        add(0, 0, 0)
        for i, c in enumerate(string):
            add(i, i, 0)
            P, Q = Q, []
            
            for start, j in P:
                state = self.states[j]
                if state is None or c == state:
                    add(start, i+1, j+1)
    
        return answers
