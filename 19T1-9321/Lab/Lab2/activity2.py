# Load the dataset into a dataframe
# Replace the cell value of "Place of Publication" with "London" if it contains "London", and replace all '-' characters with space
# Keep the first 4 digit number in "Date of Publication"
# Convert "Date of Publication" cells to numbers
# Replace NaN with 0 for the cells of "Date of Publication"
# Print the dataframe to see if the changes have been applied properly

import pandas as pd 

if __name__ == "__main__":
    csv_file = "Books.csv"
    df = pd.read_csv(csv_file)

    # Replace the cell value of "Place of Publication" with "London" if it contains "London",
    # and replace all "-" characters with space
    # We use the apply method which applies a lambda function to the cells of the dataframe
    df['Place of Publication'] = df['Place of Publication'].apply(lambda x: 'London' if 'London' in x else x.replace('-', ' '))

    ################################################################################################################
    # Here is also another approach using numpy.where                                                              #
    #    import numpy as np                                                                                        #
    #    london = df['Place of Publication'].str.contains('London')                                                #
    #    df['Place of Publication'] = np.where(london, 'London', df['Place of Publication'].str.replace('-', ' ')) #
    ################################################################################################################
    print(df['Place of Publication'])

    # We use Pandas' extract method which for each subject string in the Series,
    # extracts groups from the first match of regular expression pat.
    new_date = df['Date of Publication'].str.extract(r'^(\d{4})', expand=False)
    # ^(\d{4}) : matches 4 digit numbers in the beginning of the string
    new_date = pd.to_numeric(new_date)
    print(df['Date of Publication'])

    # replace all NaN with 0
    new_date = new_date.fillna(0)
    df['Date of Publication'] = new_date
    print(df['Date of Publication'])