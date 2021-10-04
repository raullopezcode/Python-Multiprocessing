import pandas as pd
from tqdm.auto import tqdm
from runner.SingleCore import SingleCore

class Runner:
    def __init__(self, path: str, iterations: int, config: dict):
        self.path = path
        self.config = config
        self.iterations = iterations
        self.df = pd.read_csv(path)
        self.results = []
    
    def run(self):
        methods = [
            SingleCore,
        ]

        for method in methods:
            print(f"Running {method.__name__}")
            for _ in tqdm(range(self.iterations), desc=f"Method: {method.__name__}", position=0):
                running_method = method(self.df, self.config)
                running_method.run()
                running_method.save()
                self.results.append(running_method.results.data)