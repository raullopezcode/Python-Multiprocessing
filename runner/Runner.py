import pandas as pd
from tqdm.auto import tqdm
from runner.Processes import Processes
from runner.SingleCore import SingleCore
from runner.Threads import Threads

class Runner:
    def __init__(self, path: str, iterations: int, config: dict, threads=[], processes=[]):
        self.path = path
        self.config = config
        self.iterations = iterations
        self.df = pd.read_csv(path)
        self.results = []
        self.threads = threads
        self.processes = processes
    
    def run(self):
        methods = [
            SingleCore,
        ]

        for _ in range(len(self.threads)):
            methods.append(Threads)
        
        for _ in range(len(self.processes)):
            methods.append(Processes)

        i_threads = 0
        i_processes = 0
        for method in methods:
            print(f"Running {method.__name__}")
            for _ in tqdm(range(self.iterations), desc=f"Method: {method.__name__}", position=0):
                if method == Threads:
                    running_method = method(self.df, self.config, threads=self.threads[i_threads])
                elif method == Processes:
                    running_method = method(self.df, self.config, processes=self.processes[i_processes])
                else:
                    running_method = method(self.df, self.config)

                running_method.run()
                running_method.save()
                self.results.append(running_method.results.data)
            
            if method == Threads:
                i_threads += 1
            elif method == Processes:
                i_processes += 1