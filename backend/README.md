# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Documentation for Trivia Project

Trivia API Reference

Description: The Trivia API provides several APIs that can be used to populate a trivia database for use in the /quizzes API which allows users to play a trivia game which includes 5 questions in either a specific category or all categories.  The APIs also include the ability to retrieve a list of questions (which are paginated to 10 questions a page), retrieve a list of questions for a specific category, search the trivia database for a specific search term (case insensitive) and finally, the ability to delete a question.
 
  Getting Started
  * Base URL: At present this app can only be run locally and is not hosted on a base URL. The backend app is hosted (by defaul) at http://127.0.0.1:5000/, which is set as a proxy in the frontend app configuration.
  * Authentication: This version of the app does not require authentication or API keys.

Error Handling

Errors are returned as json objects in the following format:

{
    "success": False,
    "error": 400,
    "message": "bad request",
}

The Trivia API will return the following error codes:
  * 400: "bad request"
  * 401: "no more questions"
  * 404: "resource not found"
  * 422: "unprocessable"
  * 500: "internal server error"

Endpoints

`GET '/trivia_api/v1.01/categories'

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
- Errors: No errors are returned in this endpoint

Return json example:
```json
{
  "categories": [
   [
     "Science"
   ],
   [
     "Art"
   ],
   [
     "Geography"
   ],
   [
     "History"
   ],
   [
     "Entertainment"
   ],
   [
     "Sports"
   ]
}
```

Curl Example:
$ curl -X GET localhost:5000/trivia_api/v1.01/categories
{
  "categories": [
    [
      "Science"
    ], 
    [
      "Art"
    ], 
    [
      "Geography"
    ], 
    [
      "History"
    ], 
    [
      "Entertainment"
    ], 
    [
      "Sports"
    ]
  ]


GET '/trivia_api/v1.01/questions?page=1'

- Fetches paginated questions (currently defined as up to 10 questions) based on the input page number
- Request Arguments: page number to display
- Returns: An object containing a list of questions based on the requested page, total number of questions, list of the categories 'type' and the categories 'id' for the first question returned.
  Errors: This API can return an error of 404 if there are no questions to return

Return json example:
```json
{
  "questions": [{'id': 1, 'question': 'What is the largest known land animal?', 'answer': 'Elephant', 'category': 1}]
  "totalQuestions": 1
  "categories": ['Science', 'Art', 'Geography', 'History', 'Entertainment', 'Sports'],
  "currentCategory": 1,
}
```

Curl Examples:
SUCCESS:
$ curl -X GET localhost:5000/trivia_api/v1.01/questions?page=1
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "currentCategory": 1, 
  "questions": [
    {
      "answer": "Elephant", 
      "category": 1, 
      "difficulty": 2, 
      "id": 34, 
      "question": "What is the largest known land animal?"
    }, 
    {
      "answer": "Zero", 
      "category": 1, 
      "difficulty": 2, 
      "id": 35, 
      "question": "How many bones do sharks have?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Oxygen", 
      "category": 1, 
      "difficulty": 3, 
      "id": 31, 
      "question": "What element did Joseph Priestley discover in 1774?"
    }, 
    {
      "answer": "Ozone", 
      "category": 1, 
      "difficulty": 3, 
      "id": 32, 
      "question": "What inorganic molecule is produced by lightning?"
    }, 
    {
      "answer": "Mercury", 
      "category": 1, 
      "difficulty": 3, 
      "id": 33, 
      "question": "What is the nearest planet to the sun?"
    }, 
    {
      "answer": "Water lily paintings", 
      "category": 2, 
      "difficulty": 4, 
      "id": 37, 
      "question": "Claude Monet is most known for his paintings of what? "
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "totalQuestions": 33
}

ERROR
$ curl -X GET localhost:5000/trivia_api/v1.01/questions?page=1000
{
  "error": 404, 
  "message": "NotFound", 
  "success": false
}


DELETE '/trivia_api/v1.01/questions/<int:question_id>'

- Deletes the question associated with the input question_id
- Request Arguments: question_id is the 'id' of the question to be deleted
- Returns: An object with 'success' set to True when the delete is successful
- Errors: This API returns error 400 or 422

Return json example:
```json
{
    "success": True,
}
```

Curl Examples:
SUCCESS
$ curl -X DELETE localhost:5000/trivia_api/v1.01/questions/59
{
  "success": true
}
ERROR
$ curl -X DELETE localhost:5000/trivia_api/v1.01/questions/590
{
  "error": 422, 
  "message": "unprocessable", 
  "success": false
}

POST '/trivia_api/v1.01/questions'
- Returns a list of questions based on an input search term
- Request Arguments: provide a json object containing 'searchTerm' and the value to use in the search
- Returns: If questions are found that match the search term, a list of questions containing the search term
- Errors: This API returns errors 404 or 422

Input json example:
```json

{
  'searchTerm': 'name'
}
```

Return json example:
```json
{
    'questions': [{'id': 9, 'question': "What boxer's original name is Cassius Clay?", 'answer': 'Muhammad Ali', 'difficulty': 1, 'category': 4}, {'id': 10, 'question': 'Which is the only team to play in every soccer World Cup tournament?', 'answer': 'Brazil', 'difficulty': 3, 'category': 6}],
    'totalQuestions': 2,
    'currentCategory':  History
}
```

Curl examples:
SUCCESS
$ curl -X POST localhost:5000/trivia_api/v1.01/questions -H "content-Type: application/json" -d '{"searchTerm": "name"}'
{
  "currentCategory": "History", 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }
  ], 
  "totalQuestions": 2
}
ERROR
$ curl -X POST localhost:5000/trivia_api/v1.01/questions -H "content-Type: application/json" -d '{"searchTerm": "not found"}'
{
  "error": 404, 
  "message": "NotFound", 
  "success": false
}

POST '/trivia_api/v1.01/questions'
- Using the provided input json containing data for a single question, adds the question to the questions table
- Request Arguments: Provide a json object containing the following: question (text), answer(text), difficulty(1..5), category(1..6)
- Returns: 
- Errors:

Input json example:
```json
{
  'question': 'This is an Art question?', 
  'answer': 'Art', 
  'difficulty': 1, 
  'category': '1'
}
```

Return json example for successful add:
```json
{
  "success": True,
}
```

Curl Examples:
SUCCESS
$ curl -X POST localhost:5000/trivia_api/v1.01/questions -H "content-Type: application/json" -d '{"question": "This is an Art question number 2?", "answer": "Art", "difficulty": 1, "category": "1"}'
{
  "success": true
}
ERROR:
$ curl -X POST localhost:5000/trivia_api/v1.01/questions -H "content-Type: application/json" -d '{"question": "This is an Art question number 2?", "answer": "Art", "difficulty": 1, "category": "1"}'
{
  "error": 404, 
  "message": "NotFound", 
  "success": false
}

GET '/trivia_api/v1.01/categories/<int:cat_id>/questions'
- Returns a list of questions based on the input category id .. though this id is one less than the categories 'id' since it is an index into the categories (which starts at zero)
- Request Arguments: category id index.  This is one less than the categories 'id' since it is an index into the categories (which starts at zero) 
- Returns: Returns a list of questions matching the category provided
- Errors: This API returns errors 404 (if no questions match the category) or 422 (general exception)

Return json example:
```json
{
  "currentCategory": [
    "Science"
  ],
  "questions": [
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "totalQuestions": 1 
}
```

Curl Examples:
SUCCESS
$ curl -X GET localhost:5000/trivia_api/v1.01/categories/0/questions
{
  "currentCategory": [
    "Science"
  ], 
  "questions": [
    { "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Oxygen", 
      "category": 1, 
      "difficulty": 3, 
      "id": 31, 
      "question": "What element did Joseph Priestley discover in 1774?"
    }, 
    {
      "answer": "Ozone", 
      "category": 1, 
      "difficulty": 3, 
      "id": 32, 
      "question": "What inorganic molecule is produced by lightning?"
    }, 
    {
      "answer": "Mercury", 
      "category": 1, 
      "difficulty": 3, 
      "id": 33, 
      "question": "What is the nearest planet to the sun?"
    }, 
    {
      "answer": "Elephant", 
      "category": 1, 
      "difficulty": 2, 
      "id": 34, 
      "question": "What is the largest known land animal?"
    }, 
    {
      "answer": "Zero", 
      "category": 1, 
      "difficulty": 2, 
      "id": 35, 
      "question": "How many bones do sharks have?"
    }
  ], 
  "totalQuestions": 6
}
ERROR
$ curl -X GET localhost:5000/trivia_api/v1.01/categories/10/questions
{
  "error": 422, 
  "message": "unprocessable", 
  "success": false
}

POST '/trivia_api/v1.01/quizzes'

- Returns the first (or next) question in the selected category quiz.  The quiz consists of 5 random questions in a selected category OR random question in all categories (specified by category name "click')
- Request Arguments: json object containing
      list of previous_questions (identified by questions.id) such as [2, 10, 25]  The initial list will be empty.
      category: this is the categories.type value (such as "Science", or 'click' to select questions in all categories)
- Errors returned: This API returns 401 or 422

Input json example:
```json
{
    'previous_questions': [], 
    'quiz_category': {'type': ['Science'], 'id': '0'}
}
```

Return json example:
```json
{
  "question": 
    {
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?",
      "answer": "Blood",
      "difficulty": 4,
      "category": 1,
    }
}
```

Curl Examples:
SUCCESS
$ curl -X POST localhost:5000/trivia_api/v1.01/quizzes -H "content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"type": ["Science"], "id": "0"}}'
{
  "question": {
    "answer": "Elephant", 
    "category": 1, 
    "difficulty": 2, 
    "id": 34, 
    "question": "What is the largest known land animal?"
  }
}

ERROR
$ curl -X POST localhost:5000/trivia_api/v1.01/quizzes -H "content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"type": ["Science"], "id": "0"}}'
{
  "error": 422, 
  "message": "unprocessable", 
  "success": false
}
