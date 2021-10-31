from runner.RunningMethod import RunningMethod
import scipy.stats as stats
from concurrent.futures import ThreadPoolExecutor

class Threads(RunningMethod):
    def run(self):
        n_threads = self.kwargs['threads']
        threads_data = []
        for dependent_variable in self.config['targets']:
            target_values = self.df[dependent_variable].unique()
            for independent_variable in self.numerical_columns:
                if independent_variable in self.config['ignore'] or dependent_variable == independent_variable:
                    continue
                
                threads_data.append((dependent_variable, independent_variable, target_values))
        
        # Now we will execute the threads in groups of `n_threads`
        with ThreadPoolExecutor(max_workers=n_threads) as executor:
            for data in threads_data:
                executor.submit(self._run_thread, *data)
    
    def _run_thread(self, dependent_variable, independent_variable, target_values):
        grouped_values = []
        for value in target_values:
            grouped_values.append(self.df[self.df[dependent_variable] == value][independent_variable].values)

        result = stats.f_oneway(*grouped_values)
        return result
    
    def version(self):
        return 1
                
    def option(self):
        if self.kwargs['threads'] == 1:
            return '1 Thread'

        return f'{self.kwargs["threads"]} Threads'

