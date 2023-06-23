import streamlit as st
import pandas as pd
import base64
from datetime import datetime
import numpy as np

# Constants for column names
PERCENTAGE_COLUMNS = ['Home Win %', 'Draw %', 'Away Win %', 'BTTS %', 'BTTS Home Win %', 'BTTS Away Win %',
                      'BTTS Draw %', 'BTTS No Draw %', 'Over 0.5 Goals %', 'Over 1.5 Goals %', 'Over 2.5 Goals %',
                      'Over 3.5 Goals %', 'Over 4.5 Goals %']
AVERAGE_COLUMNS = ['Average Goals For Home', 'Average Goals For Away']

def staking_plan(bank_balance, decimal_odds, winning_probability):
    """
    This function uses the Kelly formula to calculate the optimal stake size based on the bank balance, odds,
    and winning probability.
    """
    # Convert decimal odds to fractional
    fractional_odds = decimal_odds - 1

    # Calculate the implied probability
    implied_probability = 1 / decimal_odds

    # Convert winning probability from percentage to fraction
    winning_probability = winning_probability / 100

    # Calculate the Kelly fraction
    kelly_fraction = (fractional_odds * winning_probability - (1 - winning_probability)) / fractional_odds

    # Ensure the Kelly fraction is within 0 and 0.05 (1 - 5%)
    kelly_fraction = np.clip(kelly_fraction, 0, 0.05)

    # Calculate the stake
    stake = bank_balance * kelly_fraction

    return stake, kelly_fraction

def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)
    b64 = base64.b64encode(object_to_download.encode()).decode()
    href = f'data:file/csv;base64,{b64}'
    return f'<a href="{href}" download="{download_filename}">{download_link_text}</a>'

def prepare_data(data, percentage_columns, average_columns):
    for column in percentage_columns:
        if column in data.columns:
            if data[column].dtype == 'object':
                data.loc[:, column] = (data[column].str.rstrip('%').astype(float)).round(2).astype(str) + '%'
            else:
                data.loc[:, column] = (data[column] * 100).round(2).astype(str) + '%'
    for column in average_columns:
        if column in data.columns:
            data.loc[:, column] = data[column].apply(lambda x: '{:.2f}'.format(x))
    return data

# File paths and data loading
data_files = {
    "Belgium": "https://raw.githubusercontent.com/lottiealice18/BTTS/main/Belgium.csv",
    "England": "https://raw.githubusercontent.com/lottiealice18/BTTS/main/England.csv",
    "France": "https://raw.githubusercontent.com/lottiealice18/BTTS/main/France.csv",
    "Germany": "https://raw.githubusercontent.com/lottiealice18/BTTS/main/Germany.csv",
    "Holland": "https://raw.githubusercontent.com/lottiealice18/BTTS/main/Holland.csv",
    "Italy": "https://raw.githubusercontent.com/lottiealice18/BTTS/main/Italy.csv",
    "Portugal": "https://raw.githubusercontent.com/lottiealice18/BTTS/main/Portugal.csv",
    "Scotland": "https://raw.githubusercontent.com/lottiealice18/BTTS/main/Scotland.csv",
    "Spain": "https://raw.githubusercontent.com/lottiealice18/BTTS/main/Spain.csv",
    "Turkey": "https://raw.githubusercontent.com/lottiealice18/BTTS/main/Turkey.csv",
}

data = {k: pd.read_csv(v) for k, v in data_files.items()}

# Configuration for the data processing
config = {
    "Belgium": {
        "league_order": ['Belgian Pro League'],
        "data": data["Belgium"],
        "percentage_columns": PERCENTAGE_COLUMNS,
        "average_columns": AVERAGE_COLUMNS
    },
    "England": {
        "league_order": ['Premiership', 'Championship', 'League One', 'League Two'],
        "data": data["England"],
        "percentage_columns": PERCENTAGE_COLUMNS,
        "average_columns": AVERAGE_COLUMNS
    },
    "France": {
        "league_order": ['France Ligue One', 'France Ligue Two'],
        "data": data["France"],
        "percentage_columns": PERCENTAGE_COLUMNS,
        "average_columns": AVERAGE_COLUMNS
    },
    "Germany": {
        "league_order": ['German Bundesliga', 'German Bundesliga Two'],
        "data": data["Germany"],
        "percentage_columns": PERCENTAGE_COLUMNS,
        "average_columns": AVERAGE_COLUMNS
    },
    "Holland": {
        "league_order": ['Netherlands Ersdvisle'],
        "data": data["Holland"],
        "percentage_columns": PERCENTAGE_COLUMNS,
        "average_columns": AVERAGE_COLUMNS
    },
    "Italy": {
        "league_order": ['Italy Serie A', 'Italy Serie B'],
        "data": data["Italy"],
        "percentage_columns": PERCENTAGE_COLUMNS,
        "average_columns": AVERAGE_COLUMNS
    },
    "Portugal": {
        "league_order": ['Portugal Primerira Liga'],
        "data": data["Portugal"],
        "percentage_columns": PERCENTAGE_COLUMNS,
        "average_columns": AVERAGE_COLUMNS
    },
    "Scotland": {
        "league_order": ['Scottish Premiership', 'Scottish Division One', 'Scottish Division Two'],
        "data": data["Scotland"],
        "percentage_columns": PERCENTAGE_COLUMNS,
        "average_columns": AVERAGE_COLUMNS
    },
    "Spain": {
        "league_order": ['La Liga', 'Spanish Secunda'],
        "data": data["Spain"],
        "percentage_columns": PERCENTAGE_COLUMNS,
        "average_columns": AVERAGE_COLUMNS
    },
    "Turkey": {
        "league_order": ['Turkey Super Lig'],
        "data": data["Turkey"],
        "percentage_columns": PERCENTAGE_COLUMNS,
        "average_columns": AVERAGE_COLUMNS
    }
}

