import time
import os
import random
from abc import ABC, abstractmethod

class GameCharacter(ABC):
    def __init__(self, className, health, mana, level = 1):
        self.className = className
        self.max_health = health
        self.max_mana = mana 
        self.health = health 
        self.mana = mana
        self.level = level
        self.is_defending = False

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
        super().__init__(className = "Warrior", health = 150, mana = 30, level = level)

class Mage(GameCharacter):
    def __init__(self, level=1):
        super().__init__(className = "Mage", health = 80, mana = 120, level = level)

    def attack(self):
        return f"Mage (Lvl {self.level}) hurls a Shadow Bomb!", 10 * self.level 
    
    def defend(self):
        self.is_defending = True   
        return f"You have cast a Dark Veil Shield."
    
    def cast_spell(self):
        if self.mana >= 30:
            self.mana -= 30
            return f"Mage unleashes a Gloom Burst", 40 * self.level 
        else: 
            return f"Not enough mana.", 0
        
class Archer(GameCharacter):
    def __init__(self, level=1):
        super().__init__(className = "Archer", health = 100, mana = 60, level = level)

    def attack(self):
        if self.max_mana != self.mana:
            self.mana += 5
        return f"Archer (Lvl {self.level}) fires a volley of arrows!", 15 * self.level

    def defend(self):
        self.is_defending = True
        if self.max_mana != self.mana:
            self.mana += 5
        return f"Archer dashes out to evade the attack"

    def cast_spell(self):
        if self.mana >= 15:
            self.mana -= 15
            return f"Archer fires a Charge Arrow!", 30 * self.level
        else:
            return f"Not enough mana.", 0

class Assassin(GameCharacter):
    def __init__(self, level=1):
        super().__init__(className = "Assassin", health = 90, mana = 60, level = level)

    def attack(self):
        if self.max_mana != self.mana:
            self.mana += 10
        return f"Assassin (Lvl {self.level}) slashed with a dagger", 20 * self.level

    def defend(self):
        self.is_defending = True
        if self.max_mana != self.mana:
            self.mana += 10
        return f"Assassin used Invisibility to dodge the enemy attack"
    
    def cast_spell(self):
        if self.mana >= 20:
            self.mana -= 20
            return f"Assassin enchants weapon with poison!", 35 * self.level
        else:
            return f"Not enough mana", 0
    
class Enemy:
    def __init__(self, name, health, level = 1):
        self.name = name
        self.max_health = health 
        self.health = health
        self._attack = int(health * 0.15)
        self.level = level

    def attack(self, player):
        if player.is_defending:
            player.is_defending = False
            return f"{self.name} attacks, but it miss!", 0
        else:
            return f"{self.name} attacks viciously!", self._attack
        
    def take_damage(self, amount):
        self.health -= amount
        return f"{self.name} takes {amount} damage! Remaining health: {max(self.health, 0)}"

enemy_data = [
    ("Goblin", 50),
    ("Orc Brute", 90),
    ("Shadow Wraith", 75),
    ("Fire Imp", 60),
    ("Frost Troll", 120),
    ("Dark Acolyte", 70),
    ("Bone Knight", 100),
    ("Venom Serpent", 65),
    ("Blood Revenant", 110),
    ("Void Walker", 85),
    ("Stone Golem", 150),
    ("Necromancer", 80),
    ("Swamp Beast", 130),
    ("Thunder Hawk", 70),
    ("Crimson Bandit", 60),
    ("Abyssal Hound", 95),
    ("Skeletal Archer", 55),
    ("Blight Mage", 75),
    ("Doom Bringer", 140),
    ("Plague Rat", 45),
    ("Harpy Matron", 85),
    ("Spectral Assassin", 100),
    ("Molten Drake", 160),
    ("Crypt Horror", 120),
    ("Wind Djinn", 90)
]

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":

    print("[1] Warrior")
    print("[2] Mage")
    print("[3] Archer")
    print("[4] Assassin")

    classChoice = input("Select a Class: ")

    time.sleep(2)
    clear()

    if classChoice == "1":
        player = Warrior()
    elif classChoice == "2":
        player = Mage()
    elif classChoice == "3":
        player = Archer()
    elif classChoice == "4":
        player = Assassin()
    else:
        print("Invalid Choice")
        exit()

    enemy_name, enemy_health = random.choice(enemy_data)
    enemy = Enemy(enemy_name, health=enemy_health)

    while True:
        print("\n--- BATTLE START ---")
        print(f"Enemy: {enemy.name} | HP: {enemy.health} | Lvl: {enemy.level}")
        print(f"Player: {player.className} | HP: {player.health} | Mana: {player.mana} | Lvl: {player.level}")

        # Player turn
        print("[1] Attack")
        print("[2] Defend")
        print("[3] Cast Spell")
        action = input("Choose action: ")
        if action == "1":
            desc, damage = player.attack()
        elif action == "2":
            desc = player.defend()
            damage = 0
        elif action == "3":
            desc, damage = player.cast_spell()
        else:
            print("Invalid action, turn skipped.")
            continue

        clear()

        print("\n--- BATTLE LOG ---")
        print(desc)
        
        if damage > 0:
            print(enemy.take_damage(damage))

        if enemy.health <= 0:
            print(f"{enemy.name} defeated!")

            #Level up player
            player.level += 1
            print(f"Level Up! New Level: {player.level}")

            #Restore player
            player.health = player.max_health
            player.mana = player.max_mana

            #Scale player
            player.health += (player.level - 1) * 50
            player.mana += (player.level - 1) * 25

            # Respawn a stronger enemy
            new_name, base_health = random.choice(enemy_data)
            scaled_health = int(base_health * 1.5) + (player.level * 5)
            enemy = Enemy(new_name, health=scaled_health, level=player.level)
            print(f"\nA new {enemy.name} appears with {enemy.health} HP and Level {enemy.level}!")

            time.sleep(5)
            clear()
            continue

        # Enemy turn
        desc, damage = enemy.attack(player)
        print(desc)
        player.health -= damage
        print(f"You take {damage} damage. Your remaining health: {max(player.health, 0)}")

        if player.health <= 0:
            print("You have been defeated. Game Over!")
            break
            
        time.sleep(5)
        clear()