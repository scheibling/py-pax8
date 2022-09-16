import requests
from datetime import datetime, timedelta
from .types import *
from .exceptions import UnexpectedResponseException
from typing import List


class Pax8RestClient:
    def __init__(self, client_id: str, client_secret: str, cache_token: bool = True, cache_location: str = '/tmp/pax8_token'):
        self.__id = client_id
        self.__secret = client_secret
        self.__token = None
        self.__expiry = None
        self.__baseurl = "https://api.pax8.com/v1/"
        self.__appurl = "https://app.pax8.com/p8p/api/v3"
        self.__default_headers = {}
        self.connected = False

        ## Todo: IMPLEMENT CACHE_TOKEN TO DISK LOCATION

    def __str__(self):
        return "Pax8Connection (Active)" if self.is_connected() else "Pax8Connection (Inactive)"
    
    def renew_token(self, force=False):
        if self.is_connected() and not force:
            return
        
        body = {
            "client_id": self.__id,
            "client_secret": self.__secret,
            "audience": "api://p8p.client",
            "grant_type": "client_credentials"
        }
        
        req = requests.post("https://login.pax8.com/oauth/token", json=body)
        if req.status_code == 200:
            req = req.json()
            self.__token = f"{req['token_type']} {req['access_token']}"
            self.__expiry = (datetime.now() + timedelta(seconds=req['expires_in'])).timestamp()
            self.connected = True
            return
        
        raise Exception(f"Failed to get tokens from Pax8: {req.status_code} {req.reason} {req.text}")
    
    def is_connected(self): return self.connected and self.__expiry > datetime.now().timestamp()
    
    def get_request(self, uri: str, qs: dict = {}) -> None:
        req = requests.get(f"{uri}", headers = self.__default_headers, params=qs)
        if req.status_code != ResponseType.OK.value:
            raise UnexpectedResponseException(f"Failed to get companies from Pax8: {ResponseType(req.status_code)} {req.text}")
        return req
    
    def list_resource(self, type: str, qs: dict, content_only: bool = True):
        res = self.get_request(f"{self.__baseurl}{type}", qs).json()
        return res if not content_only else res['content']
    
    def list_nested_resource(self, parent_type: str, parent_id: str, child_type: str, qs: dict = {}, content_only: bool = True):
        res = self.get_request(f"{self.__baseurl}{parent_type}/{parent_id}/{child_type}", qs).json()
        return res if not content_only else res['content']

    def get_resource(self, type: str, id: str): return self.get_request(f"{self.__baseurl}{type}/{id}").json()
    def get_nested_resource(self, parent_type: str, parent_id: str, child_type: str, child_id: str): return self.get_request(f"{self.__baseurl}{parent_type}/{parent_id}/{child_type}/{child_id}").json()

    def list_companies(self, filter: CompanyFilter = CompanyFilter) -> List[Company]: return [Company.objectify(x) for x in self.list_resource('companies', filter.get_qs())]
    def list_products(self, filter: ProductFilter = ProductFilter) -> List[Product]: return [Product.objectify(x) for x in self.list_resource('products', filter.get_qs())]
    def list_provisioning_details(self, product_id: str) -> List[ProvisioningDetail]: return [ProvisioningDetail.objectify(x) for x in self.list_nested_resource('products', product_id, 'provision-details')]
    def list_dependencies(self, product_id: str) -> Dependencies: return Dependencies.objectify(self.list_nested_resource('products', product_id, 'dependencies', content_only=False))
        
    
    
    
    def get_company(self, id: str) -> Company:
        return self.get_rsource('companies', id)
    
    
    
    def get_product(self, id: str) -> Product:
        pass

    def get_contact(self, id: str) -> Contact:
        pass

    # def get_company(self, id: str) -> Company:
    #     return Company.objectify(self.get_resource('companies', id))
    
    def create_company(self, company: Company, contacts: List[Contact] = None) -> None:
        pass