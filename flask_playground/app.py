from flask import Flask, render_template, request, url_for
import psutil
import matplotlib.pyplot as plt; plt.rcdefaults()
import datetime
import numpy as np
import logging
import os

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

@app.route('/fizzbuzz/<fizz_number>')
def fizz(fizz_number):
    fizz_number = int(fizz_number)
    def fizzBuzz(fizz_number):
    count = 1
    _returnString = '<div>'
    while count <= fizz_number:
        _fizz = ''
        _buzz = ''
        if count % 2 == 0 or count % 3 == 0:
            _fizz = 'fizz'
        
        if count % 2 == 1 or count % 3 == 0:
            _buzz = 'buzz'
            
        _returnString += f"<div>{_fizz}{_buzz}\n</div>"

        count += 1

    _returnString += '</div>'
    return _returnString

@app.route('/reverse/<_reverse_string>', methods=['GET'])
def reverseString(_reverse_string):
    _input_string = _reverse_string
    _output_string = ''

    _input_len = len(_input_string) - 1

    while _input_len >= 0:
        _output_string += _input_string[_input_len]
        _input_len -= 1

    return(_output_string)

# this route will create a simple bar chart of your basic CPU percent utilization over x seconds
@app.route('/cpu_load/<_seconds>')
def cpu_load(_seconds):
    _interval = int(_seconds)
    _times = []
    _cpu_utilization = []
    _start_time =  datetime.datetime.now().strftime("%H:%M:%S")

    for x in range(_interval):
        _now = datetime.datetime.now().strftime("%M:%S")
        logging.info(x)
        logging.info(_now)
        _times.append(_now)
        _cpu_usage = psutil.cpu_percent(interval=1)
        logging.info(_cpu_usage)
        _cpu_utilization.append(_cpu_usage)

    y_pos = np.arange(len(_times))
    plt.bar(y_pos, _cpu_utilization, align='center', alpha=.05)
    plt.xticks(y_pos, _times, rotation='vertical')
    plt.ylabel('Usage')
    plt.title(f'CPU Utilization over {_interval} seconds, from {_start_time}')
    plt.savefig(f'./static/fig{_start_time}.png')

    full_filename = f"/fig{_start_time}.png"
    return render_template("index.html", cpu_chart = full_filename)

if __name__ == "__main__":
    app.run(debug=True)