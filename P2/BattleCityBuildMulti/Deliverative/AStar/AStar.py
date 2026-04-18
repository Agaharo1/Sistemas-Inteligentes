
#Algoritmo A* genérico que resuelve cualquier problema descrito usando la plantilla de la
#la calse Problem que tenga como nodos hijos de la clase Node
from platform import node


class AStar:

    def __init__(self, problem):
        self.open = [] # lista de abiertos o frontera de exploración
        self.precessed = set() # set, conjunto de cerrados (más eficiente que una lista)
        self.problem = problem #problema a resolver

    def GetPlan(self):
        findGoal = False
        
        self.open.clear()
        self.precessed.clear()
        initial = self.problem.Initial()
        initial.SetH(self.problem.Heuristic(initial))
        self.open.append(initial)
        path = []
        

        while not findGoal and len(self.open) > 0:
            self.open.sort(key=lambda x: x.F())
            
            current = self.open.pop(0)
            
            if self.problem.IsASolution(current):
                findGoal = True
                path = self.ReconstructPath(current)
            else:
                self.precessed.add(current)
                
                successors = self.problem.GetSucessors(current)
                
                for successor in successors:
                    if successor not in self.precessed:
                        newG = current.G() + self.problem.GetGCost(successor)
                        
                        inOpen = self.GetSucesorInOpen(successor)
                        
                        if inOpen is None:
                            self._ConfigureNode(successor, current, newG)
                            successor.SetH(self.problem.Heuristic(successor))
                            self.ApendInOpen(successor)
                        else:
                            if newG < inOpen.G():
                                self._ConfigureNode(inOpen, current, newG)
                                inOpen.SetH(self.problem.Heuristic(inOpen))

        for node in path:
            print(f"Path node: {node}")          
        
        return path

    def _ConfigureNode(self, node, parent, newG):
        node.SetParent(parent)
        node.SetG(newG)
        node.SetH(self.problem.Heuristic(node))


    def ApendInOpen(self, node):
        if node.g == None:
            print("ApendInOpen ", node.x, node.y)
        self.open.append(node)
    def GetSucesorInOpen(self,sucesor):
        i = 0
        found = None
        while found == None and i < len(self.open):
            node = self.open[i]
            i += 1
            if node == sucesor:
                found = node
        return found

    #reconstruye el path desde la meta encontrada.
    def ReconstructPath(self, goal):
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = current.GetParent()
        return path[::-1]



