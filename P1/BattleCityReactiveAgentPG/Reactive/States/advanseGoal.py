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
        self.agentX = perception[AgentConsts.AGENT_X]
        self.agentY = perception[AgentConsts.AGENT_Y]

        if(perception[AgentConsts.COMMAND_CENTER_X]<=0):
            print("base destruidaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaAAAAAAAAAAAAAAAaaaaa")  
            self.base_x = perception[AgentConsts.EXIT_X]
            self.base_y = perception[AgentConsts.EXIT_Y]  

        else:
            self.base_x = perception[AgentConsts.COMMAND_CENTER_X]
            self.base_y = perception[AgentConsts.COMMAND_CENTER_Y]
        return self.base_x, self.base_y, self.agentX, self.agentY

    def perceptionToAction(self, perception):
        UP = perception[AgentConsts.NEIGHBORHOOD_UP]
        DOWN = perception[AgentConsts.NEIGHBORHOOD_DOWN]
        RIGHT = perception[AgentConsts.NEIGHBORHOOD_RIGHT]
        LEFT = perception[AgentConsts.NEIGHBORHOOD_LEFT]
        
        return UP, DOWN, RIGHT, LEFT

    def Update(self, perception, map, agent):
        print("AdvanseGoal Update")
        objX, objY, agentX, agentY = self.actualizarCoordenadas(perception)
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
        if agentX < objX - 1.3:
            action = AgentConsts.MOVE_RIGHT
        elif agentX > 1.3 + objX:
            action = AgentConsts.MOVE_LEFT
        elif agentY < objY:
            action = AgentConsts.MOVE_UP
        elif agentY >  objY:
            action = AgentConsts.MOVE_DOWN

        # ==========================================================
        # FASE 3: Comprobar Atascos y planear nueva Evasión
        # ==========================================================
        estoy_atascado = (agentX == self.last_x) and (agentY == self.last_y)

        if estoy_atascado and  (agentY >  objY) and self.last_action != AgentConsts.NO_MOVE:
            print("¡Atascado con muro irrompible! Iniciando maniobra de 4 turnos...")
            
            if self.last_action == AgentConsts.MOVE_DOWN and DOWN == AgentConsts.UNBREAKABLE:
                self.evasion_sequence = [AgentConsts.MOVE_RIGHT, AgentConsts.MOVE_DOWN, AgentConsts.MOVE_DOWN] 
                

            elif self.last_action == AgentConsts.MOVE_RIGHT and RIGHT == AgentConsts.UNBREAKABLE:
                action = AgentConsts.MOVE_LEFT 
                self.evasion_sequence = [AgentConsts.MOVE_LEFT, AgentConsts.MOVE_DOWN, AgentConsts.MOVE_DOWN] 
                

            elif self.last_action == AgentConsts.MOVE_LEFT and LEFT == AgentConsts.UNBREAKABLE:
                action = AgentConsts.MOVE_RIGHT 
                self.evasion_sequence = [AgentConsts.MOVE_RIGHT, AgentConsts.MOVE_DOWN, AgentConsts.MOVE_DOWN] 

        elif estoy_atascado and (agentY < objY) and self.last_action != AgentConsts.NO_MOVE:

            if self.last_action == AgentConsts.MOVE_UP and UP == AgentConsts.UNBREAKABLE and RIGHT== AgentConsts.UNBREAKABLE:
                action = AgentConsts.MOVE_LEFT 
                self.evasion_sequence = [AgentConsts.MOVE_LEFT, AgentConsts.MOVE_LEFT, AgentConsts.MOVE_UP]   

            elif self.last_action == AgentConsts.MOVE_UP and UP == AgentConsts.UNBREAKABLE and LEFT== AgentConsts.UNBREAKABLE:
                action = AgentConsts.MOVE_RIGHT 
                self.evasion_sequence = [AgentConsts.MOVE_RIGHT, AgentConsts.MOVE_RIGHT, AgentConsts.MOVE_UP]

            elif self.last_action == AgentConsts.MOVE_RIGHT and RIGHT == AgentConsts.UNBREAKABLE:
                action = AgentConsts.MOVE_LEFT 
                self.evasion_sequence = [AgentConsts.MOVE_LEFT, AgentConsts.MOVE_UP, AgentConsts.MOVE_UP] 
                
            elif self.last_action == AgentConsts.MOVE_LEFT and LEFT == AgentConsts.UNBREAKABLE:
                action = AgentConsts.MOVE_RIGHT 
                self.evasion_sequence = [AgentConsts.MOVE_RIGHT, AgentConsts.MOVE_UP, AgentConsts.MOVE_UP] 

          
         
        self.last_x = agentX
        self.last_y = agentY
        self.last_action = action
        agent.ultimo=action
        return action, True

    def Transit(self, perception, map):
        UP = perception[AgentConsts.NEIGHBORHOOD_UP]
        DOWN = perception[AgentConsts.NEIGHBORHOOD_DOWN]
        RIGHT = perception[AgentConsts.NEIGHBORHOOD_RIGHT]
        LEFT = perception[AgentConsts.NEIGHBORHOOD_LEFT]
        
        print(f"[AdvanseGoal Transit] UP={UP}, DOWN={DOWN}, RIGHT={RIGHT}, LEFT={LEFT}")
        print(f"[AdvanseGoal Transit] BASE constant = {AgentConsts.COMMAND_CENTER}")
    
        # Si la base está como vecino en alguna dirección, cambiar a ShootBase
        if UP == AgentConsts.COMMAND_CENTER or DOWN == AgentConsts.COMMAND_CENTER or RIGHT == AgentConsts.COMMAND_CENTER or LEFT == AgentConsts.COMMAND_CENTER or UP == AgentConsts.PLAYER or DOWN == AgentConsts.PLAYER or RIGHT == AgentConsts.PLAYER or LEFT == AgentConsts.PLAYER:
            print("[AdvanseGoal Transit] ¡OBJETIVO DETECTADO! Cambiando a ShootBase")
            return "Rotate"
        
        print("[AdvanseGoal Transit] Objetivo no detectado, permaneciendo en AdvanseGoal")
        return self.id
    
    def Reset(self):
        self.last_x = -1
        self.last_y = -1
        self.last_action = AgentConsts.NO_MOVE
        self.evasion_sequence = [] 
        self.updateTime = 0