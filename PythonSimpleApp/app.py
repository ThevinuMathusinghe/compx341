import time
import math

import redis
from flask import Flask, make_response, jsonify


app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


def checkPrime(number):
    if(number < 2):
        return False
    if(number == 2):
        return True
    if(number % 2 == 0):
        return False
    i = 3
    to = math.sqrt(number)
    while i <= to:
        if(number % i == 0):
            return False
        i += 2
    return True


@app.route('/isPrime/<int:number>')
def isPrime(number):

    result = checkPrime(number)
    if(result == True):
        # Stores the number in a list
        cache.lpush('PrimeNumber_List', number)
        return '{}'.format(number) + " is prime\n"
    else:
        return '{}'.format(number) + " is not prime\n"


@app.route('/primeStored')
def primeStored():
    try:
        value = cache.lrange("PrimeNumber_List", 0, -1)
        returnList = []
        for index, v in enumerate(value):
            returnList.append(int(v))
        return make_response(jsonify({"PrimeNumber List": returnList}))
    except Exception as ex:
        return "error {".format(ex)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

