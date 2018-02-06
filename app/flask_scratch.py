"""
    This is just a playground for flask. Not for production.
"""

from flask import Flask
from flask import url_for, abort, redirect, render_template, make_response, session, request, escape


app = Flask(__name__)
app.secret_key = '\xf1\xe9\n =o\xc9\xbd"\x800\xdd^\xb2{\x92\xda\xa8_\x8bBX\x99W'


@app.route('/')
def index():
    if 'username' in session:
        return 'you are logged in as: {}. <a href=\"{}\">logout</a>'.format(escape(session['username']),
                                                                            url_for('logout'))
    return "you are not logged in. log in <a href=\"{}\">click here</a>".format(url_for('login'))


@app.route('/projects/')
def projects():
    return "the projects page"


@app.route('/about')
def about():
    return "the about page"


# response example
@app.route('/resp')
def resp_example():
    resp = make_response('this is text', 201)
    resp.headers['x-custom-header'] = 'dina'
    return resp


@app.route('/ab')
def ab():
    app.logger.debug('this is a debug message')
    abort(404)
    return redirect(url_for('about'))


@app.errorhandler(404)
def page_not_found(error):
    return 'page not found: {}'.format(error), 200


# session example, use the secret key above
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
# end of session example


if __name__ == "__main__":
    app.run(debug=True)

