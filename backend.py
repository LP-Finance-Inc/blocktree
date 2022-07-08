from flask import *
import json, time
from blocktree import *

app = Flask(__name__)


@app.route("/blocktree", methods=["GET"])
def request_blocktree():
    args = request.args
    account = args.get("account", type=str)
    lim = args.get("lim", default=10, type=int)
    data_set = BlockTree().get_total_tx(account, lim)

    json_dump = json.dumps(data_set)
    return json_dump


@app.route("/tokens", methods=["GET"])
def request_token():
    args = request.args
    account = args.get("account", type=str)
    data_set = BlockTree().get_tokens(account)
    json_dump = json.dumps(data_set)
    return json_dump


if __name__ == "__main__":
    app.run(debug=True)
