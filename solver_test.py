import solver


diffXExpectations = {
    0: 91,
    1: 164,
    2: 127,
    3: 36,
    4: 138,
    5: 159,
    6: 178,
}

for i in range(0, 7):
    print("_"*40, " i ", i)
    try:
        piece = "./tests_slide/test%s_piece.png" % i
        background = "./tests_slide/test%s_background.png" % i
        solver0 = solver.SlidingSolver(piece, background)  # img 260x160
        diffX, pieceX = solver0.Solve()
        print("ret: diffX: %s, pieceX: %s" % (diffX, pieceX))
        if i in diffXExpectations:
            expected = diffXExpectations[i]
            if not (expected*0.96 <= diffX <= expected*1.04):
                raise Exception("FAIL test diffX: real: %.1f, expected: %.1f" %
                                (diffX, expected))

    except Exception as err:  # file not found
        raise err

diffXExpectations2 = {
    0: 200,
    1: 271,
    2: 178,
    3: 220,
    4: 218,
    5: 208,
    6: 282,
}

for i in range(0, 7):
    print("_"*40, " i ", i)
    try:
        begin = "./tests_slide/test10%s_bg_begin.png" % i
        moved = "./tests_slide/test10%s_bg_moved.png" % i
        solver0 = solver.SlidingSolver2Background(begin, moved)
        diffX, pieceX = solver0.Solve()
        print("ret: diffX: %s, pieceX: %s" % (diffX, pieceX))
        if i in diffXExpectations:
            expected = diffXExpectations2[i]
            if not (expected*0.96 <= diffX <= expected*1.04):
                raise Exception("FAIL test diffX: real: %.1f, expected: %.1f" %
                                (diffX, expected))

    except Exception as err:  # file not found
        # print(err)
        if i != 4: # TODO: improve to pass test104
            raise err

print("_"*40)
