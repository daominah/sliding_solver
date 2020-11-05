import cv2 as cv
import solver


if __name__ == '__main__': # TODO: features matching chinese captcha
    img1Gray = cv.imread("/home/tungdt/Desktop/test14_order.png", cv.IMREAD_GRAYSCALE)
    img2Gray = cv.imread("/home/tungdt/Desktop/test11_bg.png", cv.IMREAD_GRAYSCALE)

    # img1, img2 = img1Gray, img2Gray
    img1 = solver.CalcImageEdge(img1Gray)
    img2 = solver.CalcImageEdge(img2Gray)

    # keyPoints and descriptors result from a feature detector
    kp1, des1, kp2, des2 = None, None, None, None
    if True:
        sift = cv.SIFT_create()
        kp1, des1 = sift.detectAndCompute(img1, None)
        # imgDebug = cv.drawKeypoints(img1, kp1, None, color=(0, 255, 0), flags=0)
        # cv.imshow("", imgDebug); cv.waitKey()
        kp2, des2 = sift.detectAndCompute(img2, None)
    else:
        orb = cv.ORB_create()
        kp1 = orb.detect(img1, None)
        kp1, des1 = orb.compute(img1, kp1)
        imgDebug = cv.drawKeypoints(img1, kp1, None, color=(0, 255, 0), flags=0)
        cv.imshow("", imgDebug); cv.waitKey()
        kp2 = orb.detect(img2, None)
        kp2, des2 = orb.compute(img2, kp2)

    bf = cv.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < 0.8*n.distance:
            good.append(m)

    MIN_MATCH_COUNT = 4
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()
        h, w = img1.shape
        pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
        dst = cv.perspectiveTransform(pts, M)
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
