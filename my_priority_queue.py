# -*- coding: utf-8 -*-

class PriorityQueue:

    def __init__(self):
        '''tworzy nową pustą kolejkę priorytetową'''
        self.c = []

    def is_empty(self):
        '''zwraca odpowiedź na pytanie, czy kolejka priorytetowa jest pusta'''
        return self.c == []

    def detach(self):
        '''usuwa element o najwyższym priorytecie -- oraz zwraca parę (element, priorytet);
        w przypadku kilku elementów o najwyższym priorytecie brany jest ten dodany najwcześniej;
        w przypadku pustej kolejki -- wyjątek ValueError'''
        if self.is_empty():
            raise ValueError
        
        return self.c.pop(0)

    def attach(self, x, pri):
        '''dokłada nowy element do kolejki priorytetowej'''
        if self.is_empty():
            self.c.insert(0, (x, pri))
        
        for i in range(0, len(self.c)): 
            if self.c[i][1] >= pri: 
                if i == (len(self.c)):
                    self.c.insert(i+1, (x, pri))

            else:
                self.c.insert(i, (x, pri))
                
    def front(self):
        '''zwraca (bez usuwania) element o najwyższym priorytecie jako parę (element, priorytet);
        w przypadku kilku elementów o najwyższym priorytecie brany jest ten dodany najdawniej;
        w przypadku pustej kolejki -- wyjątek ValueError'''
        if self.is_empty():
            raise ValueError
        return self.c[0]