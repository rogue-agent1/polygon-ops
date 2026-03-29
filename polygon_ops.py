#!/usr/bin/env python3
"""polygon_ops - Polygon area, centroid, clipping, and point-in-polygon."""
import sys, json, math

def area(poly):
    n = len(poly)
    return abs(sum(poly[i][0]*poly[(i+1)%n][1]-poly[(i+1)%n][0]*poly[i][1] for i in range(n))) / 2

def centroid(poly):
    n = len(poly); A = area(poly) * 2
    cx = sum((poly[i][0]+poly[(i+1)%n][0])*(poly[i][0]*poly[(i+1)%n][1]-poly[(i+1)%n][0]*poly[i][1]) for i in range(n)) / (3*A)
    cy = sum((poly[i][1]+poly[(i+1)%n][1])*(poly[i][0]*poly[(i+1)%n][1]-poly[(i+1)%n][0]*poly[i][1]) for i in range(n)) / (3*A)
    return (cx, cy)

def point_in_polygon(point, poly):
    x, y = point; n = len(poly); inside = False
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]; xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj-xi)*(y-yi)/(yj-yi)+xi):
            inside = not inside
        j = i
    return inside

def convex_hull_2d(points):
    points = sorted(set(points))
    if len(points) <= 1: return points
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0: lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0: upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]

def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def perimeter(poly):
    n = len(poly)
    return sum(math.sqrt((poly[(i+1)%n][0]-poly[i][0])**2+(poly[(i+1)%n][1]-poly[i][1])**2) for i in range(n))

def is_convex(poly):
    n = len(poly); sign = None
    for i in range(n):
        c = cross(poly[i], poly[(i+1)%n], poly[(i+2)%n])
        if c != 0:
            if sign is None: sign = c > 0
            elif (c > 0) != sign: return False
    return True

def main():
    square = [(0,0),(4,0),(4,4),(0,4)]
    triangle = [(0,0),(6,0),(3,5)]
    print("Polygon operations demo\n")
    print(f"  Square area: {area(square)}")
    print(f"  Square centroid: {centroid(square)}")
    print(f"  Square perimeter: {perimeter(square)}")
    print(f"  Triangle area: {area(triangle)}")
    print(f"  (2,2) in square: {point_in_polygon((2,2), square)}")
    print(f"  (5,5) in square: {point_in_polygon((5,5), square)}")
    pts = [(1,1),(3,0),(4,2),(2,4),(0,3),(2,1),(3,3),(1,2)]
    hull = convex_hull_2d(pts)
    print(f"  Convex hull of {len(pts)} points: {hull}")
    print(f"  Square convex: {is_convex(square)}")

if __name__ == "__main__":
    main()
