import random
import sys
import os
import pyperclip
import webview
import platformdirs
import configparser
from markdown_pdf import MarkdownPDF

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
        self.windowTitle = f'Markoid - {self.file_path}' if self.file_path else 'Markoid'

    def read_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        self.file_path = config.get('DEFAULT', 'file_path', fallback=None)
        self.report_path = config.get('DEFAULT', 'report_path', fallback=None)
        self.report_type = config.get('DEFAULT', 'report_type', fallback='md')
        return config
    
    def write_config(self):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {
            'file_path': self.file_path,
            'report_path': self.report_path,
            'report_type': self.report_type
            }
        with open(self.config_file, 'w') as configfile:
            config.write(configfile)
        self.windowTitle = f'Markoid - {self.file_path}' if self.file_path else 'Markoid'
        window.set_title(self.windowTitle)

    def get_student_list(self):
        print(f'API:get_student_list: {self.report_path}') 
        if self.report_path is None:
            return []
        
        files=os.listdir(self.report_path)
        student_list = []
        for file in files:
            if file.endswith('.'+self.report_type):
                student_list.append(file[:-len('.'+self.report_type)])
        print(f'Students: {student_list}')
        return student_list

    def init(self):
        response = {'message': 'Hello from Python {0}'.format(sys.version)}
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

    def setReportFolder(self):
        result= window.create_directory_dialog()
        self.report_path= result[0]
        self.write_config()
        return self.get_student_list()


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
    
    def setWindow(self, window):
        print('API:setWindow')
        self.window = window

    def write_results(self, student, text):
        print(f'API:write_results: {student}')
        if self.report_path is None:
            return {'message': 'No report path set!'}
        target_file = os.path.join(self.report_path, student + '.' + self.report_type)
        if not os.path.exists(self.report_path):
            os.makedirs(self.report_path)
        content=''
        with open(target_file, 'r', encoding='utf-8') as file:
            content = file.read()
        if self.report_type == 'md':
            text = text.replace('\n', '\n\n')
        content = content.replace('<!-- Markoid -->', text )
        with open(target_file, 'w', encoding='utf-8') as file:
            file.write(content)
        return {'message': 'Results written to file!'}
    
    def make_pdf(self, student):
        print(f'API:make_pdf: {student}')
        if self.report_path is None:
            return {'message': 'No report path set!'}
        target_file = os.path.join(self.report_path, student + '.' + self.report_type)
        if not os.path.exists(self.report_path):
            os.makedirs(self.report_path)
        pdf_file = os.path.join(self.report_path, student + '.pdf')
        pdf = MarkdownPDF()
        pdf.convert(target_file, pdf_file)
        return {pdf_file}
       

if __name__ == '__main__':
    api = Api()

    #with open('index.html', 'r', encoding='utf-8') as file:
    #    html = file.read()

    window = webview.create_window(api.windowTitle, 'assets/index.html', js_api=api)
    webview.start(debug=False)
