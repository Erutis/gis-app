from sanic import Sanic
from sanic.response import json

app = Sanic("my-hello-world-app")


@app.route("/")
async def get(request):
    return json({"hello": "turd"})


if __name__ == "__main__":
    app.run()
