import random 
import math
import pygame

pygame.init()
pygame.display.set_caption('Convex Hull')
WIDTH, HEIGHT = 750, 750
OFFSET = 10
WHITE = (245, 245, 245)
RED =  (255, 50, 50)
GRAY = (64, 64, 64)

points = [(random.randrange(OFFSET, WIDTH - OFFSET), random.randrange(OFFSET, HEIGHT - OFFSET)) for _ in range(100)]
p0 = 0
fps = 10
started = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
fpsclock = pygame.time.Clock()

def orientation(P, Q, R):
    (xp, yp), (xq, yq), (xr, yr) = P, Q, R
    return xq * (yr - yp) + xp * (yq - yr) + xr * (yp - yq)

def dist(p1, p2):
    x1, y1, x2, y2 = *p1, *p2
    return (y2 - y1) ** 2 + (x2 - x1) ** 2

def polar_angle(p1, p2):
    if p1[1] == p2[1]:
        return -math.pi
    dy = p1[1] - p2[1]
    dx = p1[0] - p2[0]
    return math.atan2(dy, dx)

def draw(all_points, *hull_points):
    screen.fill(GRAY)
    for x, y in all_points:
        pygame.draw.circle(screen, WHITE, (x, y), 8)

    for pts in hull_points:
        for curr, nxt in zip(pts, pts[1:]):
            pygame.draw.line(screen, RED, curr, nxt, 4)
        try:
            pygame.draw.line(screen, RED, pts[0], hull_points[1], 4)
        except:
            pass
    fpsclock.tick(fps)
    pygame.display.update()

def Graham_Scan():
    global points, p0
    p0 = min(points, key=lambda p: (p[1], p[0]))
    points.sort(key=lambda p: (polar_angle(p0, p), dist(p0, p)))
    hull = []
    for p in points:
        while len(hull) >= 2 and orientation(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)
        draw(points, hull)

    hull.append(points[0])
    return hull

def Andrew():
    global points 
    points.sort()
    lower = []
    for p in points:
        while len(lower) >= 2 and orientation(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
        draw(points, lower)

    higher = []
    for p in points:
        while len(higher) >= 2 and orientation(higher[-2], higher[-1], p) >= 0:
            higher.pop()
        higher.append(p)
        draw(points, lower, higher)

    return lower[::-1] + higher[1:-1] + [lower[-1]]

def main():
    # hull = Andrew()
    hull = Graham_Scan()

    while True:
        draw(points, hull)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

if __name__ == '__main__':
    main()