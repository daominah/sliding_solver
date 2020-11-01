from solver import PuzleSolver

diffXExpectations = {
    0: 91,
    1: 165,
    2: 127,
    3: 36,
    4: 137,
    5: 160,
}

for i in range(0, 6):
    print("_"*40, " i ", i)
    try:
        piece, background = "test%s_piece.png" % i, "test%s_background.png" % i
        solver = PuzleSolver(piece, background)  # img 260x160
        diffX, pieceX = solver.get_position()
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

if False:
    try:
        piece, background = "tmp_debug_piece.png", "tmp_debug_background.png"
        solver = PuzleSolver(piece, background)  # img 260x160
        diffX, pieceX = solver.get_position()
    except Exception as err:
        print("error tmp test: ", err)
