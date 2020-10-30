from solver import PuzleSolver


for i in range(0, 6):
    print("_"*40, " i ", i)
    try:
        piece, background = "test%s_piece.png" % i, "test%s_background.png" % i
        solver = PuzleSolver(piece, background)  # img 260x160
        diffX, pieceX = solver.get_position()
    except Exception as err:  # file not found
        if str(err).__contains__("src.empty"):
            continue
        print("error i %s: %s" % (i, err))
print("_"*40)

if True:
    try:
        piece, background = "tmp_debug_piece.png", "tmp_debug_background.png"
        solver = PuzleSolver(piece, background)  # img 260x160
        diffX, pieceX = solver.get_position()
    except Exception as err:
        print("error tmp test: ", err)
