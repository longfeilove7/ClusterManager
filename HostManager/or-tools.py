from __future__ import print_function
from ortools.linear_solver import pywraplp

def main():
  solver = pywraplp.Solver('SolveSimpleSystem',
                           pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
  x = solver.NumVar(0, 1, 'x')
  y = solver.NumVar(0, 2, 'y')
  objective = solver.Objective()
  objective.SetCoefficient(x, 1)
  objective.SetCoefficient(y, 1)
  objective.SetMaximization()
  solver.Solve()
  print('Solution:')
  print('x = ', x.solution_value())
  print('y = ', y.solution_value())

if __name__ == '__main__':
  main()