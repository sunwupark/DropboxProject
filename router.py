# views.py
import firebase_admin
from firebase_admin import credentials, firestore, db
from fastapi import FastAPI
import json
import random
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi import status
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from services import login_service

router = APIRouter()

cred = credentials.Certificate("file-ground-firebase-adminsdk-k8zwz-2dbb250413.json")
firebase_admin.initialize_app(cred,
                              {'databaseURL':'https://file-ground-default-rtdb.asia-southeast1.firebasedatabase.app//'})

# Get Firestore client
dbs = firestore.client()


@router.get("/naver/login")
async def naver_login(request: Request):
    redirect_uri = request.url_for("naver_callback")
    print('redirect_uri:', redirect_uri)
    naver_login_url = login_service.get_naver_login_url(redirect_uri)
    return HTMLResponse(f'<h1><a href="{naver_login_url}">Sign in with Naver</a></h1>')


@router.get("/naver/callback")
async def naver_callback(request: Request, response: Response, code: str = None, state: str = None):
    if code is None or state is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Missing code or state parameter")
    login_token = await login_service.get_naver_login_token(code, state)
    response.set_cookie(key="access_token", value=login_token["access_token"])
    return login_token
    # return {"access_token": login_token["access_token"]}


@router.get("/auth/refresh")
async def auth_refresh(request: Request):
    return HTMLResponse()

@router.get("/")
async def root():
    return {"message": "Hello World oh yeah sumin is legend"}


@router.post("/users")
async def create_user(user: dict):
    #Add new user to Realtime Database Firebase
    ref = db.reference("/users/" + user["id"])
    ref.push().set(user)
    # Add new user document to Firestore
    doc_ref = dbs.collection(u'users').document(user["id"])
    doc_ref.set(user)

    return {"message": "User created successfully"}

@router.get("/users")
async def get_users(user_id: str):
    #Retrieve user from RealtimeDatabase
    ref = db.reference("/users")
    user_info = ref.get()
    return_dict = {}
    for key, value in user_info.items():
        return_dict[key] = value
    # Retrieve user document from Firestore
    doc_ref = dbs.collection(u'users').document(user_id)
    doc = doc_ref.get()


@router.get("/users/{user_id}")
async def get_user(user_id: str):
    #Retrieve user from RealtimeDatabase
    ref = db.reference("/users/" + user_id)
    user_info = ref.get()
    return_dict = {}
    for key, value in user_info.items():
        return_dict[key] = value
    # Retrieve user document from Firestore
    doc_ref = dbs.collection(u'users').document(user_id)
    doc = doc_ref.get()

    return return_dict.items()

    if doc.exists:
        return doc.to_dict()
    else:
        return {"message": "User not found"}
    
@router.post("/photos")
async def upload_photo(photo: dict):
    #Add new photo to Realtime Database Firebase
    ref = db.reference("/photos/" + photo["id"])
    ref.push().set(photo)
    # Add new photo document to Firestore
    doc_ref = dbs.collection(u'photos').document(photo["id"])
    doc_ref.set(photo)

    return {"message": "Photo created successfully"}

@router.get("/photos/{photo_id}")
async def get_photo(photo_id: str):
    #Retrieve user from RealtimeDatabase
    ref = db.reference("/photos/" + photo_id)
    photo_info = ref.get()
    return_dict = {}
    for key, value in photo_info.items():
        return_dict[key] = value
    # Retrieve user document from Firestore
    doc_ref = dbs.collection(u'photos').document(photo_id)
    doc = doc_ref.get()

    return return_dict.items()

    if doc.exists:
        return doc.to_dict()
    else:
        return {"message": "User not found"}
    
@router.post("/ground")
async def create_ground(ground: dict):
    #Add new user to Realtime Database Firebase
    while(True):
        random_num = random.randint(100000, 999999)
        id = random_num
        ref = db.reference("/ground/")
        ground_info = ref.get()

        if ground_info == "'None'":
            ground["id"] = str(id)
            break
        
        bool = False
        for key, value in ground_info.items():
            if value["id"] == id:
                bool = True
        if bool == False:
            print(id)
            ground["id"] = str(id)
            break
    
    ref = db.reference("/ground/" + str(ground["id"]))
    ref.set(ground)

    return {"message": "User created successfully"}

@router.get("/ground/{ground_id}")
async def get_ground(ground_id: str):
    #Retrieve user from RealtimeDatabase
    ref = db.reference("/ground/" + ground_id)
    ground_info = ref.get()
    return_dict = {}
    for key, value in ground_info.items():
        return_dict[key] = value
    return return_dict
