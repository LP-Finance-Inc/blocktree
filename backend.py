from flask import *
import json, time
from blocktree import *
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)


@app.route("/blocktree", methods=["GET"])
def request_blocktree():
    args = request.args
    account = args.get("account", type=str)
    lim = args.get("lim", default=10, type=int)
    data_set = BlockTree().get_total_tx(account, lim)

    json_dump = json.dumps(data_set)
    return json_dump


if __name__ == "__main__":
    app.run()
