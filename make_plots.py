import pylab as plt
import pandas as pd

plt.style.use('fivethirtyeight')

suffix='1D0B'

df=pd.read_csv('store_'+suffix+'.csv')

print("check raw data")
df.groupby('sample_size')['experiment_number'].count()


plt.clf()
df.groupby('sample_size')['p_value_RTs'].mean().plot(label='RT')
df.groupby('sample_size')['p_value_Acc'].mean().plot(label='accuracy')
df.groupby('sample_size')['p_value_Drift'].mean().plot(label='drift')
plt.ylabel('mean_p_value')
plt.legend(loc=0)
plt.savefig('mean_p_values_'+suffix+'.png',bbox_inches='tight')





'''
Plotting both the average proportion of p-values for RTs and Accuracy
'''
plt.clf()
df['RTsig']=(df['p_value_RTs']<0.05)*1 #for fascinating reasons boolean values break the sum function https://github.com/pandas-dev/pandas/issues/3752
df['Acsig']=(df['p_value_Acc']<0.05)*1 #for fascinating reasons boolean values break the sum function https://github.com/pandas-dev/pandas/issues/3752
df['Drsig']=(df['p_value_Drift']<0.05)*1 #for fascinating reasons boolean values break the sum function https://github.com/pandas-dev/pandas/issues/3752

total_n=df.groupby('sample_size')['RTsig'].count()
total_sig=df.groupby('sample_size')['RTsig'].sum()

total_n2=df.groupby('sample_size')['Acsig'].count()
total_sig2=df.groupby('sample_size')['Acsig'].sum()

total_n3=df.groupby('sample_size')['Drsig'].count()
total_sig3=df.groupby('sample_size')['Drsig'].sum()



prop_p_values_RTs = (total_sig/total_n)  # Renaming RT Proportion for a separate figure
prop_p_values_Acc = (total_sig2/total_n2) # Renaming Accuracy Proportion for a separate figure
prop_p_values_Drf = (total_sig3/total_n3) # Renaming Accuracy Proportion for a separate figure

plt.clf() # Clear previous plot
prop_p_values_RTs.plot(label='RTs')
prop_p_values_Acc.plot(label='Acc')
prop_p_values_Drf.plot(label='Drift')
plt.title('sample size v proportion of sig. p values')
plt.ylabel('proportion of sig. p values')
plt.xlabel('sample size')
plt.ylim([-0.05, 1.05]) # Setting y axis limits so we can clearly see 0 to 1
plt.legend(loc=0)
plt.savefig('prop_sig_p_values_'+suffix+'.png',bbox_inches='tight')