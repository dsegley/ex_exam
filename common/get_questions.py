from urllib.request import urlopen
from bs4 import BeautifulSoup
from common.progress_bar import printProgressBar


def get_question(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.find('div', {'class': 'question'}).get_text()
    title = soup.find('h1', {'class': 'entry-title'}).get_text()
    reference = soup.find('div', {'class': 'explanation'})
    correct_answer = soup.find('div', {'class': 'answer'}).get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    for line in soup.find_all('strong'):
        text_line = line.get_text()
        if (len(text_line) < 2):
            continue
        try:
            index = text.index(text_line)
            text = text[:index] + '\n' + text[index:]
        except ValueError:
            pass

    text = title + '\n' + text + '\n' + correct_answer
    if reference is not None:
        text = text + reference.get_text()

    text = text + '\n'
    return text


def run_get_questions(num):
    num = int(num) + 1
    # lets gooo
    url = "https://exampracticetests.com/aws/Cloud_Practitioner_CLF-C01/aws-certified-cloud-practitioner-clf-c01-question"
    text = ''
    # 1 to 558
    printProgressBar(0, num, prefix='Progress:', suffix='Complete', length=50)
    for i in range(1, num):
        next = url + f"{i:03}" + '/' 
        text = text + get_question(next) + '\n'
        printProgressBar(i + 1, num, prefix='Progress:', suffix='Complete', length=50)

    with open("QuestionsUwU.txt", "w", encoding='utf8') as text_file:
        text_file.write(text)