# Import Modules
import pygame
import random
import time
import math

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ouranos")
font = pygame.font.SysFont("Courier", 24)
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
BLUE = (0, 0, 255)

# Game Constants
DICE_TYPES = ["d4", "d6", "d8", "d10", "d12", "d20", "d100"]
# Cumulative levels needed for next die
UNLOCK_LEVELS = [5, 12, 21, 32, 45, 60]


class Player:
    def __init__(self):
        self.level = 1
        self.xp = 0
        self.xp_to_level = self.calculate_xp_required()
        self.unlocked_dice = ["d4"]
        self.active_die = "d4"
        self.potions = []
        self.next_die_index = 0
        self.last_rolls = []
        self.total_rolls = 0

    def calculate_xp_required(self):
        # Exponential curve with milestone adjustments
        base_xp = 10 * (self.level ** 1.4)

        # Every 5 levels, reduce XP needed by 20% as a bonus
        if self.level % 5 == 0:
            base_xp *= 0.8

        return int(base_xp)

    def roll_dice(self):
        rolls = []
        total_xp = 0

        # Roll all unlocked dice
        for die in self.unlocked_dice:
            max_roll = int(die[1:])
            roll = random.randint(1, max_roll)
            rolls.append((die, roll))
            total_xp += roll

        self.last_rolls = rolls
        self.total_rolls += 1
        self.xp += total_xp

        # Check for level up
        if self.xp >= self.xp_to_level:
            self.level_up()

        return rolls, total_xp

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_level
        self.xp_to_level = self.calculate_xp_required()

        # Check for new dice unlocks
        if self.next_die_index < len(UNLOCK_LEVELS) and self.level >= UNLOCK_LEVELS[self.next_die_index]:
            new_die = DICE_TYPES[self.next_die_index + 1]
            self.unlocked_dice.append(new_die)
            self.next_die_index += 1
            return new_die
        return None

    def use_potion(self, potion_index):
        if 0 <= potion_index < len(self.potions):
            return self.potions.pop(potion_index)
        return None


class Alchemy:
    def __init__(self):
        self.recipes = {
            "Luck Potion": {"ingredients": ["herb", "herb", "herb"], "effect": "+1 to all rolls", "duration": 30},
            "Critical Brew": {"ingredients": ["herb", "gem", "mushroom"], "effect": "10% crit chance", "duration": 20},
            "XP Doubler": {"ingredients": ["gem", "gem", "herb"], "effect": "2x XP", "duration": 60}
        }
        self.available_ingredients = [
            "herb", "gem", "mushroom", "flower", "root"]

    def brew_potion(self, ingredients):
        for name, recipe in self.recipes.items():
            if sorted(ingredients) == sorted(recipe["ingredients"]):
                return {
                    "name": name,
                    "effect": recipe["effect"],
                    "duration": recipe["duration"],
                    "time_created": time.time()
                }
        return None


class Astrology:
    def __init__(self):
        self.events = {
            "Blood Moon": {"effect": "2x XP", "duration": 30, "color": (255, 0, 0)},
            "Mercury Retrograde": {"effect": "Inverted rolls", "duration": 60, "color": (100, 100, 100)},
            "Solar Eclipse": {"effect": "Automatic crits", "duration": 45, "color": GOLD},
            "Stellar Alignment": {"effect": "No XP penalty", "duration": 90, "color": BLUE}
        }
        self.active_event = None
        self.event_start_time = 0

    def update(self):
        # 0.1% chance per second to trigger an event (if none active)
        if self.active_event is None and random.random() < 0.001:
            self.active_event = random.choice(list(self.events.keys()))
            self.event_start_time = time.time()
        elif self.active_event and time.time() > self.event_start_time + self.events[self.active_event]["duration"]:
            self.active_event = None

    def get_active_effect(self):
        if self.active_event:
            return self.events[self.active_event]["effect"]
        return None


def draw_ascii_die(surface, die_type, x, y, color=WHITE):
    # Simple ASCII representations for each die
    die_art = {
        "d4": [" /\\ ", "/__\\", f" {random.randint(1, 4)} "],
        "d6": [" _____ ", "|     |", f"|  {random.randint(1, 6)}  |", " ‾‾‾‾‾ "],
        "d8": ["  /\\  ", " /  \\ ", f"/ {random.randint(1, 8):2} \\", " ‾‾‾‾ "],
        "d10": ["  /\\  ", " /  \\ ", f"| {random.randint(1, 10):2}|", " \\__/ "],
        "d12": [" /\\ ", "/  \\", f"|{random.randint(1, 12):2}|", "\\__/"],
        "d20": [" /\\ ", "/  \\", f"|{random.randint(1, 20):2}|", "\\__/"],
        "d100": [" ___ ", f"|{random.randint(1, 100):3}|", " ‾‾‾ "]
    }

    for i, line in enumerate(die_art.get(die_type, [die_type])):
        text = font.render(line, True, color)
        surface.blit(text, (x, y + i * 20))


