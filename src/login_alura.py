from bs4 import BeautifulSoup
import requests
import os

url_login = 'https://cursos.alura.com.br/signin'
url_course = 'https://cursos.alura.com.br/course/aws-servicos-custos/task/134731'

payload = {
    'username': os.getenv('ALURA_USER'),
    'password': os.getenv('ALURA_PASS')
}
data = []

# Start the session and doing the login using the payload and keep the session alive
with requests.Session() as session:
    # Login
    response = session.post(url_login, data=payload)
    if response.status_code == 200:
        # Get the course
        response = session.get(url_course)
        if response.status_code == 200:
            # Get the content
            content = response.text
            soup = BeautifulSoup(content, 'html.parser')
            elemento = soup.select_one('#transcription')
            data = {
                'title': elemento.find('h2').get_text(),
                'content': elemento.get_text()
            }
        
print(data)