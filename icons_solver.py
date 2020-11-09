import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


# twitch params for features matching chinese captcha
def CalcImageEdge3(imgGrey, isPiece=False):
    img1 = np.uint8(imgGrey)
    if isPiece:
        img1 = cv.bitwise_not(img1)
        h, w = img1.shape
        img1 = cv.resize(img1, (4*w, 4*h), )
        img1 = cv.addWeighted(img1, 1.2, np.zeros(img1.shape, dtype=np.uint8), 0, 0)
        # img1 = cv.GaussianBlur(img1, (3, 3), 0)
        # plt.imshow(img1, 'gray'), plt.show()

        pass
    else:
        # img1 = cv.bilateralFilter(img1, 5, 75, 75)
        img1 = cv.GaussianBlur(img1, (3, 3), 0)
        pass
    # plt.imshow(img1, 'gray'), plt.show()

    scale = 1
    delta = 0
    ddepth = cv.CV_16S
    grad_x = cv.Sobel(img1, ddepth, 1, 0, ksize=3, scale=scale,
                      delta=delta, borderType=cv.BORDER_DEFAULT)
    grad_y = cv.Sobel(img1, ddepth, 0, 1, ksize=3, scale=scale,
                      delta=delta, borderType=cv.BORDER_DEFAULT)
    abs_grad_x = cv.convertScaleAbs(grad_x)
    abs_grad_y = cv.convertScaleAbs(grad_y)
    img1 = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    # whoCare, ret = cv.threshold(ret, 85, 255, cv.THRESH_BINARY)

    # plt.imshow(img1, 'gray'), plt.show()
    return img1


def FeatureMatch(iconGray, backgroundGray):
    img1, img2 = iconGray, backgroundGray

    img1 = CalcImageEdge3(iconGray, isPiece=True)
    img2 = CalcImageEdge3(backgroundGray)

    # kp1, des1, kp2, des2: keyPoints and descriptors from feature detector
    # the larger contrastThreshold , the less features
    # the larger edgeThreshold, the more edge-like features
    sift = cv.SIFT_create(contrastThreshold=0.1024, edgeThreshold=6)
    kp1, des1 = sift.detectAndCompute(img1, None)
    # print("len(kp1): ", len(kp1))

    sift2 = cv.SIFT_create(contrastThreshold=0.09, edgeThreshold=4)
    # imgDebug = cv.drawKeypoints(img1, kp1, None, color=(0, 255, 0), flags=0); plt.imshow(imgDebug, 'gray'), plt.show()
    kp2, des2 = sift2.detectAndCompute(img2, None)
    # imgDebug = cv.drawKeypoints(img2, kp2, None, color=(0, 255, 0), flags=0); plt.imshow(imgDebug, 'gray'), plt.show()

    good = []
    if True:
        bf = cv.BFMatcher()  # brute force matcher
        matches = bf.knnMatch(des1, des2, k=2)
        # store all the good matches as per Lowe's ratio test.
        for m, n in matches:
            if m.distance < 0.8*n.distance:
                good.append(m)
    else:
        bf = cv.BFMatcher(crossCheck=True)
        matches = bf.match(des1, des2)
        for m in matches: good.append(m)
    print("len(good matches): ", len(good))

    MIN_MATCH_COUNT = 4

    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        # print("src_pts: ", src_pts.shape, src_pts)
        # print("dst_pts: ", dst_pts.shape, dst_pts)
        transformation, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 1)
        # transformation, mask = cv.findHomography(src_pts, dst_pts, cv.RHO, 1)
        matchesMask = mask.ravel().tolist()
        h, w = img1.shape
        pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
        # print("transformation: ", transformation)
        if transformation is not None:
            dst = cv.perspectiveTransform(pts, transformation)
            img2 = cv.polylines(img2, [np.int32(dst)], True, 255, 3, cv.LINE_AA)
    else:
        print("not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
        matchesMask = None

    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=(255, 0, 0),
                       matchesMask=matchesMask,  # draw only inliers
                       flags=2)
    img3 = cv.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)
    plt.imshow(img3, 'gray'), plt.show()
