#!/usr/bin/env python3
"""polygon_ops - Polygon area, centroid, PIP, clipping, boolean ops."""
import sys, argparse, math

def area(poly):
    n = len(poly); a = 0
    for i in range(n):
        j = (i+1) % n
        a += poly[i][0]*poly[j][1] - poly[j][0]*poly[i][1]
    return abs(a) / 2

def centroid(poly):
    n = len(poly); cx = cy = a6 = 0
    for i in range(n):
        j = (i+1) % n
        cross = poly[i][0]*poly[j][1] - poly[j][0]*poly[i][1]
        cx += (poly[i][0]+poly[j][0]) * cross
        cy += (poly[i][1]+poly[j][1]) * cross
        a6 += cross
    if abs(a6) < 1e-10: return (0,0)
    return (cx/(3*a6), cy/(3*a6))

def point_in_polygon(point, poly):
    x, y = point; n = len(poly); inside = False
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]; xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj-xi)*(y-yi)/(yj-yi)+xi):
            inside = not inside
        j = i
    return inside

def perimeter(poly):
    n = len(poly)
    return sum(math.sqrt((poly[(i+1)%n][0]-poly[i][0])**2+(poly[(i+1)%n][1]-poly[i][1])**2) for i in range(n))

def is_convex(poly):
    n = len(poly); sign = None
    for i in range(n):
        o = poly[i]; a = poly[(i+1)%n]; b = poly[(i+2)%n]
        cross = (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
        if abs(cross) < 1e-10: continue
        s = cross > 0
        if sign is None: sign = s
        elif s != sign: return False
    return True

def sutherland_hodgman(subject, clip):
    def inside(p, a, b):
        return (b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0]) >= 0
    def intersect(p1, p2, a, b):
        x1,y1 = p1; x2,y2 = p2; x3,y3 = a; x4,y4 = b
        d = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
        if abs(d) < 1e-10: return p1
        t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/d
        return (x1+t*(x2-x1), y1+t*(y2-y1))
    output = list(subject)
    for i in range(len(clip)):
        if not output: break
        a, b = clip[i], clip[(i+1)%len(clip)]
        inp = list(output); output = []
        for j in range(len(inp)):
            curr, prev = inp[j], inp[j-1]
            if inside(curr, a, b):
                if not inside(prev, a, b): output.append(intersect(prev, curr, a, b))
                output.append(curr)
            elif inside(prev, a, b):
                output.append(intersect(prev, curr, a, b))
    return output

def main():
    p = argparse.ArgumentParser(description="Polygon operations")
    p.add_argument("--demo", action="store_true")
    args = p.parse_args()
    if args.demo:
        square = [(0,0),(10,0),(10,10),(0,10)]
        triangle = [(5,0),(15,10),(5,10)]
        print(f"Square area: {area(square)}")
        print(f"Square perimeter: {perimeter(square):.2f}")
        print(f"Square centroid: {centroid(square)}")
        print(f"Square convex: {is_convex(square)}")
        print(f"(5,5) in square: {point_in_polygon((5,5), square)}")
        print(f"(15,5) in square: {point_in_polygon((15,5), square)}")
        clipped = sutherland_hodgman(triangle, square)
        print(f"Triangle clipped to square: {len(clipped)} vertices, area={area(clipped):.2f}")
    else: p.print_help()
if __name__ == "__main__": main()
