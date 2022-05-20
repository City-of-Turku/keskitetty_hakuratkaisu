from datetime import datetime
from requests.exceptions import ReadTimeout, ConnectionError
from uuid import uuid4
import re
import requests
import time


class NLPProcessorClient:
    nlp_instances = []
    nlp_dictionary_lck = False

    def __init__(self, api_url, dictionary_path):
        self.instance_id = uuid4()
        self.api_url = api_url
        self.dictionary_path = dictionary_path

        self.nlp_instances.append(self.instance_id)
        if len(self.nlp_instances) == 1:
            self.nlp_dictionary_lck = False
        
        # Waiting for the NLP container API to initialize
        start = datetime.now()
        while(True):
            elapsed = datetime.now() - start
            if elapsed.seconds > 60:
                raise ReadTimeout(message='NLP container ping timed out. Could not get status 200 response.')

            try:
                data = ' '.encode('utf-8')
                headers = {'Content-Type': 'text/plain; charset: utf-8'}
                response = requests.post(self.api_url, headers=headers, data=data, timeout=10)

                if response.status_code == 200:
                    print('NLP container ready!')
                    break

            except ReadTimeout as e:
                print('Waiting for NLP container init...')
                time.sleep(10)
            except ConnectionError as e:
                print('Waiting for NLP container init...')
                time.sleep(10)
            except Exception as e:
                print(e.with_traceback)
                raise ReadTimeout(message=f'Failed to connect NLP container. {e.with_traceback}')
        
        # Initialize dictionary file
        try:
            with open(dictionary_path, 'at', encoding='utf-8'):
                print('NLP dictionary file ready.')
        except Exception as e:
            raise FileNotFoundError(f'Failed to initialize NLP dictionary file. {e.with_traceback}')

    def __del__(self):
        self.nlp_instances.remove(self.instance_id)
        print("NLP instance deleted")

    def process(self, content):
        content = self.remove_non_alpha_and_duplicates(content)
        content = self.remove_existing(content)

        stemmed_content = self.process_with_nlp(content) if len(content) > 0 else None
        
        if stemmed_content:
            self.add_results(stemmed_content)

    def remove_non_alpha_and_duplicates(self, content):
        tokens = content.lower().split()
        result = ""

        for token in tokens:
            token = token.strip(' ,."\\/\'?!:;')
            if len(token) > 3 and not re.search('[^a-zäö]', token) and not re.search(f'\\b{token}\\b', result):
                result += token if len(result) == 0 else f' {token}'

        return result

    def remove_existing(self, content):
        with open(self.dictionary_path, 'rt', encoding='utf-8') as file:
            tokens = content.split()
            existing = file.read()
            result = ""

            for token in tokens:
                if not re.search(f'\\b{token}\\b', existing):
                    result += token if len(result) == 0 else f' {token}'

        return result

    def process_with_nlp(self, content):
        try:
            data = content.encode('utf-8')
            headers = {'Content-Type': 'text/plain; charset: utf-8'}
            response = requests.post(self.api_url, headers=headers, data=data, timeout=30)

            if response.status_code == 200:
                response_content = response.content.decode(response.encoding)
            else:
                response_content = None

        except Exception as e:
            print(e.with_traceback)
            return None

        if response_content:
            stemmed_tokens_lst = []

            for line in response_content.splitlines():
                if len(line) > 0 and line[0].isnumeric():
                    tokens = line.split('\t')
                    stemmed_token = f'{tokens[1]} => {tokens[2]}'.replace('#', "")
                    stemmed_tokens_lst.append(stemmed_token)

            return stemmed_tokens_lst
        else:
            return None

    def add_results(self, stemmed_content):
        start = datetime.now()
        while(self.nlp_dictionary_lck):
            elapsed = datetime.now() - start
            if not elapsed.seconds > 10:
                time.sleep(0.1)
            else:
                print('NLP dictionary filelock timed out. Attempting to modify file with filelock active.')
                break

        with open(self.dictionary_path, 'rt', encoding='utf-8') as file:
            nlp_dictionary = file.read()
            self.nlp_dictionary_lck = True
        
        for item in stemmed_content:
            values = item.split(' => ')

            i = nlp_dictionary.find(f'=> {values[1]}\n')

            if i > -1:
                pre_lf = nlp_dictionary.rfind('\n', 0, i)
                post_lf = nlp_dictionary.find('\n', i)
                line = nlp_dictionary[pre_lf + 1: post_lf]
                newline = line.replace(' => ', f', {values[0]} => ')
                nlp_dictionary = nlp_dictionary.replace(line, newline)
            else:
                nlp_dictionary += f'{item}\n'
    
        with open(self.dictionary_path, 'wt', encoding='utf-8') as file:
            file.write(nlp_dictionary)
        
        self.nlp_dictionary_lck = False