PAGES = {
    "Home": "home_page",
    "Stats and Leagues": "stats_and_leagues_page",
    "Today's Matches": "todays_matches_page",
    "Betting Systems and Promotions Page": "betting_and_promotions"
}

def home_page():
    st.title("Both Teams to Score and Goals Scored Percentages")
    st.write("Welcome to Both Teams to Score and Goals Scored Percentages!")
    st.write(
        "This website provides comprehensive statistics on both teams to score (BTTS) and the percentage of goals scored in football matches. The data is based on historic meetings between two teams, covering the 2023/2024 football season across various European leagues.")
    st.write(
        "Our extensive database includes statistics from over 20 seasons, offering valuable insights into the performance of teams when playing at home or away. You can access information such as win, draw, and loss percentages, BTTS percentages, average goals per team, and the percentage of matches with over 0.5 goals to over 4.5 goals.")
    st.write(
        "All the data presented on this website can be downloaded in CSV format, allowing you to analyze and explore the statistics further. We offer downloads for all the leagues available, providing a comprehensive dataset for your analysis.")
    st.write(
        "Additionally, we provide a convenient 'Today's Matches' button that generates a CSV file containing the matches scheduled for today. This allows you to stay up-to-date with the latest matches and access real-time data for your analysis.")
    st.write(
        "Feel free to explore the sidebar to select a country and league of interest. Once selected, you can view and download the corresponding data. We hope that these statistics enhance your understanding of both teams to score and goals scored percentages, empowering you to make informed decisions.")
    st.write(
        "Please note that the statistics provided are based on historical data and should be used for informational purposes only.")

def stats_and_leagues_page():
    # Sidebar for selections
    st.sidebar.title("Selections")

    # Dropdown for country selection
    country_selection = st.sidebar.selectbox("Country", list(config.keys()), 0)

    # Dropdown for league selection
    league_selection = st.sidebar.radio("League", config[country_selection]["league_order"])

    # Read the data for selected country
    data = config[country_selection]["data"]

    # Prepare the data
    data = prepare_data(data, config[country_selection]["percentage_columns"],
                        config[country_selection]["average_columns"])

    # Display the country and league
    st.header(f"{country_selection} {league_selection}")

    # Download link for the limited data
    download_link_text = f'Please download {country_selection} {league_selection} info as a CSV'
    tmp_download_link = download_link(data[data['League'] == league_selection], 'YOUR_DOWNLOADED_DATA.csv', download_link_text)
    st.markdown(tmp_download_link, unsafe_allow_html=True)

    # Display a limited number of rows by default
    limited_data = data[data['League'] == league_selection].head(10)
    full_data = data[data['League'] == league_selection]

    # Remove index column numbers
    limited_data_display = limited_data.reset_index(drop=True)
    full_data_display = full_data.reset_index(drop=True)

    # Button to display all rows
    if st.button("View All"):
        st.table(full_data_display)
    else:
        st.table(limited_data_display)

    # Trigger download
    st.write('')
    st.write('')

