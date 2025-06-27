# Agile Artifacts

## Sprint backlog list of achievables (annotate changes made during sprint, including data required)

- Improve code optimization
- Encrypt sensitive information
- Improve UX further
- Add a final README.md
- Conduct thorough tests and evaluation

## Increment (what must be achieved by the end of the sprint)

- Optimize code through caching weather information locally
- Encrypt TOTP and Email to improve sensitive information security
- Implement customisation regarding colour schemes
- Update README.md to include finalised system and user documentation
- Test using a range of methodologies

## Sprint Review (Focus on project management)

### What challenges did you have

- Integrating secure encryption for sensitive user data (TOTP secrets and emails) required careful handling to avoid breaking authentication and user flows.
- Implementing weather data caching involved managing cache invalidation and ensuring up-to-date information without excessive API calls.
- Ensuring accessibility and usability for all user groups, especially for users with limited technical skills or accessibility needs.
- Managing and testing 2FA setup and verification across different devices and authenticator apps.
- Handling edge cases in recipe saving (e.g., preventing duplicate saves) and review submission.

### What did you do well

-Successfully optimized code by implementing local caching for weather information, reducing API calls and improving response time.

- Enhanced security by encrypting TOTP secrets and user emails in the database.
- Improved user experience by adding a customizable colour scheme (dark mode) and ensuring the UI is accessible and readable for all ages.
- Completed and updated the README.md with comprehensive system and user documentation.
- Thoroughly tested all core functionalities, including dietary filtering, review system, and 2FA, with positive feedback from a diverse group of clientel.

### What will you do differently next time

- Allocate more time for user feedback sessions earlier in the sprint to catch usability issues sooner.
- Automate more of the testing process, especially for edge cases and security features, to reduce manual testing workload.
- Improve documentation of code changes and decisions during the sprint for easier tracking and knowledge sharing.
