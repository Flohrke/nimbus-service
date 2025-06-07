# Nimbus - Weather Service
## by Felix Lohrke - 2025

This project provides weather information through a Django backend.
It consists of a main Django project called **nimbus** and an app called **weather**, which handles all functionalities 
for retrieving the most common weather or average temperatures for a specific city and time range.

---

## Project Structure

```
nimbus/           # Django project root (settings, urls, wsgi, etc.)
weather/          # Django app with models, views, helpers, and logic
    database_helper.py  # Script to fetch initial weather data
    ...
requirements.txt  # Python dependencies
manage.py
```

---

## Features

* **Average Temperature:** Get the average daily temperature for a city over a given date range.
* **Most Common Weather:** Retrieve the most frequently occurring weather condition for a city within a specified period.
* **City-based Data:** All weather queries are performed per city and time range.

---

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/Flohrke/nimbus-service.git
cd <your-project-directory>
```

### 2. Create and Activate a Virtual Environment

```sh
python3 -m venv venv
source venv/bin/activate 
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Set Up the Database

```sh
python manage.py makemigrations
python manage.py migrate
```

### 5. Fetch Initial Weather Data

Set the timerange that you want to populate your DB with and then run the script to populate your database with data 
from the open source API.

NOTE: There is already data pre-saved as json available under weather/data/weather_data_2024-01-01_2024-12-31.json 
which will be used by default. If you want to fetch data from the public API you need to delete it.
```sh
python -m weather.database_helper
```

**API used:**

https://open-meteo.com/en/docs/historical-weather-api

---

## Usage

After completing setup, you can start the Django development server:

```sh
python manage.py runserver
```

You can now access API endpoints for:

* Getting average temperature per city and period
* Getting most common weather per city and period

See the [API documentation](API.md) for details on endpoint usage.

---
