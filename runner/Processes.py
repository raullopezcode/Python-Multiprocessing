from runner.RunningMethod import RunningMethod
import scipy.stats as stats
import multiprocessing as mp

def run_process(df, dependent_variable, independent_variable, target_values):
    grouped_values = []
    for value in target_values:
        grouped_values.append(df[df[dependent_variable] == value][independent_variable].values)

    result = stats.f_oneway(*grouped_values)
    return result

class Processes(RunningMethod):
    def run(self):
        n_processes = self.kwargs['processes']
        processes = []
        for dependent_variable in self.config['targets']:
            target_values = self.df[dependent_variable].unique()
            for independent_variable in self.numerical_columns:
                if independent_variable in self.config['ignore'] or dependent_variable == independent_variable:
                    continue
                
                processes.append((self.df, dependent_variable, independent_variable, target_values))
        
        # Now we will execute in groups of `n_processes`
        with mp.Pool(processes=n_processes) as pool:
            for data in processes:
                pool.apply_async(run_process, *data)
    
    def version(self):
        return 1
                
    def option(self):
        if self.kwargs['processes'] == 1:
            return '1 Process'

        return f'{self.kwargs["processes"]} Processes'

