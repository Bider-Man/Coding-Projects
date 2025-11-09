# Import Modules
import pygame
import random
import time
import json
import os
import math

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((900, 650))
pygame.display.set_caption("Ouranos")
font = pygame.font.SysFont("Courier", 20)
title_font = pygame.font.SysFont("Courier", 32, bold = True)
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
BLUE = (100, 150, 255)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
DARK_PURPLE = (100, 10, 100)
DARK_GRAY = (50, 50, 50)
LIGHT_BROWN = (181, 101, 29)
FOREST_GREEN = (34, 139, 34)
DESERT_YELLOW = (210, 190, 120)
CAVE_GRAY = (80, 80, 90)
WATER_BLUE = (50, 120, 180)

# Game Constants
DICE_TYPES = ["d4", "d6", "d8", "d10", "d12", "d20"]
UNLOCK_LEVELS = [2, 4, 6, 8, 10, 12]
SAVE_FILE = "ouranos_save.json"
DICE_ANIMATION_INTERVAL = 1
SCAVENGE_TIME = 15

# Pathfinder 2e XP thresholds
XP_THRESHOLDS = [0, 1000, 3000, 6000, 10000, 15000, 21000, 28000, 36000, 45000, 
                 55000, 66000, 78000, 91000, 105000, 120000, 136000, 153000, 171000, 190000]

# Classes
class Player:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.level = 1
        self.xp = 0
        self.unlocked_dice = ["d4"]
        self.potions = []
        self.next_die_index = 0
        self.last_rolls = []
        self.total_rolls = 0
        self.ingredients = {"herb": 0, "gem": 0, "mushroom": 0, "flower": 0, "root": 0}

    def calculate_xp_required(self):
        if self.level >= len(XP_THRESHOLDS):
            return XP_THRESHOLDS[-1]
        return XP_THRESHOLDS[self.level]

    def roll_dice(self):
        rolls = []
        total_xp = 0
        
        # Apply active potion effects
        xp_multiplier = 1.0
        for potion in self.potions[:]:
            if potion["effect"] == "2x XP":
                xp_multiplier = 2.0
            elif potion["effect"] == "+1 to all rolls":
                total_xp += len(self.unlocked_dice)

        # Roll all unlocked dice
        for die in self.unlocked_dice:
            max_roll = int(die[1:])
            roll = random.randint(1, max_roll)
            rolls.append((die, roll))
            total_xp += roll

        total_xp = int(total_xp * xp_multiplier)
        self.last_rolls = rolls
        self.total_rolls += 1
        self.xp += total_xp

        if self.xp >= self.calculate_xp_required():
            self.level_up()
            
        return rolls, total_xp

    def level_up(self):
        self.level += 1
        
        if self.next_die_index < len(UNLOCK_LEVELS) and self.level >= UNLOCK_LEVELS[self.next_die_index]:
            new_die = DICE_TYPES[self.next_die_index + 1]
            self.unlocked_dice.append(new_die)
            self.next_die_index += 1
            return new_die
        return None

    def scavenge(self):
        ingredients_gained = []
        
        # Base chance to find something
        if random.random() < 0.7:  # 70% chance to find at least one item
            ingredient = random.choice(list(self.ingredients.keys()))
            quantity = random.randint(1, 3)
            self.ingredients[ingredient] += quantity
            ingredients_gained.append((ingredient, quantity))
            
            # Chance for bonus item
            if random.random() < 0.3:
                ingredient = random.choice(list(self.ingredients.keys()))
                quantity = random.randint(1, 2)
                self.ingredients[ingredient] += quantity
                ingredients_gained.append((ingredient, quantity))
        
        return ingredients_gained

    def to_dict(self):
        return {
            "level": self.level,
            "xp": self.xp,
            "unlocked_dice": self.unlocked_dice,
            "potions": self.potions,
            "next_die_index": self.next_die_index,
            "total_rolls": self.total_rolls,
            "ingredients": self.ingredients,
        }

    @classmethod
    def from_dict(cls, data):
        player = cls()
        player.level = data["level"]
        player.xp = data["xp"]
        player.unlocked_dice = data["unlocked_dice"]
        player.potions = data["potions"]
        player.next_die_index = data["next_die_index"]
        player.total_rolls = data["total_rolls"]
        player.ingredients = data.get("ingredients", {"herb": 0, "gem": 0, "mushroom": 0, "flower": 0, "root": 0})
        return player

