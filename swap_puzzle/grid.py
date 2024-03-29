"""
This is the grid module. It contains the Grid class and its associated methods.
"""
from itertools import permutations
import random
import matplotlib.pyplot as plt
from graph import Graph
import heapq
import copy
class Grid():
    """
    A class representing the grid from the swap puzzle. It supports rectangular grids. 

    Attributes: 
    -----------
    m: int
        Number of lines in the grid
    n: int
        Number of columns in the grid
    state: list[list[int]]
        The state of the grid, a list of list such that state[i][j] is the number in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..m and columns are numbered 0..n.
    """
    
    def __init__(self, m, n, initial_state = []):
        """
        Initializes the grid.

        Parameters: 
        -----------
        m: int
            Number of lines in the grid
        n: int
            Number of columns in the grid
        initial_state: list[list[int]]
            The intitial state of the grid. Default is empty (then the grid is created sorted).
        """
        self.m = m
        self.n = n
        if not initial_state:
            initial_state = [list(range(i*n+1, (i+1)*n+1)) for i in range(m)]            
        self.state = initial_state

    def __str__(self): 
        """
        Prints the state of the grid as text.
        """
        output = f"The grid is in the following state:\n"
        for i in range(self.m): 
            output += f"{self.state[i]}\n"
        return output

    def __repr__(self): 
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: m={self.m}, n={self.n}>"

    def is_sorted(self):
        """
        Checks is the current state of the grid is sorted and returns the answer as a boolean.
        """
        b = Grid(len(self.state), len(self.state[0])) #new sorted grid
        if self.state == b.state :
            return True
        else :
            return False
        

    def swap(self, cell1, cell2):
        """
        Implements the swap operation between two cells. It can be an impossible swap but we created a function that convert an impossible swap in a sequence of possible swap (see solver.py line 51)

        Parameters: 
        -----------
        cell1, cell2: tuple[int]
            The two cells to swap. They must be in the format (i, j) where i is the line and j the column number of the cell. 
        """
        self.state[cell1[0]][cell1[1]], self.state[cell2[0]][cell2[1]] = self.state[cell2[0]][cell2[1]], self.state[cell1[0]][cell1[1]]
       

    def swap_seq(self, cell_pair_list):
        """
        Executes a sequence of swaps. 

        Parameters: 
        -----------
        cell_pair_list: list[tuple[tuple[int]]]
            List of swaps, each swap being a tuple of two cells (each cell being a tuple of integers). 
            So the format should be [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...].
        """
        n = len(cell_pair_list)
        for i in range(n):
            a1 = cell_pair_list[i][0]
            a2 = cell_pair_list[i][1]
            self.swap(a1, a2)
    @classmethod
    def grid_from_file(cls, file_name): 
        """
        Creates a grid object from class Grid, initialized with the information from the file file_name.
        
        Parameters: 
        -----------
        file_name: str
            Name of the file to load. The file must be of the format: 
            - first line contains "m n" 
            - next m lines contain n integers that represent the state of the corresponding cell

        Output: 
        -------
        grid: Grid
            The grid
        """
        with open(file_name, "r") as file:
            m, n = map(int, file.readline().split())
            initial_state = [[] for i_line in range(m)]
            for i_line in range(m):
                line_state = list(map(int, file.readline().split()))
                if len(line_state) != n: 
                    raise Exception("Format incorrect")
                initial_state[i_line] = line_state
            grid = Grid(m, n, initial_state)
        return grid


    def rep_grid(self):
        """
        Plot a representation of a grid, according to its current state, using matplotlib.pyplot.
        
        Parameters: 
        -----------
        Output: 
        -------
        """
        #quadrillage
        for k in range(self.n):
            for j in range(self.m):
                plt.plot([k-1, k, k, k-1, k-1], [j-1, j-1, j, j, j-1], 'k')

        #remplissage des cases avec leurs pondérations respectives
        for i in range(self.m-1, -1, -1):
            for j in range(0,self.n):
                plt.text(j-1/2, self.m - 2 -(i-1/2), round(self.state[i][j], 1), fontsize = 15, horizontalalignment = 'center', verticalalignment = 'center')
        
        plt.axis('off')    
        plt.show()

    def grid_to_tuple(self):
        """
        Convert a grid (2-dimensionals) into a tuple (1-dimensional) with the following rule : (first line, second line, ... , last line)
        
        Parameters: 
        -----------
        Output: 
        -------
        t : tuple(int) 
            Describe the state of a grid using a tuple
        """
        l = []
        m = self.m
        n = self.n
        for i in range(m):
            for j in range(n):
                l.append(self.state[i][j])
        t = tuple(l)
        return t

    def tuple_to_int(self, t):
        """
        Convert a tuple describing a state of a grid into a integer (hash function)
        
        Parameters: 
        -----------
        t : tuple(int)
            Describe the state of a grid using a tuple
        Output: 
        -------
        a : int 
            Describe the state of a grid using an integer
        """
        res = ""
        for i in range(len(t)):
            res = res + str(t[i])
        a = int(res)
        return a

    def int_to_tuple(self, n):
        """
        Convert a int describing a state of a grid into a tuple (reciprocal hash function)
        
        Parameters: 
        -----------
        a : int 
            Describe the state of a grid using an integer
        Output: 
        -------
        t : tuple(int)
            Describe the state of a grid using a tuple
        """
        a = str(n)
        b = len(a)
        t = []
        for i in range(b):
            t.append(int(a[i]))
        return tuple(t)

    def swap_in_tuples(self, t, i, j):
        """
        Allow the swap of two elements in a tuple (by creating a new one because tuple is a immutable object)       
        
        Parameters: 
        -----------
        t : tuple
            Tuple on wich we want to make a swap
        i, j: index of the tuple elements that we want to swap
        Output: 
        -------
        T : tuple
            Tuple on wich the swap was made
        """
        L = list(t)
        L[i], L[j] = L[j], L[i]
        T = tuple(L)
        return T

    def tuple_to_grid(self, t, m, n):
        """
        Convert a tuple into a grid. m*n must be equal to len(t)
        
        Parameters : 
        -----------
        t: tuple
            Tuple to be converted.
        m, n : int
            Respectively the number of lines and column of the grid
        Output :
        -------
        g : Grid
            Grid with the numbers gave by t and with dimensions (m,n)
        """
       
        L = []
        for i in range(m):
            L2 = []
            for j in range(n):
                L2.append(t[n*i + j])
            L.append(L2)
        g = Grid(m, n, L)
        return g   

    def simple_swap(self, g1, g2):
        """
        Returns the swap from g1 to g2 which are only separated by one swap
        
        Parameters: 
        -----------
        g1 : grid
        g2 : grid
        Output: 
        -------
        T : tuple(tuple(int, int), tuple(int, int))
            Tuple of the swap from g1 to g2
        """
        m, n = g1.m, g1.n
        L = []
        for i in range(m):
            for j in range(n):
                if g1.state[i][j] != g2.state[i][j]:
                    L.append((i,j))
        T = tuple(L)
        return T

    def bfs_2(self):
        """
        Gives a solution of optimal length for the swap puzzle using BFS algorithm
        
        Parameters: 
        -----------
        Output: 
        -------
        L_p : list[tuple(tuple(int, int), tuple(int, int))]
            List of swaps that described the optimal solution to go from the initial state of grid to the sorted state
        """
        n,m = self.n, self.m
        A = n*m
        L = list(permutations(range(1, A+1), A))
        g = Graph()
        L_hash = []
        for i in L:
            L_hash.append(self.tuple_to_int(i))
        g.nodes = L_hash
        for t in L: 
            for j in range(m):
                for i in range(n-1):
                    g.add_edge(self.tuple_to_int(t),self.tuple_to_int(self.swap_in_tuples(t,n*j + i, n*j + i+1 )))
            for j in range(m-1):
                for i in range(n):
                    g.add_edge(self.tuple_to_int(t),self.tuple_to_int(self.swap_in_tuples(t,n*j + i, n*(j+1) + i)))
        src = self.tuple_to_int(self.grid_to_tuple())

        c = Grid(m,n)
        dst = self.tuple_to_int(c.grid_to_tuple())
            
        X = g.bfs(src, dst)
        L_s = []
        N = len(X)
        for i in range(N-1):
            L_s.append(self.simple_swap(self.tuple_to_grid(self.int_to_tuple(X[i]), self.m, self.n), self.tuple_to_grid(self.int_to_tuple(X[i+1]), self.m, self.n)))
        T_s = tuple(L_s)  
        return T_s
