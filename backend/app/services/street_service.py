def interpolate_points(start_point: list, end_point: list, num_points: int):
    lat_step = (end_point[1] - start_point[1]) / (num_points - 1)
    lon_step = (end_point[0] - start_point[0]) / (num_points - 1)

    points = []
    for i in range(num_points):
        lat = start_point[1] + lat_step * i
        lon = start_point[0] + lon_step * i
        points.append([lon, lat])

    return points