from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server import db
from server.models import Exercise, Workout, WorkoutExercise
from server.schemas import (
    exercise_schema, exercises_schema,
    workout_schema, workouts_schema,
    workout_exercise_schema,
)


def register_routes(app):

    @app.get("/")
    def index():
        return jsonify({"message": "Workout Tracker API is running."})

    @app.get("/exercises")
    def get_exercises():
        return jsonify(exercises_schema.dump(Exercise.query.all())), 200

    @app.get("/exercises/<int:id>")
    def get_exercise(id):
        exercise = Exercise.query.get(id)
        if not exercise:
            return jsonify({"error": "Exercise not found."}), 404
        return jsonify(exercise_schema.dump(exercise)), 200

    @app.post("/exercises")
    def create_exercise():
        try:
            data = exercise_schema.load(request.get_json() or {})
            exercise = Exercise(**data)
            db.session.add(exercise)
            db.session.commit()
            return jsonify(exercise_schema.dump(exercise)), 201
        except ValidationError as err:
            db.session.rollback()
            return jsonify({"errors": err.messages}), 400
        except (ValueError, IntegrityError) as err:
            db.session.rollback()
            return jsonify({"error": str(getattr(err, "orig", err))}), 400

    @app.delete("/exercises/<int:id>")
    def delete_exercise(id):
        exercise = Exercise.query.get(id)
        if not exercise:
            return jsonify({"error": "Exercise not found."}), 404
        db.session.delete(exercise)
        db.session.commit()
        return jsonify({}), 204

    @app.get("/workouts")
    def get_workouts():
        return jsonify(workouts_schema.dump(Workout.query.all())), 200

    @app.get("/workouts/<int:id>")
    def get_workout(id):
        workout = Workout.query.get(id)
        if not workout:
            return jsonify({"error": "Workout not found."}), 404
        return jsonify(workout_schema.dump(workout)), 200

    @app.post("/workouts")
    def create_workout():
        try:
            data = workout_schema.load(request.get_json() or {})
            workout = Workout(**data)
            db.session.add(workout)
            db.session.commit()
            return jsonify(workout_schema.dump(workout)), 201
        except ValidationError as err:
            db.session.rollback()
            return jsonify({"errors": err.messages}), 400
        except (ValueError, IntegrityError) as err:
            db.session.rollback()
            return jsonify({"error": str(getattr(err, "orig", err))}), 400

    @app.delete("/workouts/<int:id>")
    def delete_workout(id):
        workout = Workout.query.get(id)
        if not workout:
            return jsonify({"error": "Workout not found."}), 404
        db.session.delete(workout)
        db.session.commit()
        return jsonify({}), 204

    @app.post("/workouts/<int:id>/exercises")
    def add_exercise_to_workout(id):
        workout = Workout.query.get(id)
        if not workout:
            return jsonify({"error": "Workout not found."}), 404
        try:
            data = workout_exercise_schema.load(request.get_json() or {})
            exercise = Exercise.query.get(data["exercise_id"])
            if not exercise:
                return jsonify({"error": "Exercise not found."}), 404
            if not any([data.get("sets"), data.get("reps"), data.get("duration_seconds")]):
                return jsonify({"errors": {"_schema": ["Provide sets/reps or a duration_seconds value."]}}), 400
            workout_exercise = WorkoutExercise(
                workout_id=workout.id, exercise_id=exercise.id,
                sets=data.get("sets"), reps=data.get("reps"),
                duration_seconds=data.get("duration_seconds"),
            )
            db.session.add(workout_exercise)
            db.session.commit()
            return jsonify(workout_schema.dump(workout)), 201
        except ValidationError as err:
            db.session.rollback()
            return jsonify({"errors": err.messages}), 400
        except (ValueError, IntegrityError) as err:
            db.session.rollback()
            return jsonify({"error": str(getattr(err, "orig", err))}), 400
