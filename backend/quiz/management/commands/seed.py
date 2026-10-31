import random
import zlib

from django.core.management.base import BaseCommand
from quiz.models import Category, Question

# ---------------------------------------------------------------
# PART 1: the original 40 questions
# Format: (text, option a, b, c, d, correct letter, difficulty)
# ---------------------------------------------------------------
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

# ---------------------------------------------------------------
# PART 2: 80 NEW questions (20 per category)
# Format: (text, CORRECT answer, wrong 1, wrong 2, wrong 3, difficulty)
# The position of the correct answer (A/B/C/D) is shuffled automatically.
# To add your own questions, just add a new line in the same format.
# ---------------------------------------------------------------
EXTRA = {
    "Python": [
        ("What is the output of print(type(5.0))?", "<class 'float'>", "<class 'int'>", "<class 'str'>", "<class 'double'>", "easy"),
        ("Which keyword is used to create a class?", "class", "object", "define", "struct", "easy"),
        ("What does len('Python') return?", "6", "5", "7", "Error", "easy"),
        ("Which function reads input from the user?", "input()", "scan()", "read()", "get()", "easy"),
        ("Which is the correct way to create a dictionary?", "{'a': 1}", "['a': 1]", "('a': 1)", "<'a': 1>", "easy"),
        ("Which operator performs floor division?", "//", "/", "%", "**", "medium"),
        ("What is the output of 10 % 3?", "1", "3", "0", "3.33", "easy"),
        ("Which statement exits a loop early?", "break", "stop", "exit", "skip", "easy"),
        ("What is a lambda in Python?", "An anonymous function", "A loop", "A module", "A class", "medium"),
        ("Which method converts a string to uppercase?", "upper()", "capitalize()", "big()", "toUpper()", "easy"),
        ("What does pip do?", "Installs Python packages", "Runs Python code", "Compiles code", "Formats code", "easy"),
        ("Which of these data types is mutable?", "list", "tuple", "string", "int", "easy"),
        ("What does 'self' represent inside a class method?", "The current object", "The class itself", "A global variable", "The parent class", "medium"),
        ("What is the output of 'Hi' * 3?", "HiHiHi", "Hi3", "Error", "Hi Hi Hi", "easy"),
        ("Which keyword is used to import a module?", "import", "include", "using", "require", "easy"),
        ("What does enumerate() give you?", "Index and value pairs", "Only values", "Only keys", "Sorted items", "medium"),
        ("What is the output of bool([])?", "False", "True", "None", "Error", "medium"),
        ("Which module is used to work with JSON data?", "json", "csv", "re", "os", "medium"),
        ("What is a list comprehension?", "A short way to build a list from another sequence", "A way to document lists", "A sorting method", "A type of error", "medium"),
        ("Which exception is raised when dividing by zero?", "ZeroDivisionError", "ValueError", "TypeError", "IndexError", "medium"),
    ],
    "SQL": [
        ("Which command updates existing rows in a table?", "UPDATE", "MODIFY", "CHANGE", "ALTER ROWS", "easy"),
        ("Which command removes rows from a table?", "DELETE", "REMOVE", "DROP ROW", "CLEAR", "easy"),
        ("What does SQL stand for?", "Structured Query Language", "Simple Query Language", "Sequential Query Logic", "Standard Question Language", "easy"),
        ("Which clause filters groups after GROUP BY?", "HAVING", "WHERE", "FILTER", "LIMIT", "medium"),
        ("Which function returns the highest value?", "MAX()", "TOP()", "HIGH()", "BIG()", "easy"),
        ("Which function calculates the average?", "AVG()", "MEAN()", "AVERAGE()", "MID()", "easy"),
        ("Which condition checks for NULL values?", "IS NULL", "= NULL", "== NULL", "NULL?", "medium"),
        ("What does LIMIT 5 do?", "Returns at most 5 rows", "Skips 5 rows", "Deletes 5 rows", "Adds 5 rows", "easy"),
        ("A FOREIGN KEY is used to...", "Link two tables", "Encrypt data", "Sort a table", "Delete duplicates", "medium"),
        ("Which command creates a new table?", "CREATE TABLE", "NEW TABLE", "MAKE TABLE", "ADD TABLE", "easy"),
        ("Which wildcard matches any number of characters in LIKE?", "%", "_", "*", "#", "medium"),
        ("Which JOIN returns all rows from the left table?", "LEFT JOIN", "INNER JOIN", "CROSS JOIN", "SELF JOIN", "medium"),
        ("Which keyword sorts results in descending order?", "DESC", "DOWN", "DSC", "REVERSE", "easy"),
        ("What does the BETWEEN operator do?", "Checks if a value is inside a range", "Joins two tables", "Sorts the rows", "Counts the rows", "medium"),
        ("Which statement changes the structure of a table?", "ALTER TABLE", "UPDATE TABLE", "CHANGE TABLE", "MODIFY ROWS", "medium"),
        ("Which of these is NOT an aggregate function?", "UPPER()", "SUM()", "COUNT()", "AVG()", "medium"),
        ("What is an index in a database used for?", "Speeding up searches", "Storing images", "Deleting data", "Encrypting passwords", "hard"),
        ("Which command saves a transaction permanently?", "COMMIT", "SAVE", "ROLLBACK", "STORE", "hard"),
        ("In ACID, what does the letter A stand for?", "Atomicity", "Accuracy", "Access", "Availability", "hard"),
        ("Which command gives a user permission on a table?", "GRANT", "ALLOW", "PERMIT", "GIVE", "hard"),
    ],
    "AI & Machine Learning": [
        ("What is the goal of a classification model?", "Predict a category or label", "Predict a continuous number", "Group data without labels", "Compress the data", "easy"),
        ("Which of these is a regression problem?", "Predicting house prices", "Detecting spam emails", "Recognising handwritten digits", "Grouping customers by behaviour", "medium"),
        ("What is 'training data'?", "Data used to teach the model", "Data used only for the final report", "Data that has been deleted", "Data stored on the cloud", "easy"),
        ("What is a 'feature' in machine learning?", "An input variable used for prediction", "The final output", "A type of neural network", "The accuracy score", "easy"),
        ("What is the 'label' in supervised learning?", "The correct output for an example", "The name of the dataset", "The size of the data", "A type of algorithm", "easy"),
        ("Which Python library is commonly used for classical machine learning?", "scikit-learn", "Flask", "BeautifulSoup", "Pygame", "easy"),
        ("What does 'underfitting' mean?", "The model is too simple to learn the pattern", "The model memorises the data", "The data is too large", "The model trains too fast", "medium"),
        ("Which algorithm is used for classification despite its name?", "Logistic Regression", "Linear Regression", "K-Means", "Apriori", "medium"),
        ("What is deep learning?", "Machine learning using multi-layer neural networks", "Learning by reading long books", "A database technique", "Learning without any data", "medium"),
        ("What is a confusion matrix used for?", "Evaluating classification results", "Cleaning missing values", "Plotting maps", "Encrypting data", "medium"),
        ("What does CNN stand for in deep learning?", "Convolutional Neural Network", "Computer Neural Network", "Connected Node Network", "Central Neuron Network", "medium"),
        ("CNNs are mostly used for which kind of data?", "Images", "Plain text files", "Database tables", "Network logs", "easy"),
        ("What is 'data cleaning'?", "Fixing or removing incorrect, missing or duplicate data", "Deleting the whole dataset", "Making charts", "Training the model faster", "easy"),
        ("Which technique reduces the number of features in data?", "Dimensionality reduction (such as PCA)", "Overfitting", "Data duplication", "Backpropagation", "hard"),
        ("What is gradient descent used for?", "Minimising the model's error by adjusting weights", "Collecting data", "Displaying results", "Splitting data into folders", "hard"),
        ("What is a 'hyperparameter'?", "A setting chosen before training, such as learning rate", "A value learned from the data", "The final prediction", "A type of dataset", "hard"),
        ("What does the 'learning rate' control?", "How big each weight update step is", "How many rows of data are used", "How fast the computer runs", "The number of classes", "hard"),
        ("What is reinforcement learning?", "Learning through rewards and penalties", "Learning from labelled examples only", "Learning by grouping data", "Learning from images only", "medium"),
        ("Which of these is an example of generative AI?", "A model that writes text or creates images", "A spreadsheet formula", "A basic calculator", "A file compressor", "easy"),
        ("What is a Large Language Model (LLM)?", "A model trained on huge amounts of text to understand and generate language", "A very large database", "A programming language", "A type of search engine index", "medium"),
    ],
    "General Knowledge": [
        ("Which is the smallest planet in our solar system?", "Mercury", "Mars", "Venus", "Earth", "easy"),
        ("Who was the first Prime Minister of India?", "Jawaharlal Nehru", "Mahatma Gandhi", "Sardar Patel", "Lal Bahadur Shastri", "easy"),
        ("Which is the largest mammal in the world?", "Blue whale", "African elephant", "Giraffe", "Hippopotamus", "easy"),
        ("In which year did India become independent?", "1947", "1945", "1950", "1942", "easy"),
        ("Which organ pumps blood around the human body?", "Heart", "Liver", "Lungs", "Kidney", "easy"),
        ("What is the chemical symbol for gold?", "Au", "Ag", "Gd", "Go", "medium"),
        ("Who invented the telephone?", "Alexander Graham Bell", "Thomas Edison", "Nikola Tesla", "Isaac Newton", "medium"),
        ("Which is the highest mountain peak above sea level?", "Mount Everest", "K2", "Kangchenjunga", "Mont Blanc", "easy"),
        ("Which country gifted the Statue of Liberty to the USA?", "France", "England", "Germany", "Spain", "medium"),
        ("What is the currency of Japan?", "Yen", "Won", "Yuan", "Ringgit", "medium"),
        ("Which festival is known as the festival of lights in India?", "Diwali", "Holi", "Pongal", "Eid", "easy"),
        ("Who wrote the play 'Romeo and Juliet'?", "William Shakespeare", "Charles Dickens", "Jane Austen", "Mark Twain", "easy"),
        ("Which gas do humans need to breathe in to survive?", "Oxygen", "Carbon dioxide", "Nitrogen", "Helium", "easy"),
        ("How many players are in a cricket team on the field?", "11", "9", "10", "12", "easy"),
        ("Which Indian state has the longest mainland coastline?", "Gujarat", "Tamil Nadu", "Maharashtra", "Andhra Pradesh", "medium"),
        ("Which vitamin does the skin produce in sunlight?", "Vitamin D", "Vitamin A", "Vitamin C", "Vitamin B12", "medium"),
        ("Which is the largest continent by area?", "Asia", "Africa", "Europe", "North America", "easy"),
        ("Who is known as the Missile Man of India?", "A. P. J. Abdul Kalam", "Vikram Sarabhai", "Homi Bhabha", "C. V. Raman", "medium"),
        ("Which instrument is used to measure temperature?", "Thermometer", "Barometer", "Hygrometer", "Speedometer", "easy"),
        ("In which city is the Taj Mahal located?", "Agra", "Delhi", "Jaipur", "Lucknow", "easy"),
    ],
}


