import cv2
import numpy as np


# CropPiece crops the first object (top left) on a empty background
def CropPiece(imgGray):  # return [cropped, w0, h0, w2, h2]
    denseRowIdxs = []
    denseColIdxs = []
    height, width = imgGray.shape
    isMeetPiece = False
    for rowI in range(height):
        isEmptyRow = True
        for e in imgGray[rowI, :]:
            if e != 0:
                denseRowIdxs.append(rowI)
                isMeetPiece = True
                isEmptyRow = False
        if isMeetPiece and isEmptyRow:
            break
    isMeetPiece2 = False
    for colI in range(width):
        isEmptyRow = True
        for e in imgGray[:, colI]:
            if e != 0:
                denseColIdxs.append(colI)
                isMeetPiece2 = True
                isEmptyRow = False
        if isMeetPiece2 and isEmptyRow:
            break
    w0 = denseColIdxs[0]
    h0 = denseRowIdxs[0]
    w2 = denseColIdxs[-1]
    h2 = denseRowIdxs[-1]
    # print("debug CropPiece w0, h0, w2, h2: ", w0, h0, w2, h2)
    return imgGray[h0:h2, w0:w2], w0, h0, w2, h2


def CalcImageEdge(imgGrey):
    scale = 1
    delta = 0
    ddepth = cv2.CV_16S
    imgBlur = cv2.GaussianBlur(imgGrey, (3, 3), 0)
    grad_x = cv2.Sobel(imgBlur, ddepth, 1, 0, ksize=3, scale=scale,
                       delta=delta, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(imgBlur, ddepth, 0, 1, ksize=3, scale=scale,
                       delta=delta, borderType=cv2.BORDER_DEFAULT)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    return grad


class SlidingSolver:
    def __init__(self, piecePath, backgroundPath):
        self.pieceGray = None
        self.backgroundGray = None
        try:
            self.pieceGray = cv2.imread(piecePath, cv2.IMREAD_GRAYSCALE)
        except Exception as err:
            raise Exception("error imread piece: ", err)
        if self.pieceGray is None:
            raise Exception("error piece is nil")
        try:
            self.backgroundGray = cv2.imread(backgroundPath, cv2.IMREAD_GRAYSCALE)
        except Exception as err:
            raise Exception("error imread background: ", err)
        if self.backgroundGray is None:
            raise Exception("error background is nil")

    # Solve returns diffX and pieceLeftX
    def Solve(self):
        pieceInBGEdge = CalcImageEdge(self.pieceGray)
        pieceEdge, pLeftX, _, _, _ = CropPiece(pieceInBGEdge)
        # cv2.imshow("pieceEdge: ", pieceEdge); cv2.waitKey()
        backgroundEdge = CalcImageEdge(self.backgroundGray)
        # cv2.imshow("backgroundEdge: ", backgroundEdge); cv2.waitKey()
        similarMap = cv2.matchTemplate(backgroundEdge, pieceEdge,
                                       cv2.TM_CCOEFF_NORMED)
        _, _, _, maxMatchLocation = cv2.minMaxLoc(similarMap)
        diffX = maxMatchLocation[0] - pLeftX
        # print("debug SlidingSolver: diffX: %s, pieceX: %s" % (diffX, pLeftX))
        return diffX, pLeftX


class SlidingSolver2Background:
    def __init__(self, beginBGPath, movedBGPath):
        self.beginGray = None
        self.movedGray = None
        try:
            self.beginGray = cv2.imread(beginBGPath, cv2.IMREAD_GRAYSCALE)
        except Exception as err:
            raise Exception("error imread beginBG: ", err)
        if self.beginGray is None:
            raise Exception("error beginBG is nil")
        try:
            self.movedGray = cv2.imread(movedBGPath, cv2.IMREAD_GRAYSCALE)
        except Exception as err:
            raise Exception("error imread movedBG: ", err)
        if self.movedGray is None:
            raise Exception("error movedBG is nil")

    # Solve returns diffX and pieceLeftX
    def Solve(self):
        diffEdge = CalcImageEdge(self.beginGray - self.movedGray)
        pieceEdge, pLeftX, _, pRightX, _ = CropPiece(diffEdge)
        # cv2.imshow("pieceEdge", pieceEdge); cv2.waitKey()

        replacer = np.zeros((self.beginGray.shape[0], pRightX))
        originGrayWithoutLeftPiece = np.concatenate(
            (replacer, self.beginGray[:, pRightX:]), axis=1)

        originEdge = CalcImageEdge(originGrayWithoutLeftPiece)
        # cv2.imshow("originEdge", originEdge); cv2.waitKey()
        simMap = cv2.matchTemplate(originEdge, pieceEdge, cv2.TM_CCOEFF_NORMED)
        _, _, _, maxMatchLocation = cv2.minMaxLoc(simMap)
        diffX = maxMatchLocation[0] - pLeftX
        print("debug SlidingSolver: diffX: %s, pieceX: %s" % (diffX, pLeftX))
        return diffX, pLeftX
