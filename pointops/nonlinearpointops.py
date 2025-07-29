from dip import *
from math import log

def log_transform(image):
    """ Performs the log transform
        takes as input:
        image: a greyscale image
        returns a greyscale image after applying log range compression
        Note: Be sure to apply scaling after scaling before returning the output image.
         """
    rows, cols = shape(image)
    out_image = zeros((rows, cols), uint8)
    c = 255 / log(1 + max(image))
    for i in range(rows):
        for j in range(cols):
            val = c * log(1 + image[i, j])
            out_image[i, j] = uint8(val)
    return out_image


def histogram_flattening(image):
    """ Apply histogram flattening on input image
        takes as input:
        image: a greyscale image
        returns a greyscale image after flattening
        """
    rows, cols = shape(image)
    total_pixels = rows * cols
    hist, _ = histogram(image.ravel(), 256, (0, 256))
    cdf = zeros(256)
    cdf[0] = hist[0]
    for i in range(1, 256):
        cdf[i] = cdf[i-1] + hist[i]
    out_image = zeros((rows, cols), uint8)
    for i in range(rows):
        for j in range(cols):
            out_image[i, j] = uint8((cdf[image[i, j]] - 1) * 255 / (total_pixels - 1))
    return out_image


def histogram_shaping(image, target_histogram):
    """ Performs histogram matching of the image with the target histogram
        takes as input:
        image: a greyscale image
        target_histogram: the target histogram to match the input image
        returns a greyscale image after histogram shaping
        """
    rows, cols = shape(image)
    total_pixels = rows * cols

    # pad target_histogram to 256 if it’s too short
    if len(target_histogram) < 256:
        target_histogram += [0] * (256 - len(target_histogram))

    hist, _ = histogram(image.ravel(), 256, (0, 256))
    cdf_input = zeros(256)
    cdf_input[0] = hist[0]
    for i in range(1, 256):
        cdf_input[i] = cdf_input[i-1] + hist[i]
    cdf_input = cdf_input / total_pixels

    target_total = sum(target_histogram)
    cdf_target = zeros(256)
    cdf_target[0] = target_histogram[0]
    for i in range(1, 256):
        cdf_target[i] = cdf_target[i-1] + target_histogram[i]
    cdf_target = cdf_target / target_total

    mapping = zeros(256, uint8)
    for i in range(256):
        diff = abs(cdf_target - cdf_input[i])
        mapping[i] = uint8(diff.argmin())

    out_image = zeros((rows, cols), uint8)
    for i in range(rows):
        for j in range(cols):
            out_image[i, j] = mapping[image[i, j]]
    return out_image


def histogram_matching(image, target_image):
    """ Performs histogram matching of the image with the target histogram
        takes as input:
        image: a greyscale image
        target_image: the target image to match the input image
        returns a greyscale image after histogram matching
        """
    rows, cols = shape(image)
    total_pixels = rows * cols

    hist_input, _ = histogram(image.ravel(), 256, (0, 256))
    cdf_input = zeros(256)
    cdf_input[0] = hist_input[0]
    for i in range(1, 256):
        cdf_input[i] = cdf_input[i-1] + hist_input[i]
    cdf_input = cdf_input / total_pixels

    hist_target, _ = histogram(target_image.ravel(), 256, (0, 256))
    cdf_target = zeros(256)
    cdf_target[0] = hist_target[0]
    for i in range(1, 256):
        cdf_target[i] = cdf_target[i-1] + hist_target[i]
    cdf_target = cdf_target / (shape(target_image)[0] * shape(target_image)[1])

    mapping = zeros(256, uint8)
    for i in range(256):
        diff = abs(cdf_target - cdf_input[i])
        mapping[i] = uint8(diff.argmin())

    out_image = zeros((rows, cols), uint8)
    for i in range(rows):
        for j in range(cols):
            out_image[i, j] = mapping[image[i, j]]
    return out_image
