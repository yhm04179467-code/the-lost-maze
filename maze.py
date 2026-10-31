import random


LEVELS = [
    [
        "###############",
        "#P    #      E#",
        "# ### # ##### #",
        "#   # #     # #",
        "### # ##### # #",
        "# K #       # #",
        "# ### ##### # #",
        "#   T   $   # #",
        "# ######### # #",
        "#             #",
        "###############",
    ],
    [
        "#################",
        "#P      #      E#",
        "# ##### # ##### #",
        "#   #   #     # #",
        "### # ##### # # #",
        "#   #   K   # # #",
        "# ##### ### # # #",
        "#   T   #   #   #",
        "# ### ### ##### #",
        "# $             #",
        "#################",
    ],
    [
        "###################",
        "#P      #        E#",
        "# ##### # ####### #",
        "#     # #       # #",
        "##### # ##### # # #",
        "#   K #     # # # #",
        "# ####### # # # # #",
        "#     T   #   #   #",
        "# ### ##### ##### #",
        "#   $             #",
        "###################",
    ]
]


class Player:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.health = 10
        self.score = 0
        self.steps = 0
        self.has_key = False

    def reset_for_level(self):
        self.has_key = False


def create_level(level_number):
    maze = []

    for row in LEVELS[level_number]:
        maze.append(list(row))

    return maze


def find_player(maze):
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == "P":
                maze[row][col] = " "
                return row, col


def print_maze(maze, player, level_number):
    print()
    print("=" * 35)
    print("LEVEL", level_number + 1)
    print("=" * 35)

    for row in range(len(maze)):
        line = ""

        for col in range(len(maze[row])):
            if row == player.row and col == player.col:
                line += "P"
            else:
                line += maze[row][col]

        print(line)

    print()
    print("Health:", player.health)
    print("Score:", player.score)
    print("Steps:", player.steps)

    if player.has_key:
        print("Key: Yes")
    else:
        print("Key: No")


def show_instructions():
    print()
    print("=" * 35)
    print("HOW TO PLAY")
    print("=" * 35)

    print("W = move up")
    print("S = move down")
    print("A = move left")
    print("D = move right")
    print("Q = quit game")

    print()

    print("P = player")
    print("# = wall")
    print("K = key")
    print("T = trap")
    print("$ = treasure")
    print("E = exit")

    print()
    print("Goal:")
    print("Find the key and reach the exit.")
    print("Complete all levels to win.")
    print("Avoid traps and collect treasure for points.")


def move_player(maze, player, command):
    new_row = player.row
    new_col = player.col

    if command == "w":
        new_row -= 1

    elif command == "s":
        new_row += 1

    elif command == "a":
        new_col -= 1

    elif command == "d":
        new_col += 1

    else:
        print("Invalid command.")
        return False

    if maze[new_row][new_col] == "#":
        print("You hit a wall!")
        return False

    player.row = new_row
    player.col = new_col
    player.steps += 1

    return True


def check_tile(maze, player):
    tile = maze[player.row][player.col]

    if tile == "K":
        player.has_key = True
        player.score += 10

        maze[player.row][player.col] = " "

        print("You found the key!")
        print("+10 points")

    elif tile == "$":
        player.score += 20

        maze[player.row][player.col] = " "

        print("You found treasure!")
        print("+20 points")

    elif tile == "T":
        damage = random.randint(1, 3)
        player.health -= damage

        maze[player.row][player.col] = " "

        print("You stepped on a trap!")
        print("You lost", damage, "health.")

    elif tile == "E":
        if player.has_key:
            player.score += 30

            print("You unlocked the exit!")
            print("+30 points")

            return "next"

        else:
            print("The exit is locked.")
            print("You need to find the key first.")

    if player.health <= 0:
        return "dead"

    return "continue"


def save_result(result, player):
    try:
        file = open("maze_history.txt", "a")

        file.write(
            result
            + " | Score: "
            + str(player.score)
            + " | Steps: "
            + str(player.steps)
            + " | Health: "
            + str(player.health)
            + "\n"
        )

        file.close()

    except OSError:
        print("The result could not be saved.")


def show_history():
    print()
    print("=" * 35)
    print("GAME HISTORY")
    print("=" * 35)

    try:
        file = open("maze_history.txt", "r")
        content = file.read()
        file.close()

        if content == "":
            print("No games have been recorded yet.")
        else:
            print(content)

    except FileNotFoundError:
        print("No games have been recorded yet.")


def play_game():
    player = Player()

    print()
    print("=" * 35)
    print("         THE LOST MAZE")
    print("=" * 35)
    print("Escape all levels to win!")

    for level_number in range(len(LEVELS)):
        maze = create_level(level_number)

        start_row, start_col = find_player(maze)

        player.row = start_row
        player.col = start_col
        player.reset_for_level()

        while True:
            print_maze(maze, player, level_number)

            command = input(
                "\nMove (w/a/s/d, q to quit): "
            ).lower().strip()

            if command == "q":
                print()
                print("You left the maze.")

                save_result("QUIT", player)

                return

            moved = move_player(
                maze,
                player,
                command
            )

            if not moved:
                continue

            result = check_tile(
                maze,
                player
            )

            if result == "dead":
                print_maze(
                    maze,
                    player,
                    level_number
                )

                print()
                print("=" * 35)
                print("            GAME OVER")
                print("=" * 35)

                print("You ran out of health.")
                print("Final score:", player.score)
                print("Total steps:", player.steps)

                save_result(
                    "LOSE",
                    player
                )

                return

            if result == "next":
                print()
                print(
                    "Level",
                    level_number + 1,
                    "complete!"
                )

                if level_number < len(LEVELS) - 1:
                    print("Moving to the next level...")

                break

    health_bonus = player.health * 5
    player.score += health_bonus

    print()
    print("=" * 35)
    print("             YOU WIN!")
    print("=" * 35)

    print("You escaped the entire maze.")
    print("Health bonus:", health_bonus)
    print("Final score:", player.score)
    print("Total steps:", player.steps)

    save_result(
        "WIN",
        player
    )


def main():
    while True:
        print()
        print("=" * 35)
        print("         THE LOST MAZE")
        print("=" * 35)

        print("1. Start Game")
        print("2. Instructions")
        print("3. Game History")
        print("4. Exit")

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice == "1":
            play_game()

        elif choice == "2":
            show_instructions()

        elif choice == "3":
            show_history()

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Please enter 1, 2, 3 or 4.")


main()
