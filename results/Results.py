from uuid import uuid4
import os, json, time, psutil
import pandas as pd

class Results:
    def __init__(self, name: str, file: str, version: int):
        self.uuid = uuid4().hex
        self.name = name
        self.data = {
            'name': name,
            'file': file,
            'version': version,
            'started_at': time.time()
        }
    
    def measure(self):
        self.data['ended_at'] = time.time()
        self.data['duration'] = self.data['ended_at'] - self.data['started_at']
        self.data['cpu_usage'] = psutil.cpu_percent(interval=self.data['duration'])
        self.data['ram'] = psutil.virtual_memory().percent
        self.data['available_memory'] = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total

    def save(self):
        self.create_dir()
        path = os.path.join(os.getcwd(), 'data', self.uuid + '.json')
        with open(path, 'w') as f:
            json.dump(self.data, f)

        self.save_history()

    def save_history(self):
        self.create_dir()
        csv_path = os.path.join(os.getcwd(), 'data', 'history.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df = df.append(self.data, ignore_index=True)
        else:
            df = pd.DataFrame([self.data])

        df.to_csv(csv_path, index=False)

    def create_dir(self):
        path = os.path.join(os.getcwd(), 'data')
        if not os.path.exists(path):
            os.mkdir(path)