# Sudoku Solver
A simple sudoku solver, just because we can!

## Usage
Create a text file to describe the sudoku, use . for unknown cells. Make sure your text file has exactly 9 lines of 9 characters, i didn't build any code to check the sanity of the input file! You can check the examples folder to see how the file should look.

    $ python solve.py examples/challenge2.txt
    .... lots of output ...
    **FINAL STATE**
    184795623
    279631854
    356284971
    725846319
    893157246
    461329587
    542973168
    637518492
    918462735
    $

## WIP
This project is just for fun. It can only solve simple sudokus. It has no support (yet?) for advanced tricks like  pairs/triples