def shuffle_options(text, correct, wrongs):
    """Put the correct answer in a repeatable 'random' position (A, B, C or D)."""
    options = [correct] + list(wrongs)
    random.Random(zlib.crc32(text.encode())).shuffle(options)
    return options, "abcd"[options.index(correct)]


class Command(BaseCommand):
    help = "Load sample categories and questions (safe to run many times)"

    def handle(self, *args, **options):
        created = 0

        # Part 1: original questions (letters already given)
        for cat_name, rows in DATA.items():
            cat, _ = Category.objects.get_or_create(name=cat_name)
            for text, a, b, c, d, correct, diff in rows:
                _, was_created = Question.objects.get_or_create(
                    category=cat, text=text,
                    defaults=dict(option_a=a, option_b=b, option_c=c, option_d=d,
                                  correct=correct, difficulty=diff))
                created += was_created

        # Part 2: new questions (correct position is shuffled automatically)
        for cat_name, rows in EXTRA.items():
            cat, _ = Category.objects.get_or_create(name=cat_name)
            for text, correct, w1, w2, w3, diff in rows:
                opts, letter = shuffle_options(text, correct, (w1, w2, w3))
                _, was_created = Question.objects.get_or_create(
                    category=cat, text=text,
                    defaults=dict(option_a=opts[0], option_b=opts[1], option_c=opts[2],
                                  option_d=opts[3], correct=letter, difficulty=diff))
                created += was_created

        total = Question.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f"Seed complete. {created} new questions added. Total in database: {total}."))