from flask import Flask, render_template, redirect, request, session
import random
import string
import csv

app = Flask(__name__)


def id_generator(chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(6))


def read_csv():
    lst = []
    with open("data.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            lst.append(row)
    return lst


@app.route('/')
def story():
    lst = read_csv()
    length_of_csv = len(lst)        
    return render_template('list.html',lst=lst, long=length_of_csv)


@app.route('/new_story')
def new_story():
    return render_template('story.html')



@app.route('/save', methods = ['GET'])
def saving():
    story_title = request.args.get('title')
    user_story = request.args.get('story')
    acc_criteria = request.args.get('criteria')
    business_value = request.args.get('value')
    estimation = request.args.get('estim')
    status = request.args.get('status')
    user_id = id_generator()
    story_info = [user_id, story_title, user_story, acc_criteria, business_value, estimation, status]
    print (story_info)
    session['user_id'] = user_id
    with open("data.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow(story_info)

    return redirect('/')


@app.route('/story/<int:post_id>')
def story_1(post_id):
    list_of_data = read_csv()
    return render_template('story_id.html', lst=list_of_data[post_id-1])



if __name__ == "__main__":
  app.secret_key = 'subidubi'  # Change the content of this string
  app.run(
      debug=True,  # Allow verbose error reports
      port=5000  # Set custom port
  )


