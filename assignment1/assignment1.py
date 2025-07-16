# Write your code here.
# Task 1
def hello():
    return "Hello!"
print(hello())

# Task 2
def greet(name):
    return f"Hello, {name}!"
print(greet("Mary"))

# Task 3 
def calc (a, b, operation="multiply"):
    try:
        match operation:
            case "add":
                return a + b
            case "subtract":
                return a - b
            case "multiply":
                return a * b
            case "divide":
                return a / b
            case "modulo":
                return a % b
            case "int_divide":
                return a // b
            case "power":
                return a ** b
            case _:
                return "Invalid operation"
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return "You can't multiply those values!"
    
# Task 4
def data_type_conversion(value, type):
    try:
        match type:
            case "int":
                return int(value)
            case "float":
                return float(value)
            case "str":
                return str(value)
            case _:
                return f"Unsupported type: {type}"
    except ValueError:
        return f"You can't convert {value} into a {type}." 
    
# Task 5
def grade(*args):
    try:
        average = sum(args) / len(args)
        if average >= 90:
            return 'A'
        elif average >= 80:
            return 'B'
        elif average >= 70:
            return 'C'
        elif average >= 60:
            return 'D'
        else:
            return 'F'
    except:
        return "Invalid data was provided." 

# Task 6 
def repeat(string, count): 
     result = ""
     for i in range(count):
        result += string
     return result

# Task 7
def student_scores(mode, **kwargs):
    if mode == "best":
        # Find the student with the highest score
        best_student = max(kwargs, key=kwargs.get)
        return best_student
    elif mode == "mean":
        # Calculate the average of the scores
        average = sum(kwargs.values()) / len(kwargs)
        return average
    else:
        return "Invalid mode"
# Task 8
def titleize(text):
    little_words = {"a", "on", "an", "the", "of", "and", "is", "in"}
    words = text.lower().split()  # convert entire text to lowercase and split into words
    titleized = []

    for i, word in enumerate(words):
        # Always capitalize the first and last word
        if i == 0 or i == len(words) - 1:
            titleized.append(word.capitalize())
        elif word in little_words:
            titleized.append(word)
        else:
            titleized.append(word.capitalize())

    return ' '.join(titleized)

# Task 9 
def hangman(secret, guess):
    result = ""
    for letter in secret:
        if letter in guess:
            result += letter
        else:
            result += "_"
    return result

# Task 10 
def pig_latin(text):
    vowels = "aeiou"
    words = text.split()
    result = []

    for word in words:
        if word[0] in vowels:
            # Rule 1: Starts with a vowel
            pig_word = word + "ay"
        elif word.startswith("qu"):
            # Rule 3: Starts with "qu"
            pig_word = word[2:] + "quay"
        else:
            # Rule 2: Starts with one or more consonants
            index = 0
            while index < len(word) and word[index] not in vowels:
                # Special case for "qu" inside the consonants
                if word[index] == "q" and index + 1 < len(word) and word[index + 1] == "u":
                    index += 2
                    break
                index += 1
            pig_word = word[index:] + word[:index] + "ay"
        
        result.append(pig_word)

    return ' '.join(result)
