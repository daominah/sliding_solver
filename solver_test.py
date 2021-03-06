import solver


diffXExpectations = {
    0: 91,
    1: 164,
    2: 127,
    3: 36,
    4: 138,
    5: 159,
    6: 178,
    7: 171,
    8: 129,
    9: 370,
    10: 220,
    11: 152,
}

for i in range(0, 12):
    print("_"*40, " i ", i)
    try:
        piece = "./tests_slide/test%s_piece.png" % i
        background = "./tests_slide/test%s_background.png" % i
        solver0 = solver.SlidingSolver(piece, background)  # img 260x160
        diffX, pieceX = solver0.Solve(isDebug=False)
        print("ret: diffX: %s, pieceX: %s" % (diffX, pieceX))
        if i in diffXExpectations:
            expected = diffXExpectations[i]
            if not (expected*0.96 <= diffX <= expected*1.04):
                raise Exception("FAIL test diffX: real: %.1f, expected: %.1f" %
                                (diffX, expected))

    except Exception as err:  # file not found
        print(err)
        # if i  != 7:
        #     raise err

diffXExpectations2 = {
    0: 200,
    1: 271,
    2: 178,
    3: 220,
    4: 218,
    5: 208,
    6: 282,
    7: 246,
    8: 274,
    9: 205,
    10: 249,
    12: 148,
}

for i in range(0, len(diffXExpectations2)):
    print("_"*40, " i ", i)
    try:
        begin = "./tests_slide/test1%02d_bg_begin.png" % i
        moved = "./tests_slide/test1%02d_bg_moved.png" % i
        print(begin,moved)
        solver0 = solver.SlidingSolver2Background(begin, moved)
        diffX, pieceX = solver0.Solve(isDebug=False)
        print("ret: diffX: %s, pieceX: %s" % (diffX, pieceX))
        if i in diffXExpectations2:
            expected = diffXExpectations2[i]
            if not (expected*0.96 <= diffX <= expected*1.04):
                raise Exception("FAIL test diffX: real: %.1f, expected: %.1f" %
                                (diffX, expected))

    except Exception as err:  # file not found
        print(err)
        raise err

print("_"*40)
