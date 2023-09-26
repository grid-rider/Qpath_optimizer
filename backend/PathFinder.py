# @file PathFinder.py
# @author Evan Brody
# @brief Implements the PathFinder class, which finds the shortest
#        path between two nodes in an undirected weighted graph by
#        solving a QUBO using QAOA.

# Miscellaneous
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

# Qiskit Tools
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.translators import from_docplex_mp
from qiskit_optimization.algorithms import (
    MinimumEigenOptimizer,
    MinimumEigenOptimizationResult,
    RecursiveMinimumEigenOptimizer,
    SolutionSample,
    OptimizationResultStatus,
)
from qiskit.algorithms.optimizers import COBYLA
from qiskit.algorithms.minimum_eigensolvers import QAOA, NumPyMinimumEigensolver
from qiskit.primitives import Sampler
from qiskit.utils import algorithm_globals

# IBM's docplex
from docplex.mp.model import Model

# For random seeding
import time

PENALTY = 99999 # Arbitrarily large number for constraint penalties

# Provides functionality for finding the shortest
# path between two nodes in an undirected weighted
# graph by solving a QUBO using QAOA.
class PathFinder:
    # @param wm ndarray 2D array of edge weights
    def __init__(self, wm: np.ndarray) -> None:
        assert wm.ndim == 2 # Array must be 2D.
        assert wm.shape[0] == wm.shape[1] # Array must be square.

        self.wm = wm # Weight matrix for edges
        self.cf_mdl = Model("sp_qubo") # Cost function model
    
    # Generates a QUBO equation from a number of steps,
    # a starting point, an ending point, and the QUBOSolver's
    # weight matrix for edges.
    # @param p int Number of steps from start to end
    # @param s int Index of start vertex
    # @param t int Index of end vertex
    # @return QuadraticProgram The generated QUBO equation
    def qp_from_matrix(self, p: int, s: int, t: int) -> QuadraticProgram:
        if not self.wm.any(): return
        
        assert self.wm.shape[0] == self.wm.shape[1] # Matrix must be square
        n = self.wm.shape[0]
        
        # 2D array that represents the binary variables
        # within the path matrix (p x n matrix)
        bv_mtx = self.cf_mdl.binary_var_matrix(p, n, 'x')
        
        # Add weight sum to cost function
        cf_sum = []
        for i in range(p-1):
            # Where j and k are indices of vertices
            for j in range(n):
                for k in range(n):
                    cf_sum.append(self.wm[j][k] * bv_mtx[(i, j)] * bv_mtx[(i+1, k)])
        
        # Must start at s
        cf_sum.append(PENALTY * ((1 - bv_mtx[(0, s)]) ** 2))
        # Must end at t
        cf_sum.append(PENALTY * ((1 - bv_mtx[(p-1, t)]) ** 2))
        
        # Must only visit one vertex per hop
        row_sum = []
        for i in range(p):
            for j in range(n):
                row_sum.append(bv_mtx[(i, j)])
            cf_sum.append(PENALTY * ((1 - self.cf_mdl.sum(row_sum)) ** 2))
            row_sum.clear()
            
        # Must only visit any given vertex once
        column_sum = []
        for i in range(n):
            for j in range(p):
                column_sum.append(bv_mtx[(j, i)])
            clmn_sum_exp = self.cf_mdl.sum(column_sum)
            cf_sum.append(PENALTY * (clmn_sum_exp * (clmn_sum_exp - 1)))
            column_sum.clear()
        
        self.cf_mdl.minimize(self.cf_mdl.sum(cf_sum))
        return from_docplex_mp(self.cf_mdl)
    
    # Solves a QUBO using QAOA
    # @param qp QuadraticProgram The QUBO to solve
    # @return MinimumEigenOptimizationResult The solved QUBO
    def solve_qp(self, qp: QuadraticProgram) -> MinimumEigenOptimizationResult:
        operator, offset = qp.to_ising()
        algorithm_globals.random_seed = int(time.time())
        
        qaoa_mes = QAOA(sampler=Sampler(), optimizer=COBYLA(), initial_point=[0.0, 0.0])
        qaoa = MinimumEigenOptimizer(qaoa_mes)
        qaoa_sol = qaoa.solve(qp)

        return qaoa_sol
    
    # Finds the shortest path from s to t in p hops
    # @param p int Number of hops allowed
    # @param s int Index of start vertex
    # @param t int Index of end vertex
    # @return int[] Ordered indices of vertices in the optimal path
    def find_sp(self, p: int, s: int, t: int) -> MinimumEigenOptimizationResult:
        qubo = self.qp_from_matrix(p, s, t)
        sol = self.solve_qp(qubo)
        vdict = sol.variables_dict

        return [int(var[-1]) for var in vdict if vdict[var]]
