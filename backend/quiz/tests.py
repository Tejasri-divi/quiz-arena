from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from .models import Category, Question, QuizAttempt


class QuizArenaAPITests(APITestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="Python")
        self.q1 = Question.objects.create(
            category=self.cat, text="2 + 2 ?", option_a="3", option_b="4",
            option_c="5", option_d="6", correct="b")
        self.q2 = Question.objects.create(
            category=self.cat, text="Capital of India?", option_a="Delhi", option_b="Pune",
            option_c="Goa", option_d="Agra", correct="a")

    def login(self):
        self.client.post('/api/register/', {'username': 'tej', 'password': 'Quiz@12345'}, format='json')
        res = self.client.post('/api/login/', {'username': 'tej', 'password': 'Quiz@12345'}, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res.data['access'])

    def test_register_and_login(self):
        res = self.client.post('/api/register/', {'username': 'tej', 'password': 'Quiz@12345'}, format='json')
        self.assertEqual(res.status_code, 201)
        res = self.client.post('/api/login/', {'username': 'tej', 'password': 'Quiz@12345'}, format='json')
        self.assertIn('access', res.data)

    def test_weak_password_rejected(self):
        res = self.client.post('/api/register/', {'username': 'x', 'password': '123'}, format='json')
        self.assertEqual(res.status_code, 400)

    def test_wrong_password_rejected(self):
        self.client.post('/api/register/', {'username': 'tej', 'password': 'Quiz@12345'}, format='json')
        res = self.client.post('/api/login/', {'username': 'tej', 'password': 'wrong'}, format='json')
        self.assertEqual(res.status_code, 401)

    def test_categories_list(self):
        res = self.client.get('/api/categories/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data[0]['name'], 'Python')
        self.assertEqual(res.data[0]['question_count'], 2)

    def test_questions_do_not_leak_answers(self):
        res = self.client.get(f'/api/questions/?category={self.cat.id}&limit=10')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)
        self.assertNotIn('correct', res.data[0])

    def test_submit_requires_login(self):
        res = self.client.post('/api/submit/', {}, format='json')
        self.assertEqual(res.status_code, 401)

    def test_submit_scores_on_server(self):
        self.login()
        payload = {
            'category': self.cat.id,
            'answers': {str(self.q1.id): 'b', str(self.q2.id): 'c'},   # 1 right, 1 wrong
            'question_ids': [self.q1.id, self.q2.id],
        }
        res = self.client.post('/api/submit/', payload, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['score'], 1)
        self.assertEqual(res.data['total'], 2)
        self.assertEqual(QuizAttempt.objects.count(), 1)

    def test_unanswered_counts_as_wrong(self):
        self.login()
        payload = {'category': self.cat.id, 'answers': {},
                   'question_ids': [self.q1.id, self.q2.id]}
        res = self.client.post('/api/submit/', payload, format='json')
        self.assertEqual(res.data['score'], 0)
        self.assertEqual(res.data['total'], 2)

    def test_leaderboard_and_history(self):
        self.login()
        payload = {'category': self.cat.id,
                   'answers': {str(self.q1.id): 'b', str(self.q2.id): 'a'},
                   'question_ids': [self.q1.id, self.q2.id]}
        self.client.post('/api/submit/', payload, format='json')
        board = self.client.get('/api/leaderboard/')
        self.assertEqual(board.data[0]['user__username'], 'tej')
        self.assertEqual(board.data[0]['best'], 2)
        hist = self.client.get('/api/history/')
        self.assertEqual(len(hist.data), 1)
