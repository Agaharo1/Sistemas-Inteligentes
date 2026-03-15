from StateMachine.State import State
from States.AgentConsts import AgentConsts

class Rotate(State):

    def __init__(self, id):
        super().__init__(id)
        self.last_direction = AgentConsts.NO_MOVE
        self.rotation_sequence = [] 
        self.maneuver_failed=False

    def Update(self, perception, map, agent):

        # ==========================================================
        # FASE 1: Ejecutar secuencia pendiente (Estructura idéntica a AdvanseGoal)
        # ==========================================================
        if len(self.rotation_sequence) > 0:
            action = self.rotation_sequence.pop(0)
            self.last_direction = action
            agent.ultimo=action
            return action, True

        agentX = perception[AgentConsts.AGENT_X]
        agentY = perception[AgentConsts.AGENT_Y]
        playerX = perception[AgentConsts.PLAYER_X]
        playerY = perception[AgentConsts.PLAYER_Y]
        UP =perception[AgentConsts.NEIGHBORHOOD_UP]
        DOWN =perception[AgentConsts.NEIGHBORHOOD_DOWN]
        LEFT=perception[AgentConsts.NEIGHBORHOOD_LEFT]
        RIGHT=perception[AgentConsts.NEIGHBORHOOD_RIGHT]

        if self.last_direction == AgentConsts.NO_MOVE:
            self.last_direction = getattr(agent, "ultimo", AgentConsts.NO_MOVE)

        target_direction = self.calculateTargetDirection(UP,DOWN,RIGHT,LEFT)
        action = AgentConsts.NO_MOVE

        # ==========================================================
        # FASE 2: Decidir si iniciar maniobra (Equivalente a detectar atasco)
        # ==========================================================
        
        necesita_gilro = (target_direction != AgentConsts.NO_MOVE) and (self.last_direction != target_direction)

        if necesita_gilro:
            opposite = self.getOppositeDirection(target_direction)
            
            if self.isDirectionFree(perception, opposite):
                action = opposite
                self.rotation_sequence = [target_direction]
                
                self.last_direction = action
                agent.ultimo=action
                return action, True
            else:
                self.maneuver_failed = True
                return AgentConsts.NO_MOVE, True

        if self.last_direction == target_direction and target_direction != AgentConsts.NO_MOVE:
            return AgentConsts.NO_MOVE, True

        return action, True

    def Transit(self, perception, map):
        if self.maneuver_failed:
            return "AdvanseGoal"

        UP = perception[AgentConsts.NEIGHBORHOOD_UP]
        DOWN = perception[AgentConsts.NEIGHBORHOOD_DOWN]
        RIGHT = perception[AgentConsts.NEIGHBORHOOD_RIGHT]
        LEFT = perception[AgentConsts.NEIGHBORHOOD_LEFT]

        enemy_in_front = (
            (self.last_direction == AgentConsts.MOVE_UP and (UP == AgentConsts.PLAYER )) or
            (self.last_direction == AgentConsts.MOVE_DOWN and (DOWN == AgentConsts.PLAYER)) or
            (self.last_direction == AgentConsts.MOVE_RIGHT and (RIGHT == AgentConsts.PLAYER )) or
            (self.last_direction == AgentConsts.MOVE_LEFT and (LEFT == AgentConsts.PLAYER))
        )

        if enemy_in_front:
            return "Shoot"

        enemy_detected = (UP == AgentConsts.PLAYER or DOWN == AgentConsts.PLAYER or 
                        RIGHT == AgentConsts.PLAYER or LEFT == AgentConsts.PLAYER )
        
        if not enemy_detected and len(self.rotation_sequence) == 0:
            return "AdvanseGoal"
        return self.id

    def Reset(self):
        self.last_direction = AgentConsts.NO_MOVE
        self.rotation_sequence = []
        self.maneuver_failed = False


    def calculateTargetDirection(self,UP,DOWN,RIGHT,LEFT):
        if UP==AgentConsts.PLAYER :
            return AgentConsts.MOVE_UP
        elif DOWN==AgentConsts.PLAYER :
            return AgentConsts.MOVE_DOWN
        elif RIGHT==AgentConsts.PLAYER :
            return AgentConsts.MOVE_RIGHT
        elif LEFT==AgentConsts.PLAYER :
            return AgentConsts.MOVE_LEFT
        return AgentConsts.NO_MOVE

    def getOppositeDirection(self, direction):
        if direction == AgentConsts.MOVE_UP: return AgentConsts.MOVE_DOWN
        if direction == AgentConsts.MOVE_DOWN: return AgentConsts.MOVE_UP
        if direction == AgentConsts.MOVE_RIGHT: return AgentConsts.MOVE_LEFT
        if direction == AgentConsts.MOVE_LEFT: return AgentConsts.MOVE_RIGHT
        return AgentConsts.NO_MOVE

    def isDirectionFree(self, perception, direction):
        if direction == AgentConsts.MOVE_UP: return perception[AgentConsts.NEIGHBORHOOD_UP] == AgentConsts.NOTHING
        if direction == AgentConsts.MOVE_DOWN: return perception[AgentConsts.NEIGHBORHOOD_DOWN] == AgentConsts.NOTHING
        if direction == AgentConsts.MOVE_RIGHT: return perception[AgentConsts.NEIGHBORHOOD_RIGHT] == AgentConsts.NOTHING
        if direction == AgentConsts.MOVE_LEFT: return perception[AgentConsts.NEIGHBORHOOD_LEFT] == AgentConsts.NOTHING
        return False