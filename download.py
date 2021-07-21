import zipfile
import io
import requests
from tqdm import tqdm


USERNAME = "vivialprt"
REPO = "currency"
BASE_URL = f"https://api.github.com/repos/{USERNAME}/{REPO}"
ALL_ARTIFACTS = f"{BASE_URL}/actions/artifacts"
with open("secret") as secret:
    TOKEN = secret.read()
PER_PAGE = 100


def download_all():
    res = requests.get(
        ALL_ARTIFACTS, params={"page": 1, "per_page": PER_PAGE}
    ).json()
    artifacts = res["artifacts"]
    count = res["total_count"]

    for page in range(2, count // PER_PAGE + 2):
        res = requests.get(
            ALL_ARTIFACTS, params={"page": page, "per_page": PER_PAGE}
        ).json()
        artifacts += res["artifacts"]

    print(len(artifacts))
    ids = [artifact["id"] for artifact in artifacts]
    assert len(ids) == len(set(ids))

    for id_ in tqdm(ids):
        archive = requests.get(
            f"{ALL_ARTIFACTS}/{id_}/zip", auth=(USERNAME, TOKEN), stream=True
        ).content
        with zipfile.ZipFile(io.BytesIO(archive)) as z:
            z.extractall()


if __name__ == "__main__":
    download_all()
