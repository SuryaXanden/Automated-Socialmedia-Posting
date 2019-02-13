from selenium import webdriver
from time import sleep
from flask import Flask, render_template, request
from werkzeug import secure_filename
import os

def Twitter(usr,pwd,path,desc,speed):
    if usr:
        # twitDone = 0
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
        sleep(speed*3)
        #DESCRIPTION
        text_box = driver.find_element_by_id('tweet-box-home-timeline')
        #sending description
        text_box.send_keys(desc)
        #TWEET
        tweet_button = driver.find_element_by_css_selector('button.tweet-action.EdgeButton.EdgeButton--primary.js-tweet-btn')
        tweet_button.click()
        sleep(speed*5)
        driver.refresh()
        driver.close()
        # twitDone = 1
        return 1
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
        sleep(speed*4)
        remover = driver.find_element_by_tag_name('body').click()
        # remover = driver.find_element_by_tag_name('body').click()
        # # sleep(speed*2)
        #<--- code to remove opaque screen --->
        # remover = driver.find_element_by_tag_name('body').click()
        # # remover = driver.find_element_by_tag_name('body').click()
        #<--- / code to remove opaque screen --->
        #WALL
        give = driver.find_element_by_xpath("//*[@name='xhpc_message']")
        #Wait for wall
        sleep(speed)

        #DESCRIPTION
        give.send_keys(desc)
        sleep(speed)

        #ATTACH MEDIA
        # file = driver.find_element_by_xpath('//input[@data-testid="media-sprout"]')
        file = driver.find_element_by_css_selector('input[data-testid="media-sprout"]')
        sleep(speed)

        #sending media
        file.send_keys(path)
        #wait while it uploads
        sleep(speed*3)

        #POST
        post = driver.find_element_by_css_selector('button[data-testid="react-composer-post-button"]')
        post.click()
        #wait for post to be made
        sleep(speed*5)
        driver.refresh()
        driver.close()
        # faceDone = 1
        return 1
    pass

def Instagram(usr,pwd,path,desc):
    if usr:
        if pwd:
            if os.system(" instapy -u {} -p {} -f {} -t {}".format(usr,pwd,path,desc)):
                return 1
            return 0
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

    twitter = facebook = instagram = 0
    if tup:
        twitter = Twitter(tun,tup,media,desc,speed)
    if fup:
        facebook = Facebook(fun,fup,media,desc,speed)
    if iup:
        instagram = Instagram(iun,iup,media,desc)

    Done = []
    if instagram:
        Done.append('Instagram')
    
    if twitter:
        Done.append('Twitter')

    if facebook:
        Done.append('Facebook')
   
    if Done:
        return '''
                <script>
                alert('Successfully uploaded to {}');
                window.location = "/";
                </script>
        '''.format(Done)
    else:
        return '''
                <script>
                alert('An error occoured while trying to do these operations');
                window.location = "/";
                </script>
        '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=True,threaded=True)