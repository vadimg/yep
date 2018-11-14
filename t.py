import csv
import matplotlib.pyplot as plt

output = []
index = {}
with open('data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if not row['E']:
            break

        row['EP'] = float(row['E']) / float(row['P'])
        row['YEP'] = (float(row['GS10'])/100) / row['EP']
        row['Fraction'] = float(row['Fraction'])
        row['Price'] = float(row['Price'])
        row['CPI'] = float(row['CPI'])
        output.append(row)
        index[row['Date']] = row


def add_year(date):
    year, month = date.split('.')
    return '%s.%s' % (int(year) + 1, month)


def add_month(date):
    year, month = date.split('.')
    year = int(year)
    month = int(month) if month != '1' else 10
    month += 1
    if month > 12:
        year += 1
        month = 1
    if month < 10:
        month = '0%s' % month
    if month == 10:
        month = 1
    return '%s.%s' % (year, month)


def total_return(date, years):
    initial = index[date]
    shares = 1.0
    for _ in xrange(years * 12):
        date = add_month(date)
        row = index.get(date)
        if row is None:
            return None

        dividend = float(row['D']) / 12
        shares += dividend / float(row['P'])
    stock_return = (shares * float(index[date]['P']) / float(initial['P']))
    tres_ret = (1 + float(initial['GS10'])/100) ** years

    return stock_return - tres_ret


for row in output:
    row['return10'] = total_return(row['Date'], 10)

"""
fig, ax = plt.subplots()
ax.plot([float(row['Fraction']) for row in output],
        [row['return10'] for row in output])

ax.plot([float(row['Fraction']) for row in output],
        [row['YEP'] for row in output])
plt.axhline(0, color='gray', linewidth=0.1)
"""

YEAR = 1950
plt.scatter([row['YEP'] for row in output if row['Fraction'] > YEAR],
            [row['return10'] for row in output if row['Fraction'] > YEAR],
            s=1)
plt.axhline(y=0, color='gray', linestyle='-', linewidth=1)
plt.axvline(x=1, color='gray', linestyle='-', linewidth=1)

plt.show()
