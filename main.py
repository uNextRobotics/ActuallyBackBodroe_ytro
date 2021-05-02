from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from scheme import *
from SQLighter import *
import json
import pymongo
import  datetime
from datetime import timedelta
client = pymongo.MongoClient("mongodb+srv://dbMike:pMQI7fDiPLbTyNVg@cluster0.1il65.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.SberHackBack

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/User")
async def createUser(user: User):
    # db_worker = SQLighter("maindatabase.db")
    # count = db_worker.count_progress()
    # if(count == 0):
    #     cursor = db.user
    #     for document in cursor.find():
    #         db_worker.send_user(document["UserId"], 0, "string", 0, "string", 0)
    #     cursor = db.progress # choosing the collection you need
    #     for document in cursor.find():
    #         db_worker.send_progres(document["UserId"], document["date"], True)
    #         #print (document)
    # db_worker.send_user(user.UserId, user.SberId, user.Name,
    #                     user.Age, user.Gender, user.Active)
    # db_worker.close()
    post = {}
    post['UserId'] = user.UserId
    u = db.user
    post_id = u.insert_one(post)
    return user


@app.post('/SberId/')
async def createSberId(sber_id: int):
    db_worker = SQLighter("maindatabase.db")
    db_worker.send_sber_id(sber_id)
    db_worker.close()
    return sber_id


@app.post('/CategoryExercises')
async def createCategoryExercises(categ: Categoriya):
    db_worker = SQLighter("maindatabase.db")
    db_worker.send_category(categ.Name)
    db_worker.close()
    return categ

##
@app.post("/ProgressAchieve")
async def createProgressAchieve(achiv: Progres, request: Request):
    print(await request.body())
    # db_worker = SQLighter("maindatabase.db")
    # db_worker.send_progres(achiv.UserId, datetime.date.today(), achiv.Completed)
    # db_worker.close()
    post = {}
    post['UserId'] = achiv.UserId
    post['date'] = str(datetime.datetime.now() +timedelta(hours=3))
    p = db.progress
    post_id = p.insert_one(post)
    return achiv


@app.get("/UsersBySberId")
async def getUsersBySberId(sber_id: int):
    db_worker = SQLighter("maindatabase.db")
    user = db_worker.get_users_by_sberid(sber_id)
    db_worker.close()
    return user


@app.get("/ProverkaUsersByUserId")
async def ProverkaUsersByUserId(user_id: str):
    db_worker = SQLighter("maindatabase.db")
    ans = db_worker.proverka_by_user_id(user_id)
    db_worker.close()
    return ans


@app.get("/AllCategoriesExirc")
async def getAllCategoriesExirc():
    db_worker = SQLighter("maindatabase.db")
    Categ = db_worker.get_all_category()
    db_worker.close()
    return Categ


@app.get("/CategoryById")
async def getCategoryById(category_id: int):
    db_worker = SQLighter("maindatabase.db")
    categById = db_worker.get_category_by_id(category_id)
    db_worker.close()
    return categById


@app.get("/AllGroupsExercises")
async def getAllGroupsExercises():
    db_worker = SQLighter("maindatabase.db")
    group = db_worker.get_all_group()
    db_worker.close()
    return group


@app.get("/ExircicesfromGroup")
async def getExircicesfromGroup(group_id: int):
    db_worker = SQLighter("maindatabase.db")
    Exircices = db_worker.get_exircices_from_group(group_id)
    db_worker.close()
    return Exircices


@app.get("/ProgressByUser")
async def getProgressByUser(user_id: str):
    res = []
    cursor = db.progress
    for i in cursor.find({'UserId': user_id}):
        res.append({"date": i['date'][:10]})
    return res


@app.get("/Phrase")
async def getMotivationalPhrase(motivation_id: int):
    db_worker = SQLighter("maindatabase.db")
    Phras = db_worker.get_motivations_id(motivation_id)
    db_worker.close()
    return Phras


@app.get("/AchiviesFomUser")
async def getAchiviesForUser(user_id: str):
    # db_worker = SQLighter("maindatabase.db")
    # Achievements = db_worker.get_achievement_user(user_id)
    # db_worker.close()
    cursor = db.progress
    count_train = 0
    for i in cursor.find({'UserId': user_id}):
        count_train+=1
    dates = []
    for i in cursor.find({'UserId': user_id}):
        if(i['date'][:10] not in dates):
            print(i['date'][:10])
            dates.append(i['date'][:10])
    count_days= len(dates)   

    date_ = datetime.date.today()+timedelta(hours=3)
    count =0
    while(True):
        if(str(date_ - timedelta(count)) in dates):
            count+=1
        else:
            break
            
    return {"dict": count, "count_days_train": count_days, "count_train": count_train}
