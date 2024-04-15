import random
from inventory_items import Armory, Inventory, Items


class Character:
    """Base class for a character in the game.

    Attributes:
        _inventory (Inventory): Character's inventory.
        _armory (Armory): Character's armory.
        _name (str): Name of the character.
        _health (int): Health points of the character.
        _damage (int): Damage points the character can inflict.
        _shield (int): Shield points for damage absorption.
        _fatal_prop (float): Probability of causing fatal damage.
        _fatal_damage (int): Damage points when a fatal hit occurs.
        _experience (int): Current experience points.
        _level (int): Current level of the character.
    """
    _character_type: None | str = None

    def __init__(self):
        """Initializes a Character with default properties and empty inventory and armory."""

        self._inventory: Inventory = Inventory()
        self._armory: Armory = Armory()
        self._name: None | str = None
        self._health: None | int = None
        self._damage: None | int = None
        self._shield: None | int = None
        self._fatal_prop: None | float = None
        self._fatal_damage: None | int = None
        self._experience: int = 0
        self._level: int = 1

    def level_up(self) -> None:
        """Increases the character's level by 1 for every 100 experience points accumulated."""

        if self._experience >= 100:
            self._experience -= 100
            self._level += 1

    def experience_add(self, opponent_level: int | str) -> None:
        """Adds experience points based on the level of the opponent defeated.

                Args:
                    opponent_level (int): Level of the defeated opponent.
                """
        if opponent_level == "bot":
            self._experience += 4
            return
        self._experience += 20
        if opponent_level > self._level:
            level_diff = opponent_level - self._level
            self._experience += (level_diff / 10 * self._experience)

    def experience_drop(self) -> None:
        """Resets the experience points to zero."""
        self._experience = 0

    @property
    def name(self) -> str | None:
        return self._name

    @property
    def inventory(self) -> Inventory:
        return self._inventory

    @name.setter
    def name(self, name) -> None:
        self._name = name

    @property
    def fatal_prop(self) -> float | None:
        return self._fatal_prop

    @property
    def fatal_damage(self) -> int | None:
        return self._fatal_damage

    @property
    def level(self) -> int:
        return self._level

    @property
    def shield(self) -> int | None:
        return self._shield

    @property
    def type_char(self) -> str | None:
        return self._character_type

    @property
    def health(self) -> int | None:
        return self._health

    @property
    def damage(self) -> int | None:
        return self._damage

    @damage.setter
    def damage(self, value) -> None:
        self._damage = value

    @shield.setter
    def shield(self, value) -> None:
        self._shield = value

    @health.setter
    def health(self, value) -> None:
        self._health = value

    def shield_off(self) -> None:
        """Sets the shield value to zero."""
        self._shield = 0

    def type_boost_damage(self) -> None:
        """Increases the damage by 15%."""
        self._damage *= 1.15

    def reduce_shield(self, value: int) -> None:
        """Reduces the shield by a given value."""
        self._shield -= value

    def reduce_health(self, value: int) -> None:
        """Reduces the health by a given value."""
        self._health -= value

    @property
    def strike(self) -> int | None:
        return self._damage

    def level_dependent_boost(self) -> None:
        """Boosts health, shield, and damage based on the character's level."""
        self._health += (self._level/100 * self._health)
        self._shield += (self._level/100 * self._shield)
        self._damage += (self._level/100 * self._damage)

    def __count_attack_put_on(self, item: Items) -> None:
        """Boosts character stats based on the item equipped."""
        self._health *= item.boost_health
        self._shield *= item.boost_shield
        self._damage *= item.boost_damage

    def __count_attack_take_off(self, item: Items) -> None:
        """Reduces character stats based on the item unequipped."""
        self._health /= item.boost_health
        self._shield /= item.boost_shield
        self._damage /= item.boost_damage

    def check_inventory(self) -> None:
        """Allows the character to equip items from the inventory."""
        while True:
            list_of_items_to_use = [item for item in self._inventory.inventory if not item.is_on]
            result = "\n".join([f"{index + 1}. {item}" for index, item in enumerate(list_of_items_to_use)])
            print(f"{self._name}, check out your inventory:\n", result)
            index = input("\nIf you want to put something on - choose index. Else type 'n': ")
            if index.isdigit():
                try:
                    self._armory.set_item(list_of_items_to_use[int(index) - 1])
                except IndexError:
                    print("Incorrect index.")
                    continue
                self.__count_attack_put_on(list_of_items_to_use[int(index) - 1])
            else:
                return

    def check_armory(self) -> None:
        """Allows the character to unequip items from the armory."""
        while True:
            list_of_items_on = [item for item in self._armory.list_items.values() if item]
            result = "\n".join([f"{index + 1}. {item}" for index, item in enumerate(list_of_items_on)])
            print(f"{self._name}, check out your armory:\n", result)
            index = input("\nIf you want to take something off - choose index. Else type 'n': ")
            if index.isdigit():
                try:
                    self._armory.take_off_item(list_of_items_on[int(index) - 1])
                except IndexError:
                    print("Incorrect index.")
                    continue
                self.__count_attack_take_off(list_of_items_on[int(index) - 1])
            else:
                return


