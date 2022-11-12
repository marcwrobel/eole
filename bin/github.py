import os
from datetime import datetime

import requests
from core import Version


class GitHubApiException(Exception):
    def __init__(self, url, status, message, *args: object) -> None:
        super().__init__(*args)
        self.url = url
        self.status = status
        self.message = message

    def __str__(self) -> str:
        return (
            f"Call to {self.url} returned a "
            f"{self.status} HTTP code: {self.message}"
        )


class GitHubProject:
    def __init__(self, spec):
        self.spec = spec

    def owner(self) -> str:
        return self.spec["owner"]

    def repo(self) -> str:
        return self.spec["repo"]

    def web_url(self) -> str:
        return f"https://github.com/{self.owner()}/{self.repo()}"

    def api_url(self) -> str:
        return f"https://api.github.com/repos/{self.owner()}/{self.repo()}"

    # https://docs.github.com/en/rest/releases/releases#list-releases
    def releases(self) -> []:
        url = f"{self.api_url()}/releases?per_page=100&page="

        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "Éole",
        }
        if "GITHUB_API_TOKEN" in os.environ:
            token = os.environ.get("GITHUB_API_TOKEN")
            headers["Authorization"] = f"token {token}"

        page = 1
        may_have_more_pages = True
        result = []
        while may_have_more_pages:
            response = requests.get(url + str(page), headers=headers)
            if response.status_code != 200:
                raise GitHubApiException(
                    url, response.status_code, response.text
                )

            releases = list(response.json())
            result.extend(
                list(
                    map(
                        lambda r: Version(
                            r["name"], self.__to_date(r["published_at"])
                        ),
                        filter(
                            lambda r: not (r["draft"])
                            and not (r["prerelease"]),
                            releases,
                        ),
                    )
                )
            )

            page = page + 1
            may_have_more_pages = len(releases) > 0

        return result

    @staticmethod
    def __to_date(s):
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").date()
