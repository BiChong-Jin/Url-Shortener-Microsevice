import os
import random
import string

import redis
from flask import Flask, jsonify, redirect, request

app = Flask(__name__)
r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379)


def generate_key(length=6):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


@app.route("/shorten", methods=["POST"])
def shorten():
    long_url = request.json["url"]
    key = generate_key()
    r.set(key, long_url)

    return jsonify({"short_url": f"/{key}"})


@app.route("/<key>")
def redirect_url(key):
    url = r.get(key)
    if url:
        return redirect(url.decode())

    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
