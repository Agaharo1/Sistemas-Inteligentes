import random
from States.AgentConsts import AgentConsts

class GoalMonitor:

    GOAL_COMMAND_CENTRER = 0
    GOAL_LIFE = 1
    GOAL_PLAYER = 2
    GOAL_EXIT = 3
    def __init__(self, problem, goals, finalGoal):
        self.goals = goals
        self.finalGoal = finalGoal
        self.problem = problem
        self.lastTime = -1
        self.recalculate = False

    def ForceToRecalculate(self):
        self.recalculate = True

    def NeedReplaning(self, perception, map, agent):
        if self.recalculate:
            self.recalculate = False
            self.lastTime = perception[AgentConsts.TIME]
            return True
        #TODO definir la estrategia de cuando queremos recalcular
        #puede ser , por ejemplo cada cierto tiempo o cuanod tenemos poca vida.
        # Replanificar cada 50 unidades de tiempo
        if perception[AgentConsts.TIME] - self.lastTime > 50:
            self.lastTime = perception[AgentConsts.TIME]
            return True
        # Replanificar si tenemos poca vida (menos de 50% de la salud)
        if perception[AgentConsts.HEALTH] < 50:
            self.lastTime = perception[AgentConsts.TIME]
            return True
        return False
    
    #selecciona la meta mas adecuada al estado actual
    def SelectGoal(self, perception, map, agent):
        #TODO Mejorar esta modo chapuza
        # Estrategia: Priorizar por salud
        # Si tenemos poca salud, buscar la vida
        if(perception[AgentConsts.COMMAND_CENTER_X]<=0):
            print("Seleccionando meta: EXIT")
            return self.goals[self.GOAL_EXIT]
          
        # Si tenemos salud media/alta, atacar al jugador
        elif perception[AgentConsts.HEALTH] == 2:
            print("Seleccionando meta: PLAYER")
            return self.goals[self.GOAL_PLAYER]
        # En otro caso, buscar el command center (primera meta válida)
        else:
            print("Seleccionando meta: COMMAND CENTER")
            for goal in self.goals:
                if goal is not None:
                    return goal

    
    def UpdateGoals(self,goal, goalId):
        self.goals[goalId] = goal
