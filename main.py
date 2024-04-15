import pickle

from character import Character, Warrior, Mage, Rogue, Paladin
from bots import Bot
from inventory_items import Helmet, LHandWeapon, RHandWeapon, Shoes, Shield, Ring
from game import Game

players = dict()
file_name: str = 'players.pkl'


def open_file() -> None:
    """Open and load the player's data file if it exists."""
    global players
    try:
        with open(file_name, 'rb') as file:
            players = pickle.load(file)
    except FileNotFoundError:
        print("Creating a new file...")


def save_file() -> None:
    """Save the current state of players' data to a file."""
    with open(file_name, 'wb') as file:
        pickle.dump(players, file)


def choose_characters(name) -> Character:
    """
    Allows a user to choose a character type and equips them with default equipment.

    Args:
        name (str): The name of the player choosing the character.

    Returns:
        Character: The character chosen by the player, fully equipped.
    """
    characters = Warrior(), Paladin(), Mage(), Rogue()
    equipment = {
        'helmet': Helmet(),
        'sword': LHandWeapon(),
        'axe': RHandWeapon(),
        'shield': Shield(),
        'shoes': Shoes(),
        'ring': Ring()
    }
    result = "\n".join([f"{i + 1}: {k.type_char}" for i, k in enumerate(characters)])
    print(result)
    while True:
        index = input(f"{name}, choose a type for your character. Enter an index: ")
        try:
            player = characters[int(index) - 1]
            break
        except (ValueError, IndexError):
            print("Incorrect index. Try again.")
    player.name = name
    for item in equipment.values():
        player.inventory.add_item(item)
    return player


def forest_training(player, game) -> None:
    """
    Manages a training session in the forest, where the player fights against a bot.

    Args:
        player (Character): The player's character who is training.
        game (Game): The game session where the training occurs.
    """
    go_forest = input(f"{player.name}, do you want to train in the forest? y/n ")
    if go_forest == "y":
        while True:
            new_bot = next(Bot.gen_bot())
            while True:
                game.forest_training(player, new_bot)
                if game.forest_train_winner(player, new_bot):
                    break
            cont = input("Do you want to continue: y/n ")
            if cont == "n":
                break


def main() -> None:
    """
    Main function to handle game setup, play, and teardown.
    """
    while True:
        open_file()
        player1_name = input("Player1, your character's name: ")
        if not players.get(player1_name):
            player1 = choose_characters(player1_name)
            players[player1.name] = player1
        player1 = players[player1_name]

        player2_name = input("Player2, your character's name: ")
        if not players.get(player2_name):
            player2 = choose_characters(player2_name)
            players[player2.name] = player2
        player2 = players[player2_name]

        player1.check_inventory()
        player1.check_armory()

        player2.check_inventory()
        player2.check_armory()

        new_game = Game(player1, player2)
        new_game.save_health_shield_damage()

        forest_training(player1, new_game)
        forest_training(player2, new_game)

        new_game.restore_health_shield()
        new_game.boost_char_damage()

        while True:

            new_game.take_a_strike()
            if new_game.check_winner():
                break

        save_file()
        another_round = input("One more fight? y/n ")
        if another_round == "n":
            break


if __name__ == "__main__":
    main()
