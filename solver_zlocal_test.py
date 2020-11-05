import solver


# begin = "/home/tungdt/Desktop/zbegin.png"
# moved = "/home/tungdt/Desktop/zmoved.png"

begin = "tests_slide/test109_bg_begin.png"
moved = "tests_slide/test109_bg_moved.png"

solver0 = solver.SlidingSolver2Background(begin, moved)
diffX, pieceX = solver0.Solve(isDebug=True)
print("ret: diffX: %s, pieceX: %s" % (diffX, pieceX))
