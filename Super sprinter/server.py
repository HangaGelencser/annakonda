from flask import Flask, render_template, redirect, request, session, url_for
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
    return render_template('list.html', lst=lst, long=length_of_csv)


@app.route('/new_story')
def new_story():
    return render_template('story.html')


@app.route('/update/<int:post_id>')
def update_story(post_id):
    list_of_data = read_csv()
    story_title = request.args.get('title')
    user_story = request.args.get('story')
    acc_criteria = request.args.get('criteria')
    business_value = request.args.get('value')
    estimation = request.args.get('estim')
    status = request.args.get('status')
    user_id = id_generator()
    actual_list = [user_id, story_title, user_story, acc_criteria, business_value, estimation, status]
    print (actual_list)
    for i in range(len(list_of_data)):
        if post_id-1 == i:
            list_of_data[i] = actual_list
    with open("data.csv", "w") as file:
        datawriter = csv.writer(file)
        datawriter.writerows(list_of_data)
    return redirect("/")


@app.route('/delete/<int:post_id>')
def delete(post_id):
    list_of_data = read_csv()
    story_title = request.args.get('title')
    user_story = request.args.get('story')
    acc_criteria = request.args.get('criteria')
    business_value = request.args.get('value')
    estimation = request.args.get('estim')
    status = request.args.get('status')
    user_id = id_generator()
    actual_list = [user_id, story_title, user_story, acc_criteria, business_value, estimation, status]
    print (list_of_data)
    print (post_id)
    data_info = []
    for i in range(len(list_of_data)):
        print (i)
        print ("BENT")
        if post_id == i+1:
            print ("IFBENT")
            continue
        else:
            print ("ELSEBENT")
            data_info.append(list_of_data[0])
    print (data_info)
    return redirect('/')

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
    session['user_id'] = user_id
    with open("data.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow(story_info)
    return redirect('/')


@app.route('/story/<int:post_id>')
def story_1(post_id):
    list_of_data = read_csv()
    return render_template('story_id.html', post_id=post_id, lst=list_of_data[post_id-1])



if __name__ == "__main__":
  app.secret_key = 'subidubi'  # Change the content of this string
  app.run(
      debug=True,  # Allow verbose error reports
      port=5000  # Set custom port
  )


