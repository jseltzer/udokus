class Board():
    def __init__(self: 'Board', rows: list=None):
        self.rows = rows if rows else [[0 for i in range(9)] for i in range(9)]

    def __str__(self: 'Board', changes: list=[], div: bool=True) -> str:
        """Return human-readable board format."""
        colour = {'red':'\033[91m', 'yellow':'\033[93m', 'green':'\033[92m', 'end':'\033[0m'}
        hr = ''
        i = 0
        for row in self.rows:
            j = 0
            for val in row:
                if val == 0:
                    hr += colour['red'] + '- ' + colour['end']
                elif changes != []:
                    if (j,i) == changes[-1]:
                        hr += colour['green'] + str(val) + ' ' + colour['end']
                    elif (j,i) in changes:
                        hr += colour['yellow'] + str(val) + ' ' + colour['end']
                    else:
                        hr += str(val) + ' '
                else:
                    hr += str(val) + ' '
                j += 1
                if j == 3 or j == 6:
                    hr += '| '
            i += 1
            if i == 3 or i == 6:
                hr += '\n' + '-'*21
            hr += '\n'
        return hr[:-1]

    def __eq__(self: 'Board', other: 'Board') -> bool:
        return self.rows == other.rows

    def __repr__(self: 'Board') -> str:
        return 'Board(' + repr(self.rows) + ')'

    def _is_well_defined(self: 'Board') -> bool:
        """Check for proper row amount and lengths."""
        return (len(self.rows) == 9 
                and all([len(row) == 9 for row in self.rows])
                and all([x<10 and x>-1 for x in self.get_vals(self.rows)])
               )

    def _is_legal(self: 'Board'):
        return not (self.has_dupes(self.rows) or self.has_dupes(self.get_cols()) 
                    or any([self.has_dupes([self.get_box(n)]) for n in range(9)]))
        #what about boxes!

    def has_dupes(self: 'Board', rows: [list, list, ]) -> bool:
        """Return True if each row doesn't have any dupes (besides 0)."""
        return any([list(filter(lambda x: row[x] != 0 and row[x] in row[:x] + row[x+1:], range(len(row)))) != [] for row in rows])

    def in_row(self: 'Board', row: int, val: int) -> bool:
        return val in self.rows[row]

    def in_col(self: 'Board', col: int, val: int) -> bool:
        return val in self.get_col(col)

    def get_col(self: 'Board', col: int) -> list:
        return [self.rows[n][col] for n in range(9)]

    def get_cols(self: 'Board') -> [list, list, ]:
        return [self.get_col(n) for n in range(9)]

    def get_vals(self: 'Board', rows: [list, list, ]) -> list:
        l = []
        for row in rows:
            [l.append(val) for val in row]
        return l

    """
    Boxes:
    [0][1][2]
    [3][4][5]
    [6][7][8]
    """

    def get_box(self: 'Board', id: int, values: bool=False) -> list:
        l = []
        x = 3 * (id%3)
        y = 3 * (id//3)
        if values:
            [l.extend(self.rows[n][x:x+3]) for n in range(y,y+3)]
        else:
            for j in range(3):
                [l.append((j, n)) for n in range(y,y+3)]              
        return l

    def get_box_vals(self: 'Board', id: int) -> list:
        return self.get_box(id, True)

    def get_box_cords(self: 'Board', id: int) -> list:
        return self.get_box(id)

    def coords_to_box_id(self: 'Board', coords: (int, int)) -> int:
        return (coords[0]//3) + 3*(coords[1]//3)
