from time import sleep
from json import dumps
from kafka import KafkaProducer
from random import randrange,choices
import string
from decimal import Decimal
from random import randint
from datetime import datetime 
from confluent_kafka import Producer


producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))


def push():
    id = 1
    for e in range(1000):
        user_id = randint(1, 10)
        amount = str(str(randint(1, 2000)) + '.' + str(randint(0, 99)))
        time = datetime.now().timestamp()
        transaction = {
            "transaction_id": id, 
            "user_id": user_id, 
            "amount": amount, 
            "timestamp": int(time), 
            "location": "New York"
        }
        producer.send('transactions', value=transaction)
        print(transaction)
        sleep(randrange(3))
        print("produced message ", e)
        id += 1

try:
    while True:
        push()
except KeyboardInterrupt:
    producer.close()
    print("exit")