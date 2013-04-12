from itertools import repeat

def rex(pattern):
    tokens = Tokens(pattern)

    def option():
        es = [sequence()]
        while tokens.maybe('|'):
            es.append(sequence())
        return Option(es)
        
    def sequence():
        es = [repetition()]
        while tokens.avoid_peek('|)'):
            es.append(repetition())
        return Sequence(es)
        
    def repetition():
        e = primary()
        if tokens.maybe('?'):
            e = Repetition(e, 0, 1)
        elif tokens.maybe('*'):
            e = Repetition(e, 0, float('inf'))
        elif tokens.maybe('+'):
            e = Repetition(e, 1, float('inf'))
        return e
        
    def primary():
        if tokens.maybe('.'):
            return Any()
        elif tokens.maybe('('):
            e = option()
            tokens.maybe(')')
            return e
        elif tokens.avoid_peek('.+*?()|'):
            return Literal(tokens.next())

    return option()

class Tokens:
    def __init__(self, pattern):    
        self.pattern = pattern
        self.i = 0

    def eof(self):
        return self.i >= len(self.pattern)

    def avoid_peek(self, chars):
        if self.eof() or self.pattern[self.i] in chars:
            return None
        return self.pattern[self.i]
        
    def next(self):
        self.i += 1
        return self.pattern[self.i - 1]

    def maybe(self, chars):
        if self.eof() or self.pattern[self.i] not in chars:
            return None
        return self.next()
       
            
def backtrack(it, atleast, atmost, string, i):
    if atleast <= 0: yield 0
    if atmost <= 0: return

    child = next(it)
    for consumed in child.consume(string, i):
        for result in backtrack(it, atleast-1, atmost-1, string, i+consumed):
            yield consumed + result

class Machine(object):
    def match(self, string):
        for i in range(len(string)):
            for consumed in self.consume(string, i):
                if consumed > 0:
                    yield (i, consumed)           

class Literal(Machine):
    def __init__(self, char):
        self.char = char
       
    def consume(self, string, i):
        if i < len(string) and string[i] == self.char:
            yield 1

class Any(Machine):
    def consume(self, string, i):
        if i < len(string):
            yield 1

class Sequence(Machine):
    def __init__(self, children):
        self.children = children
        
    def consume(self, string, i):
        n = len(self.children)
        return backtrack(iter(self.children), n, n, string, i)
              
class Option(Machine):
    def __init__(self, children):
        self.children = children
        
    def consume(self, string, i):
        for child in self.children:
            for consumed in child.consume(string, i):
                yield consumed

class Repetition(Machine):
    def __init__(self, child, atleast, atmost):
        self.child = child
        self.atleast = atleast
        self.atmost = atmost
        
    def consume(self, string, i):
        return backtrack(repeat(self.child), self.atleast, self.atmost, string, i)
              

    
    
