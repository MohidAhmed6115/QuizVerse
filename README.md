# QuizVerse

QuizVerse is a web-based quiz game built with Flask and Jinja templates, styled with Tailwind CSS. It lets users create an account, choose a quiz category, and answer multiple-choice questions pulled from a MySQL database.

## Features

### Implemented / In Progress
- **User Login** — authenticate existing users
- **User Signup** — create a new account
- **Main Page** — landing page introducing the game
- **Category Selection** — choose which type of quiz to play (e.g. Science, History, Geography, Human Body)
- **Question Bank** — questions served from a MySQL database

### Planned
- **Community Question Submission** — allow users to contribute new questions to the database

## Tech Stack

| Layer     | Technology        |
|-----------|--------------------|
| Backend   | Flask (Python)     |
| Templating| Jinja2             |
| Frontend  | Tailwind CSS       |
| Database  | MySQL              |

## Project Structure

```
quizverse/
├── app.py                 # Application entry point
├── templates/
│   ├── base.html          # Shared layout
│   ├── index.html         # Main/landing page
│   ├── login.html         # Login page
│   ├── signup.html        # Signup page
│   └── quiz/               # Quiz selection and question pages
├── static/
│   └── assets/             # Images and static files
├── requirements.txt
└── README.md
```

*(Adjust this tree to match your actual folder layout as the project grows.)*

## Getting Started

### Prerequisites
- Python 3.x
- MySQL server running locally or accessible remotely
- pip

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/<your-username>/quizverse.git
   cd quizverse
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables

   Create a `.env` file in the project root with your database credentials and Flask secret key:
   ```
   FLASK_SECRET_KEY=your_secret_key
   DB_HOST=localhost
   DB_USER=your_mysql_user
   DB_PASSWORD=your_mysql_password
   DB_NAME=quizverse
   ```

5. Set up the database

   Create the MySQL database and required tables (users, questions, categories, etc.) before running the app.

6. Run the application
   ```bash
   flask run
   ```

   The app will be available at `http://127.0.0.1:5000`.

## Usage

1. Visit the main page and sign up for an account, or log in if you already have one.
2. Choose a quiz category from the selection page.
3. Answer the multiple-choice questions and view your results.

## Roadmap

- [ ] Finalize login and signup flows
- [ ] Build category selection page
- [ ] Connect question bank to MySQL
- [ ] Add scoring and results summary
- [ ] Allow users to submit new questions
- [ ] Add leaderboards

## Contributing

Contributions are welcome once the core features are stable. Please open an issue to discuss any significant changes before submitting a pull request.

## License

No license has been chosen yet. All rights reserved by default until a license is added.
