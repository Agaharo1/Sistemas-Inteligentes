
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
        
        #mientras no encontremos la meta y haya elementos en open....
        while not findGoal and len(self.open) > 0:
            # Ordenar abiertos por F (G + H) para obtener el nodo con menor coste estimado
            self.open.sort(key=lambda x: x.F())
            
            # Extraer el nodo con menor F
            current = self.open.pop(0)
            
            # Comprobar si es la meta
            if self.problem.IsASolution(current):
                findGoal = True
                path = self.ReconstructPath(current)
            else:
                # Añadir a cerrados
                self.precessed.add(current)
                
                # Generar sucesores
                successors = self.problem.GetSucessors(current)
                
                for successor in successors:
                    if successor not in self.precessed:
                        # Calcular el nuevo G
                        newG = current.G() + self.problem.GetGCost(successor)
                        
                        # Comprobar si ya está en abiertos
                        inOpen = self.GetSucesorInOpen(successor)
                        
                        if inOpen is None:
                            # No está en abiertos, lo añadimos
                            self._ConfigureNode(successor, current, newG)
                            successor.SetH(self.problem.Heuristic(successor))
                            self.ApendInOpen(successor)
                        else:
                            # Está en abiertos, comprobar si el nuevo camino es mejor
                            if newG < inOpen.G():
                                self._ConfigureNode(inOpen, current, newG)
                                inOpen.SetH(self.problem.Heuristic(inOpen))

        for node in path:
            print(f"Path node: {node}")          
        
        return path

    #nos permite configurar un nodo (node) con el padre y la nueva G
    def _ConfigureNode(self, node, parent, newG):
        node.SetParent(parent)
        node.SetG(newG)
        node.SetH(self.problem.Heuristic(node))


    def ApendInOpen(self, node):
        if node.g == None:
            print("ApendInOpen ", node.x, node.y)
        self.open.append(node)

    #nos dice si un sucesor está en abierta. Si esta es que ya ha sido expandido y tendrá un coste, comprobar que le nuevo camino no es más eficiente
    #En caso de serlos, _ConfigureNode para setearle el nuevo padre y el nuevo G, asi como su heurística
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
        # Invertir el path para darlo en orden desde inicio a meta
        return path[::-1]



