from abc import ABC, abstractmethod

class GameCharacter(ABC):
    def __init__(self, health, mana, level):
        self.health = 100
        self.mana = 50
        self.level = 1

    @abstractmethod
    def attack(self):
        pass

    @abstractmethod
    def defend(self):
        pass

    @abstractmethod
    def cast_spell(self):
        pass

class Warrior(GameCharacter):
    pass
class Mage(GameCharacter):
    pass
class Archer(GameCharacter):
    pass
class Assassin(GameCharacter):
    pass
    #test branch assassin





        
