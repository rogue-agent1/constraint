#!/usr/bin/env python3
"""constraint - Constraint satisfaction problem solver."""
import sys, itertools

class Variable:
    def __init__(self, name, domain):
        self.name = name
        self.domain = list(domain)

class Constraint:
    def __init__(self, variables, predicate):
        self.variables = variables
        self.predicate = predicate

    def satisfied(self, assignment):
        vals = []
        for v in self.variables:
            if v not in assignment:
                return True
            vals.append(assignment[v])
        return self.predicate(*vals)

class CSP:
    def __init__(self):
        self.variables = {}
        self.constraints = []

    def add_variable(self, name, domain):
        self.variables[name] = Variable(name, domain)
        return self

    def add_constraint(self, var_names, predicate):
        self.constraints.append(Constraint(var_names, predicate))
        return self

    def all_different(self, var_names):
        for i in range(len(var_names)):
            for j in range(i + 1, len(var_names)):
                self.add_constraint([var_names[i], var_names[j]], lambda a, b: a != b)
        return self

    def solve(self):
        return self._backtrack({})

    def _backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return dict(assignment)
        unassigned = [v for v in self.variables if v not in assignment]
        var = min(unassigned, key=lambda v: len(self.variables[v].domain))
        for value in self.variables[var].domain:
            assignment[var] = value
            if all(c.satisfied(assignment) for c in self.constraints):
                result = self._backtrack(assignment)
                if result is not None:
                    return result
            del assignment[var]
        return None

    def solve_all(self, limit=100):
        solutions = []
        self._backtrack_all({}, solutions, limit)
        return solutions

    def _backtrack_all(self, assignment, solutions, limit):
        if len(solutions) >= limit:
            return
        if len(assignment) == len(self.variables):
            solutions.append(dict(assignment))
            return
        unassigned = [v for v in self.variables if v not in assignment]
        var = unassigned[0]
        for value in self.variables[var].domain:
            assignment[var] = value
            if all(c.satisfied(assignment) for c in self.constraints):
                self._backtrack_all(assignment, solutions, limit)
            del assignment[var]

def test():
    csp = CSP()
    csp.add_variable("A", [1, 2, 3])
    csp.add_variable("B", [1, 2, 3])
    csp.add_variable("C", [1, 2, 3])
    csp.all_different(["A", "B", "C"])
    sol = csp.solve()
    assert sol is not None
    assert len(set(sol.values())) == 3
    all_sols = csp.solve_all()
    assert len(all_sols) == 6
    csp2 = CSP()
    csp2.add_variable("X", [1, 2, 3, 4])
    csp2.add_variable("Y", [1, 2, 3, 4])
    csp2.add_constraint(["X", "Y"], lambda x, y: x + y == 5)
    sol2 = csp2.solve()
    assert sol2["X"] + sol2["Y"] == 5
    all2 = csp2.solve_all()
    assert len(all2) == 4
    csp3 = CSP()
    csp3.add_variable("A", [1])
    csp3.add_variable("B", [1])
    csp3.all_different(["A", "B"])
    assert csp3.solve() is None
    print("All tests passed!")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("constraint: CSP solver. Use --test")