class Alchemy:
    def __init__(self):
        self.recipes = {
            "Luck Potion": {"ingredients": ["herb", "herb", "herb"], "effect": "+1 to all rolls", "duration": 30, "color": GREEN},
            "Critical Brew": {"ingredients": ["herb", "gem", "mushroom"], "effect": "10% crit chance", "duration": 20, "color": RED},
            "XP Doubler": {"ingredients": ["gem", "gem", "herb"], "effect": "2x XP", "duration": 60, "color": GOLD},
            "Astral Essence": {"ingredients": ["flower", "root", "gem"], "effect": "Boost astrology", "duration": 45, "color": PURPLE},
        }

    def brew_potion(self, ingredients, player):
        for name, recipe in self.recipes.items():
            if sorted(ingredients) == sorted(recipe["ingredients"]):
                # Check if player has enough ingredients
                can_brew = True
                temp_ingredients = player.ingredients.copy()
                for ing in recipe["ingredients"]:
                    if temp_ingredients[ing] <= 0:
                        can_brew = False
                        break
                    temp_ingredients[ing] -= 1
                
                if can_brew:
                    player.ingredients = temp_ingredients
                    potion = {
                        "name": name,
                        "effect": recipe["effect"],
                        "duration": recipe["duration"],
                        "time_created": time.time(),
                        "color": recipe["color"]
                    }
                    return potion
        return None

class Astrology:
    def __init__(self):
        self.events = {
            "Blood Moon": {"effect": "2x XP", "duration": 60, "color": RED},
            "Mercury Retrograde": {"effect": "Inverted Rolls", "duration": 45, "color": DARK_PURPLE},
            "Solar Eclipse": {"effect": "Automatic Crits", "duration": 90, "color": GOLD},
            "Stellar Alignment": {"effect": "No XP Penalty", "duration": 45, "color": BLUE},
            "Cosmic Winds": {"effect": "Faster Rolling", "duration": 30, "color": PURPLE}
        }
        self.active_event = None
        self.event_start_time = 0

    def update(self, player):
        current_time = time.time()
        player.potions = [p for p in player.potions if p["duration"] < 0 or (current_time - p["time_created"] < p["duration"])]
    
        if (self.active_event is None and random.random() < 0.00002):
            self.active_event = random.choice(list(self.events.keys()))
            self.event_start_time = current_time

        elif (self.active_event and current_time > self.event_start_time + self.events[self.active_event]["duration"]):
            self.active_event = None

