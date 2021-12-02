### Application Overview 
This application reads the data from two data stores i.e. PostgreSQL (student data) and MongoDB (teacher data) and process them to generate a json output. The output json consists the list of teachers with their respective students mapped by class_id.

Application loads the output json file to AWS S3 File storage.

Also the code is written by considering an optimal tradeoff between the space and time complexity of the code and the optimal performance of the multiple approaches to perform the task.
 
 
### Modules used 
- os         : to access files from local directory
- json       : to output a proper json formatted data
- pandas     : for processing csv and parquet files
- boto3      : for accessing S3 bucket files and exception handling corresponding to S3 functionalities
- dotenv     : to load environment variables from .env file
- pymongo    : to connect python application with Mongo Db database.
- sqlalchemy : to connect python application with Postgres Db.

### Application setup
Assuming Postgres Db and Mongo Db are already being running using docker containers, if not start the databases first using docker-compose from problem statement.


##### Clone repository
```git
git clone <url>
```

##### Create .env file
```
touch .env
```
set environment variables in .env i.e. 
- AWS_SECRET_ACCESS_KEY=""
- AWS_ACCESS_KEY_ID=""
- AWS_REGION_NAME=""
- BUCKET_NAME=""
- DATABASE=""
- MONGO_PORT=""
- PASSWORD=""
- USERNAME=""
- MONGO_HOST=""
- POSTGRES_HOST=""
- POSTGRES_PORT=""
##### Create virtual environment 
```bash
virtualenv -p python3 env
```
 
##### Activate environment 
```bash
source env/bin/activate
```

##### Install requirements
```bash
pip install -r requirements.txt
``` 

##### Command to run app
```python
python src/main.py
```

### Docker commands 
```dockerfile
$ docker build -t my-app .
$ docker run -it --rm --name my-running-app my-app
```