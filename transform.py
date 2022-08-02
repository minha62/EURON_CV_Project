# import the necessary packages
import numpy as np
import cv2

def order_points(pts):
    # initialize a list of coordinates that will be ordered
    # allocate memory for the four ordered points
    # ordered by top-left, top-right, botton-right, botton-left
    rect = np.zeros((4,2), dtype="float32")

    # the top-left point will have the smallest x+y sum
    # whereas the botton-right point will have the largest x+y sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # compute the difference btw the points
    # the top-right point will have the smallest difference,
    # whereas the botton-left point will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmin(diff)]

    # return the ordered coordinates
    return rect


def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack these coordinates
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # determine the dimensions of our new warped image
    # compute the width of the new image,
    # which will be the largest distance
    # btw bottom-right and botton-left x-coordinates
    # or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image,
    # which will be the maximum distance 
    # btw the top-right and bottom-right y-coordinates
    # or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # we have the dimensions of the new image,
    # construct the set of destination points to obtain a "birds eye view"
    # (i.e. top-down view) of the image
    # again specifying points in the top-left, top-right, bottom-right, bottom-left order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    
    # compute the perspective transform matrix and then apply it
    # cv2.getPerspectiveTansform function requires two arguments
    #    'rect' - list of 4 ROI points in the original image
    #    'dst'  - list of transformed image
    #     returns M, which is the actual transformation matrix
    M = cv2.getPerspectiveTransform(rect, dst) 
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight)) # top-down view

    # return the warped image
    return warped