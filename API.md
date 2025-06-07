
---

# Nimbus - Weather Service API

This API allows querying weather information for cities, such as average temperature and most common weather conditions over a specified period.

## Base URL

```
/weather/
```

---

## Endpoints

### 1. `GET /weather/average-temperature/`

**Description:**
Returns the average temperature for a city over a date range.

**Parameters:**

| Name  | Type   | Required | Example      | Description             |
| ----- | ------ | -------- |--------------| ----------------------- |
| city  | string | yes      | `Berlin`     | The name of the city    |
| start | date   | yes      | `2024-01-01` | Start date (YYYY-MM-DD) |
| end   | date   | yes      | `2024-01-31` | End date (YYYY-MM-DD)   |

**Example Request:**

```
GET /weather/average-temperature/?city=Berlin&start=2024-01-01&end=2024-01-31
```

**Response:**

* **200 OK**

  ```json
  {
    "city": "Berlin",
    "average_temperature": 3.5
  }
  ```
* **400 Bad Request**
  Missing or invalid parameters.

  ```json
  {
    "error": "Missing city name"
  }
  ```
* **404 Not Found**
  No data for that period/city.

  ```json
  {
    "error": "No data available"
  }
  ```

---

### 2. `GET /weather/most-common-weather/`

**Description:**
Returns the most common weather condition for a city over a date range.

**Parameters:** (Same as above)

**Example Request:**

```
GET /weather/most-common-weather/?city=Berlin&start=2024-01-01&end=2024-01-31
```

**Response:**

* **200 OK**

  ```json
  {
    "city": "Berlin",
    "most_common_weather": "partly cloudy"
  }
  ```
* **400 Bad Request**

  ```json
  {
    "error": "Missing city name"
  }
  ```
* **404 Not Found**

  ```json
  {
    "error": "No data available"
  }
  ```

---

### 3. `GET /weather/`

**Description:**
A welcome message.

**Example Response:**

```
Welcome to the Nimbus - Weather Service!
```

---

## Error Handling

* All errors return a JSON object with an `"error"` field and appropriate HTTP status code.

---

## Examples

#### Average temperature for Berlin, January 2025

```sh
curl "http://localhost:8000/weather/average-temperature/?city=Berlin&start=2024-01-01&end=2024-01-31"
```

#### Most common weather for Berlin, January 2025

```sh
curl "http://localhost:8000/weather/most-common-weather/?city=Berlin&start=2024-01-01&end=2024-01-31"
```

---

## Conventions

* Dates must be in `YYYY-MM-DD` format.
* All responses are JSON unless otherwise stated.
* All endpoints are `GET` requests.

---