class Warrior(Character):
    """
    Represents a Warrior character with enhanced attributes.

    Inherits from Character class and specializes it with higher base health, damage, and special fatality chances.

    Attributes:
        _character_type (str): A string denoting the type of character ('warrior').
        __base_damage (int): Base damage capability of the Warrior.
        __base_shield (int): Base shield capacity of the Warrior.
        __base_health (int): Base health points of the Warrior.
        __fatality_probability (float): Probability of causing a fatal strike.
        __fatality_damage (int): Additional damage points if a fatal strike occurs.
    """
    _character_type = "warrior"
    __base_damage = 120
    __base_shield = 200
    __base_health = 1200
    __fatality_probability = 1 if random.random() <= 0.1 else 0  # 10% probability
    __fatality_damage = 400

    def __init__(self) -> None:
        """Initializes the Warrior with predefined base stats and fatality settings."""

        super().__init__()
        self._health = Warrior.__base_health
        self._damage = Warrior.__base_damage
        self._shield = Warrior.__base_shield
        self._fatal_prop = Warrior.__fatality_probability
        self._fatal_damage = Warrior.__fatality_damage

    def __str__(self) -> str:
        return (f"Warrior \nName: {self._name} \nLevel: {self._level} \nHealth: {self._health}"
                f"\nShield: {self._shield} \nDamage: {self._damage} \nFatality: {self.__fatality_damage}"
                f"\nExperience: {self._experience}")


class Mage(Character):
    """
    Represents a Mage character with magic-based attributes.

    Inherits from Character class and specializes it with magical damage abilities and lower health and shield.

    Attributes:
        _character_type (str): A string denoting the type of character ('mage').
        __base_damage (int): Base magic damage capability of the Mage.
        __base_shield (int): Base magic shield capacity of the Mage.
        __base_health (int): Base health points of the Mage.
        __fatality_probability (float): Higher probability of magical fatality.
        __fatality_damage (int): Magical damage points if a fatal strike occurs.
    """
    _character_type = "mage"
    __base_damage = 130
    __base_shield = 150
    __base_health = 800
    __fatality_probability = 1 if random.random() <= 0.15 else 0  # 15% probability
    __fatality_damage = 250

    def __init__(self) -> None:
        """Initializes the Mage with specific magical attributes and fatality settings."""

        super().__init__()
        self._health = Mage.__base_health
        self._damage = Mage.__base_damage
        self._shield = Mage.__base_shield
        self._fatal_prop = Mage.__fatality_probability
        self._fatal_damage = Mage.__fatality_damage

    def __str__(self) -> str:
        return (f"Mage \nName: {self._name} \nLevel: {self._level} \nHealth: {self._health}"
                f"\nShield: {self._shield} \nDamage: {self._damage} \nFatality: {self.__fatality_damage}"
                f"\nExperience: {self._experience}")


class Rogue(Character):
    """
    Represents a Rogue character known for stealth and quick attacks.

    Inherits from Character class and specializes it with quick damage abilities and moderate health.

    Attributes:
        _character_type (str): A string denoting the type of character ('rogue').
        __base_damage (int): Base quick attack damage capability of the Rogue.
        __base_shield (int): Base agility-based shield capacity of the Rogue.
        __base_health (int): Base health points of the Rogue.
        __fatality_probability (float): High probability of stealth-based fatality.
        __fatality_damage (int): Damage points if a stealth fatal strike occurs.
    """
    _character_type = "rogue"
    __base_damage = 110
    __base_shield = 100
    __base_health = 1000
    __fatality_probability = 1 if random.random() <= 0.2 else 0  # 20% probability
    __fatality_damage = 200

    def __init__(self) -> None:
        """Initializes the Rogue with agility-based attributes and high stealth fatality settings."""

        super().__init__()
        self._health = Rogue.__base_health
        self._damage = Rogue.__base_damage
        self._shield = Rogue.__base_shield
        self._fatal_prop = Rogue.__fatality_probability
        self._fatal_damage = Rogue.__fatality_damage

    def __str__(self) -> str:
        return (f"Rogue \nName: {self._name} \nLevel: {self._level} \nHealth: {self._health}"
                f"\nShield: {self._shield} \nDamage: {self._damage} \nFatality: {self.__fatality_damage}"
                f"\nExperience: {self._experience}")


class Paladin(Character):
    """
        Represents a Paladin character with a balance of defense and offense.

        Inherits from Character class and specializes it with balanced attributes in health, shield, and damage.

        Attributes:
            _character_type (str): A string denoting the type of character ('paladin').
            __base_damage (int): Base damage capability of the Paladin.
            __base_shield (int): Base shield capacity of the Paladin.
            __base_health (int): Base health points of the Paladin.
            __fatality_probability (float): Moderate probability of causing a divine strike.
            __fatality_damage (int): Divine damage points if a fatal strike occurs.
        """
    _character_type = "paladin"
    __base_damage = 115
    __base_shield = 180
    __base_health = 1100
    __fatality_probability = 1 if random.random() <= 0.12 else 0  # 12% probability
    __fatality_damage = 350

    def __init__(self) -> None:
        """Initializes the Paladin with divine attributes and balanced fatality settings."""

        super().__init__()
        self._health = Paladin.__base_health
        self._damage = Paladin.__base_damage
        self._shield = Paladin.__base_shield
        self._fatal_prop = Paladin.__fatality_probability
        self._fatal_damage = Paladin.__fatality_damage

    def __str__(self) -> str:
        return (f"Paladin \nName: {self._name} \nLevel: {self._level} \nHealth: {self._health}"
                f"\nShield: {self._shield} \nDamage: {self._damage} \nFatality: {self.__fatality_damage}"
                f"\nExperience: {self._experience}")


if __name__ == "__main__":
    ...
