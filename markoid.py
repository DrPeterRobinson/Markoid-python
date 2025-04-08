import random
import sys
import os
import pyperclip
import webview
import platformdirs
import configparser

class Api:

    def __init__(self):
        app_name = 'Markoid'
        app_author = 'DrPeterRobinson'
        config_dir = platformdirs.user_config_dir(app_name, app_author)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        self.config_dir = config_dir
        self.config_file = os.path.join(self.config_dir, 'config.ini')
        self.lines = []
        if os.path.exists(self.config_file):
            self.read_config()
            self.read_data()
        else:
            self.file_path = None

    def read_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        self.file_path = config.get('DEFAULT', 'file_path', fallback=None)
        return config
    
    def write_config(self):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'file_path': self.file_path}
        with open(self.config_file, 'w') as configfile:
            config.write(configfile)

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

    def error(self):
        raise Exception('This is a Python exception')
    
    def openFile(self):
        file_types = ('Text Files (*.txt)', 'All files (*.*)')

        result = window.create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types
        )
        self.file_path= result[0]
        return self.read_data()
    
    def read_data(self):
        if self.file_path is None:
            return []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            self.lines = content.split('\n')
        return self.lines

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
        self.write_config()

    def copyToClipboard(self, text):
        pyperclip.copy(text)
        return {'message': 'Text copied to clipboard!'} 
    
    def get_lines(self):
        return self.lines
        

if __name__ == '__main__':
    api = Api()

    #with open('index.html', 'r', encoding='utf-8') as file:
    #    html = file.read()

    window = webview.create_window('Markoid', 'assets/index.html', js_api=api)
    webview.start(debug=True)