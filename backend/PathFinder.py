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
    GroverOptimizer,
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

# Provides functionality for finding the shortest
# path between two nodes in an undirected weighted
# graph by solving a QUBO using QAOA.
class PathFinder:
    max_hops = 4 # Max number of steps to go from start to end in a graph
    penalty = 99999 # Arbitrarily large number for constraint penalties
    # @param wm ndarray 2D array of edge weights
    def __init__(self, wm: np.ndarray) -> None:
        assert wm.ndim == 2 # Array must be 2D.
        assert wm.shape[0] == wm.shape[1] # Array must be square.

        self.wm = wm # Weight matrix for edges
        self.cf_mdl = Model("sp_qubo") # Cost function model
    
    # Generates a QUBO equation from a starting point, an ending
    # point, and the PathFinder's weight matrix for edges.
    # @param s int Index of start vertex
    # @param t int Index of end vertex
    # @return QuadraticProgram The generated QUBO equation
    def qp_from_matrix(self, s: int, t: int) -> QuadraticProgram:
        if not self.wm.any(): return
        if s is None or t is None: raise Exception
        
        assert self.wm.shape[0] == self.wm.shape[1] # Matrix must be square
        n = self.wm.shape[0]
        
        # 2D array that represents the binary variables
        # within the path matrix (max_hops x n matrix)
        bv_mtx = self.cf_mdl.binary_var_matrix(self.max_hops, n, 'x')
        
        # Add weight sum to cost function
        cf_sum = []
        for i in range(self.max_hops-1):
            # Where j and k are indices of vertices
            for j in range(n):
                for k in range(n):
                    cf_sum.append(self.wm[j][k] * bv_mtx[(i, j)] * bv_mtx[(i+1, k)])
        
        # Must start at s
        cf_sum.append(self.penalty * ((1 - bv_mtx[(0, s)]) ** 2))
        # Must end at t
        cf_sum.append(self.penalty * ((1 - bv_mtx[(self.max_hops-1, t)]) ** 2))
        
        # Must only visit one vertex per hop
        row_sum = []
        for i in range(self.max_hops):
            for j in range(n):
                row_sum.append(bv_mtx[(i, j)])
            cf_sum.append(self.penalty * ((1 - self.cf_mdl.sum(row_sum)) ** 2))
            row_sum.clear()
        
        # NOT NECESSARY
        # Must only visit any given vertex once
        # column_sum = []
        # for i in range(n):
        #     for j in range(self.max_hops):
        #         column_sum.append(bv_mtx[(j, i)])
        #     clmn_sum_exp = self.cf_mdl.sum(column_sum)
        #     cf_sum.append(self.penalty * (clmn_sum_exp * (clmn_sum_exp - 1)))
        #     column_sum.clear()
        
        self.cf_mdl.minimize(self.cf_mdl.sum(cf_sum))
        return from_docplex_mp(self.cf_mdl)
    
    # Solves a QUBO using QAOA
    # @param qp QuadraticProgram The QUBO to solve
    # @return MinimumEigenOptimizationResult The solved QUBO
    def solve_qp(self, qp: QuadraticProgram) -> MinimumEigenOptimizationResult:
        # algorithm_globals.random_seed = int(time.time())
        
        # npme_mes = NumPyMinimumEigensolver()
        # qaoa_mes = QAOA(sampler=Sampler(), optimizer=COBYLA(), initial_point=[0.0, 0.0])
        # qaoa = MinimumEigenOptimizer(qaoa_mes)
        # qaoa_sol = qaoa.solve(qp)
        
        npme_mes = NumPyMinimumEigensolver()
        npme = MinimumEigenOptimizer(npme_mes)
        npme_sol = npme.solve(qp)

        return npme_sol
    
    # Finds the shortest path from s to t
    # @param s int Index of start vertex
    # @param t int Index of end vertex
    # @return list Ordered indices of vertices in the optimal path
    def find_sp(self, s: int, t: int) -> list:
        qubo = self.qp_from_matrix(s, t)
        print("Solving...")
        sol = self.solve_qp(qubo)
        print("Solved.")
        vdict = sol.variables_dict

        hops = [int(var[-1]) for var in vdict if vdict[var]]
        path = []
        for i in hops:
            if i not in path: path.append(i)
        
        return path
