#!/usr/bin/env python3
"""Polygon operations. Zero dependencies."""
import math

def polygon_area(vertices):
    n = len(vertices)
    if n < 3: return 0
    area = 0
    for i in range(n):
        j = (i+1) % n
        area += vertices[i][0]*vertices[j][1] - vertices[j][0]*vertices[i][1]
    return abs(area) / 2

def polygon_perimeter(vertices):
    n = len(vertices); p = 0
    for i in range(n):
        j = (i+1) % n
        p += math.hypot(vertices[j][0]-vertices[i][0], vertices[j][1]-vertices[i][1])
    return p

def polygon_centroid(vertices):
    n = len(vertices); cx = cy = 0; a = 0
    for i in range(n):
        j = (i+1) % n
        cross = vertices[i][0]*vertices[j][1] - vertices[j][0]*vertices[i][1]
        a += cross
        cx += (vertices[i][0]+vertices[j][0]) * cross
        cy += (vertices[i][1]+vertices[j][1]) * cross
    a /= 2
    if abs(a) < 1e-10: return (0, 0)
    return (cx/(6*a), cy/(6*a))

def point_in_polygon(point, vertices):
    x, y = point; n = len(vertices); inside = False
    j = n - 1
    for i in range(n):
        xi,yi = vertices[i]; xj,yj = vertices[j]
        if ((yi > y) != (yj > y)) and (x < (xj-xi)*(y-yi)/(yj-yi)+xi):
            inside = not inside
        j = i
    return inside

def is_convex(vertices):
    n = len(vertices)
    if n < 3: return False
    sign = None
    for i in range(n):
        o = vertices[i]; a = vertices[(i+1)%n]; b = vertices[(i+2)%n]
        cross = (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
        if abs(cross) < 1e-10: continue
        s = cross > 0
        if sign is None: sign = s
        elif s != sign: return False
    return True

if __name__ == "__main__":
    sq = [(0,0),(1,0),(1,1),(0,1)]
    print(f"Area: {polygon_area(sq)}, Perimeter: {polygon_perimeter(sq)}")
