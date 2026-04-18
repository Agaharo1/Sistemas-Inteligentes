from StateMachine.State import State
from States.AgentConsts import AgentConsts
from MyProblem.BCProblem import BCProblem


class ExecutePlan(State):

    def __init__(self, id):
        super().__init__(id)
        self.nextNode = 0
        self.lastMove = 0
        self.transition = ""

    def Start(self,agent):
        self.transition = ""
        self.XPos = -1
        self.YPos = -1
        self.noMovements = 0

    def Update(self, perception, map, agent):
        shot = False
        move = self.lastMove
        xW = perception[AgentConsts.AGENT_X]
        yW = perception[AgentConsts.AGENT_Y]
        distance=abs(self.XPos - xW) + abs(self.YPos - yW)
        self.XPos = xW
        self.YPos = yW

        pX = perception[AgentConsts.PLAYER_X]
        pY = perception[AgentConsts.PLAYER_Y]
        if pX > 0 and pY > 0:
            distToPlayer = abs(xW - pX) + abs(yW - pY)
            if distToPlayer < 6.0:  
                is_in_sight = False
                move_towards = AgentConsts.NO_MOVE
                directions = [
                    (AgentConsts.NEIGHBORHOOD_UP, AgentConsts.MOVE_UP),
                    (AgentConsts.NEIGHBORHOOD_DOWN, AgentConsts.MOVE_DOWN),
                    (AgentConsts.NEIGHBORHOOD_RIGHT, AgentConsts.MOVE_RIGHT),
                    (AgentConsts.NEIGHBORHOOD_LEFT, AgentConsts.MOVE_LEFT)
                ]
                for dir_idx, move_cmd in directions:
                    if perception[dir_idx] == AgentConsts.PLAYER:
                        move_towards = move_cmd
                        is_in_sight = True
                        break
                
                if is_in_sight:
                    self.lastMove = move_towards
                    return move_towards, (perception[AgentConsts.CAN_FIRE] == 1)
                else:
                    diffX = pX - xW
                    diffY = pY - yW
                    if abs(diffX) > abs(diffY):
                        move_towards = AgentConsts.MOVE_RIGHT if diffX > 0 else AgentConsts.MOVE_LEFT
                    else:
                        move_towards = AgentConsts.MOVE_UP if diffY > 0 else AgentConsts.MOVE_DOWN
                    
                    self.lastMove = move_towards
                    return move_towards, (perception[AgentConsts.CAN_FIRE] == 1)
        # -----------------------------------------------

        if distance < 0.1 :
            self.noMovements += 1
        else:
            self.noMovements = 0
        x,y = BCProblem.WorldToMapCoordFloat(xW,yW,agent.problem.ySize)
        plan = agent.GetPlan()
        if len(plan) == 0 : 
            agent.goalMonitor.ForceToRecalculate()
            return AgentConsts.NO_MOVE,False
        
        nextNode = plan[0]
        if self.IsInNode(nextNode,x,y,self.lastMove,0.17) and len(plan) >= 1:
            plan.pop(0)
            if len(plan) == 0: 
                agent.goalMonitor.ForceToRecalculate()
                return AgentConsts.NO_MOVE,False
            nextNode = plan[0]
        goal = agent.problem.GetGoal()
       
        if  len(plan) <= 1 and (goal.value == AgentConsts.PLAYER or goal.value == AgentConsts.COMMAND_CENTER): 
            self.transition = "Attack"
            move = self.GetDirection(nextNode,x,y)
            agent.directionToLook = move-1 
            shot = self.lastMove == move and perception[AgentConsts.CAN_FIRE] == 1
        else:
            move = self.GetDirection(nextNode,x,y)
            shot = nextNode.value == AgentConsts.BRICK or nextNode.value == AgentConsts.COMMAND_CENTER
        self.lastMove = move
        return move, shot

    def Transit(self,perception, map):
        if self.transition != None and self.transition != "":
            return self.transition
        elif self.noMovements > 5:
            return "RandomMovement"
        return self.id

    @staticmethod
    def MoveDown(node,x,y):
        return abs(node.x+0.5 - x) <= abs(node.y+0.5 - y) and (node.y+0.5) >= y 
    

    @staticmethod
    def MoveUp(node,x,y):
        return abs(node.x+0.5 - x) <= abs(node.y+0.5 - y) and (node.y+0.5) <= y 
    

    @staticmethod
    def MoveRight(node,x,y):
        return abs(node.x+0.5 - x) >= abs(node.y+0.5 - y) and (node.x+0.5) >= x 
    

    @staticmethod
    def MoveLeft(node,x,y):
        return abs(node.x+0.5 - x) >= abs(node.y+0.5 - y) and (node.x +0.5) <= x 
    
    @staticmethod
    def IsInNode(node, x,y, lastDir, threshold):
        distanceX = abs((node.x+0.5) - x)
        distanceY = abs((node.y+0.5) - y)
        inAceptZone = abs((node.x+0.5) - x) < threshold and abs((node.y+0.5) - y)< threshold 
        if inAceptZone:
            return True
        else:
            directionX,directionY = ExecutePlan.GetDirectionVector(lastDir)
            simulateX = x+directionX*threshold
            simulateY = y+directionY*threshold
            simulateDistanceX = abs((node.x+0.5) - simulateX)
            simulateDistanceY = abs((node.y+0.5) - simulateY)
            if (simulateDistanceX+simulateDistanceY) > (distanceX+distanceY): 
                return True
            else: 
                return False

    @staticmethod
    def GetDirectionVector(direction):
        if direction == AgentConsts.NO_MOVE:
            return 0.0, 0.0
        elif direction == AgentConsts.MOVE_UP:
            return 0.0, -1.0
        elif direction == AgentConsts.MOVE_DOWN:
            return 0.0, 1.0
        elif direction == AgentConsts.MOVE_RIGHT:
            return 1.0, 0.0
        else:
            return -1.0, 0.0

    def GetDirection(self, node, x, y):
        if ExecutePlan.MoveDown(node,x,y):
            return AgentConsts.MOVE_DOWN
        elif ExecutePlan.MoveUp(node,x,y):
            return AgentConsts.MOVE_UP
        elif ExecutePlan.MoveRight(node,x,y):
            return AgentConsts.MOVE_RIGHT
        elif ExecutePlan.MoveLeft(node,x,y):
            return AgentConsts.MOVE_LEFT
        else:
            return AgentConsts.NO_MOVE

