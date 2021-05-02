import sqlite3
from collections import Counter


class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def proverka_by_user_id(self, user_id):
        """
        Проверяет есть ли пользователь с данным id
        :param user_id:
        :return: bool
        """
        result = self.cursor.execute(
            f"SELECT * FROM user WHERE user_token = '{user_id}'").fetchall()
        if (result):
            res = 1
        else:
            res = 0
            self.cursor.execute(
            f"INSERT INTO user (user_token) VALUES('{user_id}')")
            self.connection.commit()
        return 1

    def send_category(self, category_name):
        """
        Добавляет категорию
        :param category_name:
        :return:
        """
        self.cursor.execute(
            f"INSERT INTO training_category (name) VALUES('{category_name}')")
        self.connection.commit()

    def send_progres(self, user_id, date, completed):
        """
        Добавляет прошресс юзера
        """
        self.cursor.execute(
            f"INSERT INTO progress (user_token, date, completed) VALUES('{user_id}', '{date}', '{completed}')")
        self.connection.commit()

    def send_sber_id(self, sber_id):
        """
        Вставка в БД нового пользователя
        :param int: id пользователя
        """
        self.cursor.execute(
            f"INSERT INTO devise (sber_id) VALUES('{sber_id}')")
        self.connection.commit()

    def send_user(self, user_id,  sber_id, username, age, gender, active):
        """
        Вставка в БД нового пользователя
        """
        count = self.cursor.execute(
            f"SELECT Count(*) FROM user WHERE user_token = '{user_id}'").fetchall()
        if (count == 0):
            self.cursor.execute(
            f"INSERT INTO user (user_token, sber_id, name, age, gender, active) VALUES('{user_id}','{sber_id}', '{username}', '{age}', '{gender}', '{active}')")
            self.connection.commit()

    def get_users_by_sberid(self, sber_id):
        """
        достает юзеров по сберайди
        """
        users = self.cursor.execute(
            f"SELECT * FROM user WHERE sber_id = '{sber_id}'").fetchall()
        result = []
        for i in range(len(users)):
            res = dict()
            res["id"] = users[i][0]
            res["user_token"] = users[i][1]
            res["sber_id"] = users[i][2]
            res["name"] = users[i][3]
            res["age"] = users[i][4]
            res["gender"] = users[i][5]
            res["active"] = users[i][6]
            result.append(res)

        return result

    def get_all_category(self):
        """
        Достает все категории
        """
        category = self.cursor.execute(
            f"SELECT * FROM training_category").fetchall()
        result = []
        for i in range(len(category)):
            res = dict()
            res["id"] = category[i][0]
            res["name"] = category[i][1]
            result.append(res)
        return result

    def get_progres_by_user(self, user_token):
        """
        Достает прогрес юзера
        """
        progres = self.cursor.execute(
            f"SELECT * FROM progress WHERE user_token = '{user_token}'").fetchall()
        result = []
        for progres_day in progres:
            res = dict()
            res["id"] = progres_day[0]
            res["user_id"] = progres_day[1]
            res["date"] = progres_day[2]
            res["completed"] = progres_day[3]
            result.append(res)
        return result

    def get_category_by_id(self, category_id):
        """
        Достает категорию по айди
        """
        category = self.cursor.execute(
            f"SELECT * FROM training_category WHERE id = '{category_id}'").fetchall()
        result = []
        for i in range(len(category)):
            res = dict()
            res["id"]=category[i][0]
            res["name"] = category[i][1]
            result.append(res)
        return result

    def get_all_group(self):
        """
        Достает все группы
        """
        group = self.cursor.execute(
            f"SELECT * FROM training_group").fetchall()
        result = []
        for i in range(len(group)):
            res = dict()
            res['id'] = group[i][0]
            res["name"] = group[i][1]
            res["short_discription"] = group[i][2]
            res["discription"] = group[i][3]
            res["image"] = group[i][4]
            result.append(res)
        return result

    def get_exircices_from_group(self, group_id):
        """
        Достает задания одной группы
        """

        exircices_id = self.cursor.execute(
            f"SELECT training_id FROM training_training_group WHERE training_group_id = '{group_id}'").fetchall()
        result = []
        for exircices in exircices_id:
            ex_id = exircices[0]
            ex = self.cursor.execute(
                f"SELECT * FROM training WHERE id = '{ex_id}'").fetchall()
            res = dict()
            res["id"] = ex[0][0]
            res["category"] = self.cursor.execute(
                f"SELECT name FROM training_category WHERE id = '{ex[0][1]}'").fetchall()[0][0]
            res["name"] = ex[0][2]
            res["discription"] = ex[0][3]
            res["photo"] = ex[0][4]
            res["time"] = ex[0][5]
            res["discriptionJoy"] = ex[0][6]
            result.append(res)
        return result

    def get_sber_id(self, sber_id):
        """
        Вставка в БД нового пользователя
        :param int: id пользователя
        """
        devise = self.cursor.execute(
            f"SELECT * FROM devise WHERE sber_id = '{sber_id}'").fetchall()
        return devise

    def get_motivations_id(self, id):
        """
        Достает мотивационную фразу из бд
        """
        phras = self.cursor.execute(
            f"SELECT * FROM motivation WHERE id = '{id}'").fetchall()
        result = []
        res = dict()
        res["id"] = phras[0][0]
        res["name"] = phras[0][1]
        res["discription"] = phras[0][2]
        res["author"] = phras[0][3]
        result.append(res)
        return result
    def count_progress(self):
        res = self.cursor.execute("select Count(*) from progress").fetchall()
        return res[0][0]
    def get_achievement_user(self, user_id):
        count=1
        days=0
        while(count!=0):
            count=self.cursor.execute(
            f"select Count(*) from (select date(date) as curr_date, Count(*) from progress  where user_token = '{user_id}' group by  date(date)) where curr_date=date(date('now',\"-{days} day\"))").fetchall()
            if(count[0][0]>0):
                days+=1
            count=count[0][0]
        

        count_train = self.cursor.execute(
            f"select Count(*) from progress where user_token = '{user_id}'").fetchall()
        
        count_days_train = self.cursor.execute(
            f"select count(*) from (select * from progress where user_token='{user_id}' group by date(date))").fetchall()
        res =dict()
        res['dict']=days
        res['count_train']=count_train[0][0]
        res['count_days_train']=count_days_train[0][0]
        return res



    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
