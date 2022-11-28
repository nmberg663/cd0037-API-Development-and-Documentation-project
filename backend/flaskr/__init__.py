import os
import sys
import json
from flask import (
        Flask, 
        request, 
        abort, 
        jsonify, 
        )

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection, return_all):
    if return_all == False:
        page = request.args.get("page", 1, type=int)

        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
    else:
        start = 0
        end = len(selection)

    questions = [question.format() for question in selection]
    if end > 1:
        selected_questions = questions[start:end]
    else:
        selected_questions = questions

    return selected_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Origin", "*"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories", methods=['GET'])
    def retrieve_categories():
        query = Category.query.order_by(Category.id).with_entities(Category.type)
        if query.count() == 0:
            abort(404)

        return jsonify(
            {
                "categories": query.all(),
            }
        )

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route("/questions", methods=["GET"])
    def retrieve_questions():
        selection = Question.query.order_by(Question.category).all()

        current_questions = paginate_questions(request, selection, False)

        if len(current_questions) == 0:
            abort(404)

        for question in current_questions:
            current_category = question['category']
            break;

        query = Category.query.order_by(Category.id).with_entities(Category.id, Category.type)
        queryCount = query.count()
        if queryCount == 0:
            abort(404)

        categories = []
        for category in query:
            categoryType = category.type
            categories.append(category.type)

        return jsonify(
            {
                "questions": current_questions,
                "totalQuestions": len(selection),
                "categories": categories,
                "currentCategory": current_category,
            }
        )


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                print('Did not find question for delete. id = ', str(question_id))
                abort(400)

            question.delete()

            return jsonify(
                {
                    "success": True,
                }
            )

        except:
            print('caught exception in delete_question')
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions", methods=["POST"])
    def create_search_question():
        body = request.get_json()
        data = []
        try:
            search_term = body.get("searchTerm", None)
            if search_term != None:
                result = Question.query.filter(func.lower(Question.question).contains(search_term.lower())).with_entities(Question.id, Question.question, Question.answer, Question.difficulty, Question.category).order_by(Question.category).all()

                result_count = len(result)
                if (result_count == 0):
                    print('did not find anything with the search_term: ', search_term)
                    abort(404)
                else:
                    # obtain first category type
                    for first_question in result:
                        related_category = Category.query.filter(Category.id == first_question.category).one_or_none()
                        category_str = related_category.type
                        break;

                    if related_category == None:
                        print('related_category was set to None')
                        abort(404)

                questionResults = [{"id": q.id, "question": q.question, "answer": q.answer, "difficulty": q.difficulty, "category": q.category} for q in result]
                return jsonify(
                    {
                        "questions": questionResults,
                        "totalQuestions": result_count,
                        "currentCategory": category_str,
                    }
                    )
            else:        
                new_question = body.get("question", None)
                new_answer = body.get("answer", None)
                new_difficulty = body.get("difficulty", None)
                new_category_str = body.get("category", None)

                if new_category_str == None or new_question == None or new_answer == None or new_difficulty == None:
                    print('category does not exist')
                    abort(404)

                existing_question = Question.query.filter(Question.question==new_question).one_or_none()
                if existing_question != None:
                    print('existing question exists!!')
                    abort(404)

                new_category = int(new_category_str) + 1

                question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
                question.insert()

                return jsonify(
                    {
                        "success": True,
                    }
                    )

        except:
            abort(404)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:cat_id>/questions", methods=["GET"])
    def questions_by_category(cat_id):

        try:
            category_id = cat_id + 1
            current_category = Category.query.filter(Category.id==category_id).with_entities(Category.type).one_or_none()

            if current_category == None:
                abort(404)

            selection = Question.query.filter(Question.category==category_id).all()

            category_questions = paginate_questions(request, selection, True)

            return jsonify(
                {
                    "questions": category_questions,
                    "totalQuestions": len(selection),
                    "currentCategory": current_category,
                }
            )
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def quiz_next_question():
        previousQuestions = []
        body = request.get_json()
        all_category = "click"
        try:
            previousQuestions = body.get("previous_questions")
            quiz_category = body.get("quiz_category")
            category_str = quiz_category['type']
            if category_str == all_category:
                foundQuestion = False
                no_questions_left = False
                while foundQuestion == False and no_questions_left == False:
                    selectedQuestion = Question.query.filter(Question.id.notin_(previousQuestions)).order_by(func.random()).limit(1).one_or_none()
                    if selectedQuestion != None:
                        foundQuestion = True
                    else:
                        no_questions_left = True
            else:
                category_id = int(quiz_category['id']) + 1
             
                if len(previousQuestions) == 0:
                    selectedQuestion = Question.query.filter(Question.category==category_id).order_by(func.random()).limit(1).one_or_none()

                else:
                    selectedQuestion = Question.query.filter(Question.category==category_id, Question.id.notin_(previousQuestions)).order_by(func.random()).limit(1).one_or_none()

            if selectedQuestion != None:

                return jsonify({
                     "question": {
                         "id": selectedQuestion.id,
                         "question": selectedQuestion.question,
                         "answer": selectedQuestion.answer,
                         "difficulty": selectedQuestion.difficulty,
                         "category": selectedQuestion.category,
                     }
                  })
            else:
                print('no more questions left')
                abort(401)


        except:
            print('/quizzes .. got exception')
            abort(422)


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "NotFound"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}),
            400,
        )


    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify({"success": False, "error": 500, "message": "internal server error"}),
            500,
        )


    return app
