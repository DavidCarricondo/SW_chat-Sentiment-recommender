from flask import Flask, request

app = Flask(__name__)

PORT=3500

@app.route('/')
def hola():
    return {'Ole': 'esta es tu api'}

if __name__ == '__main__':
    app.run('0.0.0.0',PORT, debug=True)