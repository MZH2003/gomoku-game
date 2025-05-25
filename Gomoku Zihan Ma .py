"""
A Python module for the Gomoku game.
This module can enable two people, a person against a computer, or computer against computer to play Gomoku, and can load files.

Full name: Zihan Ma
StudentId: 550171414
Email: zima0826@uni.sydney.edu.au
"""


from copy import deepcopy  # you may use this for copying a board


def newGame(player1, player2):
    """
    This function can create a new 'game' dictionary.
    """
    game = {}
    game["player1"] = player1
    game["player2"] = player2
    game["who"] = 1
    game["board"] = [[0 for _ in range(8)] for _ in range(8)]
    return game


def printBoard(board):
    """
    This function can print a formatted board.
    """
    print(" |a|b|c|d|e|f|g|h|")
    print(" +-+-+-+-+-+-+-+-+")
    for i in range(len(board)):
        print_row = "%d|" % (i + 1)
        print_row += "|".join(
            [" " if e == 0 else "X" if e == 1 else "O" for e in board[i]])
        print_row += "|"
        print(print_row)
    print(" +-+-+-+-+-+-+-+-+")


def posToIndex(s: str):
    """
    This function can convert position string to indices.
    """
    s = s.replace(" ", "").lower()
    if not len(s) == 2:
        raise ValueError
    r = None
    c = None
    for e in s:
        if ord(e) >= ord('a') and ord(e) <= ord('h'):
            c = ord(e) - ord("a")
        elif ord(e) >= ord('1') and ord(e) <= ord('8'):
            r = int(e) - 1
        else:
            raise ValueError
    if r is None or c is None:
        raise ValueError
    return (r, c)


def indexToPos(t):
    """
    This function can convert indices to position string.
    """
    return chr(97 + t[1]) + str(t[0] + 1)


def loadGame(filename):
    """
    This function can load a game from a file.
    """
    with open(filename, "r") as f:
        data = f.readlines()
    game = {}
    game["player1"] = data[0].strip()
    game["player2"] = data[1].strip()
    game["who"] = int(data[2].strip())
    game["board"] = [list(map(int, e.strip().split(","))) for e in data[3:11]]
    return game


def getValidMoves(board):
    """
    This function can get a list of all valid moves.
    """
    validMoves = []
    for i in range(8):
        for j in range(8):
            if board[i][j] == 0:
                validMoves.append((i, j))
    return validMoves


def makeMove(board, move, who):
    """
    This function can make a move.
    """
    board[move[0]][move[1]] = who
    return board


def hasWon(board, who):
    """
    This function can check for a winner.
    """
    # check columns
    for i in range(8):
        temp1 = 0
        for j in range(8):
            if board[j][i] == who:
                temp1 += 1
                if temp1 == 5:
                    return True
            else:
                temp1 = 0
    # check rows
    for i in range(8):
        temp2 = 0
        for j in range(8):
            if board[i][j] == who:
                temp2 += 1
                if temp2 == 5:
                    return True
            else:
                temp2 = 0
    # check diagonal line
    for i in range(4):
        for j in range(4):
            if board[i][j] == who and board[i + 1][j + 1] == who and board[i + 2][j + 2] == who and board[i + 3][j + 3] == who and board[i + 4][j + 4] == who:
                return True
    for i in range(4):
        for j in range(4, 8):
            if board[i][j] == who and board[i + 1][j - 1] == who and board[i + 2][j - 2] == who and board[i + 3][j - 3] == who and board[i + 4][j - 4] == who:
                return True
    return False


def suggestMove1(board, who):
    """
    This function can make an easy computer opponent.
    """
    # First check if among all valid moves of player number who there is a move which leads to an immediate win for this player. In this case, return such a winning move.
    validMoves = getValidMoves(board)
    for i, j in validMoves:
        temp_board = deepcopy(board)
        temp_board[i][j] = who
        if hasWon(temp_board, who):
            return (i, j)
    # If there is no winning move for player number who, we will try to prevent the other player from winning. This is done by checking if there is a winning move for the other player and returning it.
    other_who = 1 if who == 2 else 2
    for i, j in validMoves:
        temp_board = deepcopy(board)
        temp_board[i][j] = other_who
        if hasWon(temp_board, other_who):
            return (i, j)
    # Otherwise, if there is no immediate winning move for both players, the function simply returns a valid move.
    return validMoves[0]


