# Agile Artifacts

## Sprint backlog list of achievables (annotate changes made during sprint, including data required)

~~- Secure user registration and login system~~
~~- Privacy handling policy~~
~~- Implement a strict content security policy~~
~~- Secure session management~~
~~- Passwords securely stored after being hashed~~
~~- User's location is attained for weather~~
~~- User preferences are accounted for~~
~~- 2 Factor Authentication~~

## Increment (what must be achieved by the end of the sprint)

- SQLite database design and integration for login/sign-up
- Functioning login and signup page
- Users can input dietary preferences/requirements
- Secure web development practices throughout all stages of app developement(Frontend, Backend, data handling)

## Sprint Review (Focus on project management)

### What challenges did you have

- Managing session cookies:

  - Ensuring secure handling and storage of session cookies, especially with 2FA and user authentication, required reiteration and review of my code that left me at times where it felt as if I was spinning my wheels but after planning and testing I got it to work.

- Coordinating Frontend and backend integration:
  - Aligning the data flow between user input forms, backend validation, and database storage took more time and effort than expected as I had to carefully interpret debugging tools to understand where In the frontend and backend communication that problems were occuring.

### What did you do well

- Debugged any issues:
  - Proactively tested both frontend and backend components to ensure smooth integration especially during implementation of my 2FA where i utilised browser developer tools to diagnose the issue (Being incorrect CSP headers not allowing images) and get 2FA working in my application.
- Communicated with clients:
  - A few times throughout the sprint I had to take a step back and analyse the feasibility of the project scope but after consulting with my clients I understood that they weren't expecting the new ChatGPT but just an application to eleviate their decision fatigue.
- Secure development practices:
  - I ensured that all user data was sanitized for security of the application and further hashed and stored their information securely for the security and privacy of users.

### What will you do differently next time

- Breakdown larger tasks into smaller ones:
  - This will help me have more manageable and feasible objectives to improve progress tracking and will provide more incentive to me as I will see more day-to-day improvements to the software.
- Time allocation:
  - Allocate more time for thorough plsnninh and task estimation to reduce unexpected delays.
