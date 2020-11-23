import pathlib
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    matrix = []
    for i in range(len(values)):
        if (i+1) % n == 0:
            matrix.append(values[(i+1)-n:(i+1)])
    return matrix
    pass


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row, col = pos
    ans = []
    for i in range(len(grid[0])):
        ans.append(grid[row][i])
    return ans
    pass


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    row, col = pos
    ans = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if col == j:
                ans.append(grid[i][col])
    return ans
    pass


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    ans = []
    row, col = pos
    row = (row // 3) * 3
    col = (col // 3) * 3
    for i in range(row, row+3):
        for j in range(col, col+3):
            ans.append(grid[i][j])
    return ans
    pass


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    row, col = -1, -1
    for i in range(len(grid[0])):
        for j in range(len(grid[0])):
            if grid[i][j] == '.':
                row, col = i, j
                break
    if row != -1 and col != -1:
        pos = (row, col)
        return pos
    else:
        return None
    pass


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    val = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    values = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
    what = []
    r, c = pos
    row = get_row(grid, (r, 0))
    col = get_col(grid, (0, c))
    bl = get_block(grid, pos)
    for i in range(len(row)):
        for j in range(len(val)):
            if row[i] == val[j]:
                what.append(val[j])
    for i in range(len(col)):
        for j in range(len(val)):
            if col[i] == val[j]:
                what.append(val[j])
    for i in range(len(bl)):
        for j in range(len(val)):
            if bl[i] == val[j]:
                what.append(val[j])
    what = set(what)
    values = values - what
    return values
    pass


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]"""
    pos = find_empty_positions(grid)
    if pos is None:
        return grid
    row, col = pos
    for i in find_possible_values(grid, pos):
        grid[row][col] = i
        sol = solve(grid)
        if sol:
            return sol
    grid[row][col] = '.'
    pass


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles
    for i in range(len(solution)):
        row = set(get_row(solution, (i, 0)))
        if row != {'1', '2', '3', '4', '5', '6', '7', '8', '9'}:
            return False
            break
    for i in range(len(solution)):
        col = set(get_col(solution, (0, i)))
        if col != {'1', '2', '3', '4', '5', '6', '7', '8', '9'}:
            return False
            break
    for i in range(0, len(solution), 3):
        for j in range(0, len(solution), 3):
            bl = set(get_block(solution, (i, j)))
            if bl != {'1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                return False
                break
    return True
    pass


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    import random
    arr = ['.']*9
    empty_grid = []
    for i in range(9):
        empty_grid.append(arr.copy())
    grid = solve(empty_grid)
    if N >= 81:
        return grid
    else:
        n = 81 - N
        while n != 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if grid[row][col] != '.':
                grid[row][col] = '.'
                n-=1
    return grid
    pass


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
