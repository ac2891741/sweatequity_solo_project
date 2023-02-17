from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import workout

@app.route('/missionstatement')
def mission():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('mission.html')

@app.route('/cardio')
def cardio():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    all_workouts = workout.Workout.get_all()
    return render_template('cardio.html', user = user.User.select_user(data), workouts = all_workouts )

@app.route('/strength_training')
def strength_training():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    all_workouts = workout.Workout.get_all()
    return render_template('strength_training.html', user = user.User.select_user(data), workouts = all_workouts )

@app.route('/create_a_workout')
def create_a_workout():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('create_workout.html', user = user.User.select_user(data))

@app.route('/create_a_workout_2')
def create_a_workout_2():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('create_workout_2.html', user = user.User.select_user(data))

@app.route('/creating_the_workout_2', methods=['POST'])
def creating_the_workout_2():
    if 'user_id' not in session:
        return redirect('/logout')
    if not workout.Workout.validate_workouts(request.form):
        return redirect('/create_a_workout')
    data = {
        'name' : request.form['name'],
        'each_exercise' : request.form['each_exercise'],
        'user_id' : session['user_id']
    }
    workout.Workout.save(data)
    return redirect('/cardio')

@app.route('/creating_the_workout', methods=['POST'])
def creating_the_workout():
    if 'user_id' not in session:
        return redirect('/logout')
    if not workout.Workout.validate_workouts(request.form):
        return redirect('/create_a_workout')
    data = {
        'name' : request.form['name'],
        'each_exercise' : request.form['each_exercise'],
        'user_id' : session['user_id']
    }
    workout.Workout.save(data)
    return redirect('/strength_training')

@app.route("/view_workout/<int:workout_id>")
def view_workout(workout_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'workout_id' : workout_id
    }
    return render_template('view.html', workout = workout.Workout.select_one(data))

@app.route('/like/<int:id>')
def likeworkout(id):
    if 'user_id' not in session:
        return redirect('/')
    id_data={
        "workout_id": id
    }
    one_workout=workout.Workout.get_one(id_data)
    add_like= int(one_workout.likes) + 1
    update_data={
        "id" : id,
        "likes": add_like
    }
    workout.Workout.add_like(update_data)
    return redirect('/strength_training')

@app.route('/edit_workout/<int:workout_id>')
def edit_workout(workout_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'workout_id' : workout_id
    }
    user_data = {
        'id': session['user_id']
    }
    return render_template('edit.html', workout = workout.Workout.select_one(data), user = user.User.select_user(user_data))

@app.route('/creating_the_workout/edit/<int:workout_id>', methods=['POST'])
def update_workout(workout_id):
    if 'user_id' not in session:
        return redirect ('/logout')
    if not workout.Workout.validate_workouts(request.form):
        return redirect(f'/edit_workout/{workout_id}')

    data ={
        "workout_id" : request.form['workout_id'],
        "name" : request.form['name'],
        "each_exercise": request.form['each_exercise'],

    }

    workout.Workout.update(data)
    return redirect("/strength_training")

@app.route('/delete_workout/<int:workout_id>')
def destroy(workout_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'workout_id': workout_id,
    }
    workout.Workout.destroy(data)
    return redirect("/strength_training")

@app.route('/destroy_workout/<int:workout_id>')
def deleting(workout_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'workout_id': workout_id,
    }
    workout.Workout.destroy(data)
    return redirect("/cardio")