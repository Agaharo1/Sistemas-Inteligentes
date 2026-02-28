from StateMachine.State import State
from States.AgentConsts import AgentConsts
import random

class AdvanseGoal(State):

    def __init__(self, id):
        super().__init__(id)
        self.last_x = -1
        self.last_y = -1
        self.last_action = AgentConsts.NO_MOVE
        
       
        self.evasion_sequence = []

    def actualizarCoordenadas(self, perception):
        self.base_x = perception[AgentConsts.COMMAND_CENTER_X]
        self.base_y = perception[AgentConsts.COMMAND_CENTER_Y]
        self.agentX = perception[AgentConsts.AGENT_X]
        self.agentY = perception[AgentConsts.AGENT_Y]
        
        return self.base_x, self.base_y, self.agentX, self.agentY

    def perceptionToAction(self, perception):
        UP = perception[AgentConsts.NEIGHBORHOOD_UP]
        DOWN = perception[AgentConsts.NEIGHBORHOOD_DOWN]
        RIGHT = perception[AgentConsts.NEIGHBORHOOD_RIGHT]
        LEFT = perception[AgentConsts.NEIGHBORHOOD_LEFT]
        
        return UP, DOWN, RIGHT, LEFT

    def Update(self, perception, map, agent):
        baseX, baseY, agentX, agentY = self.actualizarCoordenadas(perception)
        UP, DOWN, RIGHT, LEFT = self.perceptionToAction(perception)
        
        # ==========================================================
        # FASE 1: ¿Estamos en medio de una maniobra de evasión de 4 turnos?
        # ==========================================================
        if len(self.evasion_sequence) > 0:
            action = self.evasion_sequence.pop(0) 
            self.last_x = agentX
            self.last_y = agentY
            self.last_action = action
            return action, True

        # ==========================================================
        # FASE 2: Lógica Normal (Movimiento Ideal)
        # ==========================================================
        action = AgentConsts.NO_MOVE
        if agentX < baseX - 0.5:
            action = AgentConsts.MOVE_RIGHT
        elif agentX > 0.5 + baseX:
            action = AgentConsts.MOVE_LEFT
        elif agentY < baseY:
            action = AgentConsts.MOVE_UP
        elif agentY > baseY:
            action = AgentConsts.MOVE_DOWN

        # ==========================================================
        # FASE 3: Comprobar Atascos y planear nueva Evasión
        # ==========================================================
        estoy_atascado = (agentX == self.last_x) and (agentY == self.last_y)

        if estoy_atascado and self.last_action != AgentConsts.NO_MOVE:
            print("¡Atascado con muro irrompible! Iniciando maniobra de 4 turnos...")
            
            if self.last_action == AgentConsts.MOVE_DOWN and DOWN == AgentConsts.UNBREAKABLE:
                self.evasion_sequence = [AgentConsts.MOVE_RIGHT, AgentConsts.MOVE_DOWN, AgentConsts.MOVE_DOWN] 
                

            elif self.last_action == AgentConsts.MOVE_RIGHT and RIGHT == AgentConsts.UNBREAKABLE:
                action = AgentConsts.MOVE_LEFT 
                self.evasion_sequence = [AgentConsts.MOVE_LEFT, AgentConsts.MOVE_DOWN, AgentConsts.MOVE_DOWN] 
                

            elif self.last_action == AgentConsts.MOVE_LEFT and LEFT == AgentConsts.UNBREAKABLE:
                action = AgentConsts.MOVE_RIGHT 
                self.evasion_sequence = [AgentConsts.MOVE_RIGHT, AgentConsts.MOVE_DOWN, AgentConsts.MOVE_DOWN] 
                

            else:
                if self.last_action == AgentConsts.MOVE_UP or self.last_action == AgentConsts.MOVE_DOWN:
                    action = AgentConsts.MOVE_UP
                elif self.last_action == AgentConsts.MOVE_RIGHT:
                    action = AgentConsts.MOVE_DOWN
                elif self.last_action == AgentConsts.MOVE_LEFT:
                    action = AgentConsts.MOVE_DOWN

    
        self.last_x = agentX
        self.last_y = agentY
        self.last_action = action

        return action, True
    
    def Transit(self, perception, map):
        return self.id
    
    def Reset(self):
        self.last_x = -1
        self.last_y = -1
        self.last_action = AgentConsts.NO_MOVE
        self.evasion_sequence = [] 
        self.updateTime = 0