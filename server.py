from config.Factory import ConfigFactory
from datasets import download_datasets
from flask import Flask, json, render_template, request
from runner.Runner import Runner
from services.files import get_files_info
import os.path

download_datasets()
app = Flask(__name__)

@app.route("/")
def index():
    files = get_files_info()
    return render_template('index.html', files=files)

@app.route('/test/<id>')
def show(id):
    config = ConfigFactory.from_name(id)
    return render_template('test.html', config=config, id=id)

@app.route('/test/<id>/run', methods=['POST'])
def run(id):
    iterations = request.form.get('iterations')
    if iterations is None or int(iterations) <= 0:
        return json.dumps({'error': 'Invalid number of iterations'})
    
    threads = list(map(int, map(str.strip, request.form.get('threads').split(','))))
    print(threads)
    min_cores = request.form.get('min_cores', 1)
    max_cores = request.form.get('max_cores', 10)
    
    config = ConfigFactory.from_name(id)
    runner = Runner(os.path.join('datasets', id + '.csv'), int(iterations), config, threads=threads, min_cores=min_cores, max_cores=max_cores)
    runner.run()
    return json.dumps({'success': True, 'results': runner.results})

app.run(debug=True)