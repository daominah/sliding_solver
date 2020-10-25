# Solver for GeeTest's sliding CAPTCHA

## API

This server listens HTTP on port 15715 (hard coded).

### [/solve](http://127.0.0.1:15715/solve) POST

Example request body:

````json
{
    "Piece": "base64ed",
    "Background": "base64ed"
}
````

Response (position X of the piece to the background):

````json
{
    "MostLeftX": 91
}
````

## Dockerfile

````bash
docker build --tag=daominah/sliding_solver .

docker run --rm -p 15715:15715 -v ${PWD}:/python/src/app daominah/sliding_solver
````

## References

* Origin project: [peduajo/geetest-slice-captcha-solver](https://github.com/peduajo/geetest-slice-captcha-solver)

* [OpenCV](https://pypi.org/project/opencv-python/3.4.11.43/) for Python
