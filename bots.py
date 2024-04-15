import random

from typing import Generator
from inventory_items import Items, Helmet, LHandWeapon, RHandWeapon, Shoes, Shield, Ring


class Bot:
    """
    Represents a Bot character in a game that can fight, drop items, and be dynamically boosted based on the
    opponent's level.

    Attributes:
        _type (str): Identifier for the type of character, always set to 'bot'.
        __drop_item_probability (float): Probability that the bot will drop an item upon defeat, set to 95%.
    """
    _type: str = "bot"
    __drop_item_probability: float = 1 if random.random() <= 0.05 else 0  # 5% probability

    def __init__(self) -> None:
        """
        Initializes a Bot with a predefined set of items and base attributes.
        """
        self._inventory: list[Items] = [Helmet(), LHandWeapon(), RHandWeapon(), Shield(), Shoes(), Ring()]
        self._health: int = 300
        self._damage: int = 15
        self._level: str = "bot"

    def boost_bot(self, opponent_level: int) -> None:
        """
        Dynamically increases the bot's health and damage based on the opponent's level.

        Args:
            opponent_level (int): The level of the opponent, used to calculate the boost factor.
        """
        self._health += (opponent_level / 10 * self._health)
        self._damage += (opponent_level / 10 * self._damage)

    def drop_item(self) -> Items:
        """
        Randomly selects and returns an item from the bot's inventory based on the drop probability.

        Returns:
            Items | None: The item dropped by the bot, or None if no item is dropped.
        """
        if self.__drop_item_probability:
            item = random.choice(self._inventory)
            print(f"You picked up a new item: \n{item}.")
            return item

    def reduce_health(self, value: int) -> None:
        """
        Reduces the bot's health by a specified value.

        Args:
            value (int): The amount of health to reduce.
        """
        self._health -= value

    @property
    def attack(self) -> int:
        return self._damage

    @property
    def health(self) -> int:
        return self._health

    @property
    def level(self) -> str:
        return self._level

    @staticmethod
    def gen_bot() -> Generator:
        """
        Generates an infinite sequence of Bot instances.

        Yields:
            Generator: A generator yielding new instances of Bot indefinitely.
        """
        while True:
            yield Bot()


if __name__ == "__main__":
    ...
