from time import sleep
import pygame
from pygame.locals import *
import random
import os

pygame.mixer.init()
pygame.mixer.music.load("battle2.wav")

#base template for characters
class Character:
    def __init__(self, name, health=100, strength=0, defense=1, energy=0):
        self.name = name
        self.health = health
        self.strength = strength
        self.defense = defense
        self.energy = energy
        self.skills = []
        self.original_health = health
        self.original_strength = strength
        self.original_defense = defense
        self.original_energy = energy
        
    def attack(self, opponent):
        opponent.health -= self.strength//opponent.defense
    
    def status_report(self):
        print(f"{self.name}: Health {self.health}, Energy {self.energy}")
        
    def defend(self):
        self.defense = self.defense*2
        print(f"""
{self.name} takes a defensive stance!
""")
        
    def defense_reset(self):
        self.defense = self.original_defense
        
    def add_skill(self, skill):
        self.skills.append(skill)
        
    def level_up(self):
        self.original_health = self.original_health+20
        self.original_energy = self.original_energy+20
        self.original_strength = self.original_strength+10
        
    def display_skills(self):
        for skill in self.skills:
            print(f"{self.skills.index(skill)+1}. {skill.name}: {skill.cost} energy")
            print(f"{skill.description}")
            
    def use_skill(self, skill, target):
        if skill in self.skills:
            skill.activate(self, target)
        else:
            print("You don't have that skill")
        
    def recover(self):
        self.energy += 10
        if self.energy > self.original_energy:
            self.energy = self.original_energy
        if self.strength < 5:
            self.strength = 5
        
    def full_heal(self):
        self.health = self.original_health
        self.energy = self.original_energy
        self.strength = self.original_strength
        
#template for player characters
class Player(Character):
    def __init__(self, name, weapon, health=100, strength=20, defense=1, energy=100):
        super().__init__(name, health, strength, defense, energy)
        self.weapon = weapon
        
    def attack(self, opponent):
        super().attack(opponent)
        print(f"""{self.name} attacks {opponent.name} with {self.weapon}! {self.strength // opponent.defense} damage!
""")
        
#skills for the players to know
class Skill:
    def __init__(self, name, description, modifier=0, cost=0):
        self.name = name
        self.modifier = modifier
        self.cost = cost
        self.description = description

#strength booster to increase damage
class Booster(Skill):
    def __init__(self, name, description, modifier=10, cost=30):
        super().__init__(name, description, modifier, cost)
        
    def activate(self, hero, target):
        target.strength += 10
        print(f"{hero.name} focuses his energy into empowering his allies! {target.name}'s strength has been boosted by {self.modifier}!")
        target.energy -= self.cost

class Debuff(Skill):
    def __init__(self, name, description, modifier=5, cost=30):
        super().__init__(name, description, modifier, cost)
        
    def activate(self, hero, target):
        target.strength -= 10
        print(f"{hero.name} chants a wicked spell to weaken foes! {target.name}'s strength has been reduced by {self.modifier}!")

#Big old blast to kill fast
class SpecialMove(Skill):
    def __init__(self, name, description, modifier=2, cost=50):
        super().__init__(name, description, modifier, cost)
        
    def activate(self, hero, target):
        blaster = hero.strength * self.modifier
        target.health -= blaster // target.defense
        hero.energy -= self.cost
        print(f"{hero.name} gathers power and unleashes it at {target.name} for {blaster // target.defense} damage!")

class HealingMove(Skill):
    def __init__(self, name, description, modifier=50, cost=40):
        super().__init__(name, description, modifier, cost)
    
    def activate(self, hero, target):
        #Nothing to see here
        return

#Establishing the brawler "Oliver" and his skills
oliver = Player("Oliver", "a flurry of punches and kicks")
resonance_boost = Booster("Resonance Boost", "Boosts an ally's attack power")
resonance_blast = SpecialMove("Resonance Blast", "A powerful damaging surge of energy")
#resonance_shield = 
oliver.add_skill(resonance_boost)
oliver.add_skill(resonance_blast)

