from dip import *

def linear_point_operation(image, p, l):
    """ Performs the linear point operation (px+l) on the input image
        takes as input:
        image: a greyscale image
        p: the parameter p in px+l
        l: the parameter l in px + l
        returns a greyscale image after applying linear point operation """
    rows, cols = shape(image)
    out_image = zeros((rows, cols), uint8)
    for i in range(rows):
        for j in range(cols):
            val = p * image[i, j] + l
            if val < 0:
                val = 0
            elif val > 255:
                val = 255
            out_image[i, j] = uint8(val)
    return out_image


def image_negative(image):
    """ Computes the image negative of the input image
        takes as input:
        image: a greyscale image
        returns a greyscale image that is negative of the input
        Note: You can call linear_point_operations functions with appropriate p and l"""
    return linear_point_operation(image, -1, 255)


def full_contrast_stretch(image):
    """ Performs a full contrast stretch on the input image
        takes as input:
        image: a greyscale image
        returns a greyscale image after applying full contrast stretch
        Note: You can call linear_point_operations functions with appropriate p and l"""
    min_val = min(image)
    max_val = max(image)
    if max_val - min_val == 0:
        return image
    p = 255 / (max_val - min_val)
    l = -p * min_val
    return linear_point_operation(image, p, l)
