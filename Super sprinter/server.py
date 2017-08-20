from flask import Flask, render_template, redirect, request, session, url_for
import random
import string
import csv

app = Flask(__name__)


def id_generator(chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(6))


def read_csv():
    lst = []
    with open("data.csv", "r", newline='') as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            lst.append(row)
    return lst


def obtained_data():
    story_title = request.args.get('title')
    user_story = request.args.get('story')
    acc_criteria = request.args.get('criteria')
    business_value = request.args.get('value')
    estimation = request.args.get('estim')
    status = request.args.get('status')
    user_id = id_generator()
    actual_list = [user_id, story_title, user_story, acc_criteria, business_value, estimation, status]
    session['user_id'] = user_id
    return actual_list


def write_rows(filename):
    with open("data.csv", "w") as file:
        datawriter = csv.writer(file)
        datawriter.writerows(filename)


@app.route('/')
def story():
    list_of_data = read_csv()
    length_of_csv = len(list_of_data)  
    return render_template('list.html', lst=list_of_data, long=length_of_csv)


@app.route('/new_story')
def new_story():
    return render_template('story_id.html')


@app.route('/update/<int:post_id>')
def update_story(post_id):
    list_of_data = read_csv()
    actual_list = obtained_data()
    for i in range(len(list_of_data)):
        if post_id-1 == i:
            list_of_data[i] = actual_list
    write_rows(list_of_data)
    return redirect("/")


@app.route('/delete/<int:post_id>')
def delete(post_id):
    list_of_data = read_csv()
    data_info = []
    for i in range(len(list_of_data)):
        if post_id == i+1:
            continue
        else:
            data_info.append(list_of_data[i])
    write_rows(data_info)
    return redirect('/')


@app.route('/save', methods=['GET'])
def saving():
    story_info = obtained_data()
    with open("data.csv", "a") as file:
        datawriter = csv.writer(file)
        datawriter.writerow(story_info)
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