class ScavengeGame:
    def __init__(self):
        self.biomes = {
            "Forest": {
                "color": FOREST_GREEN,
                "common": ["herb", "mushroom"],
                "uncommon": ["flower", "root"],
                "rare": ["gem"]
            },
            "Desert": {
                "color": DESERT_YELLOW,
                "common": ["root", "herb"],
                "uncommon": ["gem", "mushroom"],
                "rare": ["ancient relic"]
            },
            "Caves": {
                "color": CAVE_GRAY,
                "common": ["mushroom", "gem"],
                "uncommon": ["root", "crystal"],
                "rare": ["dark essence"]
            }
        }
        self.current_biome = "Forest"
        self.objects = []
        self.active = False
        self.result = None
        self.start_time = 0
        self.time_left = 0
        self.generate_objects()

    def generate_objects(self):
        self.objects = []
        biome = self.biomes[self.current_biome]

        # Generate Common Items
        for _ in range(random.randint(5, 8)):
            item = random.choice(biome["common"])
            size = random.randint(25, 40)
            self.objects.append({
                "name": item,
                "color": self.get_item_color(item),
                "rect": pygame.Rect(
                    random.randint(50, 800 - size),
                    random.randint(100, 450 - size),
                    size, size
                ),
                "rarity": "common"
            })

        # Generate Uncommon Items
        for _ in range(random.randint(2, 3)):
            item = random.choice(biome["uncommon"])
            size = random.randint(35, 50)
            self.objects.append({
                "name": item,
                "color": self.get_item_color(item),
                "rect": pygame.Rect(
                    random.randint(50, 800 - size),
                    random.randint(100, 450 - size),
                    size, size
                ),
                "rarity": "uncommon"
            })

        # Generate Rare Items
        if random.random() < 0.3:
            item = random.choice(biome["rare"])
            size = 45
            self.objects.append({
                "name": item,
                "color": self.get_item_color(item),
                "rect": pygame.Rect(
                    random.randint(50, 800 - size),
                    random.randint(100, 450 - size),
                    size, size
                ),
                "rarity": "rare"
            })

    def get_item_color(self, item):
        colors = {
            "herb": GREEN,
            "mushroom": (220, 150, 150),
            "flower": PURPLE,
            "root": LIGHT_BROWN,
            "gem": BLUE,
            "crystal": (200, 200, 255),
            "dark essence": DARK_PURPLE,
            "ancient relic": GOLD
        }
        return colors.get(item, WHITE)

    def start(self):
        self.active = True
        self.result = None
        self.start_time = time.time()
        self.time_left = SCAVENGE_TIME
        self.current_biome = random.choice(list(self.biomes.keys()))
        self.generate_objects()

    def update(self):
        if self.active:
            self.time_left = max(0, SCAVENGE_TIME - (time.time() - self.start_time))
            if self.time_left <= 0:
                self.active = False
                return "time_up"
        return None

    def draw(self, surface):
        # Biome Background
        biome_color = self.biomes[self.current_biome]["color"]
        pygame.draw.rect(surface, biome_color, (0, 0, 900, 650))

        # Title
        title = title_font.render(f"Scavenging in: {self.current_biome}", True, WHITE)
        surface.blit(title, (300, 20))

        # Timer
        timer_text = font.render(f"Time Left: {int(self.time_left)}s", True, WHITE)
        surface.blit(timer_text, (700, 20))

        # Draw Objects
        for obj in self.objects:
            pygame.draw.rect(surface, obj["color"], obj["rect"])

            if obj["rarity"] == "uncommon":
                pygame.draw.rect(surface, GOLD, obj["rect"], 3)
            elif obj["rarity"] == "rare":
                pygame.draw.rect(surface, (255, 50, 255), obj["rect"], 4)

        # Instructions
        instructions = [
            "Click on the objects to gather them",
            "Gold border = uncommon",
            "Purple border = rare"
        ]
        for i, line in enumerate(instructions):
            text = font.render(line, True, WHITE)
            surface.blit(text, (50, 550 + i * 25))

        if self.result:
            rarity_color = WHITE
            if self.result["rarity"] == "uncommon":
                rarity_color = GOLD
            elif self.result["rarity"] == "rare":
                rarity_color = (255, 50, 255)

            found_text = font.render(f"Found: {self.result['name']} (x{self.result['quantity']})", True, rarity_color)
            surface.blit(found_text, (350, 580))

    def handle_click(self, pos):
        for obj in self.objects:
            if obj["rect"].collidepoint(pos):
                if obj["rarity"] == "common":
                    quantity = random.randint(1, 5)
                elif obj["rarity"] == "uncommon":
                    quantity = random.randint(1, 3)
                else:
                    quantity = 1

                self.result = {
                    "name": obj["name"],
                    "quantity": quantity,
                    "rarity": obj["rarity"]
                }
                self.objects.remove(obj)
                return obj["name"], quantity
        return None

class DiceAnimator:
    def __init__(self):
        self.current_values = {}
        self.target_values = {}
        self.animation_start_time = 0
        self.is_animating = False
        self.last_change_time = 0
    
    def start_animation(self, target_values, immediate=False):
        self.target_values = target_values
        self.animation_start_time = time.time()
        self.is_animating = not immediate
        self.last_change_time = time.time()
        
        # Initialize values
        for die, target_val in target_values.items():
            max_val = int(die[1:])
            if immediate:
                self.current_values[die] = target_val
            else:
                self.current_values[die] = random.randint(1, max_val)
    
    def update_animation(self):
        if not self.is_animating:
            return False
        
        elapsed = time.time() - self.animation_start_time
        progress = min(elapsed / 1.0, 1.0)  # 1 second animation
        
        # Update values during animation
        if time.time() - self.last_change_time > DICE_ANIMATION_INTERVAL:
            self.last_change_time = time.time()
            for die, target_val in self.target_values.items():
                max_val = int(die[1:])
                if progress < 0.9:  # Random numbers for first 90%
                    self.current_values[die] = random.randint(1, max_val)
                else:  # Settle on final value
                    self.current_values[die] = target_val
        
        if progress >= 1.0:
            self.is_animating = False
            return False
        return True
    
    def get_current_values(self):
        return self.current_values

