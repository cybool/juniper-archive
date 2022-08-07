# standard library
import logging

# third party
import yaml
from fastapi import FastAPI

# local
from mist import MistApi
from webhook import WebhookData, WebhookResponse


# -----------------------------------------------------------------------------
# Set up our FastAPI app
# -----------------------------------------------------------------------------
app = FastAPI(
    title="Juniper Mist Kentic Webhook Receiver",
    description="Collect Kentic webhooks and execute Mist API function",
    version="1.0",
)

APP_NAME = "webhook-listener"

# -----------------------------------------------------------------------------
# Set up local file logging
# -----------------------------------------------------------------------------
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_logging = logging.FileHandler(f"{APP_NAME}.log")
file_logging.setFormatter(formatter)
logger.addHandler(file_logging)


def log_to_file(data):
    logger.info(f"WebhookData received:\n{data}")
    # logger.info(f"EventType: {data.EventType}")


# -----------------------------------------------------------------------------
# Webhook Receiver
# -----------------------------------------------------------------------------
@app.post("/webhook/", response_model=WebhookResponse, status_code=200)
async def webhook(webhook_input: WebhookData):

    # log webhook_input to local file
    log_to_file(webhook_input)

    # load contents of our config.yaml file into an object named `mist`
    with open("config.yaml", "r", encoding="utf-8") as file:
        mist = yaml.safe_load(file)

    log_to_file(mist)

    # pass in the contents of config.yaml into an instance of MistApi
    mist_api = MistApi(**mist)

    # execute the shutdown of our interface
    shutdown = mist_api.shutdown_iface()

    # log shutdown result to local file
    log_to_file(shutdown)
    return {"result": "ok"}