def todays_matches_page():
    st.title("Today's Matches")
    st.write("Here is a list of today's matches.")
    st.write(
        "Please download the data as a CSV file (Link at the bottom of the page) to explore it further. In Excel, you can use filters to sort and analyze the data. For example, you can sort columns from largest to smallest to identify interesting patterns or trends.")
    st.write(
        "Make sure to check out the 'Betting Systems and Promotions Page' for the latest offers and promotions to enhance your betting experience.")

    # Load today's matches data
    todays_matches = pd.read_csv("https://raw.githubusercontent.com/lottiealice18/BTTS/main/Todays%20Matches.csv")

    # Initialize an empty list to store today's matches with stats
    todays_data_with_stats = []

    # Loop over each country's data
    for country in config.keys():
        # Load country's data
        country_data = config[country]["data"]

        # Prepare the country's data
        country_data = prepare_data(country_data, config[country]["percentage_columns"],
                                    config[country]["average_columns"])

        # Merge today's matches with this country's data on 'Home Team' and 'Away Team'
        merged_data = pd.merge(todays_matches, country_data, on=['Home Team', 'Away Team'], how='inner')

        # Append this to the overall list
        todays_data_with_stats.append(merged_data)

    # Combine all dataframes
    todays_data_with_stats = pd.concat(todays_data_with_stats)

    # Display the data
    st.dataframe(todays_data_with_stats)

    # Get column names from the filtered DataFrame
    columns = todays_data_with_stats.columns.tolist()

    # Remove unwanted columns
    unwanted_columns = ['Home Team', 'Away Team', 'League']
    columns = [column for column in columns if column not in unwanted_columns]

    # Add "None" option to the column selection
    columns.insert(0, "None")

    # Select columns using radio buttons
    selected_column = st.radio("Select Columns", columns)

    if selected_column == "None":
        # Display the original DataFrame
        st.dataframe(todays_data_with_stats)
    else:
        # Filtered DataFrame based on the selected column
        filtered_data = todays_data_with_stats[['Home Team', 'Away Team', selected_column]]

        # Display the filtered data
        st.dataframe(filtered_data)

    # Download link for the data
    download_link_text = "Click here to download today's matches as a CSV"
    tmp_download_link = download_link(todays_data_with_stats, 'todays_matches.csv', download_link_text)
    st.markdown(tmp_download_link, unsafe_allow_html=True)

    # Trigger download
    st.write('')
    st.write('')




def betting_and_promotions():
    st.title("Betting Systems and Promotions")

    st.sidebar.title("System Selection")
    system_selection = st.sidebar.radio("Select a System",
                                        ['None', 'Value Bet Calculator', '18 Team Combination System', 'System 3',
                                         'System 4',
                                         'System 5'])
        # Rest of your code...

    if system_selection == 'None':
        st.write("Welcome to the Betting Systems and Offers page!")
        st.write(
            "Here, you can find a collection of betting systems and exclusive offers to enhance your betting experience.")
        st.write(
            "Explore the available systems and offers to make informed decisions and maximize your chances of success.")
        st.write(
            "Please note that betting involves risk, and it's essential to gamble responsibly. Only participate if you meet the legal age requirements in your jurisdiction.")

    elif system_selection == 'Value Bet Calculator':
        st.title("Value Bet Calculator")
        st.write(
            "A 'Value Bet' occurs when you think the probability of an outcome happening is greater than the probability implied by the bookmaker's odds. "
            "This calculator will help you to identify potential 'Value Bets', but it's important to remember that even a 'Value Bet' is not guaranteed to win. "
            "Each bet is a separate event, and the outcome is influenced by many variables that can be unpredictable. Please bet responsibly."
        )
        # Get user inputs
        num_outcomes = st.number_input("Enter the number of possible outcomes", min_value=2)
        decimal_odds = st.number_input("Enter the odds", min_value=1.01)
        user_probability = st.number_input("Enter your estimated probability (%)", min_value=0.01, max_value=100.0)

        # Calculate implied probability
        implied_probability = round(100 / decimal_odds, 2)

        # Display the results
        st.write(f"The implied probability based on the odds is: {implied_probability}%")
        if user_probability > implied_probability:
            st.write("Based on your estimated probability, this could be a Value Bet.")
        else:
            st.write("Based on your estimated probability, this does not appear to be a Value Bet.")

    elif system_selection == '18 Team Combination System':
        st.title("18 Team Combination System")
        st.write("The 18 Team Combination System involves selecting 18 teams and creating combinations of them "
                 "such that at least one line will contain 4 wins if 7 of the 18 selected teams win. "
                 "This is achieved using a 'wheel' system, a strategic play method designed to optimize the number "
                 "of winning combinations.")

        combinations = [
            "01 02 03 04 05 06",
            "07 08 09 10 11 12",
            "13 14 15 16 17 18",
            "01 07 13 08 14 03",
            "02 09 15 10 04 05",
            "11 17 06 12 16 18",
            "01 09 14 10 15 05",
            "02 07 11 03 13 16",
            "08 12 04 18 06 17",
            "01 08 11 15 03 16",
            "02 13 09 04 17 05",
            "07 14 10 18 12 06",
        ]

        st.write("For example, the system creates combinations like this:")

        for combination in combinations:
            st.code(combination)

        st.write("This is just a strategic play method and does not guarantee a profit. "
                 "The outcome will still depend on the accuracy of your predictions and the inherent randomness "
                 "of the betting event.")

    elif system_selection == 'System 3':
        st.write("Hello, you've selected System 3!")

    elif system_selection == 'System 4':
        st.write("Hello, you've selected System 4!")

    elif system_selection == 'System 5':
        st.write("Hello, you've selected System 5!")

def main():
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Select a Page", list(PAGES.keys()))
    if selection == "Home":
        home_page()
    elif selection == "Stats and Leagues":
        stats_and_leagues_page()
    elif selection == "Today's Matches":
        todays_matches_page()
    elif selection == "Betting Systems and Promotions Page":
        betting_and_promotions()

if __name__ == "__main__":
    main()
