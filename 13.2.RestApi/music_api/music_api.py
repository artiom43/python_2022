# from fastapi import HTTPException, Body
from fastapi.responses import JSONResponse

from fastapi import FastAPI, Header
from pydantic import BaseModel
from fastapi import status


app = FastAPI()


class Post(BaseModel):
    name: str
    age: int
    # headers: any


class Track(BaseModel):
    name: str | None
    artist: str | None
    year: int | None
    genres: list[str] | None


COUNT = 0
COUNT_OF_TRACK = {}
UNITED_COUNT_OF_TRACK = 0
UNITED_DICT_OF_TRACK = {}
dict_of_users: dict[str, dict[int | str, Track]] = {}


@app.post("/api/v1/registration/register_user")
def register_used(post: Post) -> dict[str, str]:
    global COUNT
    # print(commons)
    # print(id_tr)
    # print(post.name, post.age)
    # print(header.dict()['x-train'])
    COUNT += 1
    dict_of_users["a"*(40 - len(str(COUNT))) + str(COUNT)] = {}
    COUNT_OF_TRACK["a"*(40 - len(str(COUNT))) + str(COUNT)] = 0
    return {'token': "a"*(40 - len(str(COUNT))) + str(COUNT)}


# async def common_parametrs(headers=Header(default=None, convert_underscores=True)):
#     return {'headers': headers}


@app.post("/api/v1/tracks/add_track", status_code=status.HTTP_201_CREATED)
def add_track(x_token: str | None = Header(default=None), track: Track | None = None) -> JSONResponse | dict[str, int]:
    global COUNT_OF_TRACK
    global UNITED_COUNT_OF_TRACK
    if x_token is None:
        return JSONResponse({"detail": "Missing token"}, status_code=401)
    if x_token not in dict_of_users:
        return JSONResponse({"detail": "Incorrect token"}, status_code=401)

    if track is None:
        return JSONResponse({"detail": None}, status_code=0)
    # return JSONResponse("Missing token", status_code=401)
    if track.name is None or track.artist is None:
        return JSONResponse({"detail": "missing arguments"}, status_code=422)
    # current_count_of_track = COUNT_OF_TRACK[x_token] + 1
    UNITED_COUNT_OF_TRACK += 1
    current_count_of_track = UNITED_COUNT_OF_TRACK
    COUNT_OF_TRACK[x_token] += 1
    dict_of_users[x_token][current_count_of_track] = track
    UNITED_DICT_OF_TRACK[current_count_of_track] = track
    # print(track.name, track.artist, "sdf")
    return {"track_id": current_count_of_track}


@app.delete("/api/v1/tracks/{track_id}")
def delete_track(track_id: int, x_token: str | None = Header(default=None)) -> JSONResponse:
    global COUNT_OF_TRACK
    # print(track_id)
    if x_token is None:
        return JSONResponse({"detail": "Missing token"}, status_code=401)
    if x_token not in dict_of_users:
        return JSONResponse({"detail": "Incorrect token"}, status_code=401)
    # if track_id not in dict_of_users[x_token]:
    #     return JSONResponse({"detail": "Invalid track_id"}, status_code=404)
    if track_id not in UNITED_DICT_OF_TRACK:
        return JSONResponse({"detail": "Invalid track_id"}, status_code=404)
    # del dict_of_users[x_token][track_id]
    del UNITED_DICT_OF_TRACK[track_id]
    return JSONResponse({"status": "track removed"}, status_code=200)


@app.get("/api/v1/tracks/all")
def get_all_about_track(x_token: str | None = Header(default=None)) -> JSONResponse:
    # print(x_token, "get_all")
    if x_token is None:
        return JSONResponse({"detail": "Missing token"}, status_code=401)
    if x_token not in dict_of_users:
        return JSONResponse({"detail": "Incorrect token"}, status_code=401)
    answer_list = []
    # for track_id, track in dict_of_users[x_token].items():
    for track_id, track in UNITED_DICT_OF_TRACK.items():
        if track.genres is None:
            track.genres = []
        answer_list.append({'name': track.name, 'artist': track.artist, 'year': track.year,
                            'genres': track.genres})
    return JSONResponse(answer_list, status_code=200)


@app.get("/api/v1/tracks/{track_id}")
def get_info_about_track(track_id: int | str | None = None, x_token: str | None = Header(default=None),
                         name: str | None = None, artist: str | None = None) -> JSONResponse:
    global dict_of_users
    # print(track_id)
    # print(x_token)
    # if track_id == 'all':
    #     print(x_token, "get_all")
    #     if x_token is None:
    #         return JSONResponse({"detail": "Missing token"}, status_code=401)
    #     if x_token not in dict_of_users:
    #         return JSONResponse({"detail": "Incorrect token"}, status_code=401)
    #     answer_list = []
    #     for track_id, track in dict_of_users[x_token].items():
    #         if track.genres is None:
    #             track.genres = []
    #         answer_list.append({'name': track.name, 'artist': track.artist, 'year': track.year,
    #                             'genres': track.genres})
    #     return JSONResponse(answer_list, status_code=200)
    if type(track_id) == str and track_id.startswith("search"):
        print("sdf")
        # dict_of_vars = dict(parse.parse_qsl(parse.urlsplit(track_id).query))
        print(name, artist, "search ", " question")
        if x_token is None:
            return JSONResponse({"detail": "Missing token"}, status_code=401)
        if x_token not in dict_of_users:
            return JSONResponse({"detail": "Incorrect token"}, status_code=401)
        if name is None and artist is None:
            return JSONResponse({"detail": "You should specify at least one search argument"}, status_code=422)
        answer_list = []
        for track_id, track in UNITED_DICT_OF_TRACK.items():
            if (track.name == name or name is None) and (track.artist == artist or artist is None):
                answer_list.append(track_id)
        return JSONResponse({"track_ids": answer_list}, status_code=200)

    if x_token is None:
        return JSONResponse({"detail": "Missing token"}, status_code=401)
    if x_token not in dict_of_users:
        return JSONResponse({"detail": "Incorrect token"}, status_code=401)
    if track_id not in dict_of_users[x_token]:
        return JSONResponse({"detail": "Invalid track_id"}, status_code=404)
    return JSONResponse({'name': dict_of_users[x_token][track_id].name,
                         'artist': dict_of_users[x_token][track_id].artist}, status_code=200)
