
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_one = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']]
diag_two = [['I1', 'H2', 'G3', 'F4', 'E5', 'D6', 'C7', 'B8', 'A9']]

unitlist = row_units + column_units + square_units + diag_one + diag_two
unitlist = unitlist


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).

    See Also
    --------
    Pseudocode for this algorithm on github:
    https://github.com/udacity/artificial-intelligence/blob/master/Projects/1_Sudoku/pseudocode.md
    """
    out = values.copy()
    
    twin_pairs = [(boxA, boxB) for boxA in cross('ABCDEFGHI', '123456789') for boxB in peers[boxA] if values[boxA] == values[boxB] and len(values[boxA]) == 2]
    #print('This round has the following naked twins: {}'.format(twin_pairs))
    for twin in twin_pairs:
        all_peers = peers[twin[0]].intersection(peers[twin[1]])
        #print('{} and {} have the value {} and combined peers: {}'.format(twin[0], twin[1], out[twin[0]], all_peers))
        for peer in all_peers:
            for digit in out[twin[0]]:
                old = out[peer]
                out[peer] = out[peer].replace(digit,'')
                #print('  Removing value in peer ' + peer + ': ' + old + ' -> ' + out[peer])
    return out

def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        #print('Elim value (' + digit + ') for peers of box ' + box)
        for peer in peers[box]:
            old = values[peer]
            values[peer] = values[peer].replace(digit,'')
            #print('  Removing value in peer ' + peer + ': ' + old + ' -> ' + values[peer])
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for unit in unitlist:
        #print('Checking unit: ' + str(unit))
        for number in '123456789':
            containing_boxes = []
            for box in unit:
                if number in values[box]:
                    containing_boxes.append(box)
            if len(containing_boxes) == 1:
                only_box = containing_boxes[0]
                #print('Replacing ' + only_box + ': ' + values[only_box] + ' -> ' + number)
                values[only_box] = number
                pass
    return values



def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)

        values = only_choice(values)
        
        values = naked_twins(values)
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            print('Returning False because of failed sanity check!')
            return False
    return values



def search(values, depth = 0):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    reduced = reduce_puzzle(values)

    if reduced == False:
        return False
    
    # Choose one of the unfilled squares with the fewest possibilities
    boxes = [[box, len(reduced[box])] for box in reduced if len(reduced[box]) > 1]

    if len(boxes) is 0:
        return reduced
    
    boxes.sort(key=lambda tup: tup[1]) # take min
    search_box = boxes[0][0]
        
    # Now use recursion to solve each one of the resulting sudokus, and if
    # one returns a value (not False), return that answer!
    
    for digit in reduced[search_box]:
        next_sudoku = reduced.copy()
        next_sudoku[search_box] = digit
        result = search(next_sudoku, depth+1)
        if result is not False:
            return result

    #print('Ending search in {} with values: {}'.format(search_box, reduced[search_box]))
    return False

def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    print('Solving ...')
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)
    
    
    diag_sudoku_grid = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)
    
    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
