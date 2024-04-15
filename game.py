from character import Character
from bots import Bot


class Game:
    """
    A game controller class that handles the interactions between two characters in a game setting.

    Attributes:
        character_1 (Character): The first character in the game.
        character_2 (Character): The second character in the game.
    """
    def __init__(self, character_1: Character, character_2: Character) -> None:
        """
        Initializes the game with two characters and sets up initial health, shield, and damage.

        Args:
            character_1 (Character): The first player's character.
            character_2 (Character): The second player's character.
        """
        self.character_1 = character_1
        self.character_2 = character_2
        self.__char_1_health = None
        self.__char_2_health = None
        self.__char_1_shield = None
        self.__char_2_shield = None
        self.__char_1_damage = None
        self.__char_2_damage = None

    def save_health_shield_damage(self) -> None:
        """
        Saves the current health, shield, and damage states of both characters.
        """
        self.__char_1_health = self.character_1.health
        self.__char_1_shield = self.character_1.shield
        self.__char_1_damage = self.character_1.damage

        self.__char_2_health = self.character_2.health
        self.__char_2_shield = self.character_2.shield
        self.__char_2_damage = self.character_2.damage

    def restore_health_shield(self) -> None:
        """
        Restores the health, shield, and damage states of both characters to the last saved state.
        """
        self.character_1.health = self.__char_1_health
        self.character_1.shield = self.__char_1_shield
        self.character_1.damage = self.__char_1_damage

        self.character_2.damage = self.__char_2_damage
        self.character_2.health = self.__char_2_health
        self.character_2.shield = self.__char_2_shield

    @staticmethod
    def forest_training(character: Character, bot: Bot) -> None:
        """
        Simulates a training session in a forest scenario where a character fights a bot.

        Args:
            character (Character): The player's character.
            bot (Character): The bot character used for training.
        """
        char_strike_damage = character.strike
        bot.boost_bot(character.level)
        bot_strike_damage = bot.attack

        if character.fatal_prop:
            char_strike_damage += character.fatal_damage

        if bot_strike_damage < character.shield:
            character.reduce_shield(bot_strike_damage)
        elif bot_strike_damage >= character.shield:
            bot_strike_damage -= character.shield
            character.shield_off()
            character.reduce_health(bot_strike_damage)

        bot.reduce_health(char_strike_damage)

    @staticmethod
    def forest_train_winner(character: Character, bot: Bot) -> None | str:
        """
        Determines the winner of a forest training session and updates experience and inventory accordingly.

        Args:
            character (Character): The player's character.
            bot (Character): The bot character used for training.

        Returns:
            None | str: A message indicating the result of the training session.
        """
        if character.health > 0 >= bot.health:
            character.experience_add(bot.level)
            character.level_up()

            prize = bot.drop_item()
            if prize:
                character.inventory.add_item(prize)
            print(f"Congrats! You kicked bot's ass!")
            return f"Congrats! You kicked bot's ass!"
        elif character.health <= 0 < bot.health:
            character.experience_drop()
            print("You lost to the bot. Loser.")
            return "You lost to the bot. Loser."
        elif character.health <= 0 >= bot.health:
            character.experience_drop()
            print("Both characters lost.")
            return "Both characters lost."

    def boost_char_damage(self) -> None:
        """
        Boosts _damage of the character based on the type advantage in matchups between character_1 and character_2.
        """
        char_1_type = self.character_1.type_char
        char_2_type = self.character_2.type_char

        if char_1_type == "warrior" and char_2_type == "mage":
            self.character_1.type_boost_damage()
        elif char_1_type == "mage" and char_2_type == "rogue":
            self.character_1.type_boost_damage()
        elif char_1_type == "rogue" and char_2_type == "paladin":
            self.character_1.type_boost_damage()
        elif char_1_type == "paladin" and char_2_type == "warrior":
            self.character_1.type_boost_damage()

        elif char_2_type == "warrior" and char_1_type == "mage":
            self.character_2.type_boost_damage()
        elif char_2_type == "mage" and char_1_type == "rogue":
            self.character_2.type_boost_damage()
        elif char_2_type == "rogue" and char_1_type == "paladin":
            self.character_2.type_boost_damage()
        elif char_2_type == "paladin" and char_1_type == "warrior":
            self.character_2.type_boost_damage()

    def check_winner(self) -> None | str:
        """
        Checks for a winner based on the health of the characters after a confrontation.

        Returns:
            None | str: A message indicating the winner or if both characters lost.
        """
        if self.character_1.health > 0 >= self.character_2.health:
            self.restore_health_shield()
            self.character_1.experience_add(self.character_2.level)
            self.character_1.level_up()
            self.character_1.level_dependent_boost()
            self.character_2.experience_drop()
            print(f"\nThe winner: \n{self.character_1}")
            return f"The winner: \n{self.character_1}"
        elif self.character_1.health <= 0 < self.character_2.health:
            self.restore_health_shield()
            self.character_2.experience_add(self.character_1.level)
            self.character_2.level_up()
            self.character_2.level_dependent_boost()
            self.character_1.experience_drop()
            print(f"\nThe winner: \n{self.character_2}")
            return f"The winner: \n{self.character_2}"
        elif self.character_1.health <= 0 >= self.character_2.health:
            self.restore_health_shield()
            self.character_2.experience_drop()
            self.character_1.experience_drop()
            print("\nBoth characters lost.\n")
            return "Both characters lost."

    def take_a_strike(self) -> None:
        """
        Processes the damage exchange between character_1 and character_2 during a fight.
        """
        char_1_strike_damage = self.character_1.strike
        char_2_strike_damage = self.character_2.strike

        if self.character_1.fatal_prop:
            char_1_strike_damage += self.character_1.fatal_damage
        if self.character_2.fatal_prop:
            char_2_strike_damage += self.character_2.fatal_damage

        if char_2_strike_damage < self.character_1.shield:
            self.character_1.reduce_shield(char_2_strike_damage)
        elif char_2_strike_damage >= self.character_1.shield:
            char_2_strike_damage -= self.character_1.shield
            self.character_1.shield_off()
            self.character_1.reduce_health(char_2_strike_damage)

        if char_1_strike_damage < self.character_2.shield:
            self.character_2.reduce_shield(char_1_strike_damage)
        elif char_1_strike_damage >= self.character_2.shield:
            char_1_strike_damage -= self.character_2.shield
            self.character_2.shield_off()
            self.character_2.reduce_health(char_1_strike_damage)


if __name__ == "__main__":
    ...