def suggestMove2(board, who):
    """
    This function can make a computer opponent.
    """
    # First check if among all valid moves of player number who there is a move which leads to an immediate win for this player. In this case, return such a winning move.
    validMoves = getValidMoves(board)
    for i, j in validMoves:
        temp_board = deepcopy(board)
        temp_board[i][j] = who
        if hasWon(temp_board, who):
            return (i, j)
    # If there is no winning move for player number who, we will try to prevent the other player from winning. This is done by checking if there is a winning move for the other player and returning it.
    other_who = 1 if who == 2 else 2
    for i, j in validMoves:
        temp_board = deepcopy(board)
        temp_board[i][j] = other_who
        if hasWon(temp_board, other_who):
            return (i, j)
    # If the program runs here, it means that there is no winning point on the board for our side and no winning point for the other side, then we will look for the place where there are three consecutive pieces in our row. There are three cases: 1. One end is sealed 2. Both ends are sealed 3. Neither end is sealed
    # Look first for unsealed positions at both ends.
    for i in range(8):
        for j in range(1, 5):  # Look for three positions in a row per column.
            if board[j][i] == who and board[j + 1][i] == who and board[j + 2][i] == who:
            # It means that this position is three and continuous in a row.
                if board[j - 1][i] == 0 and board[j + 3][i] == 0:
                # If both ends of a row of three can be placed, it is preferred.
                    return (j - 1, i)  # Return to one of the two positions.
    # row
    for j in range(8):
        for i in range(1, 5):  # Look for three positions in a row per column.
            if board[j][i] == who and board[j][i + 1] == who and board[j][i + 2] == who:  
            # It means that this position is three and continuous in a row.
                if board[j][i - 1] == 0 and board[j][i + 3] == 0:
                # If both ends of a row of three can be placed, it is preferred.
                    return (j, i - 1)  # Return to one of the two positions.
    # If we do not have three consecutive pieces that are not sealed at both ends, find the opposing team's three consecutive pieces that are not sealed at both ends and block him.
    # comuln
    for i in range(8):
        for j in range(1, 5):  # Look for three positions in a row per column.
            if board[j][i] == other_who and board[j + 1][i] == other_who and board[j + 2][i] == other_who:  
            # It means that this position is three and continuous in a row.
                if board[j - 1][i] == 0 and board[j + 3][i] == 0:
                # If both ends of a row of three can be placed, it is preferred.
                    return (j - 1, i)  # Return to one of the two positions.
    # row
    for j in range(8):
        for i in range(1, 5):  # Look for three positions in a row per column.
            if board[j][i] == other_who and board[j][i + 1] == other_who and board[j][i + 2] == other_who:  
            # It means that this position is three and continuous in a row.
                if board[j][i - 1] == 0 and board[j][i + 3] == 0:
                # If both ends of a row of three can be placed, it is preferred.
                    return (j, i - 1)  # Return to one of the two positions.
    # Otherwise, if there is no immediate winning move for both players, the function simply returns a valid move.
    return validMoves[0]


# ------------------- Main function --------------------
def play():
    """
    This is the main function of the Gomoku game.
    """
    print("*" * 55)
    print("***" + " " * 8 + "WELCOME TO STEFAN'S GOMOKU!" + " " * 8 + "***")
    print("*" * 55, "\n")
    print("Enter the players' names, or type 'C' or 'L'.\n")
    input_str = input().strip()
    while input_str == "":
        print("Empty string input invalid")
        print("Enter the players' names, or type 'C' or 'L'.\n")
        input_str = input().strip()
    if input_str == "L":
        print("Loading the game file, please enter the file name")
        filename = input().strip()
        if filename == "":  # Default "game.txt" if the string is empty.
            filename = "game.txt"
        game = loadGame(filename)
        printBoard(game["board"])
        validMoves = getValidMoves(game["board"]) # Get all available positions on the board at this time.
        # Since loading the game dictionary from a file, check to see if it's a tie.
        if validMoves == []:
            print("Tie!")
            return
    else:
        player1 = input_str.capitalize()
        print("Please enter the name of Player 2")
        input_str = input().strip()
        while input_str == "":
            print("Empty string input invalid")
            print("Please enter the name of Player 2")
            input_str = input().strip()
        player2 = input_str.capitalize()
        game = newGame(player1, player2)
        print("     board     \n")
        printBoard(game["board"])
        validMoves = getValidMoves(game["board"]) # Get all available positions on the board at this time.
    while True:
        board = game["board"]
        who = game["who"]
        name = game["player%d" % who]
        if name == "C":  # If the player is a computer,
            move = suggestMove2(board, who) # Figure out where the computer spot.
            print("Computer" + ("(X)" if who == 1 else "(O)") + "drop the position:",
                  indexToPos(move))  # tuple (r,c) to the substring position
        else:
            print(name + ("(X)" if who == 1 else "(O)") + " enter the drop position.")
            invalid_input = True  # Initialize a valid input is False.
            while invalid_input:  # If the input is valid, invalid input will be False to break out of the loop, otherwise keep asking.
                move_str = input()  # Get the drop position entered by the player.
                try:
                    move = posToIndex(move_str) # Converts the player's landing position to a tuple (r,c). ValueError is caught if the player enters an invalid value.
                    if move in validMoves:  # If there are no other pieces in the spot, the spot is valid, otherwise it is invalid.
                        invalid_input = False  # If the invalid input flag is set to False, the input location is valid.
                    else:
                        print("There are already pieces in this position.")
                except:
                    print("This drop is invalid")
        new_board = makeMove(board, move, who)
        print("      board     \n")
        printBoard(new_board)  # Output new board.
        # And then decide wether you've won.
        if hasWon(new_board, who):
            print(name + ("(X)" if who == 1 else "(O)") + "win！")
            break  # program ending
        # A tie is judged if you don't win.
        validMoves = getValidMoves(new_board) # Get all available positions on the board at this time.
        if validMoves == []:
            print("Tie!")
            break
        game["board"] = new_board  # Update the game dictionary board.
        game["who"] = 1 if who == 2 else 2  # Change who, the other person to drop.


# the following allows your module to be run as a program
if __name__ == '__main__' or __name__ == 'builtins':
    play()
