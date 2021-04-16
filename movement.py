def FrameMove(pos_a, pos_b):
    if pos_a != pos_b:
        if pos_a.x < pos_b.x:
            pos_a.x += 1
        elif pos_a.x > pos_b.x:
            pos_a.x -= 1
        if pos_a.y < pos_b.y:
            pos_a.y += 1
        elif pos_a.y > pos_b.y:
            pos_a.y -= 1

    return pos_a == pos_b