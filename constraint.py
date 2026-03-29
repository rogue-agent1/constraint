#!/usr/bin/env python3
"""CSP Solver - Solve constraint satisfaction problems with backtracking + AC-3."""
import sys
from collections import deque

class CSP:
    def __init__(self):
        self.variables = {}; self.constraints = []; self.neighbors = {}
    def add_var(self, name, domain):
        self.variables[name] = list(domain); self.neighbors.setdefault(name, set())
    def add_constraint(self, vars, fn):
        self.constraints.append((vars, fn))
        for v in vars:
            for u in vars:
                if u != v: self.neighbors.setdefault(v, set()).add(u)
    def ac3(self, domains):
        queue = deque()
        for v in domains:
            for n in self.neighbors.get(v, []):
                queue.append((v, n))
        while queue:
            xi, xj = queue.popleft()
            if self._revise(domains, xi, xj):
                if not domains[xi]: return False
                for xk in self.neighbors[xi]:
                    if xk != xj: queue.append((xk, xi))
        return True
    def _revise(self, domains, xi, xj):
        revised = False
        for x in domains[xi][:]:
            if not any(self._consistent(xi, x, xj, y) for y in domains[xj]):
                domains[xi].remove(x); revised = True
        return revised
    def _consistent(self, v1, val1, v2, val2):
        assign = {v1: val1, v2: val2}
        for vars, fn in self.constraints:
            if v1 in vars and v2 in vars:
                if all(v in assign for v in vars):
                    if not fn(*[assign[v] for v in vars]): return False
        return True
    def solve(self):
        domains = {v: list(d) for v, d in self.variables.items()}
        if not self.ac3(domains): return None
        return self._backtrack({}, domains)
    def _backtrack(self, assignment, domains):
        if len(assignment) == len(self.variables): return dict(assignment)
        var = min((v for v in self.variables if v not in assignment), key=lambda v: len(domains[v]))
        for val in domains[var]:
            assignment[var] = val
            ok = True
            for vars, fn in self.constraints:
                if all(v in assignment for v in vars):
                    if not fn(*[assignment[v] for v in vars]): ok = False; break
            if ok:
                result = self._backtrack(assignment, domains)
                if result: return result
            del assignment[var]
        return None

def main():
    csp = CSP()
    colors = ["red", "green", "blue"]
    for region in ["WA", "NT", "SA", "Q", "NSW", "V", "T"]:
        csp.add_var(region, colors)
    borders = [("WA","NT"),("WA","SA"),("NT","SA"),("NT","Q"),("SA","Q"),("SA","NSW"),("SA","V"),("Q","NSW"),("NSW","V")]
    for a, b in borders:
        csp.add_constraint((a, b), lambda x, y: x != y)
    print("=== CSP Solver (Australia Map Coloring) ===\n")
    solution = csp.solve()
    if solution:
        print("Solution:")
        for region in sorted(solution): print(f"  {region:4s}: {solution[region]}")
    else: print("No solution found")

if __name__ == "__main__":
    main()
