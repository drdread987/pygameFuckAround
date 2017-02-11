
def box_collide(x1, y1, w1, h1, x2, y2, w2, h2):

    if x1 + w1 >= x2 and x1 <= x2 + w2 and y1 + h1 >= y2 and y1 <= y2 + h2:
        return True
    else:
        return False
