from abc import ABC, abstractmethod

class GameCharacter(ABC):
    def __init__(self, health, mana, level):
        self.health = 100
        self.mana = 50
        self.level = 1

    @abstractmethod
    def skill(self):
        pass

    @abstractmethod
    def attack(self):
        pass





        
