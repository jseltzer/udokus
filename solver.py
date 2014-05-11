from board import Board
from time import sleep

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


def solve(b: 'Board', anim: int=0):
    if get_blanks(b) is None:
        raise Exception("board already solved!")
    print(b.__str__(solve_helper(b, anim)))
    print('Board is legal!' if b._is_legal() else 'uh-oh')
    print('Board is solved!' if get_blanks(b) is None else 'Solving incomplete.')

def solve_helper(b: 'Board', anim: int=0) -> list:
    changes = []

    blank_options = {}
    for blank in get_blanks(b):
        blank_options[blank] = list(range(1,10))

    is_changing = True
    #main loop
    #exhaust elim_direct_options for all blanks
    while is_changing:
        is_changing = False
        blanks = get_blanks(b)
        if blanks is None:
            break
        for blank in blanks:
            new_options = elim_direct_options(b, blank, blank_options[blank])
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
                    sleep(anim)
                continue


    #secondary loop/tail
    #use haymaker; check unique opts

    


    #hacky fix for final b.__str__()
    changes.append(None)

    return changes



def elim_direct_options(b: 'Board', coords: (int, int), options: list) -> list:
    # remove any options which are in the same row, col, or box as coords
    options = list(filter(lambda x: x not in (b.get_col(coords[0])
                                           + b.rows[coords[1]] 
                                           + b.get_box_vals(b.coords_to_box_id(coords))
                                          ), options
                      )
               )
    return options


def missing_num(l: list):
    """Return 1-9 digit missing from l,
    else return False.
    """
    for i in range(1,10):
        if i not in l:
            return i
    return False


def check_uniq_options(b: 'Board', blank_options: dict) -> dict:
    #check if option is unique (amongst neighbours); if so remove other options;
    #otherwise just return original options
    for blank in blank_options:
        #these can be turned into function

        old_options = eval(repr(blank_options))

        # row
        row_options = []
        x = 0
        for val in b.rows[blank[1]]:
            if x == blank[0]:
                continue
            elif val != 0:
                row_options.append(val)
            else:
                tmp = blank_options[(x, blank[1])]
                if isinstance(tmp, list):
                    row_options.extend(tmp)
                else:
                    row_options.append(tmp)
            x += 1

        mn = missing_num(row_options)
        if mn:
            blank_options[blank] = mn
            continue

        # col
        if len(blank_options[blank]) == 1:
            continue
        col_options = []
        y = 0
        for row in b.rows:
            if y == blank[1]:
                continue
            elif row[blank[0]] != 0:
                col_options.append(row[blank[0]])
            else:
                tmp = blank_options[(blank[0], y)]
                if isinstance(tmp, list):
                    col_options.extend(tmp)
                else:
                    col_options.append(tmp)
            y += 1

        mn = missing_num(col_options)
        if mn:
            blank_options[blank] = mn
            continue

        # box
        if len(blank_options[blank]) == 1:
            continue
        box_options = []
        id = b.coords_to_box_id(blank)
        for cord in b.get_box_cords(id):
            if cord == blank:
                continue
            elif b.rows[cord[1]][cord[0]] != 0:
                box_options.append(b.rows[cord[1]][cord[0]])
            else:
                tmp = blank_options[cord]
                if isinstance(tmp, list):
                    box_options.extend(tmp)
                else:
                    box_options.append(tmp)

        mn = missing_num(box_options)
        if mn:
            blank_options[blank] = mn
            continue

    if old_options == blank_options:
        print('nothing changed!')        
    

def haymaker(b: 'Board', blank_options: dict) -> dict:
    """Correctness/utility uncertain!"""
    num = 0
    freq = {}
    for blank in blank_options:
        options = blank_options[blank]
        for option in options:
            freq[option] = freq[option] + 1 if option in freq else 1
        if len(options) > 2:
            num += 1
            pointer = blank
        if num > 1:
            break
    if num == 1:
        b.rows[pointer[1]][pointer[0]] = [option for option in freq if (freq[option]-1)%2 == 0][0]
        blank_options[pointer] = num
    return blank_options
