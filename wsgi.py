from server import app

if __name__ == "__main__":
    print 'starting from wsgi.py..'
    app.run(debug=True)
