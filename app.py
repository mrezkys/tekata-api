

from flask import Flask
from flask import jsonify
import random
from kbbi import KBBI
from kbbi import TidakDitemukan

app = Flask(__name__)

import time
from flask import g

@app.before_request
def before_request():
    g.start = time.time()

@app.after_request
def after_request(response):
    diff = time.time() - g.start
    if ((response.response) and
        (200 <= response.status_code < 300) and
        (response.content_type.startswith('text/html'))):
        response.set_data(response.get_data().replace(
            b'__EXECUTION_TIME__', bytes(str(diff), 'utf-8')))
    print(bytes(str(diff), 'utf-8'))
    return response

@app.route('/check=<word>')
def word_check(word):
    try:
        result = KBBI(word)
        return {
            'status' : True,
            'message' : 'Terdapat di KBBI ',
            'data' : result.__str__(),
        }
    except TidakDitemukan as e:
        return {
            'status' : False,
            'message' : e,
        }

@app.route('/level=<level>/word')
def word(level):
    if level == '5': filename = 'data/5kata.txt'
    elif level == '4': filename = 'data/4kata.txt'
    else: filename = 'data/3kata.txt'

    with open(filename) as file:
        f = file.read()
        words = list(map(str, f.split()))
        key = random.choice(words)

    return {
      'status' : True,
      'key' : key,
    }

@app.route('/answer=<answer>&key=<key>')
def hello(answer, key):
    kbbi_check = word_check(answer)
    print(kbbi_check)
    if kbbi_check['status'] == True:
        result = list()
        all_true = True
        for i, word in enumerate(answer):
            if key.find(word)  == -1:
                result.append('false')
                all_true = False
            elif word == key[i]:
                result.append('true')
            else:
                result.append('wrong')
                all_true = False

        return {
            'status' : all_true,
            'data' :   result,
            'kbbi' : kbbi_check['data'],
        }
    else :
        return {
            'status' : False,
        }

if __name__ == "__main__":
  app.run()