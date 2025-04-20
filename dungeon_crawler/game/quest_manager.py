import random
from enum import Enum

class QuestType(Enum):
    """Quest type enumeration"""
    KILL = 0
    COLLECT = 1
    EXPLORE = 2
    BOSS = 3

class Quest:
    """Quest definition with objectives and rewards"""
    
    def __init__(self, name, description, objective, reward):
        self.name = name
        self.description = description
        self.objective = objective  # Dict with type, count, target
        self.reward = reward  # Dict with gold, xp, items
        self.progress = 0
        self.completed = False
        
    def update_progress(self, amount=1):
        """Update quest progress"""
        if self.completed:
            return False
            
        self.progress += amount
        if self.progress >= self.objective.get("count", 0):
            self.completed = True
            return True
        return False
        
    def is_complete(self):
        """Check if quest is complete"""
        return self.completed
        
    def get_progress_text(self):
        """Get quest progress text"""
        count = self.objective.get("count", 0)
        if count == 0:
            return "Completed" if self.completed else "In progress"
        return f"{self.progress}/{count}"
        
    def get_reward_text(self):
        """Get formatted reward text"""
        reward_text = []
        if "gold" in self.reward and self.reward["gold"] > 0:
            reward_text.append(f"{self.reward['gold']} gold")
        if "xp" in self.reward and self.reward["xp"] > 0:
            reward_text.append(f"{self.reward['xp']} XP")
        if "items" in self.reward and self.reward["items"]:
            for item in self.reward["items"]:
                reward_text.append(item)
        return ", ".join(reward_text) if reward_text else "None"

