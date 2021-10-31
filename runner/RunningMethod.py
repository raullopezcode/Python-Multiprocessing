from abc import ABC
import pandas as pd

from results.Results import Results

class RunningMethod(ABC):
    def __init__(self, df: pd.DataFrame, config: dict, **kwargs):
        self.df = df[:config['max_rows']]
        self.config = config
        self.kwargs = kwargs
        self.numerical_columns = self.df.select_dtypes(include=['int64', 'float64']).columns[:self.config['max_cols']]
        self.results = Results(type(self).__name__, self.option(), self.config['name'], self.version())

    def run(self):
        pass

    def version(self):
        return 1

    def option(self):
        return type(self).__name__
    
    def save(self):
        self.results.measure()
        self.results.save_history()