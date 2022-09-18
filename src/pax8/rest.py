import os
import json
from datetime import datetime, timedelta
import requests
from .exceptions import UnexpectedResponseException, UnableToCacheException
from . import enums as en

# pylint: disable=too-many-arguments
class RestClient:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        cache_token: bool = False,
        cache_location: str = "~/pax8_token.json",
        cache_encoding: str = 'utf-8'
    ):
        self.__id = client_id
        self.__secret = client_secret
        self.__token = None
        self.__expiry = None
        self.__baseurl = "https://api.pax8.com/v1/"
        self.__appurl = "https://app.pax8.com/p8p/api/v3/"
        self.__default_headers = {}

        self.cache_token = cache_token
        self.cache_location = cache_location
        self.cache_encoding = cache_encoding

        self.renew_token(force=False)

    def __str__(self):
        return (
            "Pax8Connection (Active)"
            if self.is_connected()
            else "Pax8Connection (Inactive)"
        )

    def renew_token(self, force: bool = False):
        if self.is_connected() and not force:
            return

        if self.cache_token and os.path.isfile(self.cache_location):
            with open(self.cache_location, "r", encoding=self.cache_encoding) as f:
                try:
                    cached = json.load(f)
                except json.JSONDecodeError:
                    cached = {}

            self.__token = cached.get("token", None)
            self.__expiry = cached.get("expiry", None)
            self.__default_headers = cached.get("default_headers", None)

            if self.is_connected():
                return

        body = {
            "client_id": self.__id,
            "client_secret": self.__secret,
            "audience": "api://p8p.client",
            "grant_type": "client_credentials",
        }

        req = requests.post("https://login.pax8.com/oauth/token", json=body, timeout=30)
        if req.status_code == 200:
            req = req.json()
            self.__token = f"{req['token_type']} {req['access_token']}"
            self.__expiry = (
                datetime.now() + timedelta(seconds=req["expires_in"])
            ).timestamp()
            self.__default_headers = {
                "Authorization": self.__token,
            }
            self.connected = True

            if self.cache_token:
                if not os.path.isfile(self.cache_location):
                    if cache_location[:1] == "~":
                        cache_location = os.path.expanduser(self.cache_location)
                    os.makedirs(os.path.dirname(self.cache_location), exist_ok=True)

                try:
                    with open(self.cache_location, "w+", encoding=self.cache_encoding) as f:
                        json.dump(
                            {
                                "token": self.__token,
                                "expiry": self.__expiry,
                                "default_headers": self.__default_headers,
                            },
                            f,
                        )
                except FileNotFoundError as e:
                    raise UnableToCacheException(f"Unable to cache token: {e}") from e
            return

        raise Exception(
            f"Failed to get tokens from Pax8: {req.status_code} {req.reason} {req.text}"
        )

    def is_connected(self):
        return (
            None not in [self.__token, self.__expiry, self.__default_headers]
            and self.__expiry > datetime.now().timestamp()
        )

    def get_request(self, uri: str, qs: dict = None) -> None:
        req = requests.get(f"{uri}", headers=self.__default_headers, params=qs, timeout=30)
        if req.status_code != en.ResponseType.OK.value:
            raise UnexpectedResponseException(
                f"Failed to get companies from Pax8: {en.ResponseType(req.status_code)} {req.text}"
            )
        return req

    def list_resource(self, type: str, qs: dict = None, content_only: bool = True):
        res = self.get_request(f"{self.__baseurl}{type}", qs=qs).json()
        return res if not content_only else res.get("content", [])

    # pylint: disable=dangerous-default-value
    def list_nested_resource(
        self,
        parent_type: str,
        parent_id: str,
        child_type: str,
        qs: dict = None,
        content_only: bool = True,
    ):
        res = self.get_request(
            f"{self.__baseurl}{parent_type}/{parent_id}/{child_type}", qs=qs
        ).json()
        return res if not content_only else res.get("content", [])

    def get_resource(self, type: str, id: str):
        return self.get_request(f"{self.__baseurl}{type}/{id}").json()

    def get_nested_resource(
        self, parent_type: str, parent_id: str, child_type: str, child_id: str
    ):
        return self.get_request(
            f"{self.__baseurl}{parent_type}/{parent_id}/{child_type}/{child_id}"
        ).json()

    def get_tenant_id(self, client_id: str) -> dict:
        return {
            "clientId": client_id,
            **self.get_request(
                f"{self.__appurl}companies/{client_id}/msTenantId"
            ).json(),
        }
