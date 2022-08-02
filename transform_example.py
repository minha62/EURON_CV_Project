# import the necessary packages
import transform
import numpy as np
import argparse # for parsing command line arguments
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="path to the image file")
ap.add_argument("-c", "--coords", help="comma separated list of source points") # the list of 4 points representing the region of the image (top-down)
args = vars(ap.parse_args())

# load the image and grab the source coordinates
# (i.e. the list of (x,y) points)
# NOTE: using the 'eval' function is bad form, but for this example
# let's just roll with it -- in future posts I'll show you how to
# automatically determine the coordinates without pre-supplying them
image = cv2.imread(args["image"])
pts = np.array(eval(args["coords"]), dtype="float32") # convert the points to a numpy array
# eval function

# apply the four point transform to obtain a "birds eye view" of the image
warped = transform.four_point_transform(image, pts)

# show the original and warped images
cv2.imshow("Original", image)
cv2.imshow("Warped", warped)
cv2.waitKey(0)