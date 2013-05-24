#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys, pyrex

try: input = raw_input
except NameError: pass

def simulate(machine, string):
    for i, (answer, state) in enumerate(machine.matcher(string)):
        print('Input: ' + string)
        print('       ' + i*' ' + '^' + ' (' + str(i) + ')')
        
        per_line = {j: str((start, i))+' >' for start, j in state}
    
        if answer:
            per_line[len(machine.states)] = str(answer) + ' >'
        
        for j, line in enumerate(machine.source()):
            print('{:>12}{:04d}: {}'.format(per_line.get(j, ''), j, line))

        print('-----')
        input()
        
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('usage: simulator.py <regex> <input>')
        sys.exit(1)
        
    print('-----')
    print('Matching pattern "{}" against input "{}"'.format(*sys.argv[1:]))
    print('-----')
    print()
    simulate(pyrex.rex(sys.argv[1]), sys.argv[2])
