import time
import os
import random
from abc import ABC, abstractmethod

class GameCharacter(ABC):
    def __init__(self, health, mana, level = 1):
        self.max_health = health
        self.max_mana = mana 
        self.health = health
        self.mana = mana
        self.level = level

    @abstractmethod
    def show_status(self):
        pass 

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
    def __init__(self, level = 1):
        super().__init__(health = 150, mana = 30, level = level)

class Mage(GameCharacter):
    def __init__(self, level=1):
        super().__init__(health = 80, mana = 120, level = level)

class Archer(GameCharacter):
    def __init__(self, level=1):
        super().__init__(health = 100, mana = 60, level = level)
        self.is_defending = False

    def show_status(self):
        print(f"{type(current).__name__}: | HP: {self.health}/{self.max_health} | Mana: {self.mana}/{self.max_mana} | Lvl: {self.level}")

    def defend(self):
        self.is_defending = True
        print("\nYou are ready to block the enemy's attack.\n")

    def cast_spell(self):
        if self.mana >= 10:
            self.mana -= 10
            current_enemy.health -= 10 * self.level
            print(f"\nCharged Arrow! >>----> | {current_enemy.name} loses {10 * self.level} health!\n")
        else:
            print("\nNot enough mana!\n")

    def attack(self):
        current_enemy.health -= 5 * self.level
        print(f"\nAttack with bow! | {current_enemy.name} loses {5 * self.level} health!\n")

class Assassin(GameCharacter):
    def __init__(self, level=1):
        super().__init__(health = 90, mana = 70, level = level)

class Enemy:
    def __init__(self, name, health, mana, level):
        self.name = name
        self.max_health = health 
        self.max_mana = mana
        self.health = health
        self.mana = mana
        self.level = level

    def show_status(self):
        print(f"{self.name}: | HP: {self.health}/{self.max_health} | Mana: {self.mana}/{self.max_mana} | Lvl: {self.level}")

    def move(self, player):
        action = random.randrange(1, 5)
        if action < 4:
            if player.is_defending:
                print(f"{self.name} attacks, but you PARRIED the attack!\n")
                player.is_defending = False
            else:
                player.health -= 5 * self.level
                print(f"{self.name} attack! | You lose {5 * self.level} health!\n")
        elif action == 4:
            if self.mana >= 10:
                self.mana -= 10
                player.health -= 10 * self.level
                print(f"{self.name} attacks heavily! | You lose {10 * self.level} health!\n")
            else:
                print(f"The {self.name} doesn't seem to have mana!\n")    
        
enemy = Enemy("Goblin", 50, 20, 1)
current_enemy = enemy


player = Archer()
current = player

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":

    while True:
        current.show_status()
        current_enemy.show_status()
        choice = input("Choose Action: [1] Attack [2] Defend [3] Cast Spell [4] Exit: ")
    
        if choice == "1":
            current.attack()
        elif choice == "2":
            current.defend()
        elif choice == "3":
            current.cast_spell()
        elif choice == "4":
            break
        else:
            print("Invalid choice, please try again.")

        current_enemy.move(current)
        if current.health <= 0:
            print("You have been defeated!\n")
            current.health = current.max_health 
            current.mana = current.max_mana
            print("\n<<<You have been revived!>>>\n")
            
        elif current_enemy.health <= 0:
            current.level += 1
            current.max_health += current.max_health * 0.5
            current.max_mana += current.max_mana * 0.5
            current.health = current.max_health 
            current.mana = current.max_mana 
            print(f"You have defeated the {current_enemy.name}!\n")
            enemy = random.choice([Enemy("Goblin", 50, 20, current.level), Enemy("Orc", 70, 30, current.level), Enemy("Troll", 90, 40, current.level)])
            current_enemy = enemy
            

        time.sleep(3)
        clear()