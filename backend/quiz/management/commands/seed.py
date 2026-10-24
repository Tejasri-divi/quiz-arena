from django.core.management.base import BaseCommand
from quiz.models import Category, Question

# (text, a, b, c, d, correct, difficulty)
DATA = {
    "Python": [
        ("Which keyword is used to define a function in Python?", "func", "def", "function", "define", "b", "easy"),
        ("What is the output of len([1, 2, 3])?", "2", "3", "4", "Error", "b", "easy"),
        ("Which data type is immutable in Python?", "list", "dict", "tuple", "set", "c", "easy"),
        ("Which symbol is used for comments in Python?", "//", "#", "/* */", "--", "b", "easy"),
        ("What does the 'range(3)' produce?", "1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "1, 2", "b", "easy"),
        ("Which method adds an item to the end of a list?", "add()", "insert_end()", "append()", "push()", "c", "easy"),
        ("What is the output of 2 ** 3?", "6", "8", "9", "5", "b", "easy"),
        ("Which library is mainly used for data analysis in Python?", "Flask", "Pandas", "Pygame", "Tkinter", "b", "medium"),
        ("What does a Python decorator do?", "Deletes a function", "Modifies the behaviour of a function", "Compiles code", "Creates a class", "b", "hard"),
        ("Which keyword is used to handle exceptions?", "catch", "except", "error", "handle", "b", "medium"),
    ],
    "SQL": [
        ("Which command is used to fetch data from a table?", "GET", "SELECT", "FETCH", "OPEN", "b", "easy"),
        ("Which clause filters rows in SQL?", "WHERE", "ORDER BY", "GROUP BY", "LIMIT", "a", "easy"),
        ("Which keyword removes duplicate values in results?", "UNIQUE", "DISTINCT", "DIFFERENT", "REMOVE", "b", "easy"),
        ("Which function counts the number of rows?", "SUM()", "TOTAL()", "COUNT()", "ROWS()", "c", "easy"),
        ("Which command adds new rows to a table?", "ADD", "INSERT INTO", "UPDATE", "CREATE", "b", "easy"),
        ("A PRIMARY KEY column can contain...", "Duplicate values", "NULL values", "Unique, non-null values", "Only text", "c", "medium"),
        ("Which JOIN returns only matching rows from both tables?", "LEFT JOIN", "RIGHT JOIN", "INNER JOIN", "FULL JOIN", "c", "medium"),
        ("Which clause sorts the result set?", "SORT BY", "ORDER BY", "ARRANGE", "GROUP BY", "b", "easy"),
        ("Which statement deletes a table completely?", "DELETE TABLE", "REMOVE TABLE", "DROP TABLE", "CLEAR TABLE", "c", "medium"),
        ("GROUP BY is usually used with...", "Aggregate functions", "Comments", "Views only", "Indexes only", "a", "medium"),
    ],
    "AI & Machine Learning": [
        ("What does ML stand for?", "Machine Learning", "Model Logic", "Multi Layer", "Meta Language", "a", "easy"),
        ("Which is a supervised learning algorithm?", "K-Means", "Linear Regression", "Apriori", "PCA", "b", "medium"),
        ("What is overfitting?", "Model performs well on new data", "Model memorises training data and fails on new data", "Model is too simple", "Model has no data", "b", "medium"),
        ("Which library is widely used for deep learning?", "TensorFlow", "Django", "Requests", "Matplotlib", "a", "easy"),
        ("What is a neural network inspired by?", "Computer chips", "The human brain", "Databases", "Networks cables", "b", "easy"),
        ("Which metric is used for classification accuracy?", "RMSE", "Accuracy score", "R-squared", "MAE", "b", "medium"),
        ("K-Means is an example of...", "Supervised learning", "Unsupervised learning", "Reinforcement learning", "Rule-based system", "b", "medium"),
        ("What is the purpose of a train-test split?", "Speed up coding", "Evaluate the model on unseen data", "Reduce file size", "Clean the data", "b", "easy"),
        ("NLP stands for...", "Natural Language Processing", "Neural Logic Program", "Numeric Learning Path", "Network Layer Protocol", "a", "easy"),
        ("Which activation function outputs values between 0 and 1?", "ReLU", "Sigmoid", "Linear", "Step down", "b", "hard"),
    ],
    "General Knowledge": [
        ("What is the capital of India?", "Mumbai", "New Delhi", "Kolkata", "Chennai", "b", "easy"),
        ("Which planet is known as the Red Planet?", "Venus", "Jupiter", "Mars", "Saturn", "c", "easy"),
        ("Who wrote the Indian national anthem?", "Bankim Chandra Chatterjee", "Rabindranath Tagore", "Sarojini Naidu", "Subhash Chandra Bose", "b", "medium"),
        ("How many continents are there?", "5", "6", "7", "8", "c", "easy"),
        ("Which is the largest ocean?", "Atlantic", "Indian", "Arctic", "Pacific", "d", "easy"),
        ("Which gas do plants absorb from the air?", "Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen", "b", "easy"),
        ("Who is known as the Father of the Nation in India?", "Jawaharlal Nehru", "Mahatma Gandhi", "Sardar Patel", "B. R. Ambedkar", "b", "easy"),
        ("Which is the longest river in India?", "Yamuna", "Godavari", "Ganga", "Krishna", "c", "medium"),
        ("What is H2O commonly known as?", "Salt", "Water", "Hydrogen", "Oxygen", "b", "easy"),
        ("Which is the national animal of India?", "Lion", "Elephant", "Tiger", "Leopard", "c", "easy"),
    ],
}


class Command(BaseCommand):
    help = "Load sample categories and questions"

    def handle(self, *args, **options):
        created = 0
        for cat_name, rows in DATA.items():
            cat, _ = Category.objects.get_or_create(name=cat_name)
            for text, a, b, c, d, correct, diff in rows:
                _, was_created = Question.objects.get_or_create(
                    category=cat, text=text,
                    defaults=dict(option_a=a, option_b=b, option_c=c, option_d=d,
                                  correct=correct, difficulty=diff))
                created += was_created
        self.stdout.write(self.style.SUCCESS(f"Seed complete. {created} new questions added."))
