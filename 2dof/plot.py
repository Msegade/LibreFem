import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('2dof.csv', comment='#')
df.plot(x='INST', y='DY_0')
plt.savefig('displacement.png')
