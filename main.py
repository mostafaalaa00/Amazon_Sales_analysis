import pandas as pd
import matplotlib.pyplot as plt

import matplotlib
df = pd.read_csv('Amazon Sale Report.csv')

# discover data
#print(df.info())
#print(df.head())
#print(df.nunique())
#print(df.isnull().sum())


# setting index as index column
df.set_index("index", inplace=True)

# Data Cleaning

# duplicated rows
#print(df.duplicated().sum())
df.drop_duplicates(inplace=True)
#print("NUmber of duplicates rows: " , df.duplicated().sum())

# null values
lists = ['Courier Status','fulfilled-by','Unnamed: 22','currency']
#ASIN,SKU,Sales,Channel

#fill null values with zero
df['currency'].fillna(0.0, inplace=True)
#print(df['currency'].value_counts(dropna=False))

df['Amount'].fillna(0.0, inplace=True)
#print(df['Amount'].value_counts(dropna=False))

df['promotion-ids'].fillna('no-promotion', inplace=True)

df['ship-city'].fillna('unknown', inplace=True)
df['ship-state'].fillna('unknown', inplace=True)
df['ship-postal-code'].fillna(0, inplace=True)
df['ship-country'].fillna('unknown', inplace=True)

#print(df['Courier Status'].value_counts(dropna=False))
#print(df['Unnamed: 22'].value_counts(dropna=False))
df.drop(columns=lists, inplace=True)
#add month based on date
df['Date'] = pd.to_datetime(df['Date'])
df['month']=df['Date'].dt.month
#print(df['month'].unique())
df['month'].replace([3,4,5,6],['March','April','May','June'], inplace=True)
df = df[df['month'].isin(['April','May','June'])]

#now take a look
#print(df.isnull().sum())

# Data Visualization

# total sales
'''
print("Total sales: ", df.Amount.sum())
'''
# number of product
'''
#print(df['Qty'].value_counts().plot(kind='bar'))
# major of customers order one product
#plt.show()
'''
# most popular category
'''
print(df.Category.value_counts().plot(kind='bar'))
plt.title('Most Popular Category')
plt.show()
# we see that (set) category then (kurta) and (Western Dress)
'''

# sales according months
'''
df.groupby('month')['Amount'].ave().plot(kind='pie')
plt.title('Monthly Sales')
'''
# we see that (April) the best selling month then (May) and (June)


# make a copy of data frame and separate data into shipped and canceled
# shipped mean reached to customer
df1 = df.copy()
ship1 = df1[df1['Status'] == 'Shipped']
ship2 = df1[df1['Status'] == 'Shipped - Delivered to Buyer']
shipped = pd.concat([ship1, ship2], axis=0)

# note that canceled mean unreached, binding, canceled or return to seller (unreached to customer)
canceled = df1[(df1['Status'] != 'Shipped') & (df1['Status'] != 'Shipped - Delivered to Buyer')]

# now lets discover witch factor effect in product canceling ?
'''
shipped['Fulfilment'].hist(alpha=0.5, bins=5, label='Shipped')
canceled['Fulfilment'].hist(alpha=0.5, bins=5, label='Canceled')
plt.title('Fulfilment By')
plt.show()
'''
# from the result mejorty of shipped product is by (Amazon) and less percentage by the (merchant)
# but product by merchant are canceled more so,(merchant) have a problem in shipping.


# which city order more and relation between city and canceling rate ?
'''
shipped['ship-city'].value_counts()[:10].plot(kind='bar', color='maroon', label='Shipped')
canceled['ship-city'].value_counts()[:10].plot(kind='bar', label='Canceled')
plt.title('Top Shipping City')
plt.legend()
# we see that no relation between city and canceling rate
'''

# Compute percentage below average revenue for quarter
'''
# Get latest month revenue and average quarterly revenue
group_month = df.groupby('month')['Amount'].sum()
fig,ax = plt.subplots(figsize=(8,6))
bars = ax.bar(group_month.index,group_month.values,color='gray')

quarter_avg = (group_month.values[0] + group_month.values[2]) / 2
for i, bar in (enumerate(bars)):
    if i == len(bars)-1 or i < len(bars)-2:
        continue
    pct_below_avg = round(1 - (group_month.values[i] / quarter_avg), 3)
    ax.annotate(f'{pct_below_avg}% blow average',
                xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                xytext=(0, 10), textcoords='offset points',  fontweight='bold',
                ha='center', va='bottom', fontsize=12)

ax.axhline(quarter_avg, linestyle='--', color='orange', linewidth=2, label='Q2 Average Revenue')
ax.set_title('Amazon Sales Quarter II', fontsize=22, fontweight='bold')

ax.set_xlabel(None)
ax.set_xticklabels(group_month.index, fontsize=12)
ax.set_yticklabels(list(range(0,41,5)),fontsize=14)

ax.set_ylabel('Net Revenue in 10,000 dollars', fontsize=12, labelpad=3)
ax.yaxis.grid(linestyle='--', color='gray', linewidth=0.5, dashes=(8, 5))

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_linewidth(2)
ax.spines['bottom'].set_color('black')
plt.show()
'''