class QuestManager:
    """Manager for all player quests"""
    
    def __init__(self):
        self.active_quest = None
        self.completed_quests = []
        self.available_quests = []
        self.quest_pool = []  # Template quests to generate from
        self.initialize_quest_pool()
        
    def initialize_quest_pool(self):
        """Initialize pool of quest templates"""
        # Kill quests
        self.quest_pool.extend([
            {
                "type": QuestType.KILL,
                "name_template": "Exterminate the {target}s",
                "desc_template": "Kill {count} {target}s to secure the area.",
                "target_options": ["goblin", "skeleton", "orc", "lynx", "frost_troll", "magma_elemental", "shadow_wraith"],
                "count_range": (5, 15),
                "reward_gold_range": (50, 200),
                "reward_xp_range": (100, 300)
            },
            {
                "type": QuestType.KILL,
                "name_template": "Hunt: {target} Threat",
                "desc_template": "A group of {target}s is causing trouble. Eliminate {count} of them.",
                "target_options": ["goblin", "skeleton", "orc", "lynx", "frost_troll", "magma_elemental", "shadow_wraith"],
                "count_range": (3, 10),
                "reward_gold_range": (75, 250),
                "reward_xp_range": (150, 350)
            }
        ])
        
        # Collect quests
        self.quest_pool.extend([
            {
                "type": QuestType.COLLECT,
                "name_template": "Recover the Lost {target}",
                "desc_template": "Find and retrieve the {target} hidden in this dungeon.",
                "target_options": ["ancient coin", "mysterious artifact", "enchanted gem", "lost relic", "ancient scroll"],
                "count_range": (1, 1),
                "reward_gold_range": (100, 300),
                "reward_xp_range": (200, 400)
            },
            {
                "type": QuestType.COLLECT,
                "name_template": "Gather {target}s",
                "desc_template": "Collect {count} {target}s from the dungeon depths.",
                "target_options": ["magic crystal", "rare herb", "monster essence", "ancient rune"],
                "count_range": (3, 8),
                "reward_gold_range": (80, 220),
                "reward_xp_range": (120, 320)
            }
        ])
        
        # Explore quests
        self.quest_pool.extend([
            {
                "type": QuestType.EXPLORE,
                "name_template": "Map the Unknown",
                "desc_template": "Explore {count} unexplored rooms in the dungeon.",
                "target_options": ["room"],
                "count_range": (5, 10),
                "reward_gold_range": (40, 150),
                "reward_xp_range": (80, 250)
            }
        ])
        
        # Boss quests
        self.quest_pool.extend([
            {
                "type": QuestType.BOSS,
                "name_template": "Defeat the {target}",
                "desc_template": "A powerful {target} lurks in the depths. Defeat it to earn great rewards.",
                "target_options": ["Dungeon Boss", "Ancient Guardian", "Corrupted Warlord", "Elemental Lord"],
                "count_range": (1, 1),
                "reward_gold_range": (300, 600),
                "reward_xp_range": (500, 1000)
            }
        ])
        
    def generate_quest(self, dungeon_level=1, biome=None):
        """Generate a new quest based on dungeon level and biome"""
        if not self.quest_pool:
            self.initialize_quest_pool()
            
        # Choose a quest type based on level
        if dungeon_level % 5 == 0:
            # Every 5th level is a boss level
            quest_type = QuestType.BOSS
        else:
            types = [QuestType.KILL, QuestType.COLLECT, QuestType.EXPLORE]
            weights = [0.6, 0.3, 0.1]  # Adjust probability
            quest_type = random.choices(types, weights=weights, k=1)[0]
            
        # Filter quest templates by chosen type
        templates = [q for q in self.quest_pool if q["type"] == quest_type]
        if not templates:
            # Fallback to any template if no matches
            templates = self.quest_pool
            
        # Choose a template
        template = random.choice(templates)
        
        # Determine target based on biome if applicable
        if biome and quest_type == QuestType.KILL:
            biome_enemies = {
                "CAVERN": ["goblin", "skeleton", "orc"],
                "FOREST": ["lynx", "goblin", "orc"],
                "ICE": ["frost_troll", "skeleton", "lynx"],
                "LAVA": ["magma_elemental", "orc", "frost_troll"],
                "SHADOW": ["shadow_wraith", "skeleton", "magma_elemental"]
            }
            biome_name = biome.name if hasattr(biome, 'name') else str(biome)
            target_options = biome_enemies.get(biome_name, template["target_options"])
        else:
            target_options = template["target_options"]
            
        # Select target and count
        target = random.choice(target_options)
        count = random.randint(*template["count_range"])
        
        # Scale rewards based on level
        level_multiplier = 1 + (dungeon_level - 1) * 0.2
        gold = int(random.randint(*template["reward_gold_range"]) * level_multiplier)
        xp = int(random.randint(*template["reward_xp_range"]) * level_multiplier)
        
        # Create quest name and description
        name = template["name_template"].format(target=target.capitalize(), count=count)
        description = template["desc_template"].format(target=target, count=count)
        
        # Create quest object
        quest = Quest(
            name=name,
            description=description,
            objective={"type": template["type"], "count": count, "target": target},
            reward={"gold": gold, "xp": xp}
        )
        
        return quest
        
    def add_available_quest(self, quest):
        """Add a quest to available quests"""
        self.available_quests.append(quest)
        
    def accept_quest(self, quest_index=0):
        """Accept a quest from available quests"""
        if not self.available_quests:
            return False
            
        if 0 <= quest_index < len(self.available_quests):
            if self.active_quest:
                # Can only have one active quest at a time
                self.abandon_quest()
                
            self.active_quest = self.available_quests.pop(quest_index)
            return True
        return False
        
    def abandon_quest(self):
        """Abandon the active quest"""
        if self.active_quest:
            # Put active quest back in available quests
            self.available_quests.append(self.active_quest)
            self.active_quest = None
            return True
        return False
        
    def complete_quest(self):
        """Complete the active quest and get rewards"""
        if not self.active_quest or not self.active_quest.completed:
            return None
            
        rewards = self.active_quest.reward
        self.completed_quests.append(self.active_quest)
        self.active_quest = None
        return rewards
        
    def update_quest(self, player, dungeon):
        """Update quest progress based on game state"""
        if not self.active_quest:
            # Generate a new quest if we don't have one
            if random.random() < 0.5:  # 50% chance to get a new quest
                self.active_quest = self.generate_quest(dungeon.level, dungeon.biome)
            return None
            
        quest_type = self.active_quest.objective["type"]
        target = self.active_quest.objective["target"]
        
        # Update quest progress based on type
        if quest_type == QuestType.KILL or quest_type == QuestType.KILL.value:
            # Count dead enemies of the target type
            progress = sum(1 for enemy in dungeon.enemies if 
                         enemy.enemy_type == target and not enemy.alive)
            
            # Set progress directly rather than incrementing
            old_progress = self.active_quest.progress
            self.active_quest.progress = progress
            
            # Check if quest was just completed
            if old_progress < self.active_quest.objective["count"] and progress >= self.active_quest.objective["count"]:
                self.active_quest.completed = True
                return self.active_quest.reward
                
        elif quest_type == QuestType.COLLECT or quest_type == QuestType.COLLECT.value:
            # Check if player has collected the target item
            for item in player.inventory:
                if target in item.description.lower():
                    self.active_quest.update_progress()
                    player.inventory.remove(item)
                    return self.active_quest.reward if self.active_quest.completed else None
                    
        elif quest_type == QuestType.EXPLORE or quest_type == QuestType.EXPLORE.value:
            # Count explored rooms
            explored_count = sum(1 for room in dungeon.rooms if 
                               all(dungeon.grid[y][x].explored 
                                   for y in range(room.y, room.y + room.height)
                                   for x in range(room.x, room.x + room.width)))
                                   
            # Set progress directly
            old_progress = self.active_quest.progress
            self.active_quest.progress = explored_count
            
            # Check if quest was just completed
            if old_progress < self.active_quest.objective["count"] and explored_count >= self.active_quest.objective["count"]:
                self.active_quest.completed = True
                return self.active_quest.reward
                
        elif quest_type == QuestType.BOSS or quest_type == QuestType.BOSS.value:
            # Boss quests typically completed by defeating a special enemy
            for enemy in dungeon.enemies:
                if "boss" in enemy.enemy_type.lower() and not enemy.alive:
                    self.active_quest.update_progress()
                    return self.active_quest.reward if self.active_quest.completed else None
                    
        return None 