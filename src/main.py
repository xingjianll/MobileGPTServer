from flask import Flask, request
from src.llm import ChatGPT

app = Flask(__name__)

f = open("config.txt", "r")

llm = ChatGPT(f.read())

@app.route('/', methods=['POST'])
def response():
    print(request.get_json(force=True))
    return llm.get_response(request.get_json(force=True)['conversation'])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4396)
