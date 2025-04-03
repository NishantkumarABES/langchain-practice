from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from llm_application import main
from pydantic import BaseModel

app = FastAPI()

origins = ["http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NameRequest(BaseModel):
    name: str

@app.post("/process", tags=["services"])
def process(request: NameRequest):
    try:
        print(request.name)
        # summary, pic_url = main(name)
        summary = "Elon Musk is a renowned entrepreneur and philanthropist. He is known for his innovative technological solutions and his advocacy for social justice."
        pic_url = "https://placehold.co/600x400.png"

        return JSONResponse(content={
            "summary": summary,
            "pic_url": pic_url,
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