#Establishing the mage "Amanita" and her skills
amanita = Player("Amanita", "a swing of her knife", 80, 10, 1, 150)
magic_blast = SpecialMove("Arcane Comet", "A huge blast of magical energy", 4, 75)
weaken = Debuff("Weakening Wave", "A wicked spell that weakens foes")
amanita.add_skill(weaken)
amanita.add_skill(magic_blast)

#Establishing the opponents
samson = Player("Samson", "a mighty cleave of his greatsword", 200, 30, 2)
samson.add_skill(weaken)
samson.add_skill(resonance_blast)
goji = Player("Goji", "blinding speed", 120, 30)
goji.add_skill(resonance_blast)
phoenix = Player("Phoenix", "magical power", 100, 20)
phoenix.add_skill(resonance_blast)
phoenix.add_skill(weaken)



#The combat system
def battle_grid(hero, partner, opponent):
    combatants = [hero, partner, opponent]
    opponent_exclusion = [hero, partner]
    choose_move_one = 0
    choose_move_two = 0
    while hero.health > 0 or partner.health > 0 :
        if hero.health <= 0 and hero in combatants:
            combatants.remove(hero)
        elif partner.health <= 0 and partner in combatants:
            combatants.remove(partner)
        elif partner.health > 0 and not partner in combatants:
            combatants.append(partner)
        elif hero.health > 0 and not hero in combatants:
            combatants.append(hero)
        round_over = False
        if round_over == False:
            if opponent.health > 0:
                opponent.status_report()
                print(f"""
You're in the thick of it! {opponent.name} stands across from you in the arena, imposing.
""")
                
                #Hero's turn
                if hero.health > 0:
                    move_on_one = 0
                    while move_on_one == 0:
                        print(f"""What will {hero.name} do?
""")
                        hero.status_report()
                        choose_move_one = int(input("""
1. Attack
2. Skill
3. Defend
>>"""))
                        if choose_move_one == 1:
                            move_on_one = 1
                        elif choose_move_one == 2:
                            print("""
Which skill?
""")
                            hero.display_skills()
                            skill_choice = int(input(">>"))-1
                            
                            if skill_choice <= len(hero.skills):
                                hero_skill = hero.skills[skill_choice]
                                if hero_skill.cost <= hero.energy:
                                    hero_target = int(input(f"""Targeting whom?
1. {hero.name}
2. {partner.name}
3. {opponent.name}
"""))-1
                                    move_on_one = 1
                                elif hero_skill.cost > hero.energy:
                                    print("You don't have enough energy to use that move.")
                            else:
                                print("Invalid input")
                        elif choose_move_one == 3:
                            move_on_one = 1
                        else:
                            print("Invalid input")
                else:
                    hero.health = 0
                    choose_move_one = 0
                    
                #Partner's Turn
                if partner.health > 0:
                    move_on_two = 0
                    while move_on_two == 0:
                        print(f"""What will {partner.name} do?
""")
                        partner.status_report()
                        choose_move_two = int(input("""
1. Attack
2. Skill
3. Defend
>>"""))
                        print(choose_move_two)
                        if choose_move_two == 1:
                            move_on_two = 1
                        elif choose_move_two == 2:
                            print("""
Which skill?
""")
                            partner.display_skills()
                            skill_choice = int(input(">>"))-1
                            
                            
                            if skill_choice <= len(partner.skills):
                                partner_skill = partner.skills[skill_choice]
                                if partner_skill.cost < partner.energy:
                                    partner_target = int(input(f"""Targeting whom?
1. {hero.name}
2. {partner.name}
3. {opponent.name}
"""))-1
                                    move_on_two = 1
                                else:
                                    print("You don't have enough energy to use that move")
                            else:
                                print("Invalid skill input")
                        elif choose_move_two == 3:
                            move_on_two = 1
                        else:
                            print("Invalid input")
                else:
                    hero.health = 0
                    choose_move_one = 0
                    partner.health = 0
                    choose_move_two = 0
                aim = random.random()
                if aim <= .5:
                    victim = hero
                else:
                    victim = partner
                if choose_move_one == 1:
                    hero.attack(opponent)
                elif choose_move_one == 2:
                    hero.use_skill(hero_skill, combatants[hero_target])
                elif choose_move_one == 3:
                    hero.defend()
                input("press enter to continue")
                if choose_move_two == 1:
                    partner.attack(opponent)
                elif choose_move_two == 2:
                    partner.use_skill(partner_skill, combatants[partner_target])
                elif choose_move_two == 3:
                    partner.defend()
                input("press enter to continue")
                move_decide = random.random()
                if move_decide < 0.5:
                    if opponent.energy > 0 and len(opponent.skills) > 0:  # Check if opponent has skills and energy
                        available_skills = [skill for skill in opponent.skills if skill.cost <= opponent.energy]
                        if available_skills == True:
                            chosen_skill = random.choice(available_skills)
                            target = random.choice(opponent_exclusion)
                            opponent.use_skill(chosen_skill, target)
                        else:
                            opponent.attack(random.choice(opponent_exclusion))
                    else:
                        opponent.attack(random.choice(opponent_exclusion))
                else:
                    if opponent.energy > 0:
                        available_skills = [skill for skill in opponent.skills if skill.cost <= opponent.energy]
                        if available_skills:
                            chosen_skill = random.choice(available_skills)
                            target = random.choice(opponent_exclusion)
                            opponent.use_skill(chosen_skill, target)
                        else:
                            opponent.attack(random.choice(opponent_exclusion))
                    else:
                        opponent.attack(random.choice(opponent_exclusion))
                    
                input("press enter to continue")
                hero.defense_reset()
                partner.defense_reset()
                opponent.defense_reset()
                hero.recover()
                partner.recover()
                opponent.recover()
                round_over = True
            else:
                print(f"{opponent.name} lies defeated! You are victorious!")
                return True
    else:
        print("You have been defeated. Better luck next year.")
        return False

