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

    def remove_zeroes(self, _list: t.List[int], square: int) -> t.List[int]:
        """
        removes the zeroes from
        _list as to not cause
        conflicts with building.

        returns
        -------
        _list: t.List[int]
            the list without any 
            zeroes in it.
        """

        _list = [s for s in _list if s != 0]
        if square in _list:
            _list.remove(square)
        return _list

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

        square = self.get_xy(xy)
        y, x = xy

        if square in self.remove_zeroes(self.rows[y], square):
            print("r")
            return False

        column = self.remove_zeroes(self.get_column(xy), square)
        if square in column:
            print(square, column)
            print("c")
            return False
            
        box = self.remove_zeroes(sum(self.get_box(xy), start=[]), square)
        if square in box:
            print("b")
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

        used_numbers = []
        while len(used_numbers) != 9:
            for square in range(9): #row
                if self.get_xy([square, index]) != 0:
                    used_numbers.append(self.get_xy([square, index]))
                    continue

                possible_numbers = self.get_possible_numbers([square, index], used_numbers)
                if not possible_numbers:
                    used_numbers = []
                    break

                choice = r.choice(possible_numbers)
                used_numbers.append(choice)
        
        for i in range(9):
            self.set_xy([i, index], used_numbers[i])

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

        used_numbers = []
        while len(used_numbers) != 9:
            for square in range(9): #column
                possible_numbers = self.get_possible_numbers([index, square], used_numbers)
                if not possible_numbers:
                    break
                
                choice = r.choice(possible_numbers)
                used_numbers.append(choice)

        for i in range(9):
            self.set_xy([index, i], used_numbers[i])

    def get_possible_numbers(self, xy: t.List[int, int], used_numbers: t.List[int]) -> t.Optional[t.List[int]]:     
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

        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        square = self.get_xy(xy)
        x, y = xy

        numbers = self.subtract_list(numbers, used_numbers)
        numbers = self.subtract_list(numbers, self.remove_zeroes(self.rows[y], square))
        numbers = self.subtract_list(numbers, self.remove_zeroes(self.get_column(xy), square))
        numbers = self.subtract_list(numbers, sum(self.get_box(xy), start=[]))
        return numbers

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
        
        x, y = index

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
            the column squares in
            list form.
        """

        board = sum(self.rows, start=[])
        columns = [board[i::9] for i in range(9)]
        
        try:
            return columns[index]
        except TypeError:
            pass

        x, _ = index
        return columns[x]

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
    
    def subtract_list(self, operand_one: t.List[int], operand_two: t.List[int]) -> t.List[int]:
        """
        subtracts operand_two from operand_one

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
        self.build_column(4)
        self.build_column(7)

        self.build_row(1)
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
        self.rows[x][y] = value

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
                    print(row, column)
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
sudoku_board.set_xy([2, 2], 2)
# sudoku_board.set_xy([5, 6], 5)
# sudoku_board.set_xy([8, 6], 7)
# sudoku_board.set_xy([4, 8], 9)
sudoku_board.build_board()
print(sudoku_board.validate_board())

print("\n")
sudoku_board.print_board(raw=True)


print("Seconds taken: " + str((datetime.utcnow() - start_time).total_seconds()))
