# WeatherSpoon

WeatherSpoon is a secure web application that provides weather-based recipe suggestions, allowing users to input dietary preferences and location to receive personalized recipe recommendations.

---

## Features

- **User Registration & Login:** Secure signup and login with hashed passwords.
- **Two-Factor Authentication (2FA):** Users can enable 2FA for added security.
- **Weather-Based Recipes:** Get recipe suggestions based on your local weather and dietary needs.
- **Secure Session Management:** Sessions are securely managed and protected.
- **Sanitized User Input:** All user data is sanitized to prevent security vulnerabilities.

---

## Requirements

- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/)
- SQLite (included with Python)
- [Spoonacular API Key](https://spoonacular.com/food-api) (for recipes)
- [OpenWeatherMap API Key](https://openweathermap.org/api) (if using weather API)

---

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/WeatherSpoon.git
   cd WeatherSpoon
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database:**

   - The app uses SQLite. On first run, it will create the database file if it doesn't exist.
   - If you want to manually create the tables, use the schema in `database_manager.py`.

4. **Configure API Keys:**
   - Add your Spoonacular API key in `recipes.py`:
     ```python
     SPOONACULAR_API_KEY = "YOUR_SPOONACULAR_API_KEY"
     ```
   - (Optional) Add your OpenWeatherMap API key in your weather module if required.

---

## Running the Application

1. **Start the backend API (port 3000):**

   ```bash
   python api.py
   ```

2. **Start the main Flask app (port 5000):**

   ```bash
   python main.py
   ```

3. **Open your browser and go to:**
   ```
   http://localhost:5000/
   ```

---

## Usage

- **Sign Up:** Create an account with a username, password, and location.
- **Login:** Log in with your credentials.
- **Enable 2FA (optional):** Go to your dashboard and enable two-factor authentication for extra security.
- **Get Recipes:** Enter your dietary preferences and get recipe suggestions based on your local weather.

---

## Security Notes

- All passwords are hashed before storage.
- 2FA is available and recommended for all users.
- User input is sanitized to prevent XSS and injection attacks.
- Sessions are securely managed and cookies are set with secure flags.

---

## Project Structure

```
/workspaces/Max-H-HSC-MajorProject-2025SE/
│
├── api.py                # Backend API for user management
├── main.py               # Main Flask app
├── database_manager.py   # Database functions
├── forms.py              # WTForms definitions
├── form_manager.py       # Form handling logic
├── twofa.py              # 2FA logic
├── recipes.py            # Recipe and weather logic
├── templates/            # HTML templates
├── static/               # CSS, JS, images
├── docs/                 # Documentation
└── requirements.txt      # Python dependencies
```

---

## License

## The rights of this application are under MAX

## Contact

For questions or support, please contact Maxwell Hrycyk-Oh at:

- maxwell.hrycykoh@education.nsw.gov.au
