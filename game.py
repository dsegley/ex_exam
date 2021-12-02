# Para practicar...
import os
import random
import common.get_questions as get_questions
import webbrowser
from datetime import datetime

questions = []
wrong_ans = []

def format(content):
    text = ""
    correct_ans = ""
    reference = ""
    explanation = ""
    url = ""
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
                "explanation": explanation,
                'url': url
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

        elif 'http' in line:
            index = line.find('http')
            reference = "Reference: " + line[index:]
            url = line[index:]
        
        first = False

    # last question
    questions.append({
        "text": text, 
        "ans": correct_ans, 
        "reference": reference,
        "explanation": explanation
    })


def quiz(ques, num=0):
    score = 0
    good_ans = []

    random.shuffle(ques)
    if num == 0:
        num = len(ques)

    for i in range(0, num):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{i + 1}/{num}")
        print(ques[i]['text'])
        
        ans = ''
        while len(ans) == 0:
            try:
                ans = input('\nRespuesta: ').upper()
            except ValueError as err:
                pass

        corr_ans = ques[i]['ans']
        expla = ques[i]['explanation']
        ref = ques[i]['reference']
        url = ques[i]['url']

        if sorted(ans) == sorted(corr_ans):
            score = score + 1
            print('\n¡Correcto!')
            if ques[i] in wrong_ans:
                good_ans.append(ques[i])
        else:
            print(f"\nIncorrecto\nRespuesta correcta: {corr_ans}")
            if ques[i] not in wrong_ans:
                wrong_ans.append(ques[i])

        print()
        if len(expla) > 0:
            print(expla)

        if len(ref) > 0:
            print(ref)
            print("Presione la tecla 'O' para abrir la url en el navegador")

        open = input("Presione una tecla para continuar... ").lower()
        if (open == 'o' and len(ref) > 0):
                webbrowser.open(url)

        os.system('cls' if os.name == 'nt' else 'clear')

    for i in good_ans:
        wrong_ans.remove(i)

    return score


def game():
    num_of_exer = 0
    print('GPI v.1.0')

    while num_of_exer == 0 or num_of_exer > len(questions):
        try:
            num_of_exer = int(input(f"¿De cuantas preguntas será la practica?\
(max: {len(questions)}): "))
        except ValueError as err:
            print('Ingrese un numero valido ')

    score = quiz(questions, num_of_exer)
    input(f"\nAcertó {score}/{num_of_exer}\n{score/num_of_exer * 100}% ")

    r = 'y'
    while r == 'y' and len(wrong_ans) > 0:
        r = input('¿Desea repasar las preguntas sin acertar?(y/n): ').lower()
        if (r == 'y'):
            quiz(wrong_ans)
    wrong_ans.clear()


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
        try:
            with open("QuestionsUwU.txt", "r", encoding="utf8") as file:
                content = file.read().splitlines()
            format(content)
            r = 'y'
            while r == 'y':
                game()
                r = input('Jugar de nuevo?(y/n): ').lower()
        except Exception as err:
            print(err)
   