#Le graphe g est constitué de (n*m)! sommets et de 2mn-n-m arrêtes

    def heuristique(self, grid):
        value = 0
        for i in range(self.m):
            for j in range(self.n):
                if self.state[i][j] != grid.state[i][j]:
                    value += 1
        return value/2
    
    def voisin(self):
        L_swap = []
        L_voisin = []
        E = [-1, 1]
        m = self.m
        n = self.n
        for i in range(self.m):
            for j in range(self.n):
                for k in E:
                    if i+k < self.m and i+k > -1:
                        if ((i, j), (i+k, j)) not in L_swap and ((i+k, j), (i, j)) not in L_swap:
                            L_swap.append(((i, j), (i+k, j)))

                    if j+k < self.n and j+k > -1:
                        if ((i, j), (i, j+k)) not in L_swap and ((i, j+k), (i, j)) not in L_swap:
                            L_swap.append(((i, j), (i, j+k)))
        
        for swap in L_swap:
            new_grid = self.result_swap(swap)
            L_voisin.append(new_grid)
        return L_voisin


                    

    def result_swap(self, swap):
        """
        swap : ((i_1,j_1),(i_2,j_2))
        Args:
            swap (_type_): _description_
        """
        L = copy.deepcopy(self.state)
        m = self.m
        n = self.n
        L[swap[0][0]][swap[0][1]], L[swap[1][0]][swap[1][1]] = L[swap[1][0]][swap[1][1]], L[swap[0][0]][swap[0][1]]
        G = Grid(m, n, L)
        return G

    def compareheuristique(self, grid1, grid2):
        if self.heuristique(grid1) < self.heuristique(grid2):
            return 1
        elif self.heuristique(grid1) == self.heuristique(grid2):
            return 0
        else:
            return -1

    def A_etoile(self, départ):
        m = self.m
        n = self.n
        closedFile = []
        openFile = []
        heapq.heapify(openFile)
        
        heapq.heappush(openFile, (self.heuristique(départ), 0, départ.tuple_to_int(départ.grid_to_tuple())))
        while len(openFile) > 0:
            heuristique_g, cout_g, g_int = heapq.heappop(openFile)
            g = self.tuple_to_grid(self.int_to_tuple(g_int), m, n)
            if self.state == g.state:
                closedFile.append((self.heuristique(g), cout_g, g.tuple_to_int(g.grid_to_tuple())))
        
                return closedFile
            L_voisin = g.voisin()
            cout_i = cout_g - 1
            for i in L_voisin:
                if i not in closedFile or (self.heuristique(i), cout_i, i.tuple_to_int(i.grid_to_tuple())) not in openFile:
                    openFile.append((self.heuristique(i), cout_i, i.tuple_to_int(i.grid_to_tuple())))
            heapq.heapify(openFile)
            closedFile.append((self.heuristique(g), cout_g, g.tuple_to_int(g.grid_to_tuple())))
        return None
                   




