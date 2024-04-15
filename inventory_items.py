class Items:
    """
    Base class for items in a game, defining common attributes and methods for all items.

    Attributes:
        _item_type (str): Specifies the type of item.
    """
    _item_type = None

    def __init__(self, name=None, boost_damage=None, boost_health=None, boost_shield=None) -> None:
        """
        Initializes an item with optional enhancements.

        Args:
            name (str): The name of the item.
            boost_damage (float): Damage enhancement factor.
            boost_health (float): Health enhancement factor.
            boost_shield (float): Shield enhancement factor.
        """
        self._boost_damage = boost_damage
        self._boost_health = boost_health
        self._boost_shield = boost_shield
        self._name = name
        self._is_on = False

    def __str__(self) -> str:
        """
        Returns a string representation of the item showing its type, name, and enhancements.
        """
        return (f"Type: {self._item_type} \nName: {self._name} \nBoost damage: {self._boost_damage},"
                f"boost health: {self._boost_health}, boost shield: {self._boost_shield}.")

    @property
    def boost_damage(self) -> None | float:
        return self._boost_damage

    @property
    def boost_shield(self) -> None | float:
        return self._boost_shield

    @property
    def boost_health(self) -> None | float:
        return self._boost_health

    @property
    def item_name(self) -> None | str:
        return self._name

    @classmethod
    def get_item_type(cls) -> None | str:
        return cls._item_type

    @property
    def is_on(self) -> bool:
        """Checks if the item is currently equipped."""
        return self._is_on

    def is_off(self) -> None:
        """Sets the item to unequipped state."""
        self._is_on = False


class Helmet(Items):
    """Represents a helmet with specific enhancements."""
    _item_type = "helmet"

    def __init__(self, name="Usual helmet", boost_damage=1.0, boost_health=1.0, boost_shield=1.2) -> None:
        super().__init__(name, boost_damage, boost_health, boost_shield)


class LHandWeapon(Items):
    """Represents a left-hand weapon with specific enhancements."""
    _item_type = "l_hand_weapon"

    def __init__(self, name="Simple left hand sword", boost_damage=1.2, boost_health=1.0, boost_shield=0.9) -> None:
        super().__init__(name, boost_damage, boost_health, boost_shield)


class RHandWeapon(Items):
    """Represents a right-hand weapon with specific enhancements."""
    _item_type = "r_hand_weapon"

    def __init__(self, name="Simple right hand axe", boost_damage=1.25, boost_health=1.0, boost_shield=0.85) -> None:
        super().__init__(name, boost_damage, boost_health, boost_shield)


class Shield(Items):
    """Represents a shield with specific enhancements."""
    _item_type = "shield"

    def __init__(self, name="Metal shield", boost_damage=1.05, boost_health=1.0, boost_shield=1.3) -> None:
        super().__init__(name, boost_damage, boost_health, boost_shield)


class Shoes(Items):
    """Represents shoes with specific enhancements."""
    _item_type = "shoes"

    def __init__(self, name="Leather shoes", boost_damage=1.05, boost_health=1.1, boost_shield=1.05) -> None:
        super().__init__(name, boost_damage, boost_health, boost_shield)


class Ring(Items):
    """Represents a ring with specific magical enhancements."""
    _item_type = "ring"

    def __init__(self, name="Ring of Sun", boost_damage=1.1, boost_health=1.2, boost_shield=0.9) -> None:
        super().__init__(name, boost_damage, boost_health, boost_shield)


class Inventory:
    """
    Represents a collection of items, typically held by a character or within a storage.
    """
    def __init__(self) -> None:
        """Initializes an empty inventory."""
        self.__items = list()

    def add_item(self, *args) -> None:
        """Adds items to the inventory."""
        for item in args:
            self.__items.append(item)

    def remove_item(self, item) -> None:
        """Removes an item from the inventory."""
        self.__items.remove(item)

    @property
    def inventory(self) -> list:
        return self.__items


class Armory:
    """
    Represents a set of equipped items, with logic to manage conflicts between item types.
    """
    def __init__(self) -> None:
        """Initializes an armory with placeholders for each type of item."""

        self._items_on = {
            "helmet": None,
            "l_hand_weapon": None,
            "r_hand_weapon": None,
            "shield": None,
            "shoes": None,
            "ring": None
        }

    @property
    def list_items(self) -> dict[str, None | Items]:
        return self._items_on

    def set_item(self, item: Items) -> None | str:
        """
        Equips an item, respecting rules about item conflicts (e.g., shields and weapons).

        Args:
            item (Items): The item to equip.

        Returns:
            str | None: A message if there is a conflict, or None if successful.
        """

        if item.get_item_type() == "shield" and self._items_on["l_hand_weapon"]:
            print("You can't hold shield. Take off left hand weapon first.")
            return "You can't hold shield. Take off left hand weapon first."

        elif item.get_item_type() == "l_hand_weapon" and self._items_on["shield"]:
            print("You can't hold left hand weapon. Take off shield first.")
            return "You can't hold left hand weapon. Take off shield first."

        if not self._items_on.get(item.get_item_type()):
            item._is_on = True
            self._items_on[item.get_item_type()] = item

    def take_off_item(self, item: Items) -> None:
        """
        Removes an item from being equipped, setting it to the unequipped state.

        Args:
            item (Items): The item to unequip.
        """
        self._items_on[item.get_item_type()].is_off()
        self._items_on[item.get_item_type()] = None


if __name__ == "__main__":
    ...
