import base64
import json
import tempfile

from flask import Flask
from flask import request

from solver import PuzleSolver


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
        reqBody = request.json
        pieceBase64 = reqBody["Piece"]
        pieceBase64 = removePrefix(pieceBase64, imgBase64Prefix)
        backgroundBase64 = reqBody["Background"]
        backgroundBase64 = removePrefix(backgroundBase64, imgBase64Prefix)

        pieceFile = tempfile.NamedTemporaryFile()
        # pieceFile = open("tmp_debug_piece.png", "wb")  # debug only
        pieceFile.write(base64.b64decode(pieceBase64))

        backgroundFile = tempfile.NamedTemporaryFile()
        # backgroundFile = open("tmp_debug_background.png", "wb")  # debug only
        backgroundFile.write(base64.b64decode(backgroundBase64))

        piece, background = pieceFile.name, backgroundFile.name
        print("piece: %s, background: %s" % (piece, background))
        solver0 = PuzleSolver(piece, background)
        diffX, pieceX = solver0.get_position()
        pieceFile.close()
        backgroundFile.close()
        return {"DiffX": diffX, "PieceLeftX": pieceX}
    except Exception as err:
        return str(err), 400


if __name__ == '__main__':
    print("_" * 80)
    print("page home http://127.0.0.1:15715/")
    print("page solve http://127.0.0.1:15715/solve POST")
    print("_" * 80)
    app.run(port=15715, host="0.0.0.0")
