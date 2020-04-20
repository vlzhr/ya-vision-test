import requests
from CONFIG import oatoken, catalog
from json import dumps, loads
import base64
import os


def safe_link(*args):
    return os.path.join(os.path.dirname(__file__), *args)


URL = "https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze"

token = requests.post("https://iam.api.cloud.yandex.net/iam/v1/tokens", dumps({"yandexPassportOauthToken": oatoken}))
token = loads(token.text)["iamToken"]

with open(safe_link("img", "1.png"), "rb") as f:
    content = base64.b64encode(f.read()).decode()

body = {
    "folderId": catalog,
    "analyze_specs": [{
        "content": content,
        "features": [{
            "type": "TEXT_DETECTION",
            "text_detection_config": {
                "language_codes": ["*"]
            }
        }]
    }]
}

resp = requests.post(URL, dumps(body), headers={'Authorization': 'Bearer '+token})

with open(safe_link("result.json"), "w", encoding="utf-8") as f:
    f.write(resp.text)

data = loads(resp.text)
blocks = data["results"][0]["results"][0]["textDetection"]["pages"][0]["blocks"]

items = []
for block in blocks:
    for line in block["lines"]:
        items.append(" ".join([w["text"] for w in line["words"]]))

