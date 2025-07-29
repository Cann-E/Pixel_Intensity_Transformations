
from dip import imwrite, imread
import matplotlib
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from pointops.linearpointops import *
from pointops.nonlinearpointops import *
import os
import math

matplotlib.use('Agg')

__author__ = "Pranav Mantini"
__email__ = "pmantini@uh.edu"
__version__ = "1.0.0"


def to_low_contrast(image):
    low_contrast_image = array(image, dtype=float64)
    low_contrast_image = low_contrast_image * 0.25
    low_contrast_image = low_contrast_image + 100
    return uint8(low_contrast_image)


def save_images(in_image, output_image, output_name):
    in_hist, _ = histogram(in_image.ravel(), 256, (0, 256))
    output_hist, _ = histogram(output_image.ravel(), 256, (0, 256))
    imwrite(output_name+".jpg", output_image)
    plt.figure()
    plt.plot(in_hist, label='Input')
    plt.plot(output_hist, label='Output')
    plt.legend()
    plt.savefig("%s_hist.png"%output_name)


def main():
    """ The main function that parses input arguments, calls the appropriate
        interpolation method and writes the output image """

    parser = ArgumentParser()
    parser.add_argument("-p", "--p-value", dest="p",
                        help="Parameter P for Linear Point Operations (PX+L)", metavar="P", type=float)
    parser.add_argument("-l", "--l-value", dest="l",
                        help="Parameter L for Linear Point Operations (PX+L)", metavar="L", type=float)
    args = parser.parse_args()

    output_directory = "output"

    lenna_file = "Lenna.png"
    lenna_low_contrast = "Lenna_low_contrast.jpg"
    ultrasound_file = "ultrasound.png"

    #Load test images
    image_lenna = imread(lenna_file, 0)
    image_lenna_low_contrast = imread(lenna_low_contrast, 0)
    image_ultrasound = imread(ultrasound_file, 0)

    if args.p is None:
        print("Parameter P for linear point operation (PX+L) is not defined, using default 0.75")
        p = 0.75
    else:
        p = args.p

    if args.l is None:
        print("Parameter L for linear point operation (PX+L) is not defined, using default 25")
        l = 25
    else:
        l = args.l

    # Linear Point Operations
    output = linear_point_operation(image_lenna, p, l)
    output_name_base = os.path.join(output_directory, "linear_point_ops_%s_%s"%(p,l))
    save_images(image_lenna, output, output_name_base)

    # Image Negative
    output = image_negative(image_lenna)
    output_name_base = os.path.join(output_directory, "image_negative")
    save_images(image_lenna, output, output_name_base)

    # Full Contrast stretch
    output = full_contrast_stretch(image_lenna_low_contrast)
    output_name_base = os.path.join(output_directory, "fcs")
    save_images(image_lenna_low_contrast, output, output_name_base)

    # Log Transform
    output = log_transform(image_ultrasound)
    output_name_base = os.path.join(output_directory, "log_transform")
    save_images(image_ultrasound, output, output_name_base)

    # Histogram Flattening
    output = histogram_flattening(image_lenna_low_contrast)
    output_name_base = os.path.join(output_directory, "hist_flat")
    save_images(image_lenna_low_contrast, output, output_name_base)

    # Histogram Shaping
    def norm_pty(x, mean, sigma):
        std = sigma ** 2
        factor = 1 / (2 * math.pi * std) ** 0.5
        exponent = -(x - mean) ** 2 / 2 * std
        return math.exp(exponent) * factor

    target_dist = [norm_pty(x, 128, 0.01) for x in range(255)]
    output = histogram_shaping(image_lenna_low_contrast, target_dist)
    output_name_base = os.path.join(output_directory, "hist_shaping")
    save_images(image_lenna_low_contrast, output, output_name_base)

    # Histogram Matching
    output = histogram_matching(image_lenna_low_contrast, image_lenna)
    output_name_base = os.path.join(output_directory, "hist_matching")
    save_images(image_lenna_low_contrast, output, output_name_base)


if __name__ == "__main__":
    main()