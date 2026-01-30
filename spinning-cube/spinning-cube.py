import math
import time
import os

WIDTH, HEIGHT = 60, 30
SCALE = 10
DIST = 3

cube = [
    [-1,-1,-1], [1,-1,-1], [1,1,-1], [-1,1,-1],
    [-1,-1, 1], [1,-1, 1], [1,1, 1], [-1,1, 1]
]

edges = [
    (0,1),(1,2),(2,3),(3,0),
    (4,5),(5,6),(6,7),(7,4),
    (0,4),(1,5),(2,6),(3,7)
]

def rotate(p, a, b):
    x,y,z = p
    x,z = x*math.cos(a)-z*math.sin(a), x*math.sin(a)+z*math.cos(a)
    y,z = y*math.cos(b)-z*math.sin(b), y*math.sin(b)+z*math.cos(b)
    return [x,y,z]

a = b = 0

while True:
    os.system("cls" if os.name == "nt" else "clear")
    screen = [[" "]*WIDTH for _ in range(HEIGHT)]
    points = []

    for p in cube:
        x,y,z = rotate(p, a, b)
        z += DIST
        px = int(WIDTH/2 + x/z*SCALE)
        py = int(HEIGHT/2 - y/z*SCALE)
        points.append((px,py))

    for e in edges:
        x1,y1 = points[e[0]]
        x2,y2 = points[e[1]]
        for i in range(16):
            x = int(x1 + (x2-x1)*i/15)
            y = int(y1 + (y2-y1)*i/15)
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                screen[y][x] = "#"

    print("\n".join("".join(row) for row in screen))
    a += 0.05
    b += 0.03
    time.sleep(0.08)
