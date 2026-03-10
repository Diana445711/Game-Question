from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from question_generator import generate_mcq

app = FastAPI()

# Allow browser and Unity WebGL requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Snakes and Ladders Question API running"}


# Preload all difficulties for full game 
@app.get("/game_questions")
def get_game_questions(
    easy_count: int = 20,
    medium_count: int = 10,
    hard_count: int = 10,
    topic: str = "primary school math"
):
    batch = {"easy": [], "medium": [], "hard": []}

    for _ in range(easy_count):
        batch["easy"].append(generate_mcq(topic=topic, difficulty="easy"))
    for _ in range(medium_count):
        batch["medium"].append(generate_mcq(topic=topic, difficulty="medium"))
    for _ in range(hard_count):
        batch["hard"].append(generate_mcq(topic=topic, difficulty="hard"))

    return batch