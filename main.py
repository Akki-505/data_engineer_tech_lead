import os
import json
import boto3
import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient
from sqlalchemy import create_engine

load_dotenv()


class StudentRecords:

    def __init__(self):
        self.teachers = None
        self.students = None
        self.table = 'students'
        self.collection = 'teachers'
        self.db = os.environ.get('database', 'singlestone')
        self.mongo_port = os.environ.get('mongo_port', '27017')
        self.password = os.environ.get('password', 'singlestone')
        self.username = os.environ.get('username', 'singlestone')
        self.mongo_host = os.environ.get('mongo_host', 'localhost')
        self.postgres_port = os.environ.get('postgres_port ', '5432')
        self.postgres_host = os.environ.get('postgres_host', 'localhost')

    def _connect_mongo(self, host, port, username, password, db):
        """ A util for making a connection to mongo """
        if username and password:
            mongo_uri = f'mongodb://{username}:{password}@{host}:{port}/{db}?authSource=admin'
            conn = MongoClient(mongo_uri)
        else:
            conn = MongoClient(host, port)

        return conn[db]

    def _connect_postgres(self, host, port, username, password, db):
        """ A util for making a connection to mongo """
        conn_string = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db}"
        engine = create_engine(conn_string)
        return engine

    def data_processing(self, teachers, students):
        output = []
        for tkey, each_teacher in teachers.iterrows():
            print(each_teacher)
            student_data = []
            for skey, student in students[students['cid'] == each_teacher['cid']].iterrows():
                student_data.append({
                    'student_id': student['id'],
                    'student_name': student['fname'] + ' ' + student['lname'],
                    'ssn': student['ssn'],
                    'address': student['address'],
                    'email': student['email']    
                })
            output.append({
                'teacher_id': each_teacher['id'],
                'teacher_name': each_teacher['fname'] + ' ' + each_teacher['lname'],
                'class_id': each_teacher['cid'],
                'students': student_data
            })

        try:
            s3 = boto3.client('s3', region_name=os.getenv('AWS_REGION_NAME'),
                                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
                                )
            s3.put_object(Body=str(json.dumps(output)), Bucket=os.getenv('BUCKET_NAME'), Key='output.json')
            print('json file uploaded successfully')

        except Exception as e:
            print('Unable to create and upload json file\n', e)

    def read_mongo(self, db, collection, host='localhost', port=8081, username=None, password=None, no_id=True):
        """ Read from Mongo and Store into DataFrame """

        db = self._connect_mongo(host=host, port=port, username=username, password=password, db=db)
        cursor = db[collection].find()
        data = list(cursor)
        data = data[0]
        if no_id:
            del data['_id']

        for i in data:
            data[i] = list(data[i].values())
        df = pd.DataFrame.from_dict(data) 
        return df

    def read_postgres(self, db, table, host='localhost', port=8080, username=None, password=None):

        db = self._connect_postgres(host=host, port=port, username=username, password=password, db=db)
        df = pd.read_sql(f'select * from "{table}"', db)
        return df

    def parse_files(self) -> any:
        print('Processing...')
        students = self.read_postgres(self.db, self.table, host=self.postgres_host, port=self.postgres_port, username=self.username, password=self.password)
        teachers = self.read_mongo(self.db, self.collection, host=self.mongo_host, port=self.mongo_port, username=self.username, password=self.password)

        self.data_processing(teachers, students)


if __name__ == "__main__":
    record = StudentRecords()
    record.parse_files()