def draw_xp_bar(surface, player, x=50, y=30, width=200, height=20):
    # Background
    pygame.draw.rect(surface, (50, 50, 50), (x, y, width, height))
    # Filled portion
    fill_width = int(width * (player.xp / player.xp_to_level))
    pygame.draw.rect(surface, GREEN, (x, y, fill_width, height))
    # Border and text
    border = font.render(f"LVL {player.level}: {
                         player.xp}/{player.xp_to_level}", True, WHITE)
    surface.blit(border, (x, y - 25))


def draw_dice_rolls(surface, rolls, x=400, y=100):
    title = font.render("Last Rolls:", True, WHITE)
    surface.blit(title, (x, y))

    for i, (die, roll) in enumerate(rolls):
        text = font.render(f"{die}: {roll}", True, GREEN)
        surface.blit(text, (x, y + 30 + i * 25))


def draw_unlocked_dice(surface, unlocked_dice, x=50, y=100):
    title = font.render("Your Dice:", True, WHITE)
    surface.blit(title, (x, y))

    for i, die in enumerate(unlocked_dice):
        draw_ascii_die(surface, die, x, y + 30 + i * 60))

            def draw_astrology_event(surface, astrology, x=400, y=400):
            if astrology.active_event:
        event = astrology.events[astrology.active_event]
        remaining = max(0, event["duration"] - (time.time() - astrology.event_start_time))

        # Event name
        name_text = font.render(f"Celestial Event: {astrology.active_event}", True, event["color"])
        surface.blit(name_text, (x, y))

        # Effect and timer
        effect_text = font.render(f"Effect: {event['effect']} ({int(remaining)}s)", True, WHITE)
        surface.blit(effect_text, (x, y + 25))

            def main():
    player = Player()
    alchemy = Alchemy()
    astrology = Astrology()
    running = True
    last_astrology_check = time.time()

            # Game state
    current_view = "main"  # 'main', 'alchemy'
    message_log = []
    last_roll_total = 0

            while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and current_view == "main":
                    rolls, total = player.roll_dice()
                    last_roll_total = total
                    message_log.append(f"Rolled {total} XP!")

                    # Check for new die unlock
                    new_die = None
                    if player.next_die_index < len(UNLOCK_LEVELS) and player.level >= UNLOCK_LEVELS[player.next_die_index]:
                        new_die = DICE_TYPES[player.next_die_index + 1]
                        player.unlocked_dice.append(new_die)
                        player.next_die_index += 1
                        message_log.append(f"✨ Unlocked {new_die}! ✨")

                elif event.key == pygame.K_a:
                    current_view = "alchemy" if current_view != "alchemy" else "main"
                elif event.key == pygame.K_ESCAPE:
                    current_view = "main"

        # Update systems
        if time.time() - last_astrology_check > 1:  # Check every second
            astrology.update()
            last_astrology_check = time.time()

        # Render
        screen.fill(BLACK)

        if current_view == "main":
            # Draw XP bar
            draw_xp_bar(screen, player)

            # Draw unlocked dice
            draw_unlocked_dice(screen, player.unlocked_dice)

            # Draw last rolls
            if player.last_rolls:
                draw_dice_rolls(screen, player.last_rolls)
                total_text = font.render(f"Total XP: {last_roll_total}", True, GOLD)
                screen.blit(total_text, (400, 300))

            # Draw astrology event
            draw_astrology_event(screen, astrology)

            # Draw instructions
            instructions = [
              "SPACE: Roll dice",
               "A: Alchemy Lab",
                f"Total Rolls: {player.total_rolls}"
            ]
            for i, line in enumerate(instructions):
                text = font.render(line, True, WHITE)
            screen.blit(text, (50, 500 + i * 25))

                elif current_view == "alchemy":
                # Draw alchemy screen
            title = font.render("Alchemy Lab", True, GOLD)
                screen.blit(title, (300, 50))

                # Draw recipes
                for i, (name, recipe) in enumerate(alchemy.recipes.items()):
                text = font.render(f"{i+1}. {name}: {recipe['ingredients']}", True, WHITE)
            screen.blit(text, (200, 100 + i * 30))

                # Draw player potions
            potions_title = font.render("Your Potions:", True, WHITE)
                screen.blit(potions_title, (200, 250))

                for i, potion in enumerate(player.potions):
                text = font.render(f"{i+1}. {potion['name']} ({potion['effect']})", True, GREEN)
            screen.blit(text, (200, 280 + i * 25))

                # Draw instructions
            back_text = font.render("ESC: Back to Main", True, WHITE)
                screen.blit(back_text, (50, 550))

                # Draw message log (last 3 messages)
                for i, message in enumerate(message_log[-3:]):
            text = font.render(message, True, WHITE)
                screen.blit(text, (50, 400 + i * 25))

                pygame.display.flip()
                clock.tick(60)

                if __name__ == "__main__":
                main()
