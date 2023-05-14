from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from PIL import Image
import io
import matplotlib.pyplot as plt
url = "mongodb+srv://root:12345678rk@rkdatabase.yig0aad.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url, server_api=ServerApi('1'))


class save_in_mongo:
    def __init__(self, search_term, base_path, noof_image):
        self._term = search_term
        self._path = base_path
        self._images = noof_image
        self._db  = client['images']
        self._collection = self._db[search_term]
        try:
            client.admin.command('ping')
            print("Connected to the Database")
        except Exception as e:
            print(e)

    def check(self):
        for db in client.list_database_names():
            if db == 'images':
                for col in self._db.list_collection_names():
                    if col == self._term:
                        return 'Files is already in Database do you want to update '
                    else:
                        return 'Files is not in Database do you want to save '
            else:
                return 'Folder is not in Database do you want to save '

    def save(self):
        try:
            for images in range(self._images):
                file = os.path.join(self._path, self._term, str(images)+'.jpg')
                img = Image.open(file)
                image_bytes = io.BytesIO()
                img.save(image_bytes, format='JPEG')
                bytes_val = image_bytes.getvalue()
                image = {
                    '_id': images,
                    'data': bytes_val
                }
                try:
                    self._collection.insert_one(image)
                except:
                    continue
            print('Saved all images in Database')
        except Exception as e:
            print(e)

    def show(self):
        try:
            for i in self._collection.find():
                print(i['_id'])
                pil_img = Image.open(io.BytesIO(i['data']))
                plt.imshow(pil_img)
                plt.show()
                plt.close()
        except Exception as e:
            print(e)

