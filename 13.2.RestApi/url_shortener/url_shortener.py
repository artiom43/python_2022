from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel


app = FastAPI()


class ToShort(BaseModel):
    url: str


class Shorted(BaseModel):
    url: str
    key: str


COUNTED_KEY = 0
DICT_OF_KEYS: dict[str, ToShort] = {}
DICT_OF_URLS: dict[str, str] = {}


@app.post("/shorten", response_model=Shorted, status_code=201)
def short_url(data: ToShort) -> JSONResponse:
    global COUNTED_KEY
    # print(data.url)
    if data.url in DICT_OF_URLS:
        return JSONResponse({'url': data.url, 'key': DICT_OF_URLS[data.url]}, status_code=201)
    COUNTED_KEY += 1
    current_key = str(COUNTED_KEY)
    DICT_OF_KEYS[current_key] = data
    DICT_OF_URLS[data.url] = current_key
    return JSONResponse({'url': data.url, 'key': current_key}, status_code=201)


@app.get("/go/{key}", status_code=307)
def redirect_to_url(key: str) -> JSONResponse | RedirectResponse:
    # print(key)
    if key not in DICT_OF_KEYS:
        return JSONResponse("", status_code=404)
    return RedirectResponse(DICT_OF_KEYS[key].url, status_code=307)
