import os
import slack
from datetime import datetime

WFH_MSG = os.environ.get("WFH_MSG", "wfh")
USER_ID = os.environ.get("USER_ID")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
API_TOKEN = os.environ.get("API_TOKEN")


def get_ts():
    dt = datetime.combine(datetime.today(), datetime.min.time())
    epoch = datetime.fromtimestamp(0)
    return (dt - epoch).total_seconds()


def get_dt(ts):
    try:
        return datetime.fromtimestamp(float(ts))
    except:
        return "N/A"


def post_msg(client):
    return client.chat_postMessage(channel=CHANNEL_ID, as_user=True, text=WFH_MSG)


def find_todays_msg(client):
    ts = str(get_ts())
    response = client.conversations_history(channel=CHANNEL_ID, oldest=ts)
    if response["messages"]:
        for msg in response["messages"]:
            if msg["user"] == USER_ID and msg.get("text", "").lower() == WFH_MSG:
                return msg
    return None


def main():
    client = slack.WebClient(token=API_TOKEN)
    found_msg = find_todays_msg(client)
    if found_msg:
        print(
            "Message is already present (msg: %s, dt: %s)"
            % (found_msg["text"], get_dt(found_msg["ts"]))
        )
    else:
        result = post_msg(client)
        if result["ok"]:
            print("Post following msg to slack: %s" % WFH_MSG)
        else:
            print(result)


if __name__ == "__main__":
    today = datetime.today()
    if today.isoweekday() in range(1, 6) and today.hour in range(9, 13):
        main()
