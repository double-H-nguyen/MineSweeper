import re
from board import Board


# Step 1: create the board and plant the bombs
# Step 2: show the user the board and ask for where they want to dig
# Step 3b: if location is not a bomb, dig recursively until each square is at least next to a bomb
# Step 3a: if location is a bomb, show game over message
# Step 4: repeat steps 2 and 3a/b until there are no more places to dig, player wins!

# play the game
def play(dim_size=10, num_bombs=10):
    board = Board(dim_size, num_bombs)  # create bomb and plant bombs

    safe = True  # tells the game if we dug a bomb or not

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)  # show user board

        # use regex to take multiple values between each comma
        # split function return a list of values based on the regex
        # handles '0,0' or '0,  0' or '  0  , 0   '
        user_input = re.split(',(\\s)*', input('Where do you want to dig? Input as "row,column": '))

        # sometimes split function may contain white space in the middle, so ensure you grab the values you want
        row, col = int(user_input[0]), int(user_input[-1])

        # make sure user's input is valid
        if row < 0 or row >= board.dim_size or col < 0 or col > board.dim_size:
            print("Invalid location. Try again.")
            continue

        # dig
        # True = did not find a bomb
        # False = found a bomb
        safe = board.dig(row, col)  # dig function is recursive

        if not safe:  # dug a bomb
            break

    if safe:
        print('Congratulation!')
    else:  # game over
        print('Game over :(')
        # reveal the whole board by digging through every possible spot
        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)


if __name__ == '__main__':
    play()
