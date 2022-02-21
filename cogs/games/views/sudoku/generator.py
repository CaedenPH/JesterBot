from __future__ import annotations

import typing as t
from datetime import datetime


class Square:
    bot: bool
    number: int

    @classmethod
    def empty(cls) -> Square:
        self = cls()
        self.bot = False
        self.number = 0

        return self

    @classmethod
    def from_bot(cls, number: int) -> Square:
        self = cls()
        self.bot = True
        self.number = number

        return self

    @classmethod
    def from_user(cls, number: int) -> Square:
        self = cls()
        self.bot = False
        self.number = number

        return self

    def __str__(self) -> str:
        return str(self.number)

    def __repr__(self) -> str:
        return str(self.number)



class _SudokuUtils:
    def build_box(self, index: int) -> None:
        """
        build index box 

        returns
        -------
        None
        """

        self.validate()

    def build_row(self, index: int) -> None:
        """
        build a row

        returns
        -------
        None
        """

    def get_box(self, index: int) -> t.List[int]:
        """
        get the box with index
        
        returns
        -------
        t.List[int]
            the list box
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
        return boxes[index]

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
        self.rows = [[Square.empty() for _ in range(9)] for __ in range(9)]
    
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
        validates the board using 
        list comprehension.

        returns
        -------
        bool
            whether or not the board
            is validated (can run)
        """

    def print_board(self) -> None:
        """
        visually print board 
        | debugging purposes

        returns
        -------
        None
        """

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
sudoku_board.set_xy([0, 0], 3)
sudoku_board.set_xy([2, 2], 2)
sudoku_board.set_xy([5, 6], 5)
sudoku_board.set_xy([8, 6], 7)
sudoku_board.set_xy([4, 8], 9)
sudoku_board.print_board()

print("Seconds taken: " + str((datetime.utcnow() - start_time).total_seconds()))
