def FrameMove(pos_a, pos_b, speed):
    if pos_a != pos_b:
        if pos_a.x < pos_b.x:
            pos_a.x += speed
        elif pos_a.x > pos_b.x:
            pos_a.x -= speed
        if pos_a.y < pos_b.y:
            pos_a.y += speed
        elif pos_a.y > pos_b.y:
            pos_a.y -= speed

    return pos_a == pos_b