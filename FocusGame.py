# Author: Teresa Nguyen
# Date: November 29, 2020
# Description: Create a 6x6 board game in order to play the abstract board game called Focus/Domination.
# This is set up for a two-player version of the game.

from pprint import pprint


class FocusGame:
    """Represents the 6x6 board game"""

    def __init__(self, player_color_1, player_color_2):
        """Initialize the board game with pieces preset"""

        preset_board = [[["R"], ["R"], ["G"], ["G"], ["R"], ["R"]],
                        [["G"], ["G"], ["R"], ["R"], ["G"], ["G"]],
                        [["R"], ["R"], ["G"], ["G"], ["R"], ["R"]],
                        [["G"], ["G"], ["R"], ["R"], ["G"], ["G"]],
                        [["R"], ["R"], ["G"], ["G"], ["R"], ["R"]],
                        [["G"], ["G"], ["R"], ["R"], ["G"], ["G"]]]

        s, r = player_color_1      # s = player, r = color
        p, g = player_color_2      # p = player, g = color

        self._player_1 = s
        self._player_2 = p
        self._color_1 = r.upper()
        self._color_2 = g.upper()
        self._player_color_1 = player_color_1
        self._player_color_2 = player_color_2
        self._preset_board = preset_board
        self._current_state = "UNFINISHED"
        self._whose_turn = self._player_1
        self._reserve_player_1 = []        # contains reserved pieces for player 1
        self._reserve_player_2 = []        # contains reserved pieces for player 2
        self._capture_player_1 = []        # contains player 2's pieces that has been captured
        self._capture_player_2 = []        # contains player 1's pieces that has been captured

    def get_preset_board(self):
        return self._preset_board

    def single_overflow(self, player, to_location):
        """Represents a single piece moving on a location that had 5 pieces stacked.  If the color on the bottom of
        the stack correlates to the player's color, then it moves to their reserved list, otherwise it is captured by
        that player.  This method is called on from single_move_1 or single_move_2"""

        a, b = to_location

        if player == self._player_1:
            # if bottom piece matches playerA, will move it to the init reserved list
            if self._preset_board[a][b][0] == self._color_1:
                piece = self._preset_board[a][b][0]
                return self._reserve_player_1.append(piece)
            else:
                # else will move to init captured list
                piece = self._preset_board[a][b][0]
                return self._capture_player_1.append(piece)

        if player == self._player_2:
            # if bottom piece matches playerB, will move it to the init reserved list
            if self._preset_board[a][b][0] == self._color_2:
                piece = self._preset_board[a][b][0]
                return self._reserve_player_2.append(piece)
            else:
                # else will move to init captured list
                piece = self._preset_board[a][b][0]
                return self._capture_player_2.append(piece)

    def single_move_1(self, player, coordinate_from, to_location, num):
        """Represents a single move made by Player A. This method is called on by move_piece"""

        x, y = coordinate_from
        a, b = to_location

        self._preset_board[x][y].remove(self._color_1)  # remove color from coordinate
        self._preset_board[a][b].append(self._color_1)  # add piece to new location
        if len(self._preset_board[a][b]) == 6:          # if the new location now has 6 pieces
            self.single_overflow(player, to_location)
            self._whose_turn = self._player_2  # update the turn
            return
        else:
            self._whose_turn = self._player_2  # update the turn
            return

    def single_move_2(self, player, coordinate_from, to_location, num):
        """Represents a single move made by Player B. This method is called on by move_piece"""

        x, y = coordinate_from
        a, b = to_location

        self._preset_board[x][y].remove(self._color_2)  # remove color from coordinate
        self._preset_board[a][b].append(self._color_2)  # add piece to new location
        if len(self._preset_board[a][b]) == 6:          # if the new location now has 6 pieces
            self.single_overflow(player, to_location)
            self._whose_turn = self._player_1  # update the turn
            return
        else:
            self._whose_turn = self._player_1  # update the turn
            return

    def multiple_overflow(self, player, to_location):
        """Represents multiple pieces moving on a location and resulted in over 5 pieces stacked.  If the color on the
        bottom of the stack correlates to the player's color, then it moves to their reserved list, otherwise it is
        captured by that player.  This method is called on from multiple_move_1 or multiple_move_2"""

        a, b = to_location

        # if pieces matches playerA, will move it to the reserve list, else to the captured list
        if player == self._player_1:
            pieces = len(self._preset_board[a][b]) - 5  # minus 5 so there are 5 pieces left
            pieces_to_take_out = self._preset_board[a][b][0:pieces]
            for color in pieces_to_take_out:
                if color == self._color_1:
                    pieces_to_take_out.pop(0)
                    return self._reserve_player_1.append(color)
                else:
                    pieces_to_take_out.pop(0)
                    return self._capture_player_1.append(color)

        # if pieces matches playerB, will move it to the reserve list, else to the captured list
        if player == self._player_2:
            pieces = len(self._preset_board[a][b]) - 5  # minus 5 so there are 5 pieces left
            pieces_to_take_out = self._preset_board[a][b][0:pieces]
            for color in pieces_to_take_out:
                if color == self._color_2:
                    pieces_to_take_out.pop(0)
                    return self._reserve_player_2.append(color)
                else:
                    pieces_to_take_out.pop(0)
                    return self._capture_player_2.append(color)

    def multiple_move_1(self, player, coordinate_from, to_location, num):
        """Represents multiple moves made by Player A. This method is called on by move_piece"""

        x, y = coordinate_from
        a, b = to_location

        all_pieces = self._preset_board[x][y][0:]
        for every_piece in all_pieces:
            self._preset_board[a][b].append(every_piece)  # add color to new location
        self._preset_board[x][y].clear()                  # remove pieces from coordinate_from
        if len(self._preset_board[a][b]) >= 6:            # if the new location has 6 or more pieces
            self.multiple_overflow(player, to_location)   # call overflow
            self._whose_turn = self._player_2             # update turn
            return
        else:
            self._whose_turn = self._player_2             # update the turn
            return

    def multiple_move_2(self, player, coordinate_from, to_location, num):
        """Represents multiple moves made by Player B. This method is called on by move_piece"""

        x, y = coordinate_from
        a, b = to_location

        all_pieces = self._preset_board[x][y][0:]
        for every_piece in all_pieces:
            self._preset_board[a][b].append(every_piece)  # add color to new location
        self._preset_board[x][y].clear()                  # remove pieces from coordinate_from
        if len(self._preset_board[a][b]) >= 6:            # if the new location has 6 or more pieces
            self.multiple_overflow(player, to_location)   # call overflow
            self._whose_turn = self._player_1             # update turn
            return
        else:
            self._whose_turn = self._player_1             # update the turn
            return

    def winner(self):
        """Checks to see if there is a winner.  Player that captures 6 pieces first, wins. """

        if len(self._capture_player_1) == 6:
            self._current_state = "WINNER"
            return "wins"
        elif len(self._capture_player_2) == 6:
            self._current_state = "WINNER"
            return "wins"

    def end_game(self):

        """ Represents the game already had a winner"""
        if self._current_state == "WINNER":
            return False

    def move_piece(self, player, coordinate_from, to_location, num):

        """Represents making a single move or multiple moves and checks to see if that move declares a winner"""
        x, y = coordinate_from
        a, b = to_location
        # if player is making a single move
        if self._whose_turn == player:
            if len(self._preset_board[x][y]) == num:
                if (a == x + 1 or a == x - 1) or (b == y + 1 or b == y - 1):
                    if self._preset_board[x][y][-1] == self._color_1:  # if player matches its' color
                        self.single_move_1(player, coordinate_from, to_location, num)
                        return "successfully moved"
                    else:
                        self.single_move_2(player, coordinate_from, to_location, num)
                        return "successfully moved"
        # if player is making multiple moves
                elif ((a == x + num or a == x - num) and (b == y)) or ((b == y + num or b == y - num) and (a == x)):
                    if self._preset_board[x][y][-1] == self._color_1:  # if player matches its' color
                        self.multiple_move_1(player, coordinate_from, to_location, num)
                        return "successfully moved"
                    else:
                        self.multiple_move_2(player, coordinate_from, to_location, num)
                        return "successfully moved"
                else:
                    return "Invalid location"
            else:
                return "Invalid number of pieces"
        else:
            return "Not your turn "

    def show_pieces(self, position):
        """Returns a list showing the pieces that are present at a given position on the board,
        with the bottom most piece as the first on the list"""

        x, y = position
        return self._preset_board[x][y][0:]

    def show_reserve(self, player):
        """Represents the pieces that are in reserve for the given player"""

        if player == self._player_1:
            if len(self._reserve_player_1) > 0:
                num_reserve = len(self._reserve_player_1)
                return num_reserve
            else:
                return 0
        if player == self._player_2:
            if len(self._reserve_player_2) > 0:
                num_reserve = len(self._reserve_player_2)
                return num_reserve
            else:
                return 0

    def show_captured(self, player):
        """Represents the pieces that are captured by the given player"""

        if player == self._player_1:
            if len(self._capture_player_1) > 0:
                num_capture = len(self._capture_player_1)
                return num_capture
            else:
                return 0
        if player == self._player_2:
            if len(self._capture_player_2) > 0:
                num_capture = len(self._capture_player_2)
                return num_capture
            else:
                return 0

    def reserve_move_1(self, player, to_location):
        """Represents a reserved move made by Player A. This method is called on by reserve_move"""
        a, b = to_location

        if len(self._reserve_player_1) > 0:
            reserved_pieces = self._reserve_player_1
            reserved_pieces.pop(0)
            self._preset_board[a][b].append(self._color_1)
            if len(self._preset_board[a][b]) == 6:
                # if bottom piece matches playerA, will move it to the init list
                if self._preset_board[a][b][0] == self._color_1:
                    piece = self._preset_board[a][b][0]
                    return self._reserve_player_1.append(piece)
                else:
                    # will remove the first piece if it's captured
                    piece = self._preset_board[a][b][0]
                    return self._capture_player_1.append(piece)
        else:
            return False

    def reserve_move_2(self, player, to_location):
        """Represents a reserved move made by Player B. This method is called on by reserve_move"""
        a, b = to_location

        if len(self._reserve_player_2) > 0:
            reserved_pieces = self._reserve_player_2
            reserved_pieces.pop(0)
            self._preset_board[a][b].append(self._color_2)
            if len(self._preset_board[a][b]) == 6:
                # if bottom piece matches playerB, will move it to the init list
                if self._preset_board[a][b][0] == self._color_2:
                    piece = self._preset_board[a][b][0]
                    return self._reserve_player_2.append(piece)
                else:
                    # will remove the first piece if it's captured
                    piece = self._preset_board[a][b][0]
                    return self._capture_player_2.append(piece)
        else:
            return False

    def reserve_move(self, player, to_location):
        """Places a piece from the player's reserved list to the given location on the board"""
        a, b = to_location

        if player == self._player_1:
            self.reserve_move_1(player, to_location)
        elif player == self._player_2:
            self.reserve_move_2(player, to_location)
        else:
            return


game = FocusGame(("PlayerA", "R"), ("PlayerB", "G"))
# game.move_piece("PlayerA", (0, 1), (0, 2), 1)
# game.move_piece("PlayerB", (0, 3), (0, 2), 1)
# game.move_piece("PlayerA", (0, 4), (1, 4), 1)
# game.move_piece("PlayerB", (0, 2), (0, 5), 3)
# game.reserve_move("PlayerA", (0, 1))



pprint(game.get_preset_board())