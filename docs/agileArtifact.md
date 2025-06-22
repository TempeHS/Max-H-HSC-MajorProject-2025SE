# Agile Artifacts

## Sprint backlog list of achievables (annotate changes made during sprint, including data required)

- Session management for logged in users
- More defensive data handling practices
- Implement more UX principles within application
- More features within the app to make it more accessible and enhance the User Experience

## Increment (what must be achieved by the end of the sprint)

- Implement session management through timeouts and logout during page reload
- SQL database for user's saved recipes
- Users can leave reviews for others to see
- Enhanced and responsive frontend for the weatherspoon application
- Users can edit their profiles

## Sprint Review (Focus on project management)

### What challenges did you have

- Debugging issues with Jinja2 template syntax, especially with list comprehensions and undefined variables.
- Ensuring saved recipes and reviews were correctly stored and displayed from the database.
- Improving the user interface with gradients, icons, and responsive design.
- Managing session state and user feedback (e.g., flash messages) for a better user experience.

### What did you do well

- Fixed database logic so users can save recipes and leave reviews, and ensured these are displayed correctly.
- Improved error handling and user feedback throughout the app.
- Improved security by restricting access to sensitive features until 2FA is verified.

### What will you do differently next time

- Plan for edge cases and user flows involving authentication and session state earlier in the sprint.
- Write more unit and integration tests to catch template and backend errors sooner.
- Allocate more time for testing on different devices and browsers to ensure consistent user experience.
