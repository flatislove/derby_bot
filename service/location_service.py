from numpy import sin, cos, arccos, pi, round

google_coord_lat=37.4027157622189
google_coord_lon=-122.05877978988234

def rad_to_deg(radians):
    degrees = radians * 180 / pi
    return degrees

def deg_to_rad(degrees):
    radians = degrees * pi / 180
    return radians

def get_distance_between_points(latitude1, longitude1, latitude2=google_coord_lat, longitude2=google_coord_lon):
    theta = longitude1 - longitude2
    distance = 60 * 1.1515 * rad_to_deg(
        arccos(
            (sin(deg_to_rad(latitude1)) * sin(deg_to_rad(latitude2))) + 
            (cos(deg_to_rad(latitude1)) * cos(deg_to_rad(latitude2)) * cos(deg_to_rad(theta)))))
    return round(distance * 1.609344, 2)