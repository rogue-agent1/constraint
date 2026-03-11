#!/usr/bin/env python3
"""Constraint satisfaction solver (backtracking + AC-3)."""
import sys
class CSP:
    def __init__(self):self.vars={};self.constraints=[]
    def add_var(self,name,domain):self.vars[name]=list(domain)
    def add_constraint(self,fn,scope):self.constraints.append((fn,scope))
    def ac3(self):
        queue=[(x,y) for fn,scope in self.constraints for x in scope for y in scope if x!=y]
        while queue:
            xi,xj=queue.pop(0)
            if self._revise(xi,xj):
                if not self.vars[xi]: return False
                for fn,scope in self.constraints:
                    if xi in scope:
                        for xk in scope:
                            if xk!=xi: queue.append((xk,xi))
        return True
    def _revise(self,xi,xj):
        revised=False
        for x in self.vars[xi][:]:
            if not any(self._consistent(xi,x,xj,y) for y in self.vars[xj]):
                self.vars[xi].remove(x); revised=True
        return revised
    def _consistent(self,v1,x,v2,y):
        for fn,scope in self.constraints:
            if v1 in scope and v2 in scope:
                a={v1:x,v2:y}
                if not fn(a): return False
        return True
    def solve(self,assignment={}):
        if len(assignment)==len(self.vars): return assignment
        v=min((v for v in self.vars if v not in assignment),key=lambda v:len(self.vars[v]))
        for val in self.vars[v]:
            a={**assignment,v:val}
            if all(fn(a) for fn,scope in self.constraints if all(s in a for s in scope)):
                r=self.solve(a)
                if r: return r
        return None
# Demo: map coloring
csp=CSP()
for v in 'ABCDE': csp.add_var(v,['red','green','blue'])
for a,b in [('A','B'),('A','C'),('B','C'),('B','D'),('C','D'),('C','E'),('D','E')]:
    csp.add_constraint(lambda x,a=a,b=b:x.get(a)!=x.get(b),(a,b))
print("Map coloring (5 regions, 3 colors):")
sol=csp.solve()
if sol:
    for k,v in sorted(sol.items()): print(f"  {k} = {v}")
