from locust import HttpUser, constant, task, SequentialTaskSet
import pandas as pd
import random
# locust -f basic_loading.py

FUZZER = True
# def get_parameters():
df = pd.read_csv("books_data.csv")
    # print(df.head())

def get_random_id(in_range=None):
    if in_range==None:
        id = random.randint(1,9999999)
    else:
        id = random.randint(1,in_range)

    return id

def get_random_name():
    id = random.randint(1,52000)
    row = df.iloc[id]
    return row["Name"]

def get_random_rating():
    rating = round(random.uniform(1,2), 2)
    return rating 

def get_random_review():
    id = random.randint(1,52000)
    row = df.iloc[id]
    return row["Review"]

def get_random_tag():
    id = random.randint(1,52000)
    row = df.iloc[id]
    return row["Tags"]


def get_book_data(fuzz=False):
    id = get_random_id(in_range=len(df))
    Name = get_random_name()
    Rating = get_random_rating()
    Review = get_random_review()
    Tag = get_random_tag()

    data_list = [id,Name,Rating,Review,Tag]

    if fuzz==False:
        book_data = {
            "id":id,
            "Name":Name,
            "Rating":Rating,
            "Review":Review,
            "Tag":Tag 
        }
    else:
        book_data = {
            "id":data_list[random.randint(0,4)],
            "Name":data_list[random.randint(0,4)],
            "Rating":data_list[random.randint(0,4)],
            "Review":data_list[random.randint(0,4)],
            "Tag":data_list[random.randint(0,4)] 
        }

    return book_data
# print(get_book_data())
# print(get_book_data(fuzz=True))


class Home_Search(SequentialTaskSet):

    @task
    def visitHomePage(self):
        res = self.client.get("/detail")
        print("Visit Home Page = ",res.status_code)

    @task
    def searchBook(self):
        temp_book_data = get_book_data(fuzz=FUZZER)
        rondom_tag = temp_book_data["Tag"]
        random_data = {"tag":rondom_tag } 
        res = self.client.post("/detail", data =random_data)
        print("Search book = ",res.status_code)

class AddBook(SequentialTaskSet):

    @task
    def visitAddBookPage(self):
        res = self.client.get("/addbook")
        print("Visit addbook Page = ",res.status_code)

    @task
    def AddBook(self):

        random_data = get_book_data(fuzz=FUZZER)
        res = self.client.post("/addbook", data =random_data)
        print("addbook = ",res.status_code)

class UpdateBook(SequentialTaskSet):

    @task
    def visitUpdatePage(self):
        res = self.client.get("/update")
        print("Visit UpdateBook Page = ",res.status_code)

    @task
    def UpdateBook(self):
        random_data = get_book_data(fuzz=FUZZER)
        res = self.client.post("/update", data =random_data)
        print("UpdateBook = ",res.status_code)

class DeleteBook(SequentialTaskSet):

    @task
    def visitDeletePage(self):
        res = self.client.get("/deletebook")
        print("Visit DeleteBook Page = ",res.status_code)

    @task
    def DeleteBook(self):
        temp_book_data = get_book_data(fuzz=FUZZER)
        random_id = temp_book_data["id"]
        random_data = {"id":random_id} 
        res = self.client.post("/deletebook", data =random_data)
        print("deletebook = ",res.status_code)

# get_parameters()

class MySeqTest(HttpUser):
    wait_time = constant(1)
    host = "http://127.0.0.1:5000"

    tasks = [Home_Search,AddBook,UpdateBook,DeleteBook]
    # tasks = [Home_Search,AddBook,UpdateBook]
    # tasks = [DeleteBook]


# locust -f basic_loading.py