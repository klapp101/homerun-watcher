# MLB Home Run Tracker

## Overview

This project serves as a utility for baseball enthusiasts who predict the player who'll hit the most home runs throughout a season. Given the impracticality of watching every single game, this tool is designed to fetch video clips of home runs hit by players on your team. It provides a convenient way to never miss out on those fantastic home runs!

## Features

- **Web Scraping**: Extracts player names from an MLB related website.
- **MLB API Integration**: Retrieves the player IDs corresponding to the extracted player names.
- **Home Run Video Collection**: Uses asynchronous browser automation to fetch video clips of home runs hit on a given date by players on your team.

## Dependencies

- `requests`
- `BeautifulSoup`
- `statsapi`
- `pandas`
- `selenium`
- `asyncio`
- `pyppeteer`
- `datetime`

## Setup & Usage

1. **Installation**: Before using this project, make sure to install all the required dependencies. You can do this using pip:

`pip install requests bs4 statsapi pandas selenium asyncio pyppeteer`

2. **Configuration**: Modify the `params` dictionary in the script to set the `recordID` to your team's name.
3. **Execution**: Run the script: your_script_name.py
4. **Output**: The script will print a DataFrame showing player names, their respective IDs, video titles, and video URLs of the home runs.

## Future Enhancements
- **Email Integration**: As per the project description, there's an intent to send daily emails containing video clips. This can be integrated using libraries such as `smtplib` and `email` in Python.
- **Date Automation**: Instead of hardcoding the date, the script can be modified to automatically fetch home runs for the current day or a range of dates.
- **Error Handling**: More robust error handling can be incorporated to deal with potential issues like website structure changes or API alterations.

## Contributing
Feel free to fork this project and submit pull requests for any enhancements or fixes. Ensure that you test your changes thoroughly before submitting.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
- [MLB-StatsAPI](https://github.com/toddrob99/MLB-StatsAPI/wiki) for providing a way to fetch player IDs.
- [MLB Points Derby](https://mlb.pointsderby.com/) for hosting the Homerun Points League!
