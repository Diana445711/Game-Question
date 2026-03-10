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


@app.get("/game_questions")
def get_game_questions(
    easy_count: int = 1,
    medium_count: int = 1,
    hard_count: int = 1,
    topic: str = "primary school math"
):
    batch = {"easy": [], "medium": [], "hard": []}

    for difficulty, count in [("easy", easy_count), ("medium", medium_count), ("hard", hard_count)]:
        for _ in range(count):
            try:
                batch[difficulty].append(generate_mcq(topic=topic, difficulty=difficulty))
            except Exception as e:
                batch[difficulty].append({"error": str(e)})

    return batch