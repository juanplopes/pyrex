def rex(pattern):
    tokens = Tokens(pattern)

    def option():
        split, join = State(), State()
        while True:
            start, end = sequence()
            split.then(start)
            end.then(join)
            if not tokens.maybe('|'): break
        return split, join
        
    def sequence():
        start, end = repetition()
        while tokens.peek('|)', negate=True):
            nstart, nend = repetition()
            end.then(nstart)
            end = nend
        return start, end
        
        
    def repetition():
        start, end = primary()
        while tokens.peek('?*+'):
            split, join = State(), State()
            split.then(start)
            
            if tokens.maybe('?'):
                end.then(join)
                split.then(join)
            elif tokens.maybe('*'):
                end.then(split)
                split.then(join)
            elif tokens.maybe('+'):
                end.then(split)
                end.then(join)

            start, end = split, join
        return start, end
        
    def primary():
        if tokens.maybe('.'):
            state = State(incr=1)
            return state, state
        elif tokens.maybe('('):
            e = option()
            tokens.maybe(')')
            return e
        elif tokens.peek('.+*?()|', negate=True):
            state = State(tokens.next())
            return state, state

    start, end = option()
    end.then(FinalState())
    return Machine(start)

class Tokens:
    def __init__(self, pattern):    
        self.pattern = pattern
        self.i = 0

    def peek(self, chars, negate=False):
        if self.i >= len(self.pattern) or (self.pattern[self.i] not in chars) ^ negate:
            return None
        return self.pattern[self.i]
        
    def next(self):
        self.i += 1
        return self.pattern[self.i - 1]

    def maybe(self, chars):
        return self.peek(chars) and self.next()
    
class Machine(object):
    def __init__(self, state):
        self.state = state
        
    def match(self, string):
        cache = {}
        def ask(state, s, i):
            key = (state, i)
            if key not in cache:
                cache[key] = state.consume(ask, s, i)
            return cache[key]
                
        for i in range(len(string)):
            result = ask(self.state, string, i)
            if result is not None:
                return (i, result)
    
class FinalState(object):
    def consume(self, ask, string, i):
        return 0
       
class State(object):
    def __init__(self, char='', incr=None):
        self.char = char
        self.incr = incr or len(char) or 0
        self.exits = []
       
    def then(self, state):
        self.exits.append(state)
       
    def consume(self, ask, string, i):
        if i+self.incr<=len(string) and (not self.char or string[i] == self.char): 
            for exit in self.exits:
                result = ask(exit, string, i+self.incr)
                if result is not None:
                    return self.incr+result
                    
