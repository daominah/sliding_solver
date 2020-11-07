import base64
import json
import os
import tempfile

from flask import Flask
from flask import request

from solver import SlidingSolver, SlidingSolver2Background


app = Flask(__name__)


@app.route('/')
def handleIndex():
    return """<html>
<head><title>Solver for GeeTest's sliding CAPTCHA</title></head>
<body>
    <h1>Solver for GeeTest's sliding CAPTCHA</h1>
    <br/>
    <div>
        <h3>/solve POST<h3>
        <p>Example request body:</p>
        <pre>
{
    "Piece": "",
    "Background": ""
}
        </pre>
        <p>Response (position X of the piece to the background):</p>
        <pre>
{
    "MostLeftX": 91
}
        </pre>
    </div>
</body>
</html>"""


imgBase64Prefix = "data:image/png;base64,"  # const


def removePrefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


@app.route('/solve', methods=['GET', 'POST'])
def handleSolve():
    if request.method == 'GET':
        return "Use POST request to send images data: " + \
               json.dumps({"Piece": "base64ed", "Background": "base64ed"}), \
               404

    try:
        print('*'*40)
        reqBody = request.json
        pieceBase64 = reqBody["Piece"]
        pieceBase64 = removePrefix(pieceBase64, imgBase64Prefix)
        backgroundBase64 = reqBody["Background"]
        backgroundBase64 = removePrefix(backgroundBase64, imgBase64Prefix)

        pieceFile = tempfile.NamedTemporaryFile(suffix=".png")
        # pieceFile = open("tmp_debug_piece.png", "wb")  # debug only
        pieceFile.write(base64.b64decode(pieceBase64))

        backgroundFile = tempfile.NamedTemporaryFile(suffix=".png")
        # backgroundFile = open("tmp_debug_background.png", "wb")  # debug only
        backgroundFile.write(base64.b64decode(backgroundBase64))

        piece, background = pieceFile.name, backgroundFile.name
        print("request /solve: piece: %s (%.1f kB), background: %s (%.1f kB)" % (
            piece, len(pieceBase64)/1365, background, len(backgroundBase64)/1365))
        if os.getenv("IS_DEBUG"):
            print("pieceBase64:")
            print(imgBase64Prefix+pieceBase64)
            print("backgroundBase64:")
            print(imgBase64Prefix+backgroundBase64)

        solver0 = SlidingSolver(piece, background)
        diffX, pieceX = solver0.Solve()
        pieceFile.close()
        backgroundFile.close()
        ret = {"DiffX": diffX, "PieceLeftX": pieceX}
        print("response: ", ret)
        return ret
    except Exception as err:
        print("error handleSolve: ", err)
        return str(err), 400


@app.route('/solve2', methods=['GET', 'POST'])
def handleSolve2():
    if request.method == 'GET':
        return "Use POST request to send images data: " + \
               json.dumps({"BeginBackground": "base64ed",
                           "MovedBackground": "base64ed"}), \
               404

    try:
        print('*'*40)
        reqBody = request.json
        beginBGData = reqBody["BeginBackground"]
        beginBGData = removePrefix(beginBGData, imgBase64Prefix)
        movedBGData = reqBody["MovedBackground"]
        movedBGData = removePrefix(movedBGData, imgBase64Prefix)

        beginBGFile = tempfile.NamedTemporaryFile(suffix=".png")
        beginBGFile.write(base64.b64decode(beginBGData))
        movedBGFile = tempfile.NamedTemporaryFile(suffix=".png")
        movedBGFile.write(base64.b64decode(movedBGData))

        print("request /solve2: piece: %s (%.1f kB), background: %s (%.1f kB)" % (
            beginBGFile.name, len(beginBGData)/1365,
            movedBGFile.name, len(movedBGData)/1365))
        if os.getenv("IS_DEBUG"):
            print("beginBGData:")
            print(imgBase64Prefix+beginBGData)
            print("movedBGData:")
            print(imgBase64Prefix+movedBGData)

        solver2 = SlidingSolver2Background(beginBGFile.name, movedBGFile.name)
        diffX, pieceX = solver2.Solve()
        beginBGFile.close()
        movedBGFile.close()
        ret = {"DiffX": diffX, "PieceLeftX": pieceX}
        print("response: ", ret)
        return ret
    except Exception as err:
        print("error handleSolve: ", err)
        return str(err), 400


if __name__ == '__main__':
    print("_" * 80)
    print("page home http://127.0.0.1:15715/")
    print("page solve http://127.0.0.1:15715/solve POST")
    print("_" * 80)
    app.run(port=15715, host="0.0.0.0")
