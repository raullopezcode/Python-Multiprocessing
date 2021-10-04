from runner.RunningMethod import RunningMethod
import scipy.stats as stats
from tqdm.auto import tqdm

class SingleCore(RunningMethod):
    def run(self):
        for dependent_variable in self.config['targets']:
            target_values = self.df[dependent_variable].unique()
            for independent_variable in tqdm(self.numerical_columns, desc=f'SingleCore: {dependent_variable}', position=1):
                if independent_variable in self.config['ignore'] or dependent_variable == independent_variable:
                    continue
                
                # grouped_values = []
                # for value in target_values:
                #     grouped_values.append(self.df[self.df[dependent_variable] == value][independent_variable].values)

                # result = stats.f_oneway(*grouped_values)

                # Here we should store those values with result.pvalue < 0.05
                # but will ignore this for now
    
    def version(self):
        return 1
                

