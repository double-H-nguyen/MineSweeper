import random


class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # create the board using helper function
        self.board = self.make_new_board()  # plant the bomb
        self.assign_values_to_board()

        # initialize a set to keep track of which locations we've uncovered
        # save (rol,col) tuples into this set
        self.dug = set()  # if we dig at 0,0 then self.dug = {(0,0)}

    def make_new_board(self):
        # construct a new board based on dim size and num bombs
        # construct the list of lists

        # generate a new board
        # board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)] # fancy way
        board = []
        for _ in range(self.dim_size):  # first for-loop create x-axis
            lst = []
            for _ in range(self.dim_size):  # second for-loop create y-axis
                lst.append(None)
            board.append(lst)

        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size ** 2 - 1)  # 0-99
            row = loc // self.dim_size  # row = tenth digit value
            col = loc % self.dim_size  # col = single digit value

            # check if bomb is planted already
            if board[row][col] == '*':
                continue  # bomb is already planted, don't increment bombs_planted

            board[row][col] = '*'  # plant the bomb
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        # assign a number 0-8 for all empty spaces, which represents how many neighboring bombs there are
        # precompute these and it'll save us some effort checking what's around the board later on
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # if this spot is a bomb, skip
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        # iterate through each of the neighboring positions and sum number of bombs
        # make sure to not go out of bound
        # top left: (row-1, col-1)
        # top middle: (row-1, col)
        # top right: (row+1, col+1)
        # left: (row, col-1)
        # right: (row, col+1)
        # bottom left: (row+1, col-1)
        # bottom middle: (row+1, col)
        # bottom right: (row+1, col+1)

        num_neighboring_bombs = 0
        # use max and min to make sure we don't check out of bound
        for r in range(max(0, row - 1), min(self.dim_size - 1, (row + 1)) + 1):  # bottom row to top row
            for c in range(max(0, col - 1), min(self.dim_size - 1, (col + 1)) + 1):  # left column to right column
                # original location and we know it's not a bomb, so don't need to check
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1
        return num_neighboring_bombs

    def dig(self, row, col):
        # dig at that location
        # return True if successful dig, False if bomb dug

        self.dug.add((row, col))  # keep track that we dug here

        # hit a bomb -> game over
        if self.board[row][col] == '*':
            return False
        # dig at location with neighboring bombs -> finish dig
        elif self.board[row][col] > 0:
            return True

        # self.board[row][col] == 0
        # dig at location with no neighboring bombs -> recursively dig neighbors!
        for r in range(max(0, row - 1), min(self.dim_size - 1, (row + 1)) + 1):  # bottom row to top row
            for c in range(max(0, col - 1), min(self.dim_size - 1, (col + 1)) + 1):  # left column to right column
                # we don't want to check a place we have already dug
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)

        # if our initial dig didn't hit a bomb, we shouldn't hit a bomb here
        return True

    def __str__(self):
        # magic function where if you call print on this object, it'll print out what this function returns
        # return a string that shows the board to the player

        # create a new array that represents what the user would see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = self.board[row][col]
                else:
                    # if player has not dug, do not show that area
                    visible_board[row][col] = ' '

        # put this together in a string
        string_rep = ''

        # build labels
        col_labels = [' ']
        col_wall = [' ']
        for col_num in range(self.dim_size):
            col_labels.append(str(col_num))
            col_wall.append('-')

        # Add col label
        string_rep += ' '.join(col_labels)
        string_rep += '\n'
        string_rep += ' '.join(col_wall)
        string_rep += '\n'
        for i, board_row in enumerate(visible_board):
            str_ints = [str(num) for num in board_row]  # convert ints in list to str
            string_rep += f'{i}|'
            string_rep += ' '.join(str_ints)
            string_rep += '\n'

        return string_rep