#The meat of the code
def game_time():
    victories = 0
    defeated_opponents = []
    first_match = True
    choice = 0
    while len(defeated_opponents) < 2:
        if first_match == True:
            
        
            print("""
Today is the day. The brawler Oliver and the witch Amanita have entered the tournament of Champions' Lake to meet their destiny, bringing with them only the essentials for tournament combat. Oliver has trained in the art of resonance, allowing him to boost his strength beyond his normal capabilities. Amanita has learned to channel the magic of the world and blast it at her enemies. Together, they believe they stand a chance.
""")
            print("""In this game, you will take control of Oliver and Amanita and fight your way to the top of the tournament ladder. There will be three opponents in your way, you will have to defeat them all to win.
""")
            print("""Try to manage your health and energy to best handle the challenges ahead. You will regain some energy every turn, but you won't regain health until the fight is over. However, you will be able to gain bonuses between fights that will help you in the next one.
""")
            input("Press enter to continue")
    
            print("""As our two warriors arrive at the colosseum, they each ready themselves for the challenges that lay within. Oliver steadies his breathing, Amanita chants a short protection spell. According to the rules of the tournament, they will get to choose the order in which they fight their opponents, and fight the reigning champion if they win two matches. Who will they fight first?
""")
        
            choice = int(input("""1. Phoenix the Arcane
2. Goji the Relentless

Enter a number to choose
>>"""))
            
            if choice == 1:
                print("""The stunning Phoenix. Amanita's teacher. She has long awaited the opportunity to show her master how much she's improved. Now, they will bear their magic against each other.
""")
                print("""Phoenix has debuff skills and powerful magic, but a weak attack. You'll need to be careful when fighting her.
Fight your best!
""")
                input("Press enter to continue")
                pygame.mixer.music.play()
                pbattle = battle_grid(oliver, amanita, phoenix)
                pygame.mixer.music.fadeout(50)
                if pbattle == True:
                    choice = 0
                    first_match = False
                    defeated_opponents.append(phoenix)
                else:
                    break
            elif choice == 2:
                print("""The lightning-fast Goji. Oliver's rival. The two of them have been competing against one another for a long time, but now it's time to lay this feud to rest. Today, they'll know which one is the better resonance master.
""")
                print("""Goji does the most damage out of the three, if you don't take him down quickly you're bound to lose.
Fight your best!
""")
                input("Press enter to continue")
                pygame.mixer.music.play()
                gbattle = battle_grid(oliver, amanita, goji)
                pygame.mixer.music.fadeout(50)
                if gbattle == True:
                    choice = 0
                    first_match = False
                    defeated_opponents.append(goji)
                else:
                    break
            else:
                print("Invalid choice")
                choice = 0
        oliver.level_up()
        amanita.level_up()
        print("""You've won your first fight, and as a reward you have received a boost to your stats and a new skill for each of your characters. You're halfway there.""")
        print("""Ready yourself for the next fight!""")
            
        if phoenix in defeated_opponents and not goji in defeated_opponents:
            choice = int(input("""2. Goji the Relentless

Enter a number to choose
>>"""))
        elif goji in defeated_opponents and not phoenix in defeated_opponents:
            choice = int(input("""1. Phoenix the Arcane

Enter a number to choose
>>"""))
        if choice == 1 and not phoenix in defeated_opponents:
            print("""The stunning Phoenix. Amanita's teacher. She has long awaited the opportunity to show her master how much she's improved. Now, they will bear their magic against each other.
""")
            print("""Phoenix has debuff skills and powerful magic, but a weak attack. You'll need to be careful when fighting her.
Fight your best!
""")
            pygame.mixer.music.play()
            pbattle = battle_grid(oliver, amanita, phoenix)
            pygame.mixer.music.fadeout(50)
            if pbattle == True:
                choice = 0
                first_match = False
                defeated_opponents.append(phoenix)
                oliver.full_heal
                amanita.full_heal
                choice = 0
        elif choice == 1 and phoenix in defeated_opponents:
            print("""Phoenix has already been defeated, it's time to move on to the next fight.""")
            choice = 0
            
        elif choice == 2 and goji not in defeated_opponents:
            print("""The lightning-fast Goji. Oliver's rival. The two of them have been competing against one another for a long time, but now it's time to lay this feud to rest. Today, they'll know which one is the better resonance master.
""")
            print("""Goji does the most damage out of the three, if you don't take him down quickly you're bound to lose.
Fight your best!
""")
            input("Press enter to continue")
            pygame.mixer.music.play()
            gbattle = battle_grid(oliver, amanita, goji)
            pygame.mixer.music.fadeout(50)
            if gbattle == True:
                choice = 0
                first_match = False
                defeated_opponents.append(goji)
                oliver.full_heal
                amanita.full_heal
        elif choice == 2 and goji in defeated_opponents:
            print("""Goji has already been defeated, it's time to move on to the next fight.""")
            choice = 0
        else:
            print("Invalid choice")
            choice = 0
            
            
    else:
        oliver.level_up()
        amanita.level_up()
        print("""The time has finally come for the championship. Samson the Unbeaten is your opponent. He's tougher than anyone else, so it's no surprise he's been the champion for many years.
""")
        print("""He's strong, fast, and durable. He'll take half damage from all your attacks. You'll have to outlast him if you want to win.""")
        print("""Meet your destiny!""")
        input("Press enter to continue")
        pygame.mixer.music.load("war.mp3")
        pygame.mixer.music.play()
        sbattle = battle_grid(oliver, amanita, samson)
        if sbattle == True:
            print("""The crowd screams and cheers with excitement as the champion falls to the arena floor. At first it's hard to believe, but realization dawns over Oliver and Amanita's faces as they fully understand what they've done. They've achieved their dreams. The championship is theirs!""")
            print("""Oliver takes a victory lap around the arena, Amanita breathes a sigh of relief. They will forever be recorded in the history of Champions' Lake. All thanks to you.""")
            print("""Thanks for playing""")
        
    
game_time()