from board import Board

dig = list(range(1,10))

b = Board([dig[n:] + dig[:n] for n in range(9)])

comp = Board([[1,2,3,4,5,6,7,8,9], [4,5,6,7,8,9,1,2,3], [7,8,9,1,2,3,4,5,6], [2,3,4,5,6,7,8,9,1], [5,6,7,8,9,1,2,3,4], [8,9,1,2,3,4,5,6,7],
           [3,4,5,6,7,8,9,1,2], [6,7,8,9,1,2,3,4,5], [9,1,2,3,4,5,6,7,8]])

not_comp = Board([[0,2,0,4,0,0,7,0,9], [0,5,0,7,0,0,1,2,0], [7,0,9,0,2,3,0,0,6], [2,0,4,0,6,0,8,0,1], [0,6,7,8,9,0,2,0,0], [0,9,0,2,0,4,0,6,0],
           [0,0,0,0,7,8,0,1,0], [6,0,8,0,1,0,3,4,5], [0,0,0,0,0,0,6,0,0]])

not_comp2 = Board([[6,0,0,5,0,9,0,8,0], [0,9,2,0,0,0,0,0,0], [3,0,0,0,4,1,0,0,0], [0,0,0,0,2,0,6,0,5], [2,0,1,0,7,0,8,0,3], [4,0,8,0,1,0,0,0,0],
           [0,0,0,3,9,0,0,0,1], [0,0,0,0,0,0,2,6,0], [0,7,0,4,0,2,0,0,9]])

not_comp3 = Board([[6,3,0,0,0,1,9,0,0], [9,0,4,0,5,6,1,3,0], [0,0,0,0,0,9,0,0,8], [1,0,0,0,8,0,7,0,9], [0,6,0,0,0,0,2,1,0], [2,0,5,1,0,0,0,0,0],
           [0,5,0,0,0,0,4,0,0], [0,2,1,7,0,5,0,0,0], [8,0,6,0,1,4,0,2,0]])





def get_blanks(b: 'Board'):
    x, y = 0, 0
    blanks = []
    for row in b.rows:
        for val in row:
            if val == 0:
                blanks.append((x,y))
            x += 1
        x = 0
        y += 1
    return blanks if blanks != [] else None


#solving


def solve(b: 'Board', anim: bool=False):
    if get_blanks(b) is None:
        raise Exception("board already solved!")
    print(b.__str__(solve_helper(b, anim)))
    print('Board is legal!' if b._is_legal() else 'uh-oh')
    print('Board is solved!' if b._is_legal() else 'Solving incomplete.')

def solve_helper(b: 'Board', anim: bool=False) -> list:
    changes = []

    blank_options = {}
    for blank in get_blanks(b):
        blank_options[blank] = list(range(1,10))

    is_changing = True
    #exhaust elim_options for all blanks
    while is_changing:
        is_changing = False
        blanks = get_blanks(b)
        if blanks is None:
            break
        for blank in blanks:
            new_options = elim_options(b, blank, blank_options[blank])
            #check if options have changed
            if new_options != blank_options[blank]:
                is_changing = True
                blank_options[blank] = new_options                
            #check for solved numbers
            if len(blank_options[blank]) == 1:
                is_changing = True
                b.rows[blank[1]][blank[0]] = blank_options[blank][0]
                changes.append(blank)
                if anim:
                    print(b.__str__(changes, True) + '\n')
                continue
    changes.append(None)
    return changes



def elim_options(b: 'Board', coords: (int, int), options: list) -> list:
    # remove any options which are in the same row, col, or box as coords
    options = list(filter(lambda x: x not in (b.get_col(coords[0])
                                           + b.rows[coords[1]] 
                                           + b.get_box(b.coords_to_box_id(coords))
                                          ), options
                      )
               )
    return options
