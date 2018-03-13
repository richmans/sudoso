import sys

# Represents a single cell (81 in total)
class SudoCell:
  def __init__(self, idx):
    self.value = None
    self.idx = idx
    self.possibles = [a + 1 for a in range(9)]

  def setup(self, row, column, square):
    self.row = row
    self.column = column
    self.square = square
    self.groups = [row, column, square]
    self.name = "C({}, {})".format(row.idx, column.idx)
    print("Cell {} row {} col {} sq {}".format(self.idx, row.idx, column.idx, square.idx))
  
  # set a certain value as impossible
  def impossible(self, value):
    print("Cell {} can not be {}".format(self.idx, value))
    if value in self.possibles: self.possibles.remove(value)
  
  # set the value of this cell and communicated
  # all other cells in its row, column and square that
  # they can not have this value
  def set_value(self, value):
    print("Setting value for cell {} to {}".format(self.name, value))
    self.value = value
    if self.value != None:
      self.possibles = []
      for g in self.groups:
        g.has_value(self)
  
  # true if the cell has no value yet
  def is_blank(self):
    return self.value == None
    
  # true if this cell can only have one value
  def is_single(self):
    return len(self.possibles) == 1
  
  # string representation
  def __str__(self):
    if self.value == None:
      return '.'
    else:
      return str(self.value)

# Represents a single row, column or square of 9 cells
class SudoGroup:
  def __init__(self, idx):
    self.idx  = idx
    self.cells = []
    self.opens = [a + 1 for a in range(9)]
    self.blanks = []
  
  # true if there is only 1 blank cell left in the group
  def is_hole(self):
    return len(self.blanks) == 1
    
  # Called from Cell.set_value to communicate to all other
  # cells in the group that they can not have the same value
  def has_value(self, cell):
    if cell.value in self.opens: self.opens.remove(cell.value)
    if cell in self.blanks: self.blanks.remove(cell)
    for blank_cell in self.blanks:
      blank_cell.impossible(cell.value)
  
  # add a cell to the group
  def add_cell(self, cell):
    self.cells.append(cell)
    self.blanks.append(cell)
  
  # get all blank cells that have value as a possible
  def get_blanks(self, value):
    return [c for c in self.blanks if value in c.possibles]

# Represents the state of the puzzle
class SudoState:
  def __init__(self):
    # The state exists of 81 cells
    # Every cell is in exactly 1 square, row and column
    self.squares = [SudoGroup(a) for a in range(9)]
    self.rows    = [SudoGroup(a) for a in range(9)]
    self.columns = [SudoGroup(a) for a in range(9)]
    self.cells   = [SudoCell(a) for a in range(81)]
    self.groups = self.rows + self.columns + self.squares
    self.connect_cells()
  
  # Sets up the cells in their corresponding groups
  def connect_cells(self):
    for idx, cell in enumerate(self.cells):
      row = int(idx/9)
      col = idx % 9
      square = int(row / 3) *3 + int(col / 3)
      cell.setup(self.rows[row], self.columns[col], self.squares[square])
      self.rows[row].add_cell(cell)
      self.columns[col].add_cell(cell)
      self.squares[square].add_cell(cell)
  
  # parse a puzzle state from a file
  def parse(filename):
    state = SudoState()
    cellid = 0
    for line in open(filename, 'r'):
      for letter in line.strip():
        if letter != '.':
          state.cells[cellid].set_value(int(letter))
        cellid += 1
          
    return state
  
  # Searches for cells that only have 1 possible value left
  def solve_singles(self):
    for cell in self.cells:
      if cell.is_single():
        print("Cell {} is a single!".format(cell.name))
        cell.set_value(cell.possibles[0])
        return 1
    return 0
    
  # Searches groups for values that have only one blank cell left
  def solve_holes(self):
    for group in self.groups:
      for value in group.opens:
        blanks = group.get_blanks(value)
        if len(blanks) == 1:
          cell = blanks[0]
          print("Cell {} is a is hole!".format(cell.name))
          cell.set_value(value)
          return 1
    return 0
  
  # try different solving techniques until no new information is generated
  def solve(self):
    while True:
      solved = 0
      solved += self.solve_singles()
      solved += self.solve_holes()
      if solved == 0: break
      
  # String representation of the puzzle state
  def __str__(self):
    res = ""
    for row in self.rows:
      for cell in row.cells:
        res += str(cell)
      res += "\n"
    return res
  
  # String representation of the possible values per cell
  def str_possibles(self):
    res = ""
    for row in self.rows:
      for cell in row.cells:
        res += "".join([str(a) for a in cell.possibles]) + ","
      res += "\n"
    return res
  
  # String representation of the cell indexes
  def str_idxs(self):
    res = ""
    for row in self.rows:
      for cell in row.cells:
        res += str(cell.idx) + ","
      res += "\n"
    return res
    
if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("I'd like some inputfile please!")
    sys.exit(1)
  b = SudoState.parse(sys.argv[1])
  print(b)
  b.solve()
  print("**POSITIONS**")
  print(b.str_idxs())
  print("**POSSIBLES**")
  print(b.str_possibles())
  print("**FINAL STATE**")
  print(b)
  