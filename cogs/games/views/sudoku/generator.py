from __future__ import annotations

import typing as t
import random as r

from datetime import datetime


class Square:
    bot: bool
    box: int
    number: int

    @classmethod
    def empty(cls, box) -> Square:
        self = cls()
        self.bot = False
        self.number = 0
        self.box = box

        return self

    @classmethod
    def from_bot(cls, number: int, box: int) -> Square:
        self = cls.empty(box)
        self.bot = True
        self.number = number

        return self

    @classmethod
    def from_user(cls, number: int, box: int) -> Square:
        self = cls.empty(box)
        self.bot = False
        self.number = number

        return self

    def __str__(self) -> str:
        return str(self.number)

    def __repr__(self) -> str:
        return str(self.number)

    def __int__(self) -> int:
        return self.number

class _SudokuUtils:
    def __init__(self) -> None:
        self.rows: t.List[t.List[int]] = [[Square.empty(1) for _ in range(9)] for __ in range(9)]
        for j in range(3):  # square rows
            for i in range(3):  # square columns
                for k in range(3):  # square height
                    for element in self.rows[j * 3 + k][
                        i * 3 : i * 3 + 3
                    ]:  # looping over the three values in a row (1,2,3) -> (4,5,6) -> (7,8,9) -> (1,2,3) -> ...
                        ...
    """
    represents the soduku
    utils that will be required
    when doing the brute force
    aspect of the algorithm
    """

    def validate(self, xy: t.List[int]) -> bool:
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

        square = int(self.get_xy(xy))
        y, x = xy

        if square in self.rows[y]:
            return False

        column = self.get_column(xy)
        if square in column:
            return False
            
        box = self.get_box(xy)
        if square in box:
            return False
        return True
        

    def build_box(self, index: int) -> None:
        """
        sets the value of the final
        four squares in a box while
        making sure there are no 
        conflicts.

        params
        ------
        index: int
            the box index to build.
        """

        box = self.get_box(index)

    def build_row(self, index: int) -> None:
        """
        sets the 9 values in a row
        while making sure there are
        no conflicts.

        params
        ------
        index: int
            the row index.
        """

        row = self.rows[index]

    def build_column(self, index: int) -> None:
        """
        sets the 9 values in a 
        column while making sure 
        there are no conflicts.

        params
        ------
        index: int
            the column index.
        """

        column = self.get_column(index)
        complete = False

        while True:
            numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
            r.shuffle(numbers)

            for square in range(9):
                if not self.validate([index, square]):
                    break
                complete = True
            if complete:
                break
        print(numbers)     
        column = numbers

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
            0: [board[i:i+3] for i in range(0, 27, 9)],
            1: [board[i+3:i+6] for i in range(0, 27, 9)],
            2: [board[i+6:i+9] for i in range(0, 27, 9)],
            3: [board[i:i+3] for i in range(27, 54, 9)],
            4: [board[i+3:i+6] for i in range(27, 54, 9)],
            5: [board[i+6:i+9] for i in range(27, 54, 9)],
            6: [board[i:i+3] for i in range(54, 81, 9)],
            7: [board[i+3:i+6] for i in range(54, 81, 9)],
            8: [board[i+6:i+9] for i in range(54, 81, 9)],
        }
        
        try:
            return boxes[index]
        except TypeError:
            pass

        square = self.get_xy(index)
        return boxes[square.box]


    def get_column(self, index: t.Union[int, t.List[t.List[int]]]) -> t.List[int]:
        """
        gets the column with index `index`
        or from coordinates
    
        returns
        -------
        t.List[int]
            the column squares in
            list form.
        """

        board = sum(self.rows, start=[])
        columns = [board[i::9] for i in range(9)]
        
        try:
            return columns[index]
        except TypeError:
            pass

        y, _ = index
        return columns[y]

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

class SudokuGenerator(_SudokuUtils):
    """
    represents the sodukugenerator
    class to create, solve and generate
    soduku boards.
    """

    def __init__(self) -> None:
        super().__init__()
    
    def list_subtraction(self, operand_one: t.List[int], operand_two: t.List[int]) -> t.List[int]:
        """
        subracts operand_two from operand_one

        returns
        -------
        t.List[int]
            the list of the differences
            from two to one
        """

        for index in operand_one.copy():
            if index in operand_two:
                operand_one.remove(index)
        return operand_one  

    def build_board(self) -> None:
        self.build_column(1)
        # self.build_column(4)
        # self.build_column(7)

        # self.build_row(1)
        # self.build_row(4)
        # self.build_row(7)

        # for box in range(9):
        #     self.build_box(box)

    def set_xy(self, xy: t.List[int, int], value: int) -> None:
        """
        sets the x and y 
        value to value.
        
        returns
        -------
        None
        """
        
        y, x = xy
        self.rows[x][y] = Square.from_bot(value)

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

        for row in range(9):
            for column in range(9):
                if not self.validate([row, column]):
                    return False
        return True

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

start_time = datetime.utcnow()

sudoku_board = SudokuGenerator()
# sudoku_board.set_xy([0, 0], 3)
# sudoku_board.set_xy([2, 2], 2)
# sudoku_board.set_xy([5, 6], 5)
# sudoku_board.set_xy([8, 6], 7)
# sudoku_board.set_xy([4, 8], 9)
sudoku_board.build_board()

print("\n")
sudoku_board.print_board(raw=True)


print("Seconds taken: " + str((datetime.utcnow() - start_time).total_seconds()))
