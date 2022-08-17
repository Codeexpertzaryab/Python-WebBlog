from datetime import datetime
import smtplib
from email.message import EmailMessage
from flask import Flask,render_template,request,send_file,session,redirect
import json,os
import math
from flask_sqlalchemy import SQLAlchemy

with open('Configuration.json','r') as c:
    params = json.load(c)["param"]

local_server = True
app = Flask(__name__)
app.secret_key = 'super-secret-key'

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD=  params['gmail-password']
)
if(local_server==True):
    app.config['SQLALCHEMY_DATABASE_URI']=params['local_server']
else:
    app.config['SQLALCHEMY_DATABASE_URI']=params['Production_server']    

db = SQLAlchemy(app)

class contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    namez = db.Column(db.String(50), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(200), nullable=False)
    dates = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)

class posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    content1 = db.Column(db.String(2000), nullable=False)
    content2 = db.Column(db.String(2000), nullable=False)
    content3 = db.Column(db.String(2000), nullable=False)
    tagline = db.Column(db.String(120), nullable=False)
    dates = db.Column(db.String(30), nullable=True)
    author = db.Column(db.String(80), nullable=False)
    codes = db.Column(db.String(2000),nullable=False)
    video = db.Column(db.String(150), nullable=False)
    fiveer= db.Column(db.String(150), nullable=False)
    img_file = db.Column(db.String(2000), nullable=True)
    img1 = db.Column(db.String(50), nullable=True)
    img2 = db.Column(db.String(50), nullable=True)
    img3 = db.Column(db.String(50), nullable=True)

@app.route("/",methods=['GET','POST'])
def Index():
    post = posts.query.filter_by().all()
    last = math.ceil(len(posts)/int(params['no_of_posts']))
    page = request.args.get('page')
    if(not str(page).isnumeric()):
        page = 1
    page= int(page)
    posts = posts[(page-1)*int(params['no_of_posts']): (page-1)*int(params['no_of_posts'])+ int(params['no_of_posts'])]
    if (page==1):
        prev = "#"
        next = "/?page="+ str(page+1)
    elif(page==last):
        prev = "/?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/?page=" + str(page - 1)
        next = "/?page=" + str(page + 1)

    return render_template('index.html',params=params,posts=post,prev=prev,next=next,page=page),404

@app.route("/Blog/<string:posts_slug>",methods=['GET','POST'])
def PostSlug(posts_slug):
    post = posts.query.filter_by(slug=posts_slug).first()
    return render_template('post.html',post=post,params=params),404

@app.route("/Blog/Download/<string:posts_slug>",methods=['GET','POST'])
def Download(posts_slug):
    post = posts.query.filter_by(slug=posts_slug).first()
    path = 'static\\zipfiles\\'+posts_slug+'.zip'
    return send_file(path,as_attachment=True),404

@app.route("/Home",methods=['GET','POST'])
def About():
    return render_template('about.html',params=params),404


@app.route("/Contact",methods=['GET','POST'])
def Contact():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = contacts(namez=name, phone_num = phone, msg = message, dates= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
        msg = EmailMessage()
        msg.set_content('Blog Website Programming With Zaryab' '\n' 'Message From: ' + name + '\n' 'Message: ' + message + '\n' 'Contact: '+ phone)
        msg['Subject'] = 'New Message :)'
        msg['From'] =  email
        msg['To'] =params['gmail-user']
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(params['gmail-user'], params['gmail-password'])
        server.send_message(msg)
    return render_template('contact.html',params=params),404

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if ('user' in session and session['user'] == params['UserName']):
        post = posts.query.all()
        return render_template('dashboard.html', params=params, posts = post)

    if request.method=='POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if (username == params['UserName'] and userpass == params['Password']):
            session['user'] = username
            post = posts.query.all()
            return render_template('dashboard.html', params=params, posts = post)
    
    return render_template('login.html', params=params)


@app.route("/edit", methods = ['GET', 'POST'])
def edit():
    if ('user' in session and session['user'] == params['UserName']):
        if request.method == 'POST':
            title=request.form.get('title')
            slug=request.form.get('slug')
            content=request.form.get('content')            
            content1=request.form.get('content1')
            content2=request.form.get('content2')
            content3=request.form.get('content3')
            tagline=request.form.get('tagline')
            dates=request.form.get('dates')
            author=request.form.get('author')
            codes=request.form.get('codes')
            video=request.form.get('video')
            fiveer=request.form.get('fiveer')
            img_file=request.form.get('img_file')
            img1=request.form.get('img1')
            img2=request.form.get('img2')
            img3=request.form.get('img3')
            entry = posts(title=title,slug=slug,content=content,content1=content1,content2=content2,content3=content3,tagline=tagline,dates=dates,author=author,
            codes=codes,video=video,fiveer=fiveer,img_file=img_file,img1=img1,img2=img2,img3=img3)
            db.session.add(entry)
            db.session.commit()
            return redirect('/dashboard')
    return render_template('edit.html', params=params)

@app.route("/edit/<string:sno>", methods = ['GET', 'POST'])
def editPost(sno):
    if ('user' in session and session['user'] == params['UserName']):
        if request.method == 'POST':
            title=request.form.get('title')
            slug=request.form.get('slug')
            content=request.form.get('content')            
            content1=request.form.get('content1')
            content2=request.form.get('content2')
            content3=request.form.get('content3')
            tagline=request.form.get('tagline')
            dates=request.form.get('dates')
            author=request.form.get('author')
            codes=request.form.get('codes')
            video=request.form.get('video')
            fiveer=request.form.get('fiveer')
            img_file=request.form.get('img_file')
            img1=request.form.get('img1')
            img2=request.form.get('img2')
            img3=request.form.get('img3')
            post = posts.query.filter_by(sno=sno).first()
            post.title = title
            post.slug = slug
            post.content = content
            post.content1 = content1
            post.content2 = content2
            post.content3 = content3
            post.tagline = tagline
            post.dates = dates
            post.author = author
            post.codes = codes
            post.video = video
            post.fiveer = fiveer
            post.img_file = img_file
            post.img1 = img1
            post.img2 = img2
            post.img3 = img3
            db.session.commit()
            return redirect('/dashboard')

    post = posts.query.filter_by(sno=sno).first()
    return render_template('update.html', params=params, post=post, sno=sno)


@app.route("/delete/<string:sno>", methods = ['GET', 'POST'])
def delete(sno):
    if ('user' in session and session['user'] == params['UserName']):
        post = posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/dashboard')

@app.route("/logout")
def logout():
    session.pop('user',None)
    return redirect('/dashboard')

if __name__ =='__main__':
    app.run(debug=True)