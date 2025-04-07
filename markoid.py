import random
import sys
import threading
import time
import pyperclip
import webview

class Api:

    def init(self):
        response = {'message': 'Hello from Python {0}'.format(sys.version)}
        return response

    def getRandomNumber(self):
        response = {
            'message': 'Here is a random number courtesy of randint: {0}'.format(
                random.randint(0, 100000000)
            )
        }
        return response

    def sayHelloTo(self, name):
        response = {'message': 'Hello {0}!'.format(name)}
        return response

    def error(self):
        raise Exception('This is a Python exception')
    
    def openFile(self):
        file_types = ('Text Files (*.txt)', 'All files (*.*)')

        result = window.create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types
        )
        self.file_path= result[0]
        print(self.file_path)
        with open(self.file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            lines = content.split('\n')
        print(lines)
        return lines

    def saveFile(self, lines):
        if self.file_path is None:
            file_types = ('Text Files (*.txt)', 'All files (*.*)')

            result = window.create_file_dialog(
                webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types
            )
            self.file_path = result[0]
        with open(self.file_path, 'w', encoding='utf-8') as file:
            content = '\n'.join(lines)
            file.write(content)

    def copyToClipboard(self, text):
        pyperclip.copy(text)
        return {'message': 'Text copied to clipboard!'} 
        

if __name__ == '__main__':
    api = Api()

    #with open('index.html', 'r', encoding='utf-8') as file:
    #    html = file.read()

    window = webview.create_window('Markoid', 'assets/index.html', js_api=api)
    webview.start(debug=True)