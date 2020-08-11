import sys
import os
import csv
from pathlib import Path

filename = 'monthly_csv.csv'
if not os.path.exists(filename):
    print(f'There is no file named {filename} in the working directory, giving up...')
    sys.exit()

source = input('Enter the source (GCAG or GISTEMP): ')
year_or_range_of_years = input('Enter a year or a range of years in the form XXXX -- XXXX: ')
month = input('Enter a month: ')
average = 0
years_above_average = []

first_year = year_or_range_of_years[:4]
last_year = year_or_range_of_years[-4:]
if first_year <= last_year:
    start_year = first_year
    end_year = last_year
if first_year >= last_year:
    start_year = last_year
    end_year = first_year
#print(start_year)
#print(end_year)

mon = ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
number_of_month = mon.index(month)+1
#print(number_of_month)

file = Path(filename)
mean_list = []
year_list = []
out_list = []
with open(file) as file:
    csv_file = csv.reader(file)
    for Source, Date, Mean in csv_file:
        if str(Source) == source:
            year = Date.split('-')[0]
            month_number = Date.split('-')[1]
            if int(month_number) == number_of_month:
                if int(year) >= int(start_year):
                    if int(year) <= int(end_year):
                        mean_list.append(Mean)
                        year_list.append(year)
                        out_list.append([year,Mean])
#                        print(Source, Date, Mean)
#print(out_list)
#print(mean_list)
#print(year_list)

mean_list = [ float(x) for x in mean_list ]
average = sum(mean_list) / len(mean_list)
year_list = [ int(x) for x in year_list ]
for item in out_list:
    if float(item[1]) > average:
        years_above_average.append(int(item[0]))

years_above_average = set(years_above_average)
years_above_average = sorted(years_above_average)
#print(years_above_average)
#print(average)

print(f'The average anomaly for {month} in this range of years is: {average:.2f}.')
print('The list of years when the temperature anomaly was above average is:')
print(years_above_average)
