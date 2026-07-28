from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

from server import db

VALID_DIFFICULTIES = ("beginner", "intermediate", "advanced")
VALID_CATEGORIES = ("strength", "cardio", "flexibility", "balance")


class Exercise(db.Model):
    __tablename__ = "exercises"

    __table_args__ = (
        # Table constraint #1: exercise names must be unique so trainers
        # don't end up with duplicate reusable exercises.
        UniqueConstraint("name", name="uq_exercise_name"),
        # Table constraint #2: difficulty is restricted to a fixed set of
        # values directly at the database layer, not just in Python.
        CheckConstraint(
            "difficulty IN ('beginner', 'intermediate', 'advanced')",
            name="difficulty_valid_values",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.String(200), nullable=True)
    difficulty = db.Column(db.String(20), nullable=False, default="beginner")

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan",
    )
    workouts = association_proxy("workout_exercises", "workout")

    # Model validation #1: name can't be blank/whitespace-only.
    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name cannot be empty.")
        return value.strip()

    # Model validation #2: category must be one of the supported values.
    @validates("category")
    def validate_category(self, key, value):
        if value not in VALID_CATEGORIES:
            raise ValueError(
                f"Category must be one of: {', '.join(VALID_CATEGORIES)}."
            )
        return value

    def __repr__(self):
        return f"<Exercise {self.id} {self.name}>"


class Workout(db.Model):
    __tablename__ = "workouts"

    __table_args__ = (
        # Table constraint: duration must be a positive number of minutes.
        CheckConstraint("duration_minutes > 0", name="duration_positive"),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(500), nullable=True)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan",
    )
    exercises = association_proxy("workout_exercises", "exercise")

    # Model validation: duration must be positive (backstops the DB
    # constraint with a friendlier Python-level error before INSERT).
    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value is None or value <= 0:
            raise ValueError("Workout duration must be a positive number of minutes.")
        return value

    def __repr__(self):
        return f"<Workout {self.id} {self.date}>"


class WorkoutExercise(db.Model):
    """Join model linking a Workout to an Exercise, carrying the
    per-workout performance details (sets/reps or a timed duration)."""

    __tablename__ = "workout_exercises"

    __table_args__ = (
        CheckConstraint("sets IS NULL OR sets > 0", name="sets_positive"),
        CheckConstraint("reps IS NULL OR reps > 0", name="reps_positive"),
        CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds > 0",
            name="duration_seconds_positive",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)

    sets = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    # Model validation: reject non-positive values for any of these fields.
    @validates("sets", "reps", "duration_seconds")
    def validate_has_data(self, key, value):
        if value is not None and value <= 0:
            raise ValueError(f"{key} must be a positive number.")
        return value

    def __repr__(self):
        return f"<WorkoutExercise workout={self.workout_id} exercise={self.exercise_id}>"
