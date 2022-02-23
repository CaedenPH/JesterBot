from __future__ import annotations

import typing as t
import random as r

from datetime import datetime


class _SudokuUtils:
    """
    represents the soduku
    utils that will be required
    when doing the brute force
    aspect of the algorithm
    """

    def __init__(self) -> None:
        self.rows: t.List[t.List[int]] = [[0 for _ in range(9)] for __ in range(9)]

    def set_xy(self, xy: t.List[int, int], value: int) -> None:
        """
        sets the x and y
        value to value.

        returns
        -------
        None
        """

        y, x = xy
        self.rows[x][y] = value

    def get_xy(self, xy: t.List[int, int]) -> t.List[int]:
        """
        gets the value from
        the square in x and y

        returns
        -------
        t.List[int]
            the value in square
        """

        y, x = xy
        return self.rows[x][y]

    def get_box(self, index: t.Union[int, t.List[t.List[int]]]) -> t.List[int]:
        """
        gets the box with index `index`
        or from coordinates

        returns
        -------
        t.List[int]
            the box squares in
            list form.
        """

        board = sum(self.rows, start=[])
        boxes = {
            0: [board[i : i + 3] for i in range(0, 27, 9)],
            1: [board[i + 3 : i + 6] for i in range(0, 27, 9)],
            2: [board[i + 6 : i + 9] for i in range(0, 27, 9)],
            3: [board[i : i + 3] for i in range(27, 54, 9)],
            4: [board[i + 3 : i + 6] for i in range(27, 54, 9)],
            5: [board[i + 6 : i + 9] for i in range(27, 54, 9)],
            6: [board[i : i + 3] for i in range(54, 81, 9)],
            7: [board[i + 3 : i + 6] for i in range(54, 81, 9)],
            8: [board[i + 6 : i + 9] for i in range(54, 81, 9)],
        }

        try:
            return boxes[index]
        except TypeError:
            pass

        y, x = index

        if x in [0, 1, 2] and y in [0, 1, 2]:
            return boxes[0]
        elif x in [3, 4, 5] and y in [0, 1, 2]:
            return boxes[1]
        elif x in [6, 7, 8] and y in [0, 1, 2]:
            return boxes[2]

        if x in [0, 1, 2] and y in [3, 4, 5]:
            return boxes[3]
        elif x in [3, 4, 5] and y in [3, 4, 5]:
            return boxes[4]
        elif x in [6, 7, 8] and y in [3, 4, 5]:
            return boxes[5]

        if x in [0, 1, 2] and y in [6, 7, 8]:
            return boxes[6]
        elif x in [3, 4, 5] and y in [6, 7, 8]:
            return boxes[7]
        elif x in [6, 7, 8] and y in [6, 7, 8]:
            return boxes[8]

    def get_column(self, index: t.Union[int, t.List[t.List[int]]]) -> t.List[int]:
        """
        gets the column with index `index`
        or from coordinates

        returns
        -------
        t.List[int]
            the columns squares in
            list form.
        """

        board = sum(self.rows, start=[])
        columns = [board[i::9] for i in range(9)]

        try:
            return columns[index]
        except TypeError:
            pass

        _, x = index
        return columns[x]

    def get_row(self, index: t.Union[int, t.List[t.List[int]]]) -> t.List[int]:
        """
        gets the row with index `index`
        or from coordinates

        returns
        -------
        t.List[int]
            the rows squares in
            list form.
        """

        try:
            return self.rows[index]
        except TypeError:
            pass

        y, _ = index
        return self.rows[y]

    def get_possible_numbers(self, xy: t.List[int, int], _number_bag: t.List[int]) -> t.Optional[t.List[int]]:
        """
        get all the possible numbers
        around the coordinates xy
        as to not create conflicts

        returns
        -------
        `typing.Optional[typing.List]`
            the possible number
            combinations or None
        """

        column = self.get_column(xy)
        row = self.get_row(xy)

        number_bag = _number_bag.copy()
        number_bag = self.subtract_list(number_bag, column)
        number_bag = self.subtract_list(number_bag, row)
        return number_bag

    def validate_square(self, xy: t.List[int]) -> bool:
        """
        validate that a square is not
        conflicting with any squares
        in surrounding columns, rows,
        or in the same box.

        returns
        -------
        bool
            whether or not the square
            conflicts with other squares.
        """


class SudokuGenerator(_SudokuUtils):
    """
    represents the sodukugenerator
    class to create, solve and generate
    soduku boards.
    """

    def __init__(self) -> None:
        super().__init__()

    def build_box(self, index: int) -> None:
        """
        sets the value of the 9
        squares in a box while
        making sure there are no
        conflicts.

        params
        ------
        index: int
            the box index to build.
        """

        unused_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        box_coords = {
            0: [[0, 3], [0, 3]],
            1: [[0, 3], [3, 6]],
            2: [[0, 3], [6, 9]],
            3: [[3, 6], [0, 3]],
            4: [[3, 6], [3, 6]],
            5: [[3, 6], [6, 9]],
            6: [[6, 9], [0, 3]],
            7: [[6, 9], [3, 6]],
            8: [[6, 9], [6, 9]],
        }

        for row in range(*box_coords[index][0]):
            for column in range(*box_coords[index][1]):
                xy = [row, column]

                possible_numbers = self.get_possible_numbers(xy, unused_numbers)
                if not possible_numbers:
                    return

                number = r.choice(possible_numbers)
                unused_numbers.remove(number)
                self.set_xy([column, row], number)

    def subtract_list(self, _operand_one: t.List[int], _operand_two: t.List[int]) -> t.List[int]:
        """
        subtracts operand_two from operand_one

        returns
        -------
        t.List[int]
            the list of the differences
            from two to one
        """

        operand_one = _operand_one.copy()
        operand_two = _operand_two.copy()

        for index in operand_one.copy():
            if index in operand_two:
                operand_one.remove(index)
        return operand_one

    def validate_board(self) -> bool:
        """
        validates the board by
        going through every index
        in the board and validating
        it.

        returns
        -------
        bool
            whether or not the board
            is validated (can run)
        """

    def print_board(self, raw: bool = False) -> None:
        """
        visually print board
        | debugging purposes

        returns
        -------
        None
        """

        if raw:
            print("\n".join([str(s) for s in self.rows]))
            return

        visual_board = ""
        for row in range(9):
            for column in range(9):
                visual_board += str(self.rows[row][column])
                if (column + 1) % 3 == 0 and 7 > column:
                    visual_board += "|"

            visual_board += "\n"
            if (row + 1) % 3 == 0 and 7 > row:
                visual_board += "------------\n"
        print(visual_board)

    def build_board(self) -> None:
        self.build_box(0)


start_time = datetime.utcnow()

sudoku_board = SudokuGenerator()
# sudoku_board.set_xy([0, 0], 1)
# sudoku_board.set_xy([1, 0], 2)
# sudoku_board.set_xy([2, 3], 3)
# sudoku_board.set_xy([4, 2], 4)
# sudoku_board.set_xy([5, 6], 5)
# sudoku_board.set_xy([6, 6], 6)
# sudoku_board.set_xy([7, 5], 7)
# sudoku_board.set_xy([8, 6], 8)
# sudoku_board.set_xy([8, 8], 9)
sudoku_board.build_board()

print("\n")
sudoku_board.print_board()


print("Seconds taken: " + str((datetime.utcnow() - start_time).total_seconds()))