# Functions for the Classes
def draw_die_progress_bar(surface, die_type, current_value, max_value, x, y, width=100, height=30):
    # Draw background
    pygame.draw.rect(surface, DARK_GRAY, (x, y, width, height))
    
    # Draw filled portion
    fill_width = int(width * (current_value / max_value))
    color = GREEN if current_value == max_value else BLUE
    pygame.draw.rect(surface, color, (x, y, fill_width, height))
    
    # Draw border
    pygame.draw.rect(surface, WHITE, (x, y, width, height), 2)
    
    # Draw value text
    value_color = BLACK if current_value == max_value else WHITE
    value_text = font.render(f"{current_value}", True, value_color)
    text_rect = value_text.get_rect(center=(x + width//2, y + height//2))
    surface.blit(value_text, text_rect)
    
    # Draw die type
    die_text = font.render(die_type, True, WHITE)
    surface.blit(die_text, (x, y - 25))

def draw_astrology_event(surface, astrology, x=50, y=330):
    if astrology.active_event:
        event = astrology.events[astrology.active_event]
        remaining = max(0, event["duration"] - (time.time() - astrology.event_start_time))
        
        name_text = font.render(f"Celestial Event: {astrology.active_event}", True, event["color"])
        surface.blit(name_text, (x, y))
        
        effect_text = font.render(f"Effect: {event['effect']} ({int(remaining)}s)", True, WHITE)
        surface.blit(effect_text, (x, y + 25))

def draw_unlocked_dice(surface, unlocked_dice, animator, x=50, y=100):
    current_values = animator.get_current_values()
    dice_width = 100
    spacing = 20
    
    for i, die in enumerate(unlocked_dice):
        if die in current_values:
            roll_value = current_values[die]
        else:
            roll_value = random.randint(1, int(die[1:]))
        
        draw_die_progress_bar(surface, die, roll_value, int(die[1:]), 
                            x + i * (dice_width + spacing), y, dice_width, 30)

def draw_xp_bar(surface, player, x=50, y=30, width=600, height=20):
    xp_required = player.calculate_xp_required()
    progress = min(player.xp / xp_required, 1.0) if xp_required > 0 else 0
    
    # Draw background bar
    pygame.draw.rect(surface, DARK_GRAY, (x, y, width, height))
    
    # Draw filled portion
    pygame.draw.rect(surface, GREEN, (x, y, int(width * progress), height))
    
    # Draw border
    pygame.draw.rect(surface, WHITE, (x, y, width, height), 2)
    
    # Draw level text above the bar
    level_text = font.render(f"Level {player.level}", True, WHITE)
    surface.blit(level_text, (x, y - 25))
    
    # Draw XP text below the bar to prevent overlapping
    xp_text = font.render(f"{player.xp}/{xp_required} XP", True, WHITE)
    surface.blit(xp_text, (x + (width - xp_text.get_width()) // 2, y + height + 5))

def draw_alchemy_screen(surface, alchemy, player, x=200, y=50):
    title = font.render("Alchemy Lab", True, GOLD)
    surface.blit(title, (300, y))
    
    # Recipes
    recipes_title = font.render("Recipes:", True, WHITE)
    surface.blit(recipes_title, (x, y + 40))
    
    for i, (name, recipe) in enumerate(alchemy.recipes.items()):
        text = font.render(f"{i+1}. {name}: {recipe['ingredients']}", True, WHITE)
        surface.blit(text, (x, y + 70 + i * 30))
    
    # Ingredients
    ingredients_title = font.render("Your Ingredients:", True, WHITE)
    surface.blit(ingredients_title, (x, y + 220))
    
    for i, (name, count) in enumerate(player.ingredients.items()):
        text = font.render(f"{name}: {count}", True, GREEN)
        surface.blit(text, (x, y + 250 + i * 25))
    
    # Potions
    potions_title = font.render("Your Potions:", True, WHITE)
    surface.blit(potions_title, (x, y + 375))
    
    for i, potion in enumerate(player.potions):
        if potion["duration"] > 0:
            remaining = max(0, potion["duration"] - (time.time() - potion["time_created"]))
            text = font.render(f"{i+1}. {potion['name']} ({int(remaining)}s)", True, potion.get("color", GREEN))
        else:
            text = font.render(f"{i+1}. {potion['name']} (permanent)", True, potion.get("color", GREEN))
        surface.blit(text, (x, y + 400 + i * 25))

def draw_menu(surface):
    options = [
        "1. Continue Game",
        "2. New Game",
        "3. Quit"
    ]
    
    title = title_font.render("OURANOS", True, GOLD)
    surface.blit(title, (350, 150))
    
    for i, option in enumerate(options):
        text = font.render(option, True, WHITE)
        surface.blit(text, (300, 200 + i * 40))

def save_game(player):
    data = {
        "player": player.to_dict(),
        "timestamp": time.time()
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_game():
    if not os.path.exists(SAVE_FILE):
        return None
        
    with open(SAVE_FILE, "r") as f:
        data = json.load(f)
    return Player.from_dict(data["player"])

def main():
    player = load_game()
    if player is None:
        player = Player()
    
    alchemy = Alchemy()
    astrology = Astrology()
    dice_animator = DiceAnimator()
    scavenge_game = ScavengeGame()
    running = True
    in_menu = True if player.level > 1 else False
    current_view = "main"
    message_log = []
    last_roll_total = 0
    last_day = time.localtime().tm_yday

    # Initialize dice with current values
    if player.last_rolls:
        dice_animator.start_animation({die: roll for die, roll in player.last_rolls}, immediate=False)

    while running:
        current_time = time.time()
        current_day = time.localtime().tm_yday
        screen.fill(BLACK)
        
        # Update dice animation
        dice_animator.update_animation()
        
        if in_menu:
            draw_menu(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        in_menu = False
                    elif event.key == pygame.K_2:
                        player = Player()
                        in_menu = False
                    elif event.key == pygame.K_3:
                        running = False
            pygame.display.flip()
            clock.tick(60)
            continue
            
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(player)
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and current_view == "main":
                    rolls, total = player.roll_dice()
                    last_roll_total = total
                    message_log.append(f"Rolled {total} XP!")
                    dice_animator.start_animation({die: roll for die, roll in rolls})
                    
                    if player.next_die_index < len(UNLOCK_LEVELS) and player.level >= UNLOCK_LEVELS[player.next_die_index]:
                        new_die = DICE_TYPES[player.next_die_index + 1]
                        player.unlocked_dice.append(new_die)
                        player.next_die_index += 1
                        message_log.append(f"Unlocked {new_die}!")
                
                elif event.key == pygame.K_a:
                    current_view = "alchemy" if current_view != "alchemy" else "main"
                elif event.key == pygame.K_g and current_view == "main":  # Added this line for scavenging
                    scavenge_game.start()
                elif event.key == pygame.K_ESCAPE:
                    current_view = "main"
                elif event.key == pygame.K_q:
                    save_game(player)
                    running = False
                elif event.key == pygame.K_s:
                    save_game(player)
                    message_log.append("Game saved!")
                elif event.key == pygame.K_r and current_view == "alchemy":
                    if sum(player.ingredients.values()) >= 3:
                        ingredients = random.sample(
                            [k for k, v in player.ingredients.items() for _ in range(v)], 
                            min(3, sum(player.ingredients.values())))
                        potion = alchemy.brew_potion(ingredients, player)
                        if potion:
                            player.potions.append(potion)
                            message_log.append(f"Brewed {potion['name']}!")
                        else:
                            message_log.append("Failed to brew potion!")
            
            elif event.type == pygame.MOUSEBUTTONDOWN and scavenge_game.active:
                result = scavenge_game.handle_click(event.pos)
                if result:
                    ingredient, quantity = result
                    player.ingredients[ingredient] += quantity
                    message_log.append(f"Found {quantity} {ingredient}(s)!")
                    scavenge_game.active = False

        # Update systems
        astrology.update(player)
        scavenge_game.update()
        
        # Render
        if scavenge_game.active:
            scavenge_game.draw(screen)
        else:
            if current_view == "main":
                # Top section
                draw_xp_bar(screen, player)
                
                # Middle section
                draw_unlocked_dice(screen, player.unlocked_dice, dice_animator, 50, 100)
                
                # Last roll total
                if player.last_rolls:
                    total_text = font.render(f"Total XP: {last_roll_total}", True, GOLD)
                    screen.blit(total_text, (400, 200))
                
                # Astrology event
                draw_astrology_event(screen, astrology)
                
                # Left panel: Message log
                message_title = font.render("Messages:", True, WHITE)
                screen.blit(message_title, (50, 380))
                
                for i, message in enumerate(message_log[-3:]):
                    text = font.render(message, True, WHITE)
                    screen.blit(text, (50, 410 + i * 25))
                
                # Right panel: Controls
                controls_title = font.render("Controls:", True, WHITE)
                screen.blit(controls_title, (550, 100))
                
                controls = [
                    "SPACE: Roll dice",
                    "A: Alchemy Lab",
                    "G: Go scavenging",  # Added this line
                    "S: Save Game",
                    "Q: Quit and Save",
                    f"Total Rolls: {player.total_rolls}"
                ]
                for i, line in enumerate(controls):
                    text = font.render(line, True, WHITE)
                    screen.blit(text, (550, 130 + i * 25))
                
            elif current_view == "alchemy":
                draw_alchemy_screen(screen, alchemy, player)
                
                # Controls at bottom
                controls = [
                    "R: Brew Random Potion",
                    "ESC: Back to Main"
                ]
                for i, line in enumerate(controls):
                    text = font.render(line, True, WHITE)
                    screen.blit(text, (50, 500 + i * 25))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
