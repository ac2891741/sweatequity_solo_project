from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Workout:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.each_exercise = data['each_exercise']
        self.likes = data['likes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def save(cls,data):
        query = "INSERT INTO workouts (name, each_exercise, user_id) VALUES (%(name)s, %(each_exercise)s, %(user_id)s);"
        return connectToMySQL('sweatequity').query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM workouts JOIN users ON workouts.user_id = users.id;"
        results = connectToMySQL('sweatequity').query_db(query)
        all_workouts = []

        for row in results:
            one_workout = cls(row)

            one_workout_author_info = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at'],
            }
            author = user.User(one_workout_author_info)
            one_workout.creator = author

            all_workouts.append(one_workout)
            
        return all_workouts
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM workouts WHERE id = %(workout_id)s;"
        db = connectToMySQL('sweatequity').query_db(query,data)

        return cls(db[0])

    @classmethod
    def select_one(cls, data):
        query = "SELECT * FROM workouts JOIN users ON workouts.user_id = users.id WHERE workouts.id = %(workout_id)s;"
        results = connectToMySQL('sweatequity').query_db(query, data)
        if not results:
            return False
        results = results[0]
        one_workout = cls(results)

        one_user_info = {
                'id' : results['users.id'],
                'first_name' : results['first_name'],
                'last_name' : results['last_name'],
                'email' : results['email'],
                'password' : results['password'],
                'created_at' :results['users.created_at'],
                'updated_at' : results['users.updated_at'],
            }
        one_workout.creator = user.User(one_user_info)
        
        return one_workout
    @classmethod
    def update(cls,data):
        query = "UPDATE workouts SET name=%(name)s, each_exercise=%(each_exercise)s WHERE id = %(workout_id)s;"
        return connectToMySQL('sweatequity').query_db(query,data)

    @classmethod
    def add_like(cls,data):
        query= "UPDATE workouts SET likes = %(likes)s WHERE id = %(id)s;"
        return connectToMySQL('sweatequity').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM workouts WHERE id = %(workout_id)s;"
        return connectToMySQL('sweatequity').query_db(query,data)

    @staticmethod
    def validate_workouts(data):
        is_valid = True
        if len(data["name"]) <= 0 or len(data["each_exercise"]) <= 0:
            is_valid = False
            flash("All Fields Required")
        if len(data['name']) < 3:
            flash("Name Must Require at Least 3 Characters")
            is_valid = False
        if len(data['each_exercise']) < 10:
            flash("Exercise Descriptions Must Require at Least 10 Characters")
            is_valid = False
        return is_valid