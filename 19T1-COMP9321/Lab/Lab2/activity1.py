# Load the dataset into a dataframe
# Print the columns of the dataset, and print the dataset to be familiar with the data
# Calculate and print the number of nan (not a number) in each column
# Drop the columns of dataframe by the above-mentioned black list
# Print the columns of the dataset to make sure the dataframe includes only desired columns
import pandas as pd 

def print_dataframe(dataframe, print_column=True, print_rows=True):
    if print_column:
        print(",".join([column for column in dataframe]))
    
    if print_rows:
        for index, row in dataframe.iterrows():
            print(",".join([str(row[column]) for column in dataframe]))
    
if __name__ == "__main__":
    columns_to_drop = ['Edition Statement', 'Corporate Author', 'Corporate Contributors', 'Former owner', 'Engraver', 'Contributors', 'Issuance type', 'Shelfmarks']
    csv_file = "Books.csv"
    df = pd.read_csv(csv_file)

    print("The percentage of NaN in the data per column:")
    num_of_rows = df.shape[0]
    for column in df:
        percent = 100 * df[column].isnull().sum() / num_of_rows
        print(column, str(percent) + '%')

    print("************************************************")
    print("Dataframe before dropping the columns")
    print_dataframe(df, print_rows=False)

    print("************************************************")
    print("Dataframe after dropping columns")
    df.drop(columns_to_drop, inplace=True, axis=1)
    # Pandas' drop method is used to remove columns of a dataframe
    # Inplace=True indicates that the changes should be applied to the given dataframe instead of creating a new one
    # axis=1 : whether to drop labels from the index (0/'index') or columns (1/'columns')

    print_dataframe(df, print_rows=False)
    print("************************************************")