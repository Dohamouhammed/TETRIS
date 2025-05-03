from copy import deepcopy

def clear_full_rows_and_gravity(field):
    # إزاي تمسح الصفوف الممتلئة
    full_rows = [i for i, row in enumerate(field) if all(cell != 0 for cell in row)]
    for row in full_rows:
        field.pop(row)
        field.insert(0, [0 for _ in range(len(field[0]))])  # إدراج صف فارغ في الأعلى
    return field

def evaluate_position(figure, field):
    max_y = max(block.y for block in figure)
    holes = sum(1 for y in range(len(field)) for x in range(len(field[0])) if field[y][x] == 0 and y > 0 and field[y - 1][x] != 0)
    return max_y - holes

def get_all_positions(figure, field):
    positions = []
    for rotation in range(4):
        rotated = deepcopy(figure)
        center = rotated[0]
        for i in range(4):
            x = rotated[i].y - center.y
            y = rotated[i].x - center.x
            rotated[i].x = center.x - x
            rotated[i].y = center.y + y

        for dx in range(-5, 6):
            moved = deepcopy(rotated)
            for i in range(4):
                moved[i].x += dx
            while all(0 <= f.x < len(field[0]) and f.y < len(field) and not field[f.y][f.x] for f in moved):
                for i in range(4):
                    moved[i].y += 1
            for i in range(4):
                moved[i].y -= 1
            if all(0 <= f.x < len(field[0]) and f.y < len(field) and not field[f.y][f.x] for f in moved):
                positions.append(deepcopy(moved))
    return positions

def greedy_best_move(figure, field, color):
    best_score = float("-inf")
    best_move = deepcopy(figure)
    for pos in get_all_positions(figure, field):
        score = evaluate_position(pos, field)
        if score > best_score:
            best_score = score
            best_move = pos
    return best_move
