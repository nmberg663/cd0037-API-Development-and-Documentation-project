import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format("nmberg", "abc", 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.cat1 = {"type": "Science"}
        self.cat2 = {"type": "Art"}
        self.cat3 = {"type": "Geography"}
        self.cat4 = {"type": "History"}
        self.cat5 = {"type": "Entertainment"}
        self.cat6 = {"type": "Sports"}

        self.new_question = 'What instruments does Nancy play?'
        self.new_answer = 'Clarient, Flute, Saxophone, Trombone'
        self.new_difficulty = 5
        self.new_category = 2

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_categories(self):
        print("test_get_all_categories")
        res = self.client().get("/categories")
        self.assertTrue(res.status_code == 200)
        data = json.loads(res.data)
        categories = data['categories']
        len_categories = len(categories)

        self.assertEqual(len_categories, 6)
        counter = 0;
        for category in categories:
           if counter == 0:
               self.assertTrue(category == ['Science'])
           elif counter == 1:
               self.assertTrue(category == ['Art'])
           elif counter == 2:
               self.assertTrue(category == ['Geography'])
           elif counter == 3:
               self.assertTrue(category == ['History'])
           elif counter == 4:
               self.assertTrue(category == ['Entertainment'])
           elif counter == 5:
               self.assertTrue(category == ['Sports'])
           counter = counter + 1
        pass

    def test_get_paginated_questions(self):
        print("test_Get_paginated_questions")
        db_questions = Question.query.all()
        len_db_questions = len(db_questions)
        res = self.client().get("/questions?page=1")
        data = json.loads(res.data)
        self.assertTrue(res.status_code == 200)

        returned_categories = data['categories']
        len_categories = len(returned_categories)
        self.assertTrue(len_categories == 6)

        returned_questions = data['questions']
        len_questions = len(returned_questions)
        self.assertTrue(len_questions == 10)
        self.assertTrue(len_db_questions == data['totalQuestions'])
        pass

        for question in returned_questions:
            first_category = question['category']
            break;
        self.assertTrue(first_category == data['currentCategory'])
        pass

    def test_get_paginated_questions_404(self):
        print("test_getPaginated_questions_404")
        res = self.client().get("/questions?page=10")
        self.assertTrue(res.status_code == 404)
        pass

    def test_get_questions_by_search(self):
        print("test_get_questions_by_search")
        try:
            res = self.client().post("/questions", json={'searchTerm': 'name'})
            data = json.loads(res.data)
            returned_questions = data['questions']
            len_returned_questions = len(returned_questions)
            self.assertTrue(len_returned_questions == 2)
            self.assertTrue(res.status_code == 200)
        except:
            self.assertTrue(False)
        pass

    def test_get_questions_by_search_404(self):
        print("test_get_questions_by_search_400")
        try:
            res = self.client().post("/questions", json={'searchTerm': 'not found'})
            self.assertTrue(res.status_code == 404)
        except:
            self.assertTrue(False)
        pass

    def test_add_question(self):
        print("test_add_question")
        try:
            new_question = 'How many fingers and toes do homosapiens normally have?'
            new_answer = 10
            new_difficulty = 1
            #input index of category (which indexes start at 0 = Science)
            new_category = 0
            res = self.client().post("/questions", json={'question': new_question, 'answer': new_answer, 'difficulty': new_difficulty, 'category': new_category})
            data = json.loads(res.data)
            self.assertTrue(data['success'] == True)

            added_question = Question.query.filter(Question.question==new_question).one_or_none()
            self.assertTrue(added_question != None)
            added_question.delete()
            added_question = Question.query.filter(Question.question==new_question).one_or_none()
            self.assertTrue(added_question == None)
        except:
            self.assertTrue(False)
        pass

    def test_add_question_invalid_category_404(self):
        print("test_add_question_invalid_category_404")
        try:
            new_question = "How many fingers and toes do homosapiens normally have?"
            new_answer = '10';
            new_difficulty = 1;
            #category range based on index is 0..5 input value > 5
            new_category = 8;
            res = self.client().post("/questions", json={'question': new_question, 'answer': new_answer, 'difficulty': new_difficulty, 'category': new_category})
            self.assertTrue(res.status_code == 404)
        except:
            self.assertTrue(False)
        pass

    def test_add_question_that_exists_404(self):
        print("test_add_question_that_exists_404")
        try:
            existing_question = Question.query.filter(Question.id==22).one_or_none()
            self.assertTrue(existing_question != None)
            self.assertTrue(existing_question.id == 22)
            question_22 = existing_question.question
            answer_22 = existing_question.answer
            difficulty_22 = existing_question.difficulty
            category_22 = existing_question.category - 1
            res = self.client().post("/quesetions", json={'question': question_22, 'answer': answer_22, 'difficulty': difficulty_22, 'category': category_22})
            self.assertTrue(res.status_code == 404)
        except:
            self.assertTrue(False)
        pass

    def test_delete_question(self):
        print("test_delete_question")
        try:
            #Add new question so the test controls the question being deleted
            new_question = Question(question=self.new_question, answer=self.new_answer, difficulty=self.new_difficulty, category=self.new_category)
            new_question.insert()
            added_question = Question.query.filter(Question.id==new_question.id).one_or_none()
            self.assertTrue(added_question != None)
            new_question_id = added_question.id

            #Now call API to delete the newly added question
            res = self.client().delete("/questions/"+str(new_question_id))
            data = json.loads(res.data)
            self.assertTrue(data['success'] == True)
            deleted_question = Question.query.filter(Question.id==new_question_id).one_or_none()
            self.assertTrue(deleted_question == None)

        except:
            print('caught an exception during the test')
            self.assertTrue(False)
        pass

    def test_delete_question_not_found_404(self):
        print("test_delete_question_not_found_404")
        try:
            delete_question_id = 70

            #Now call API to delete the question that does not exist
            res = self.client().delete("/questions/"+str(delete_question_id))
            data = json.loads(res.data)
            self.assertTrue(data['success'] == False)
            print('res.status_code: ', str(res.status_code))
            self.assertTrue(res.status_code == 422)

        except:
            print('caught an exception during the test')
            self.assertTrue(False)
        pass

    def test_get_questions_by_category_id(self):
        print("test_get_questions_by_category_id")
        try:
            #loop through all category id numbers -- note that input category id's are indexes so need to add 1 to get actual category id
            for i in range(0,6):
                category_id = i + 1
                current_category = Category.query.filter(Category.id==category_id).one_or_none()

                category_questions = Question.query.filter(Question.category==category_id).all()
                num_category_questions = len(category_questions)

                res = self.client().get("/categories/"+str(i)+"/questions")

                self.assertTrue(res.status_code == 200)

                data = json.loads(res.data)
                questions = data['questions']
                total_questions = data['totalQuestions']
                returned_current_category = data['currentCategory']
                self.assertTrue(total_questions == num_category_questions)
                print('current_category: ', current_category.type, ' returned_current_category: ', returned_current_category)
                self.assertTrue(current_category.type == returned_current_category[0])
        except:
            print('exception caught during get_questions_by_category')
            self.assertTrue(False)
        pass

    def test_get_questions_by_non_exiting_category_id_400(self):
        print("test_get_questions_by_non_existing_category_id_404")
        res = self.client().get("/categories/10/questions")
        self.assertTrue(res.status_code == 422)

    def test_quizzes_using_category_entertainment(self):
        print("test_quizzes_using_category_entertainment")
        try:
            new_question1 = 'Who was the first black person to win an Oscar for acting?'
            new_answer1 = 'Hattie McDonald'
            new_difficulty1 = 5
            new_category1 = 5
            add_question1 = Question(question=new_question1, answer=new_answer1, difficulty=new_difficulty1, category=new_category1)
            add_question1.insert()

            new_question2 = 'Who played Wayne in Wayne’s World 2?'
            new_answer2 = 'Mike Myers'
            new_difficulty2 = 3
            new_category2 = 5
            add_question2 = Question(question=new_question2, answer=new_answer2, difficulty=new_difficulty2, category=new_category2)
            add_question2.insert()

            new_question3 = 'In which fictitious country is “Black Panther ” set?'
            new_answer3 = 'Wakanda'
            new_difficulty3 = 1
            new_category3 = 5
            add_question3 = Question(question=new_question2, answer=new_answer2, difficulty=new_difficulty2, category=new_category2)
            add_question3.insert()

            entertainment_questions = Question.query.filter(Question.category==5)
            self.assertTrue(entertainment_questions.count() > 5)

            previous_questions = []
            quiz_category =  {'type': ['Entertainment'], 'id': '4'}
            for i in range(0,5):
                res = self.client().post("/quizzes", json={'previous_questions': previous_questions, 'quiz_category': quiz_category})               
                self.assertTrue(res.status_code == 200)
                data = json.loads(res.data)
                next_question = data['question']
                question_id = next_question['id']
                previous_questions.append(question_id)
        except:
            print('caught an exception in quizzes')
            self.assertTrue(False)
        finally:
            add_question1.delete()
            add_question2.delete()
            add_question3.delete()
        pass

    def test_quizzes_using_category_all(self):
        print("test_quizzes_using_category_all")
        try:
            previous_questions = []
            quiz_category = {'type': 'click', 'id': 0}
            all_category = "click"
            category_str = quiz_category['type']
            self.assertTrue(category_str == all_category)
            for i in range(0,5):
                res = self.client().post("/quizzes", json={'previous_questions': previous_questions, 'quiz_category': quiz_category})
                self.assertTrue(res.status_code == 200)
                data = json.loads(res.data)
                next_question = data['question']
                question_id = next_question['id']
                category_id = next_question['category']
                print('random question id: ', question_id, " associated category_id: ", category_id)
                previous_questions.append(question_id)
        except:
            print('caught an exception in quizzes')
            self.assertTrue(False)
        pass

    def test_quizzes_using_category_science_but_less_than_5_questions(self):
        print('test_quizzes_using_category_science_but_less_than_5_questions')
        try:
            science_questions = Question.query.filter(Question.category==1)
            self.assertTrue(science_questions.count() < 5)

            previous_questions = []
            #For this API, the category is the index of the category which starts at 0 instead of 1
            quiz_category =  {'type': ['Science'], 'id': '0'}
            for i in range(0,5):
                res = self.client().post("/quizzes", json={'previous_questions': previous_questions, 'quiz_category': quiz_category})
                if i < science_questions.count():
                    self.assertTrue(res.status_code == 200)
                    data = json.loads(res.data)
                    next_question = data['question']
                    question_id = next_question['id']
                    previous_questions.append(question_id)
                else:
                    self.assertTrue(res.status_code == 422)

        except:
            print('caught an exception in quizzes')
            self.assertTrue(False)
        pass

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
