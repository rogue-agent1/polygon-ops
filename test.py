from polygon_ops import polygon_area, polygon_perimeter, polygon_centroid, point_in_polygon, is_convex
sq = [(0,0),(1,0),(1,1),(0,1)]
assert abs(polygon_area(sq) - 1.0) < 0.01
assert abs(polygon_perimeter(sq) - 4.0) < 0.01
cx, cy = polygon_centroid(sq)
assert abs(cx-0.5)<0.01 and abs(cy-0.5)<0.01
assert point_in_polygon((0.5,0.5), sq)
assert not point_in_polygon((2,2), sq)
assert is_convex(sq)
assert not is_convex([(0,0),(2,0),(1,0.5),(2,1),(0,1)])
print("polygon_ops tests passed")
