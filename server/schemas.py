from marshmallow import Schema, fields, validate, validates, ValidationError

from server.models import VALID_CATEGORIES, VALID_DIFFICULTIES


class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    category = fields.String(required=True, validate=validate.OneOf(VALID_CATEGORIES))
    equipment_needed = fields.String(required=False, allow_none=True)
    difficulty = fields.String(required=False, validate=validate.OneOf(VALID_DIFFICULTIES))


class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(dump_only=True)
    exercise_id = fields.Integer(required=True)
    sets = fields.Integer(required=False, allow_none=True, validate=validate.Range(min=1))
    reps = fields.Integer(required=False, allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Integer(required=False, allow_none=True, validate=validate.Range(min=1))
    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    @validates("exercise_id")
    def validate_exercise_id(self, value, **kwargs):
        if value is None or value <= 0:
            raise ValidationError("exercise_id must reference a valid exercise.")


class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(required=True, validate=validate.Range(min=1))
    notes = fields.String(required=False, allow_none=True, validate=validate.Length(max=500))
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()
