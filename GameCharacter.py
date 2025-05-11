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
    
    def critHit(self):
        pass

class Warrior(GameCharacter):
    def __init__(self, level = 1):
        self.base_health = 180
        self.base_mana = 40
        self.health_growth = 40
        self.mana_growth = 10
        super().__init__("Warrior", self.base_health, self.base_mana, level)

    def critHit(self):
        return 1.5 if random.randint(1, 10) == 1 else 1.0

    def attack(self):
        baseDamage = 10 + (5 * self.level)
        damage = baseDamage * self.critHit()

        if self.max_mana != self.mana:
            self.mana += 5
        return f"Warrior (Lvl {self.level}) slashes with a sword!",  damage
    
    def defend(self):
        self.is_defending = True
        if self.max_mana != self.mana:
            self.mana += 5
        return f"Warrior raises shield to block the next attack."

    def cast_spell(self):
        baseDamage = 25 + (10 * self.level)
        damage = baseDamage * self.critHit()

        if self.mana >= 10:
            self.mana -= 10
            return f"Warrior uses War Cry to boost strength!", damage
        else:
            return f"Not enough mana.", 0

class Mage(GameCharacter):
    def __init__(self, level=1):
        self.base_health = 80
        self.base_mana = 120
        self.health_growth = 15
        self.mana_growth = 30
        super().__init__("Mage", self.base_health, self.base_mana, level)

    def critHit(self):
        return 1.6 if random.randint(1, 100) <= 15 else 1.0

    def attack(self):
        baseDamage = 10 + (5 * self.level)
        damage = baseDamage * self.critHit()

        if self.max_mana != self.mana:
            self.mana += 15
        return f"Mage (Lvl {self.level}) hurls a Shadow Bomb!", damage
    
    def defend(self):
        if self.mana >= 20:
            self.is_defending = True
            self.mana -= 20   
            return f"You have cast a Dark Veil Shield."
        else:
            return f"You don't have enough mana to cast Dark Veil Shield"
    
    def cast_spell(self):
        baseDamage = 30 + (15 * self.level)
        damage = baseDamage * self.critHit()

        if self.mana >= 30:
            self.mana -= 30
            return f"Mage unleashes a Gloom Burst",  damage
        else: 
            return f"Not enough mana.", 0
        
class Archer(GameCharacter):
    def __init__(self, level=1):
        self.base_health = 100
        self.base_mana = 60
        self.health_growth = 25
        self.mana_growth = 20
        super().__init__("Archer", self.base_health, self.base_mana, level)

    def critHit(self):
        return 2.0 if random.randint(1, 100) <= 25 else 1.0

    def attack(self):
        baseDamage = 12 + (4 * self.level)
        damage = baseDamage * self.critHit()
        
        if self.max_mana != self.mana:
            self.mana += 5
        return f"Archer (Lvl {self.level}) fires a volley of arrows!", damage

    def defend(self):
        self.is_defending = True
        if self.max_mana != self.mana:
            self.mana += 5
        return f"Archer dashes out to evade the attack"

    def cast_spell(self):
        baseDamage = 20 + (10 * self.level)
        damage = baseDamage * self.critHit()

        if self.mana >= 15:
            self.mana -= 15
            return f"Archer fires a Charge Arrow!", damage
        else:
            return f"Not enough mana.", 0

class Assassin(GameCharacter):
    def __init__(self, level=1):
        self.base_health = 90
        self.base_mana = 60
        self.health_growth = 20
        self.mana_growth = 25
        super().__init__("Assassin", self.base_health, self.base_mana, level)

    def critHit(self):
        return 2.25 if random.randint(1,100) <= 35 else 1.0

    def attack(self):
        baseDamage = 15 + (5 * self.level)
        damage = baseDamage * self.critHit()

        if self.max_mana != self.mana:
            self.mana += 10
        return f"Assassin (Lvl {self.level}) slashed with a dagger", damage

    def defend(self):
        if self.mana >= 10:
            self.mana -= 10
            self.is_defending = True
            return f"Assassin uses Invisibility to dodge the enemy attack"
        else:
            return f"Not enoough mana"
    
    def cast_spell(self):
        baseDamage = 25 + (12 * self.level)
        damage = baseDamage * self.critHit()

        if self.mana >= 20:
            self.mana -= 20
            return f"Assassin enchants weapon with poison!", damage
        else:
            return f"Not enough mana", 0
    
class Enemy:
    def __init__(self, name, health, level = 1):
        self.name = name
        self.level = level
        self.health = health
        self.max_health = health

        # Health scaling
        scaling_factor = 1 + (0.2 * (self.level - 1))  # 20% more health per level
        self.max_health = int(self.max_health * scaling_factor)
        self.health = self.max_health

    def attack(self, player):
        baseDamage = int(self.max_health * 0.2) 
        maxDamage = baseDamage + (5 * self.level) 
        damageRange = random.randint(baseDamage, maxDamage)

        if player.is_defending:
            defenseAccuracy = random.randint(1,10)
            if defenseAccuracy <= 8:
                player.is_defending = False
                return f"{self.name} attacks, but it miss!", 0
            else:
                player.is_defending = False
                return f"{self.name} still manage to land an attack." , damageRange
        else:
            return f"{self.name} attacks viciously!", damageRange
        
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

def scale_stat(base_value, level, growth_rate):
    return int(base_value * ((1 + growth_rate) ** (level - 1)))

if __name__ == "__main__":
    clear()
    print("\nClasses")
    print("[1] Warrior")
    print("[2] Mage")
    print("[3] Archer")
    print("[4] Assassin")

    classChoice = input("Select a Class: ")

    time.sleep(1)
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
        print("[4] Quit")
        action = input("Choose action: ")
        if action == "1":
            desc, damage = player.attack()
        elif action == "2":
            desc = player.defend()
            damage = 0
        elif action == "3":
            desc, damage = player.cast_spell()
        elif action == "4":
            clear()
            print("[1] Confirm Quit")
            print("[2] Continue")
            quitAction = input("Choose action: ")
            if action == "1":
                clear()
                break
            else:
                clear()
                continue
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
            player.max_health = player.base_health + (player.level - 1) * player.health_growth
            player.health = player.max_health

            player.max_mana = player.base_mana + (player.level - 1) * player.mana_growth
            player.mana = player.max_mana

            # Respawn a random stronger enemy
            new_name, base_health = random.choice(enemy_data)
            scaled_health = int(base_health + int(player.level * 1.2 * base_health / 10))
            enemy = Enemy(new_name, health=scaled_health, level=player.level)
            print(f"\nA new {enemy.name} appears with {enemy.health} HP and Level {enemy.level}!")

            time.sleep(5)
            clear()
            continue

        # Enemy turn
        desc, damage = enemy.attack(player)
        print(desc)
        if random.randint(1,100) <= 10:
            print(f"But {enemy.name} didn't manage to land the attack")
        else:
            player.health -= damage
            print(f"You take {damage} damage. Your remaining health: {max(player.health, 0)}")

        if player.health <= 0:
            print("You have been defeated. Game Over!")
            break
            
        time.sleep(3)
        clear()