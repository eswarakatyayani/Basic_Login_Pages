from flask import Flask, Response, render_template, request, flash
import requests, json
import sqlite3
import secrets
from passlib.hash import pbkdf2_sha256

app=Flask(__name__)
app.secret_key=secrets.token_urlsafe(32)
conn=sqlite3.connect('user.db',check_same_thread=False)
cursor=conn.cursor()

@app.route('/')
def login():
  url=requests.get('https://dog.ceo/api/breeds/image/random')
  image=json.loads(url.text)
  return render_template('login.html',imagefile=image['message'])

@app.route('/login1',methods=['POST'])
def login1(): #when users entry username and password
  user=request.form.get('username')
  pword=request.form.get('password')
  cursor.execute("SELECT username,password FROM user")  # id username password
  row=cursor.fetchall()
  for item in row:
    if (user==item[0] and pbkdf2_sha256.verify(pword,item[1])):
       url=requests.get('https://dog.ceo/api/breeds/image/random')
       image=json.loads(url.text)
       return render_template('index.html',imagefile=image['message'])
  url=requests.get('https://dog.ceo/api/breeds/image/random')
  image=json.loads(url.text)
  return render_template('login.html',imagefile=image['message'])

@app.route('/signup')
def signup():
  return render_template('signup.html')

@app.route('/signup1', methods=['POST'])
def signup1():
  user=request.form.get('username')
  pword=request.form.get('password')
  pword_rep=request.form.get('psw-repeat')
  if (pword==pword_rep):
    cursor.execute("SELECT username,password FROM user")  # id username password
    row=cursor.fetchall()
    for item in row:
      if (user==item[0] and pbkdf2_sha256.verify(pword,item[1])):
        url=requests.get('https://dog.ceo/api/breeds/image/random')
        image=json.loads(url.text)
        return render_template('index.html',imagefile=image['message'])
    cursor.execute('INSERT INTO user(username, password) VALUES(?,?)',(user,pbkdf2_sha256.hash(pword),))
    conn.commit()
    url=requests.get('https://dog.ceo/api/breeds/image/random')
    image=json.loads(url.text)
    return render_template('login.html',imagefile=image['message'])
  else:
    messages='Password and Repeat Password is not the same!!'
    flash(messages)
    return render_template('signup.html')

@app.route('/nature')
def nature():
  return render_template('nature.html')

@app.route('/dogs')
def dogs():
  n=20
  imglist=[]
  for i in range(n): #i: 0 to n-1
    url=requests.get('https://dog.ceo/api/breeds/image/random')
    image=json.loads(url.text)
    imglist.append([i+1,image['message']]) 
    #imglist = [ [1,'xxxxx'], [2,'BBBBB'] ]  total = n
  return render_template('dogs.html', data=imglist, total=n)

if __name__ == '__main__':
    app.run(port=5000, debug=True) #port > 1024
