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
        piece, background = "test%s_piece.png" % i, "test%s_background.png" % i
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
}

for i in range(0, 4):
    print("_"*40, " i ", i)
    try:
        begin, moved = "test10%s_bg_begin.png" % i, "test10%s_bg_moved.png" % i
        solver0 = solver.SlidingSolver2Background(begin, moved)
        diffX, pieceX = solver0.Solve()
        print("ret: diffX: %s, pieceX: %s" % (diffX, pieceX))
        if i in diffXExpectations:
            expected = diffXExpectations2[i]
            if not (expected*0.96 <= diffX <= expected*1.04):
                raise Exception("FAIL test diffX: real: %.1f, expected: %.1f" %
                                (diffX, expected))

    except Exception as err:  # file not found
        raise err

print("_"*40)
