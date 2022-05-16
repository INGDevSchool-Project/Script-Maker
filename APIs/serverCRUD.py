from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

books = {}

@app.route('/books/<book_id>/', methods=["GET"])
def get_book(book_id):
    if books.get(book_id):
        message = jsonify(books[book_id])
        status_code = 200
    else:
        message = {'message': 'not found'}
        status_code = 404
    return make_response(
        message,
        status_code,
    )

@app.route('/search/', methods=["GET"])
def search():
    autor = str(request.args.get('author'))
    title = str(request.args.get('title'))
    label = request.args.getlist('label')

    if autor != "None":
        for i in range(1, marime+1):
            if books[str(i)]['author'] == autor:
                message = books[str(i)]
                status_code = 200
                return make_response(
                    message,
                    status_code,
                )

        message = {'message': 'not found'}
        status_code = 404
        return make_response(
            message,
            status_code,
        )

    if title != "None":
        for i in range(1, marime+1):
            if books[str(i)]['title'] == title:
                message = books[str(i)]
                status_code = 200
                return make_response(
                    message,
                    status_code,
                )

        message = {'message': 'not found'}
        status_code = 404
        return make_response(
            message,
            status_code,
        )
    if label:
        for i in range(1, marime+1):
            labeluri = books[str(i)]['labels']
            for j in label:
                for q in labeluri:
                    if j == q :
                        message = books[str(i)]
                        status_code = 200
                        return make_response(
                            message,
                            status_code,
                        )

        message = {'message': 'not found'}
        status_code = 404
        return make_response(
            message,
            status_code,
        )
@app.route('/books/', methods=["POST"])
def post_books():
    global books
    global marime
    books.update(request.get_json())
    marime = len(books)
    return make_response(
        {'message': 'updated'},
        200,
    )


@app.route('/books/<book_id>/', methods=["DELETE"])
def delete_books(book_id):
    global books
    if books.get(book_id):
        books.pop(book_id)
        message = {}
        status_code = 204
    else:
        message = {'message': 'not found'}
        status_code = 404
    return make_response(
        message,
        status_code,
    )


if __name__ == '__main__':
    app.run(debug=True)
