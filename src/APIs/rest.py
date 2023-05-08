from flask import Flask, request
import requests
import time

app = Flask(__name__)

@app.route('/neural_network', methods=['GET', 'POST'])
def neural_network():
    if request.method == 'POST':
        return do_the_screening(request.args.get('resume'))
    else:
        return show_msg()

def do_the_screening(data):
    print(prepare_data(data))
    return prepare_data(data)

def show_msg():
    return "<p>Nothing here</p>"


def prepare_data(resume):
    resume = resume.lower()
    ps = list(";?.:!,")
    for p in ps:   
        resume = resume.replace(p, '')
    resume = resume.replace("    ", " ")
    resume = resume.replace('"', '')
    resume = resume.replace('\t', ' ')
    resume = resume.replace("'s", "")
    resume = resume.replace('\n', ' ')
    return resume
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
    url = "http://localhost:5000/neural_network"
    resume = "Some text from a resume"
    response = requests.post(url, data=resume)
    print(response.text)
