board = [
    [8,0,0,0,0,0,0,0,0],
    [0,0,3,6,0,0,0,0,0],
    [0,7,0,0,9,0,2,0,0],
    [0,5,0,0,0,7,0,0,0],
    [0,0,0,0,4,5,7,0,0],
    [0,0,0,1,0,0,0,3,0],
    [0,0,1,0,0,0,0,6,8],
    [0,0,8,5,0,0,0,1,0],
    [0,9,0,0,0,0,4,0,0]
]

def solve(b):

    find = empty_spot(b)
    if not find:
        return True #when there is not any empty spot
    else:
        row, col = find

    for i in range(1,10):
        if check(b, i, (row, col)):
            b[row][col] = i

            #Keep solving an empty spot after an empty spot
            if solve(b):
                return True
            else:
                # Set the previous value to zero if there is
                # no possible solution for the current one
                b[row][col] = 0


    return False


def check(b, num, pos):
    # Check row
    for i in range(9):
        if b[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(9):
        if b[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    row_box = pos[0] // 3
    col_box = pos[1] // 3

    for i in range(row_box*3, row_box*3 + 3):
        for j in range(col_box * 3, col_box*3 + 3):
            if b[i][j] == num and (i,j) != pos:
                return False

    return True

def show_board(b):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print('----------------------')
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print('| ', end='')
            if j == 8:
                print(board[i][j], end='\n')
            else:
                print(board[i][j],'', end='')

def empty_spot(b):
    for i in range(9):
        for j in range(9):
            if b[i][j]==0:
                return (i,j)
    return None

show_board(board)
solve(board)
print('','||||||||||||||||||||||','',sep='\n')
show_board(board)