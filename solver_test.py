from solver import SlidingSolver

diffXExpectations = {
    0: 91,
    1: 164,
    2: 127,
    3: 36,
    4: 138,
    5: 159,
}

for i in range(0, 6):
    print("_"*40, " i ", i)
    try:
        piece, background = "test%s_piece.png" % i, "test%s_background.png" % i
        solver = SlidingSolver(piece, background)  # img 260x160
        diffX, pieceX = solver.Solve()
        print("ret: diffX: %s, pieceX: %s" % (diffX, pieceX))
        if i in diffXExpectations:
            expected = diffXExpectations[i]
            if not (expected*0.96 <= diffX <= expected*1.04):
                raise Exception("FAIL test diffX: real: %.1f, expected: %.1f" %
                                (diffX, expected))

    except Exception as err:  # file not found
        if str(err).__contains__("src.empty"):
            continue
        else:
            raise err
print("_"*40)
