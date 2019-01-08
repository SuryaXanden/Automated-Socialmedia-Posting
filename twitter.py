from selenium import webdriver
from time import sleep
from flask import Flask, render_template, request
from werkzeug import secure_filename
import os
import shadow

# 8 for slow
# 5 for medium
# 2 for fast

def Twitter(usr,pwd,path,desc,speed):
    driver = webdriver.Chrome(executable_path='./chromedriver.exe')
    driver.get('https://twitter.com/login')
    usr_box = driver.find_element_by_class_name('js-username-field')
    usr_box.send_keys(usr)
    pwd_box = driver.find_element_by_class_name('js-password-field')
    pwd_box.send_keys(pwd)
    sleep(speed)
    login_button = driver.find_element_by_css_selector('button.submit.EdgeButton.EdgeButton--primary.EdgeButtom--medium')
    login_button.submit()
    sleep(speed)
    image_box = driver.find_element_by_css_selector('input.file-input.js-tooltip')
    image_box.send_keys(path)
    sleep(speed)
    text_box = driver.find_element_by_id('tweet-box-home-timeline')
    text_box.send_keys(desc)
    sleep(speed)
    tweet_button = driver.find_element_by_css_selector('button.tweet-action.EdgeButton.EdgeButton--primary.js-tweet-btn')
    tweet_button.click()
    return

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():    
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def go():
    file = request.files['media']
    filename = secure_filename(file.filename)
    media = os.path.abspath(filename)
    file.save(media)
    un = request.form['username']
    up = request.form['password']
    desc = request.form['desc']
    speed = int(request.form['speed'])
    Twitter(un,up,media,desc,speed)
    return '''
            <script>
            alert('Success :)');
            window.location = "/";
            </script>
    '''

if __name__ == '__main__':
    app.run(debug=True,threaded=True)