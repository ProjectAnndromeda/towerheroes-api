# towerheroes-api

PROOF OF CONCEPT API for Tower Heroes
This is a simple Flask API to fetch Tower Hero character data.

## Setup Instructions

### Prerequisites

1. **Python 3.x**: Make sure you have Python 3.x installed. You can download it from [python.org](https://www.python.org/).
2. **pip**: Ensure you have pip (Python package installer) installed. It usually comes with Python.

### Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/ProjectAnndromeda/towerheroes-api.git
    cd towerheroes-api
    ```

2. **Create a Virtual Environment** (optional but recommended):

    ```bash
    python -m venv venv
    ```

3. **Activate the Virtual Environment**:

    - **Windows Command Prompt**:

        ```bash
        venv\Scripts\activate
        ```

    - **Windows PowerShell**:

        ```powershell
        .\venv\Scripts\Activate.ps1
        ```

    - **macOS/Linux**:

        ```bash
        source venv/bin/activate
        ```

4. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

### Running the API

1. **Run the Flask Application**:

    ```bash
    flask run
    ```

2. **Access the API**:

    Open Google Chrome or API client (like Postman) and navigate to:

    ```
    http://127.0.0.1:5000/get_tower_info?tower_type=Chef (or any other tower type)
    ```

### Example Response

```json
{
  "gender": "Male",
  "price": "0",
  "limit": "12",
},
{
  "level 1": {
    "mana_cost": "5",
    "damage": "10",
    "range": "7",
    "detection": true,
    "rate": "1.5",
    "dps": "6.67"
  },
}
{
  "level 2": {
    "mana_cost": "10",
    "damage": "20",
    "range": "8",
    "detection": true,
    "rate": "1.4",
    "dps": "14.29"
  }
}
```

## Key Considerations

### Alpha Version

This API is currently in alpha. Many features do not work as intended. Consider checking the issues tab on GitHub.

## Attribution

If you use or modify this code, please include the following attribution in any related documentation or publicly accessible materials: "Powered by Anndromeda™ by Alina."

## License
This code is provided under the terms of the [LICENSE.md](LICENSE.txt) file included in this distribution.
