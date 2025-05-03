from copy import deepcopy

def heuristic(field):
    holes = 0
    heights = [0] * len(field[0])
    bumpiness = 0
    complete_lines = 0

    for x in range(len(field[0])):
        block = False
        for y in range(len(field)):
            if field[y][x]:
                if not block:
                    heights[x] = len(field) - y
                    block = True
            elif block:
                holes += 1

    for y in range(len(field)):
        if all(field[y]):
            complete_lines += 1

    for i in range(len(heights) - 1):
        bumpiness += abs(heights[i] - heights[i + 1])

    total_height = sum(heights)

    return (holes * 1.5) + (total_height * 0.5) + (bumpiness * 0.5) - (complete_lines * 2)

def get_possible_moves(figure, field):
    moves = []
    for rotation in range(4):
        rotated = deepcopy(figure)
        for _ in range(rotation):
            center = rotated[0]
            for i in range(4):
                x = rotated[i].y - center.y
                y = rotated[i].x - center.x
                rotated[i].x = center.x - x
                rotated[i].y = center.y + y

        for x_shift in range(-5, 6):
            test_fig = deepcopy(rotated)
            for f in test_fig:
                f.x += x_shift
            test = deepcopy(test_fig)
            while all(0 <= f.x < 10 and 0 <= f.y < 20 and not field[f.y][f.x] for f in test):
                for f in test:
                    f.y += 1
            for f in test:
                f.y -= 1
            if all(0 <= f.x < 10 and 0 <= f.y < 20 for f in test):
                moves.append(test)
    return moves

def apply_piece_to_field(field, piece, color):
    new_field = deepcopy(field)
    for f in piece:
        if 0 <= f.y < len(field) and 0 <= f.x < len(field[0]):
            new_field[f.y][f.x] = color
    return new_field

def astar_best_move(figure, field, color):
    possible_moves = get_possible_moves(figure, field)
    best_score = float('inf')
    best_move = None

    for move in possible_moves:
        simulated = apply_piece_to_field(field, move, color)
        score = heuristic(simulated)
        if score < best_score:
            best_score = score
            best_move = move

    return best_move
