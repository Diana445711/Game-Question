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
    easy_count: int = 20,
    medium_count: int = 10,
    hard_count: int = 10,
    topic: str = "primary school math"
):
    import re, time

    batch = {"easy": [], "medium": [], "hard": []}

    for difficulty, count in [("easy", easy_count), ("medium", medium_count), ("hard", hard_count)]:
        for _ in range(count):
            retries = 0
            max_retries = 3  # max times to retry before skipping
            while retries < max_retries:
                try:
                    batch[difficulty].append(generate_mcq(topic=topic, difficulty=difficulty))
                    break  # success
                except Exception as e:
                    err_str = str(e)
                    if "RESOURCE_EXHAUSTED" in err_str or "quota" in err_str:
                        # extract wait time if possible
                        match = re.search(r"retry in (\d+\.?\d*)s", err_str)
                        retry_seconds = float(match.group(1)) if match else 30
                        print(f"Quota exceeded, waiting {retry_seconds:.2f}s before retry...")
                        time.sleep(retry_seconds + 1)
                        retries += 1
                    else:
                        # Other errors: record and break
                        batch[difficulty].append({"error": err_str})
                        break
            else:
                # If max retries reached, skip question with warning
                batch[difficulty].append({"warning": f"Skipped question after {max_retries} retries due to quota limits"})

    return batch