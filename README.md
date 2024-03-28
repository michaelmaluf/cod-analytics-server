# COD Analytics Predictor Server

### [Link to application](https://codanalyticspredictor.com)

## Introduction
This is the backend for the application. The purpose of this project is to predict Call of Duty matches for teams in the Call of Duty League. The data is scraped from the league and affiliate websites and stored in a Postgres database. The server utilizes the Flask framework for consuming API requests. Gradient Boosting Machines(GBMs) are used for calculating predictions.

## Features
- Three GBMs for predictions: one for Hardpoint, Search & Destroy, and Control.
- Endpoints for processing prediction requests and serving the results.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.1 or above installed.
- Google Chrome and ChromeDriver installed.
- PostreSQL installed.

## Installation
Clone the repository and move into the project directory:
- git clone https://github.com/yourusername/cod-analytics-server.git
- cd cod-analytics-server

### Install Dependencies
To set up your environment and install required dependencies, follow these steps:
1. Ensure ChromeDriver is installed and its path is added to your system's PATH. Detailed instructions can be found in the [ChromeDriver documentation](https://chromedriver.chromium.org/documentation).
2. Ensure PostgreSQL is installed on your system. Consult the [PostgreSQL documentation](https://www.postgresql.org/docs/) for installation guidance.
3. Install the necessary Python packages using pip: pip install -r requirements.txt.

## Configuration
Create a .env file that replicates .env.example and fill all values.

## Usage
- python app.py (server will run on http://127.0.0.1:5000/ by default)
- send a request to http://127.0.0.1:5000/app/sraper with your established API key to trigger the scraper, gather all data, and fill the database
- use http://127.0.0.1:5000/predictions endpoint with the correct query parameters to trigger the models and view results

## License
This project is licensed under the MIT License.