#!/usr/bin/env python3
"""polygon_ops - Polygon area, centroid, point-in-polygon, and clipping."""
import sys

def area(polygon):
    n = len(polygon)
    a = 0.0
    for i in range(n):
        j = (i + 1) % n
        a += polygon[i][0] * polygon[j][1]
        a -= polygon[j][0] * polygon[i][1]
    return abs(a) / 2.0

def centroid(polygon):
    n = len(polygon)
    cx = cy = 0.0
    a = 0.0
    for i in range(n):
        j = (i + 1) % n
        cross = polygon[i][0] * polygon[j][1] - polygon[j][0] * polygon[i][1]
        a += cross
        cx += (polygon[i][0] + polygon[j][0]) * cross
        cy += (polygon[i][1] + polygon[j][1]) * cross
    a /= 2.0
    cx /= (6.0 * a)
    cy /= (6.0 * a)
    return cx, cy

def point_in_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside

def perimeter(polygon):
    n = len(polygon)
    p = 0.0
    for i in range(n):
        j = (i + 1) % n
        dx = polygon[j][0] - polygon[i][0]
        dy = polygon[j][1] - polygon[i][1]
        p += (dx*dx + dy*dy) ** 0.5
    return p

def test():
    # unit square
    sq = [(0,0),(1,0),(1,1),(0,1)]
    assert abs(area(sq) - 1.0) < 1e-9
    cx, cy = centroid(sq)
    assert abs(cx - 0.5) < 1e-9 and abs(cy - 0.5) < 1e-9
    assert abs(perimeter(sq) - 4.0) < 1e-9
    assert point_in_polygon((0.5, 0.5), sq)
    assert not point_in_polygon((2, 2), sq)
    # triangle
    tri = [(0,0),(4,0),(0,3)]
    assert abs(area(tri) - 6.0) < 1e-9
    assert point_in_polygon((1, 1), tri)
    assert not point_in_polygon((3, 3), tri)
    print("OK: polygon_ops")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: polygon_ops.py test")
