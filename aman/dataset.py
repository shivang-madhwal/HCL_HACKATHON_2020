import pandas as pd

df = pd.read_csv('transactionFinal.csv')
print(len(df.itemid.unique()))
# trans = df[df['event']=='transaction']

# trans.to_csv('transaction.csv')

# df1 = pd.read_csv('transaction1.csv')
# print(len(df1.no.unique()))