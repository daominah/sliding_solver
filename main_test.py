from solver import PuzleSolver


for i in range(0, 10):
    try:
        if i == 2:
            print("_"*120)
        piece, background = "test%s_piece.png" % i, "test%s_background.png" % i
        solver = PuzleSolver(piece, background)  # img 260x160
        diffX, pieceX = solver.get_position()
        print("solution for i %s: diffX: %s, pieceX: %s" % (i, diffX, pieceX))
    except Exception as err:  # file not found
        if str(err).__contains__("src.empty"):
            continue
        print("err i %s: %s" % (i, err))
print("_"*120)
