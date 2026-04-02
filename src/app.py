"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Practice team drills and compete against other schools",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["alex@mergington.edu", "nina@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Build swim technique and conditioning in the school pool",
        "schedule": "Mondays and Wednesdays, 3:00 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["maria@mergington.edu", "ryan@mergington.edu"]
    },
    "Art Workshop": {
        "description": "Explore painting, drawing, and mixed-media projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["lisa@mergington.edu", "dylan@mergington.edu"]
    },
    "Drama Club": {
        "description": "Create scenes, rehearse plays, and perform for the school",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 18,
        "participants": ["sarah@mergington.edu", "kevin@mergington.edu"]
    },
    "Science Club": {
        "description": "Perform experiments and explore science topics in depth",
        "schedule": "Fridays, 2:30 PM - 4:00 PM",
        "max_participants": 16,
        "participants": ["natalie@mergington.edu", "jason@mergington.edu"]
    },
    "Book Club": {
        "description": "Discuss novels, poetry, and nonfiction with fellow readers",
        "schedule": "Mondays, 4:00 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["hazel@mergington.edu", "lucas@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Prevent duplicate signups
    if email in activity["participants"]:
        raise HTTPException(status_code=400,
                            detail=f"{email} is already signed up for {activity_name}")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def remove_participant(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    if email not in activity["participants"]:
        raise HTTPException(status_code=404,
                            detail=f"{email} is not registered for {activity_name}")

    activity["participants"].remove(email)
    return {"message": f"Removed {email} from {activity_name}"}
