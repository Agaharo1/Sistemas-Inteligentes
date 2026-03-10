from StateMachine.State import State
from States.AgentConsts import AgentConsts

class Rotate(State):

    def __init__(self, id):
        super().__init__(id)
        self.last_direction = AgentConsts.NO_MOVE
        self.rotation_sequence = []

    def Update(self, perception, map, agent):

        UP = perception[AgentConsts.NEIGHBORHOOD_UP]
        DOWN = perception[AgentConsts.NEIGHBORHOOD_DOWN]
        RIGHT = perception[AgentConsts.NEIGHBORHOOD_RIGHT]
        LEFT = perception[AgentConsts.NEIGHBORHOOD_LEFT]
        
        baseX = perception[AgentConsts.COMMAND_CENTER_X]
        baseY = perception[AgentConsts.COMMAND_CENTER_Y]
        agentX = perception[AgentConsts.AGENT_X]
        agentY = perception[AgentConsts.AGENT_Y]
        playerX = perception[AgentConsts.PLAYER_X]
        playerY = perception[AgentConsts.PLAYER_Y]
        
        # FASE 1: Ejecutar rotación pendiente
        if len(self.rotation_sequence) > 0:
            action = self.rotation_sequence.pop(0)
            self.last_direction = action
            return action, True
        
        # FASE 2: ¿Ya estoy apuntando a un objetivo?
        if self.last_direction == AgentConsts.MOVE_UP:
            if UP == AgentConsts.COMMAND_CENTER or UP == AgentConsts.PLAYER:
                return AgentConsts.NO_MOVE, True
                
        elif self.last_direction == AgentConsts.MOVE_DOWN:
            if DOWN == AgentConsts.COMMAND_CENTER or DOWN == AgentConsts.PLAYER:
                return AgentConsts.NO_MOVE, True
                
        elif self.last_direction == AgentConsts.MOVE_RIGHT:
            if RIGHT == AgentConsts.COMMAND_CENTER or RIGHT == AgentConsts.PLAYER:
                return AgentConsts.NO_MOVE, True
                
        elif self.last_direction == AgentConsts.MOVE_LEFT:
            if LEFT == AgentConsts.COMMAND_CENTER or LEFT == AgentConsts.PLAYER:
                return AgentConsts.NO_MOVE, True
        
        # FASE 3: Decidir objetivo prioritario (PLAYER > BASE)
        player_detected = (UP == AgentConsts.PLAYER or DOWN == AgentConsts.PLAYER or 
                          RIGHT == AgentConsts.PLAYER or LEFT == AgentConsts.PLAYER)
        
        if player_detected:
            target_direction = self.calculateTargetDirection(playerX, playerY, agentX, agentY)
        else:
            target_direction = self.calculateTargetDirection(baseX, baseY, agentX, agentY)
        
        # FASE 4: Planificar rotación única
        if target_direction != self.last_direction and target_direction != AgentConsts.NO_MOVE:
            self.rotation_sequence = self.planRotation(self.last_direction, target_direction)
            if len(self.rotation_sequence) > 0:
                action = self.rotation_sequence.pop(0)
                self.last_direction = action
                return action, True
        
        return AgentConsts.NO_MOVE, True

    def calculateTargetDirection(self, targetX, targetY, agentX, agentY):
        """Calcula hacia qué dirección está el objetivo"""
        if agentX == targetX and agentY < targetY:
            return AgentConsts.MOVE_UP
        elif agentX == targetX and agentY > targetY:
            return AgentConsts.MOVE_DOWN
        elif agentY == targetY and agentX < targetX:
            return AgentConsts.MOVE_RIGHT
        elif agentY == targetY and agentX > targetX:
            return AgentConsts.MOVE_LEFT
        return AgentConsts.NO_MOVE

    def planRotation(self, current_direction, target_direction):
        """Planifica la secuencia de movimientos para girar hacia target"""
        rotations = {
            (AgentConsts.MOVE_UP, AgentConsts.MOVE_DOWN): [AgentConsts.MOVE_LEFT, AgentConsts.MOVE_DOWN],
            (AgentConsts.MOVE_UP, AgentConsts.MOVE_LEFT): [AgentConsts.MOVE_LEFT],
            (AgentConsts.MOVE_UP, AgentConsts.MOVE_RIGHT): [AgentConsts.MOVE_RIGHT],
            
            (AgentConsts.MOVE_DOWN, AgentConsts.MOVE_UP): [AgentConsts.MOVE_LEFT, AgentConsts.MOVE_UP],
            (AgentConsts.MOVE_DOWN, AgentConsts.MOVE_LEFT): [AgentConsts.MOVE_LEFT],
            (AgentConsts.MOVE_DOWN, AgentConsts.MOVE_RIGHT): [AgentConsts.MOVE_RIGHT],
            
            (AgentConsts.MOVE_LEFT, AgentConsts.MOVE_RIGHT): [AgentConsts.MOVE_UP, AgentConsts.MOVE_RIGHT],
            (AgentConsts.MOVE_LEFT, AgentConsts.MOVE_UP): [AgentConsts.MOVE_UP],
            (AgentConsts.MOVE_LEFT, AgentConsts.MOVE_DOWN): [AgentConsts.MOVE_DOWN],
            
            (AgentConsts.MOVE_RIGHT, AgentConsts.MOVE_LEFT): [AgentConsts.MOVE_UP, AgentConsts.MOVE_LEFT],
            (AgentConsts.MOVE_RIGHT, AgentConsts.MOVE_UP): [AgentConsts.MOVE_UP],
            (AgentConsts.MOVE_RIGHT, AgentConsts.MOVE_DOWN): [AgentConsts.MOVE_DOWN],
        }
        
        return rotations.get((current_direction, target_direction), [])

    def Transit(self, perception, map):
        UP = perception[AgentConsts.NEIGHBORHOOD_UP]
        DOWN = perception[AgentConsts.NEIGHBORHOOD_DOWN]
        RIGHT = perception[AgentConsts.NEIGHBORHOOD_RIGHT]
        LEFT = perception[AgentConsts.NEIGHBORHOOD_LEFT]

        enemy_perceived = (
            UP == AgentConsts.PLAYER or
            DOWN == AgentConsts.PLAYER or
            RIGHT == AgentConsts.PLAYER or
            LEFT == AgentConsts.PLAYER
        )

        # Si ya no percibe enemigo, volver a avanzar
        if not enemy_perceived:
            return "AdvanseGoal"

        enemy_in_front = (
            (self.last_direction == AgentConsts.MOVE_UP and UP == AgentConsts.PLAYER) or
            (self.last_direction == AgentConsts.MOVE_DOWN and DOWN == AgentConsts.PLAYER) or
            (self.last_direction == AgentConsts.MOVE_RIGHT and RIGHT == AgentConsts.PLAYER) or
            (self.last_direction == AgentConsts.MOVE_LEFT and LEFT == AgentConsts.PLAYER)
        )

        # Si lo está apuntando -> Shoot, si no -> Rotate
        if enemy_in_front:
            return "Shoot"

        return self.id

    def Reset(self):
        self.last_direction = AgentConsts.NO_MOVE
        self.rotation_sequence = []