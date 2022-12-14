# -*- coding: utf-8 -*-
"""state_code_words.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wXt-llIUqFTNLV1t5HiYYUqg3nmzfBZl
"""

import pandas as pd
from collections import defaultdict
from urllib.request import urlopen
from IPython.display import SVG, display

class StateCodeWords:
    
    def __init__(self):
        self.DATA = self.get_data()
        self.VOCAB = self.get_vocab()
        self.NGBR = self.get_ngbrs()

    def get_map(self):
        WIKI_URL ='https://upload.wikimedia.org/wikipedia/commons/'
        MAP_URL =  WIKI_URL + '9/92/Map_of_USA_with_state_names_2.svg'
        with urlopen(MAP_URL) as f: state_map = f.read()
        display(SVG(state_map))

    def get_vocab(self):
        VOCAB_URL = 'https://norvig.com/ngrams/sowpods.txt' # source of words
        with urlopen(VOCAB_URL) as f:
            VOCAB = [w for w in f.read().decode('utf-8').split('\n')]
        return [w for w in VOCAB if len(w) > 3]

    def get_data(self):
        GIT_URL = 'https://raw.githubusercontent.com/SumitraMukherjee/'
        CSV_FILE = 'state_code_words/main/state_neighbor.csv'
        df = pd.read_csv(GIT_URL + CSV_FILE)
        return df

    def get_ngbrs(self):
        z = zip(self.DATA.Code, self.DATA.Neighbors)
        return dict((c,n.split(',')) for c,n in z if isinstance(n, str))

    def state_wd(self, w): 
        """Returns True if w is a concatenation of state codes""" 
        return all(s in self.NGBR for s in [w[i:i+2] for i in range(0,len(w),2)])

    def get_state_words(self):
        """Returns dict D[k] = list of words formed by concatenating k states"""
        D = defaultdict(list)
        for w in self.VOCAB:
            if len(w) % 2 == 0 and self.state_wd(w):
                D[len(w)].append(w)
        return D

    def print_words(self, D):
        for k in sorted(D, reverse=True):
            print(f'\n{k}-letter words:')
            for i,w in enumerate(D[k]):
                print('\n'+w, end=', ') if i>0 and i%5==0 else print(w, end=', ')
            print()
    
    def concatenated_code_words(self):
        """Prints words formed by concatenating state codes."""
        print(f'Words formed by concatenating state codes:')
        self.print_words(self.get_state_words())

    def neighboring(self, w):
        if w[:2] not in self.NGBR: return False
        c = [w[i:i+2] for i in range(0, len(w), 2)]
        return all(c2 in self.NGBR[c1] for c1,c2 in zip(c[:-1],c[1:]))

    def get_neighboring_state_words(self):
        """Returns dict D[k] = list of words formed by concatenating k states"""
        D = defaultdict(list)
        for w in self.VOCAB:
            if len(w) % 2 == 0 and self.neighboring(w):
                D[len(w)].append(w)
        return D

    def concatenated_neighboring_code_words(self):
        """Prints words formed by concatenating neighboring state codes."""
        print(f'Words formed by concatenating neighboring state codes:')
        self.print_words(self.get_neighboring_state_words())

    def state_walk(self, k):
        """Returns dict D[s] = list of k-step walk among neighboring states
        where s is a string of sorted letters in the walk"""
        D = defaultdict(list)
        q = [s for s in self.NGBR]
        while q:
            w = q.pop()
            if len(w) == 2 * k:
                D[''.join(sorted(w))].append(w)
            else:
                q += [w+s for s in self.NGBR[w[-2:]]]
        return D

    def state_walk_anagram(self, k):
        D = self.state_walk(k)
        W = defaultdict(set)
        for w in [w for w in self.VOCAB if len(w) == 2 * k]:
            a = ''.join(sorted(w))
            if a in D:
                for p in D[a]:
                    W[w].add(p)
        return W

    def anagram_neighboring_code_walk(self):
        """Prints anagrams of concatenated neighboring state codes."""
        print(f'Anagrams of concatenated neighboring state codes:')
        for k in range(7, 2, -1):
            W = self.state_walk_anagram(k)
            if len(W) > 0:
                print(f'\n{2*k}-letter anagrams of state-code walks')
                for w in W:
                    print(f'\t{w}: {",".join(W[w])}')

    def canon(self, w):
        """Returns canonical form of cycle starting with min element"""
        p = [w[i:i+2] for i in range(0, len(w), 2)]
        i = p.index(min(p))
        return ''.join(min(p[i:]+p[:i], p[:i+1][::-1]+p[i+1:][::-1]))

    def state_cycle(self, k):
        """Returns dict D[s] = list of k-step cycle among neighboring states
        where s is a string of sorted letters in the walk"""
        D = defaultdict(set)
        q = [s for s in self.NGBR]
        while q:
            w = q.pop()
            if len(w) == 2 * k:
                if w[:2] in self.NGBR[w[-2:]]:
                    D[''.join(sorted(w))].add(self.canon(w))
            else :
                q += [w+s for s in self.NGBR[w[-2:]]]
        return D

    def state_cycle_anagram(self, k):
        D = self.state_cycle(k)
        W = defaultdict(set)
        for w in [w for w in self.VOCAB if len(w) == 2 * k]:
            a = ''.join(sorted(w))
            if a in D:
                for p in D[a]:
                    W[w].add(p)
        return W

    def anagram_neighboring_code_tour(self):
        """Prints anagrams of tours of neighboring state codes."""
        print(f'Anagrams of tours of neighboring states:')
        for k in range(6,2,-1):
            W = self.state_cycle_anagram(k)
            if len(W) > 0:
                print(f'\n{2*k}-letter anagrams of state-code tours')
                for w in W:
                    print(f'{w}: {", ".join(W[w])}')