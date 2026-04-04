#!/usr/bin/env python3
"""constraint - Constraint satisfaction solver (Sudoku, N-Queens, graph coloring, custom CSPs)."""

import sys, json, copy

class CSP:
    def __init__(self):
        self.variables = {}  # var -> domain (list of values)
        self.constraints = []  # list of (vars, check_fn)

    def add_var(self, name, domain):
        self.variables[name] = list(domain)

    def add_constraint(self, variables, check_fn):
        self.constraints.append((variables, check_fn))

    def is_consistent(self, assignment, var, val):
        assignment[var] = val
        for cvars, check in self.constraints:
            if all(v in assignment for v in cvars):
                vals = [assignment[v] for v in cvars]
                if not check(*vals):
                    del assignment[var]
                    return False
        del assignment[var]
        return True

    def solve(self, assignment=None):
        if assignment is None: assignment = {}
        if len(assignment) == len(self.variables):
            return dict(assignment)
        # MRV heuristic
        unassigned = [v for v in self.variables if v not in assignment]
        var = min(unassigned, key=lambda v: len(self.variables[v]))
        for val in self.variables[var]:
            if self.is_consistent(assignment, var, val):
                assignment[var] = val
                result = self.solve(assignment)
                if result is not None:
                    return result
                del assignment[var]
        return None

    def solve_all(self, assignment=None, limit=100):
        if assignment is None: assignment = {}
        solutions = []
        self._solve_all(assignment, solutions, limit)
        return solutions

    def _solve_all(self, assignment, solutions, limit):
        if len(solutions) >= limit: return
        if len(assignment) == len(self.variables):
            solutions.append(dict(assignment)); return
        unassigned = [v for v in self.variables if v not in assignment]
        var = min(unassigned, key=lambda v: len(self.variables[v]))
        for val in self.variables[var]:
            if self.is_consistent(assignment, var, val):
                assignment[var] = val
                self._solve_all(assignment, solutions, limit)
                del assignment[var]

def cmd_sudoku(args):
    """Solve Sudoku puzzle (81-char string, 0 for empty)."""
    puzzle = args[0] if args else '530070000600195000098000060800060003400803001700020006060000280000419005000080079'
    csp = CSP()
    for i in range(81):
        r, c = i // 9, i % 9
        name = f"r{r}c{c}"
        if puzzle[i] != '0':
            csp.add_var(name, [int(puzzle[i])])
        else:
            csp.add_var(name, list(range(1, 10)))
    # constraints: all-different in rows, cols, boxes
    def all_diff(a, b): return a != b
    for r in range(9):
        cells = [f"r{r}c{c}" for c in range(9)]
        for i in range(len(cells)):
            for j in range(i+1, len(cells)):
                csp.add_constraint([cells[i], cells[j]], all_diff)
    for c in range(9):
        cells = [f"r{r}c{c}" for r in range(9)]
        for i in range(len(cells)):
            for j in range(i+1, len(cells)):
                csp.add_constraint([cells[i], cells[j]], all_diff)
    for br in range(3):
        for bc in range(3):
            cells = [f"r{br*3+r}c{bc*3+c}" for r in range(3) for c in range(3)]
            for i in range(len(cells)):
                for j in range(i+1, len(cells)):
                    csp.add_constraint([cells[i], cells[j]], all_diff)
    sol = csp.solve()
    if sol:
        print("Solution:")
        for r in range(9):
            row = ' '.join(str(sol[f"r{r}c{c}"]) for c in range(9))
            if r % 3 == 0 and r > 0: print("  ------+-------+------")
            parts = row.split()
            print(f"  {' '.join(parts[0:3])} | {' '.join(parts[3:6])} | {' '.join(parts[6:9])}")
    else:
        print("No solution")

def cmd_queens(args):
    """Solve N-Queens problem."""
    n = int(args[0]) if args else 8
    csp = CSP()
    for i in range(n):
        csp.add_var(f"q{i}", list(range(n)))
    for i in range(n):
        for j in range(i+1, n):
            def check(a, b, di=j-i):
                return a != b and abs(a - b) != di
            csp.add_constraint([f"q{i}", f"q{j}"], check)
    sol = csp.solve()
    if sol:
        print(f"{n}-Queens solution:")
        for r in range(n):
            col = sol[f"q{r}"]
            row = ''.join('♛ ' if c == col else '· ' for c in range(n))
            print(f"  {row}")
    else:
        print("No solution")

def cmd_color(args):
    """Graph coloring: node-node ... [--colors N]"""
    colors = 3
    edges = []
    i = 0
    while i < len(args):
        if args[i] == '--colors': colors = int(args[i+1]); i += 2
        elif '-' in args[i]:
            a, b = args[i].split('-'); edges.append((a, b)); i += 1
        else: i += 1
    nodes = set()
    for a, b in edges: nodes.update([a, b])
    csp = CSP()
    palette = ['Red', 'Blue', 'Green', 'Yellow', 'Orange', 'Purple'][:colors]
    for n in nodes:
        csp.add_var(n, palette)
    for a, b in edges:
        csp.add_constraint([a, b], lambda x, y: x != y)
    sol = csp.solve()
    if sol:
        print(f"Coloring with {colors} colors:")
        for n in sorted(sol):
            print(f"  {n}: {sol[n]}")
    else:
        print(f"No {colors}-coloring exists")

CMDS = {
    'sudoku': (cmd_sudoku, '[PUZZLE] — solve Sudoku (81 chars, 0=empty)'),
    'queens': (cmd_queens, '[N] — solve N-Queens (default 8)'),
    'color': (cmd_color, 'A-B C-D ... [--colors N] — graph coloring'),
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print("Usage: constraint <command> [args...]")
        for n, (_, d) in sorted(CMDS.items()):
            print(f"  {n:8s} {d}")
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd not in CMDS: print(f"Unknown: {cmd}", file=sys.stderr); sys.exit(1)
    CMDS[cmd][0](sys.argv[2:])

if __name__ == '__main__':
    main()
