# Step 1: Import the necessary libraries
import pandas as pd
import statsmodels.api as sm
from pandas_datareader import data as pdr

# Step 2: Load the data
file_path = "../../data/spus_2024.csv"
strategies_prices = pd.read_csv(file_path, parse_dates=True, index_col=0)

# Step 3: Separate SPX and strategies
universe_name = "SPUS Bench"
universe_prices = strategies_prices[universe_name]
risk_premia_spus_prices = strategies_prices.drop(columns=[universe_name])

# Convert the strategies to returns
strategies = risk_premia_spus_prices.pct_change().dropna()
universe = universe_prices.pct_change().dropna()

# Step 4: Retrieve the Fama-French 4-factor data
ff_factors = pdr.DataReader(
    "F-F_Research_Data_Factors_daily",
    "famafrench",
    start="2024-01-01",
    end="2024-04-30",
)[0]
momentum_factor = pdr.DataReader(
    "F-F_Momentum_Factor_daily", "famafrench", start="2024-01-01", end="2024-04-30"
)[0]

# Combine the Fama-French factors and the momentum factor into a single DataFrame
ff_factors = ff_factors.join(momentum_factor["Mom   "])

# Convert the factors to daily returns as percentages
ff_factors = ff_factors / 100

# Step 5: Run the Fama-French 4-factor regression for each strategy
model_results = {}
for strategy_name in strategies.columns:
    # Merge strategy returns with the Fama-French factors
    data = pd.concat([strategies[strategy_name], ff_factors], axis=1, join="inner")

    # Prepare the data for regression
    X = data[["Mkt-RF", "SMB", "HML", "Mom   "]]
    y = data[strategy_name] - data["RF"]

    # Add a constant to the independent variables
    X = sm.add_constant(X)

    # Run the regression
    model = sm.OLS(y, X).fit()

    # Store the model results
    model_results[strategy_name] = model

# Extract the coefficients and p-values for each strategy into 2 distinctive tables
coefficients = pd.DataFrame(
    {strategy: model_results[strategy].params for strategy in model_results}
)
p_values = pd.DataFrame(
    {strategy: model_results[strategy].pvalues for strategy in model_results}
)

# Round the values to 3 decimal places
coefficients = coefficients.round(3)
p_values = p_values.round(3)

# Step 6: Display the results
print("Coefficients:")
print(coefficients)
print("\nP-Values:")
print(p_values)

# Add the universe results to these two tables
universe_data = pd.concat([universe, ff_factors], axis=1, join="inner")
X = universe_data[["Mkt-RF", "SMB", "HML", "Mom   "]]
y = universe_data[universe_name] - universe_data["RF"]
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
universe_coefficients = model.params.round(3)
universe_p_values = model.pvalues.round(3)

print("\nUniverse Coefficients:")
print(universe_coefficients)
print("\nUniverse P-Values:")
print(universe_p_values)

# Merge universe resuts with the strategy results without append method
coefficients = pd.concat([coefficients, universe_coefficients], axis=1)
p_values = pd.concat([p_values, universe_p_values], axis=1)
# Add universe name as field name
coefficients.columns = coefficients.columns.tolist()[:-1] + [universe_name]
p_values.columns = p_values.columns.tolist()[:-1] + [universe_name]


# Display the updated tables with no wrap because of too many rows
pd.set_option("display.expand_frame_repr", False)
print("\nUpdated Coefficients:")
print(coefficients)
print("\nUpdated P-Values:")
print(p_values)

# Reset the display settings
pd.reset_option("display.expand_frame_repr")

# Step 7: Save the results to a CSV file
coefficients.to_csv("../../output/coefficients.csv")
p_values.to_csv("../../output/p_values.csv")


"""
The code above is a Python script that performs the following steps:

1. Import the necessary libraries.
2. Load the data from the CSV file.
3. Separate the S&P 500 index and the strategies, convert the prices to returns, and calculate the Fama-French factors and the momentum factor.
4. Run the Fama-French 4-factor regression for each strategy and store the model results.
5. Extract the coefficients and p-values for each strategy and the S&P 500 index into two separate tables.
6. Display the results and add the S&P 500 index results to the tables.
7. Save the results to CSV files.

The script uses the `pandas`, `statsmodels`, and `pandas_datareader` libraries to load and analyze the data. It calculates the Fama-French factors and momentum factor, runs the regression analysis, and outputs the coefficients and p-values for each strategy and the S&P 500 index.

You can run this script in a Python environment to analyze the Fama-French 4-factor model for the strategies and the S&P 500 index. The results will be saved to CSV files for further analysis or reporting.

Please note that you may need to install the required libraries (`pandas`, `statsmodels`, `pandas_datareader`) if you haven't already done so. You can install them using `pip` by running the following commands in your Python environment:

"""
