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

- **Sign Up:** Create an account with a username, password, and location.(Or login with Username: Testuser, Password: Testuser123!)
- **Login:** Log in with your credentials.
- **Enable 2FA (optional):** Go to your dashboard and enable two-factor authentication for extra security.
- **Get Recipes:** Enter your dietary preferences and get recipe suggestions based on your local weather.
![Screen recording of WeatherSpoon in action](/docs/README_resources/WeatherSpoonAction.gif)

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
├── api.py                  # Backend API for user management
├── main.py                 # Main Flask app
├── database_manager.py     # Database functions and encryption
├── forms.py                # WTForms definitions and validation
├── form_manager.py         # Form handling and logic
├── recipes.py              # Recipe and weather logic
├── savedrecipes.py         # Saved recipes logic
├── sanitize.py             # Input sanitization functions
├── secure_session.py       # Secure session management
├── twofa.py                # 2FA logic and QR code generation
├── userLogic.py            # User-related business logic
│
├── templates/              # HTML templates
│   ├── add.html
│   ├── dashboard.html
│   ├── edit_profile.html
│   ├── enable_2fa.html
│   ├── index.html
│   ├── landing.html
│   ├── layout.html
│   ├── login.html
│   ├── makereview.html
│   ├── privacy.html
│   ├── recipe_detail.html
│   ├── recipes.html
│   ├── savedrecipes.html
│   ├── signup.html
│   ├── verify_2fa_setup.html
│   └── partials/
│       ├── footer.html
│       └── menu.html
│
├── static/
│   ├── css/
│   │   ├── bootstrap.min.css
│   │   └── style.css
│   └── (other static assets)
│
├── docs/                   # Documentation
│   ├── README.md
│   ├── agileArtifact.md
│   ├── productBacklog.md
│
├── requirements.txt        # Python dependencies
```

---

## Project Pitch

![Screen recording of Project Pitch](/docs/README_resources/WeatherSpoonPitch.gif)

## Summary of Agile Sprints

### Sprint 1

Link to Branch:

- [Sprint 1](https://github.com/TempeHS/Max-H-HSC-MajorProject-2025SE/tree/sprint-0.1)

Implemented features:

- Secure Registration and login
- Hashed passwords
- Privacy by design
- User Preferences
- 2FA
  Improvements for next Sprint:

- Improve on breaking down tasks
- Better time allocation

### Sprint 2

Link to branch:

- [Sprint 2](https://github.com/TempeHS/Max-H-HSC-MajorProject-2025SE/tree/sprint-0.2)

Implemented Features:

- Session management
- Save recipes
- Profile editing
- Improved UX

Improvements for next Sprint:

- Plan for edge cases
- Write more tests and test on a wider range of devices

### Sprint 3

Link to branch:

- [Sprint 3](https://github.com/TempeHS/Max-H-HSC-MajorProject-2025SE/tree/sprint-0.3)

Implemented Features:

- Code optimization
- Encryption
- Customisation

Improvements for next Sprint:

- Plan migrations for encrypted data
- Automate documentation updates.

## Final Gantt chart

![Final Gantt](/docs/README_resources/WeatherSpoonCompleteGantt.png)

## Developer Documentation

### Developer Diaries

[Dev Diaries](https://drive.google.com/file/d/1k5Ftu-xBbS_1tu243NFiDBR6TFCbrsTg/view)

### UAT Document

[UAT Document](https://drive.google.com/file/d/1nKfKVMcLi9HadYzIh3A15DHeNux20pI4/view)

### Completed Systems Report

[Completed Sytems Report](https://drive.google.com/file/d/1P80kld4iCAnFM5e9pN7_eGtV4A6YWl3n/view)

## Remaining Product Backlog

- Prevent duplicate recipe saves in the saved recipes list.
- Allow users to edit or delete their reviews after submission.
- Add keyboard navigation and enhanced screen reader support for improved accessibility.
- Implement user notifications for important actions (e.g., successful save, review posted, 2FA enabled).
- Add analytics/dashboard for users to view their activity (e.g., recipes saved, reviews posted).
- Improve error messages for API failures or connectivity issues.
- Add multi-language support for broader accessibility.
- Enhance mobile responsiveness further for a wider range of devices.

## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.

## The rights of this application are under MAX

## Contact

For questions or support, please contact Maxwell Hrycyk-Oh at:

- maxwell.hrycykoh@education.nsw.gov.au
