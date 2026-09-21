'''
Load the data produced by the data-generator, specifically the 
data contained within the samples.csv file and split them by
the problem type
'''

import pandas as pd

# The data generator produces these types:
# 1: A near vacuum; we are not interested in this case.
# 2: Positive-pressure solution. (Is there better clarification that this?)
# 3: 2 shock case, with shocks moving left and right (p* > pL and pR)
# 4: A right moving shock and left moving expansion wave
# 5: A left moving shock and a right moving expansion wave
# Actually, the code already has types, which might provide further insight.
# These were added many years ago, by myself!
problem_type = [2,3,4,5]

# Load the samples file
# The samples file produced by the data-generator does not include headers
my_columns = ['rhoL', 'uL', 'TL', 'rhoR', 'uR', 'TR', 's1', 's2', 's3', 'type']
df = pd.read_csv('./data-generator/samples.csv', names=my_columns)
print("Hello")

# Now create split CSV files using each type
for problem in problem_type:
    fileName = f"./data-generator/samples_type_{problem}.csv"
    df_problem = df[df['type'] == problem]
    no_samples = len(df_problem)
    print(f"Loaded {no_samples} for problem type = {problem}")
    # Now to save these in CSV form
    df_problem.to_csv(fileName, index=False)

