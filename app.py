from selenium import webdriver
from time import sleep
from flask import Flask, render_template, request
from werkzeug import secure_filename
import os

def Twitter(usr,pwd,path,desc,speed):
    if usr:
        #browser
        driver = webdriver.Chrome(executable_path='./chromedriver.exe')
        #URL
        driver.get('https://twitter.com/login')
        #USERNAME
        usr_box = driver.find_element_by_class_name('js-username-field')
        #sending username
        usr_box.send_keys(usr)
        #PASSWORD
        pwd_box = driver.find_element_by_class_name('js-password-field')
        #sending password
        pwd_box.send_keys(pwd)
        #LOGIN
        login_button = driver.find_element_by_css_selector('button.submit.EdgeButton.EdgeButton--primary.EdgeButtom--medium')
        #clicking on login
        login_button.submit()

        #Wait until login
        sleep(speed)

        #ATTACH MEDIA
        image_box = driver.find_element_by_css_selector('input.file-input.js-tooltip')
        #sending media
        image_box.send_keys(path)

        #wait for a bit (until its uploaded to browser maybe )
        sleep(speed)

        #DESCRIPTION
        text_box = driver.find_element_by_id('tweet-box-home-timeline')
        #sending description
        text_box.send_keys(desc)
        #TWEET
        tweet_button = driver.find_element_by_css_selector('button.tweet-action.EdgeButton.EdgeButton--primary.js-tweet-btn')
        tweet_button.click()
        sleep(speed*1.5)
        driver.close()
        return
    pass

def Facebook(usr,pwd,path,desc,speed):
    if usr:
        driver = webdriver.Chrome(executable_path='./chromedriver.exe')
        #<--- code to login --->
        driver.get('https://en-gb.facebook.com/login')
        usr_box = driver.find_element_by_id('email')
        usr_box.send_keys(usr)
        pwd_box = driver.find_element_by_id('pass')
        pwd_box.send_keys(pwd)
        login_button = driver.find_element_by_id('loginbutton')
        login_button.submit()
        #<--- / code to login --->
        #Wait until login
        sleep(speed)

        #<--- code to remove opaque screen --->
        remover = driver.find_element_by_tag_name('body').click()
        #<--- / code to remove opaque screen --->
        #WALL
        give = driver.find_element_by_xpath("//*[@name='xhpc_message']")
        #Wait for wall
        sleep(speed)

        #DESCRIPTION
        give.send_keys(desc)
        sleep(speed)

        #ATTACH MEDIA
        file = driver.find_element_by_xpath("//input[@data-testid='media-sprout']")
        sleep(speed)

        #sending media
        file.send_keys(path)
        #wait while it uploads
        sleep(speed*1.75)

        #POST
        post = driver.find_element_by_css_selector('button[data-testid="react-composer-post-button"]')
        post.click()
        #wait for post to be made
        sleep(speed*1.5)
        driver.close()
        return
    pass

def Instagram(usr,pwd,path,desc):
    if usr:
        from InstagramAPI import InstagramAPI
        InstagramAPI = InstagramAPI(usr, pwd)
        InstagramAPI.login()
        InstagramAPI.uploadPhoto(path, caption=desc)
        return
    pass

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():    
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def go():
    
    tun = request.form['tun']
    tup = request.form['tup']
    if tun is None or tup is None:
        tun = tup = ""
    
    fun = request.form['fun']
    fup = request.form['fup']
    if fun is None or fup is None:
        fun = fup = ""
    
    iun = request.form['iun']
    iup = request.form['iup']
    if iun is None or iup is None:
        iun = iup = ""
    
    file = request.files['media']
    filename = secure_filename(file.filename)
    media = os.path.abspath(filename)
    file.save(media)

    desc = request.form['desc']

    speed = int(request.form['speed'])

    Twitter(tun,tup,media,desc,speed)
    Facebook(fun,fup,media,desc,speed)
    Instagram(iun,iup,media,desc)

    return '''
            <script>
            alert('Success :)');
            window.location = "/";
            </script>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=True,threaded=True)