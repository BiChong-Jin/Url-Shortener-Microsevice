import os
import random
import string

import redis
from flask import Flask, jsonify, redirect, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = Flask(__name__)
r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379)

shorten_counter = Counter("shorten_requests_total", "Total POST /shorten calles")
shorten_latency = Histogram(
    "shorten_latency_seconds", "Time taken for shorten requests"
)


def generate_key(length=6):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


@app.route("/shorten", methods=["POST"])
@shorten_latency.time()
def shorten():
    shorten_counter.inc()
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


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
