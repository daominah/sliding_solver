from solver import PuzleSolver


for i in range(0, 3):
    piece, background = "test%s_piece.png" % i, "test%s_background.png" % i
    solver = PuzleSolver(piece, background)  # img 260x160
    solution = solver.get_position()
    print("solution for i %s: %s" % (i, solution))
