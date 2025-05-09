from abc import ABC, abstractmethod

class GameCharacter(ABC):
    def __init__(self, health, mana, level = 1):
        self.health = health
        self.mana = mana
        self.level = level

    @abstractmethod
    def attack(self):
        pass

    @abstractmethod
    def defend(self):
        pass

    @abstractmethod
    def cast_spell(self):
        pass
    
class Enemy():
    pass

class Warrior(GameCharacter):
    def __init__(self, level = 1):
        super().__init__(health = 150, mana = 30, level = level)

class Mage(GameCharacter):
    def __init__(self, level=1):
        super().__init__(health = 80, mana = 120, level = level)

class Archer(GameCharacter):
    def __init__(self, level=1):
        super().__init__(health = 100, mana = 60, level = level)

class Assassin(GameCharacter):
    def __init__(self, level=1):
        super().__init__(health = 90, mana = 70, level = level)




        
