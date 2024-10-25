# BusinessWizard
businesswizard is a Python package of useful business related helper functions. The goal is to make common business tasks a breeze by aggregating useful functions into a single package.

## Quick Start
Conda Installation: `conda install businesswizard`
Pip Installation: `pip install businesswizard`

Importing the package:
```python 
 import businesswizard 
 ```

## Functionality
* Add leading zeroes to columns
* Clean Column Text
* Create column flags and indicators
* Concatenate values based on groups
* Compute the number of calendar and business days between two dates
* Subset a dataset into individual groups
* Create a list of dates/months
* Output pre-formatted excel reports
* Query parquet files
* Query databases using either a .SQL file or written query
* Execute multiple SQL commands against a database
* Read in multiple CSV and Excel files in simultaneously (either in single dataframe or multiple dataframes)
* Compress files
* Refresh Excel Workbooks


## Examples
### Date Diff
```python
test_df = pd.DataFrame({'A':['2024-10-01', '2024-07-01'], 'B':['2023-10-01', '2023-07-01']})

test_df.date_diff('B', 'A')
```

#### Group Concat
```python
test_df = pd.DataFrame({'A':['Access', 'Connect','Access', 'Connect'], 'B':['SM', 'JJ', 'JJ', 'MS']})

test_df.group_concat(group_column='A', concat_column='B')
```

### Subset By Group
```python 
test_df = pd.DataFrame({'A':['Access', 'Connect','Access', 'Connect'], 'B':['SM', 'JJ', 'JJ', 'MS']})
subset_dfs = test_df.subset_by_group('A')
```