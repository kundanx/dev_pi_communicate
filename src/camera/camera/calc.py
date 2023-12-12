import math

def get_pixel_size(bbox) -> int:

    length  = (bbox[2] - bbox[0])
    breadth = (bbox[3] - bbox[1])

    return int((length + breadth)/2)

def get_center(bbox):

    length  = (bbox[2] - bbox[0])
    breadth = (bbox[3] - bbox[1])

    x = bbox[0] + (length/2)
    y = bbox[1] + (breadth/2)

    return int(x), int(y)

def get_distance(real_diameter, pixel_diameter, intrinsic_mat, center):

    fx = intrinsic_mat[0, 0]
    fy = intrinsic_mat[1, 1]
    cx = intrinsic_mat[0, 2]
    cy = intrinsic_mat[1, 2]

    x_img = center[0]
    y_img = center[1]

    z = (fx*real_diameter)/pixel_diameter
    x = ((x_img - cx)/fx)
    y = ((y_img - cy)/fy)

    return x, y, z
    # return math.sqrt(x**2 + y**2 + z**2)
    
def get_angle(ball_center, intrinsic_matrix) -> int:
    '''
    Get the angle of vector pointing to the detected ball_center
    '''
    fx = intrinsic_matrix[0, 0]
    fy = intrinsic_matrix[1, 1]
    f = int((fx+fy)/2)
    x_center = ball_center[0]
    y_center = ball_center[0]
    x_principal = intrinsic_matrix[0,2]
    y_principal = intrinsic_matrix[1,2]

    theta = round(math.degrees(math.atan((x_center-x_principal)/f)))
    return theta
