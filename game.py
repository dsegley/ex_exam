# Para practicar...
import os
import random
import common.get_questions as get_questions
from datetime import datetime

questions = []

def format(content):
    text = ""
    correct_ans = ""
    reference = ""
    explanation = ""
    in_explanation = False
    first = True
    for line in content:
        if len(line.strip()) == 0:
            continue

        if 'AWS Certified Cloud Practitioner CLF-C01' in line and not first:
            in_explanation = False
            questions.append({
                "text": text, 
                "ans": correct_ans, 
                "reference": reference,
                "explanation": explanation
            })
            text = line
            in_explanation = False
            explanation = ""
            reference = ""

        elif 'Correct Answer' in line:
            index = line.find(':')
            correct_ans = line[index + 2:]

        elif 'Reference:' not in line and 'https' not in line and \
            'Explanation' not in line and not in_explanation:
            text = text + '\n' + line

        elif 'Explanation' in line:
            in_explanation = True
            explanation = explanation + line

        elif 'https' in line:
            index = line.find('https')
            reference = "Reference: " + line[index:]
        
        first = False

    # last question
    questions.append({
        "text": text, 
        "ans": correct_ans, 
        "reference": reference,
        "explanation": explanation
    })


def game():
    num_of_exer = 0
    score = 0

    print('GPI v.1.0')

    while num_of_exer == 0 or num_of_exer > len(questions):
        try:
            num_of_exer = int(input(f"¿De cuantas preguntas será la practica?\
(max: {len(questions)}): "))
        except ValueError as err:
            print('Ingrese un numero valido ')

    os.system('cls' if os.name == 'nt' else 'clear')
    
    random.shuffle(questions)

    for i in range(0, num_of_exer):
        print(f"{i + 1}/{num_of_exer}")
        print(questions[i]['text'])
        
        ans = ''
        while len(ans) == 0:
            try:
                ans = input('\nRespuesta: ').upper()
            except ValueError as err:
                pass

        corr_ans = questions[i]['ans']
        expla = questions[i]['explanation']
        ref = questions[i]['reference']

        if sorted(ans) == sorted(corr_ans):
            score = score + 1
            print('\n¡Correcto!')
        else:
            print(f"\nIncorrecto\nRespuesta correcta: {corr_ans}")

        print()
        if len(expla) > 0:
            print(expla)

        if len(ref) > 0:
            print(ref)

        input()
        os.system('cls' if os.name == 'nt' else 'clear')

    input(f"\nAcertó {score}/{num_of_exer}\n{score/num_of_exer * 100}% ")


if __name__ == '__main__':
    random.seed(datetime.now().second)

    try:
        with open("QuestionsUwU.txt", "r", encoding="utf8") as file:
            content = file.read().splitlines()
    except FileNotFoundError as err:
        print('QuestionsUwU no encontrado...')
        num = input('¿Cuantas preguntas desea descargar?(max 558): ')
        print('Obteniendo preguntas, esto puede tomar unos minutos...')
        get_questions.run_get_questions(num)

    finally:
        with open("QuestionsUwU.txt", "r", encoding="utf8") as file:
            content = file.read().splitlines()
        format(content)
        r = 'y'
        while r == 'y':
            game()
            r = input('Jugar de nuevo?(y/n): ').lower()
   