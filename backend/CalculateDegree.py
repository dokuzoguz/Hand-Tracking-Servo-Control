import math

def CalDeg(point1 , point2):
    x1 = point1.x
    y1 = point1.y

    x2 = point2.x
    y2 = point2.y
    
    if y1>y2:
        if x1>x2:
            return 0
        else:
            return 180

    angle_rad = math.atan2((y2-y1) , (x1-x2))
    angle_deg = 180 * angle_rad / math.pi

    return angle_deg