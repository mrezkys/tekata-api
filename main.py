

from flask import Flask
from flask import jsonify
import random
from kbbi import KBBI
from kbbi import TidakDitemukan

app = Flask(__name__)

@app.route('/check=<word>')
def word_check(word):
    try:
        result = KBBI(word)
        return {
            'status' : True,
            'message' : 'Terdapat di KBBI',
            'data' : result,
        }
    except TidakDitemukan as e:
        return {
            'status' : False,
            'message' : e,
        }

@app.route('/level=<level>/word')
def word(level):
    if level == '5': filename = '5kata.txt'
    elif level == '4': filename = '4kata.txt'
    else: filename = '3kata.txt'

    with open(filename) as file:
        f = file.read()
        words = list(map(str, f.split()))
        key = random.choice(words)

    return key

@app.route('/answer=<answer>&key=<key>')
def hello(answer, key):
    kbbi_check = word_check(answer)
    print(kbbi_check)
    if kbbi_check['status'] == True:
        def check_index(char, word):
            try:
                return word.index(char)
            except ValueError:
                return 'not found'

        word_index = 0
        result = list()
        for word in answer:
            check = check_index(word, key)
            if check == 'not found':
                print(word + ' tidak ada')
                result.append('false')
            else:
                if word_index == check:
                    print(word + ' posisi benar')
                    result.append('true')
                elif word_index != check:
                    print(word + ' posisi salah')
                    result.append('wrong')
            word_index+=1

        return {
            'status' : True,
            'data' :   result,
        }
    else :
        return {
            'status' : False,
        }
    
if __name__ == '__main__':
    app.run(debug=True)
