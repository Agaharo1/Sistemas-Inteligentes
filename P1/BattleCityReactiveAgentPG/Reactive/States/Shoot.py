from StateMachine.State import State
from States.AgentConsts import AgentConsts

class Shoot(State):

    def __init__(self, id):
        super().__init__(id)
        self.last_direction = AgentConsts.NO_MOVE

    def Update(self, perception, map, agent):
        return AgentConsts.NO_MOVE, True

    def Transit(self, perception, map):
        UP = perception[AgentConsts.NEIGHBORHOOD_UP]
        DOWN = perception[AgentConsts.NEIGHBORHOOD_DOWN]
        RIGHT = perception[AgentConsts.NEIGHBORHOOD_RIGHT]
        LEFT = perception[AgentConsts.NEIGHBORHOOD_LEFT]

        enemy_perceived = (
            UP == AgentConsts.PLAYER or UP == AgentConsts.COMMAND_CENTER or
            DOWN == AgentConsts.PLAYER or DOWN == AgentConsts.COMMAND_CENTER or
            RIGHT == AgentConsts.PLAYER or RIGHT == AgentConsts.COMMAND_CENTER or
            LEFT == AgentConsts.PLAYER or LEFT == AgentConsts.COMMAND_CENTER
        )

        # Si ya no percibe enemigo, volver a avanzar
        if not enemy_perceived:
            return "AdvanseGoal"

        enemy_in_front = (
            (self.last_direction == AgentConsts.MOVE_UP and UP == AgentConsts.PLAYER) or
            (self.last_direction == AgentConsts.MOVE_DOWN and DOWN == AgentConsts.PLAYER) or
            (self.last_direction == AgentConsts.MOVE_RIGHT and RIGHT == AgentConsts.PLAYER) or
            (self.last_direction == AgentConsts.MOVE_LEFT and LEFT == AgentConsts.PLAYER) or
            (self.last_direction == AgentConsts.MOVE_UP and UP == AgentConsts.COMMAND_CENTER) or
            (self.last_direction == AgentConsts.MOVE_DOWN and DOWN == AgentConsts.COMMAND_CENTER) or
            (self.last_direction == AgentConsts.MOVE_RIGHT and RIGHT == AgentConsts.COMMAND_CENTER) or
            (self.last_direction == AgentConsts.MOVE_LEFT and LEFT == AgentConsts.COMMAND_CENTER)
        )

        # Si lo pierde de frente, volver a Rotate
        if not enemy_in_front:
            return "Rotate"

        return self.id

    def Reset(self):
        self.last_direction = AgentConsts.NO_MOVE