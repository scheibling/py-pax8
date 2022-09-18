"""
This is some module information

.. include:: ../../README.md
"""
from typing import List
from .rest import RestClient
from . import types as t
from . import filters as fi

class Pax8Client:
    def __init__(self, client_id: str, client_secret: str, cache_token: bool = True, cache_location: str = "~/pax8_token.json"):
        self.conn = RestClient(client_id, client_secret, cache_token, cache_location)
        
        self.Company = self.CompanyClient(self.conn)
        self.Contact = self.ContactClient(self.conn)
        self.Invoice = self.InvoiceClient(self.conn)
        self.Product = self.ProductClient(self.conn)
        self.Order = self.OrderClient(self.conn)
        self.Subscription = self.SubscriptionClient(self.conn)
        self.UsageSummary = self.UsageSummaryClient(self.conn)
                
        

    class ResourceClient:
        conn: RestClient

        def __init__(self, conn):
            self.conn = conn    
    
    class CompanyClient(ResourceClient):
        def list(self, filter: fi.CompanyFilter = fi.CompanyFilter):
            return [t.Company.objectify(x) for x in self.conn.list_resource('companies', filter.get_qs())]
        
        def get(self, id: str):
            return t.Company.objectify(self.conn.get_resource('companies', id))
        
        def get_ms_tenant_id(self, id: str):
            return t.CompanyMSTenantID.objectify(self.conn.get_tenant_id(id))            
        
        def list_contacts(self, id: str, filter: fi.ContactFilter = fi.ContactFilter):
            return [t.Contact.objectify(x) for x in self.conn.list_nested_resource('companies', id, 'contacts', filter.get_qs())]
    
        def get_contact(self, id: str, contact_id: str):
            return t.Contact.objectify(self.conn.get_nested_resource('companies', id, 'contacts', contact_id))
    
    class ProductClient(ResourceClient):
        def list(self, filter: fi.ProductFilter = fi.ProductFilter):
            return [t.Product.objectify(x) for x in self.conn.list_resource('products', filter.get_qs())]
        
        def get(self, id: str):
            return t.Product.objectify(self.conn.get_resource('products', id))
        
        def list_provisioning_details(self, id: str):
            return [t.ProvisioningDetail.objectify(x) for x in self.conn.list_nested_resource('products', id, 'provision-details')] 
        
        def list_dependencies(self, id: str):
            return t.Dependencies.objectify(self.conn.list_nested_resource('products', id, 'dependencies', content_only=False))

        def list_pricing(self, id: str):
            return [t.ProductPricing.objectify(x) for x in self.conn.list_nested_resource('products', id, 'pricing')]    
    
    class OrderClient(ResourceClient):
        def list(self, filter: fi.OrderFilter = fi.OrderFilter):
            return [t.Order.objectify(x) for x in self.conn.list_resource('orders', filter.get_qs())]
        
        def get(self, id: str):
            return t.Order.objectify(self.conn.get_resource('orders', id))

    class SubscriptionClient(ResourceClient):
        def list(self, filter: fi.SubscriptionFilter = fi.SubscriptionFilter):
            return [t.Subscription.objectify(x) for x in self.conn.list_resource('subscriptions', filter.get_qs())]

        def get(self, id: str):
            return t.Subscription.objectify(self.conn.get_resource('subscriptions', id))
        
        def get_history(self, id: str):
            return [t.Subscription.objectify(x) for x in self.conn.list_nested_resource('subscriptions', id, 'history')]
            
    class InvoiceClient(ResourceClient):
        def list(self, filter: fi.InvoiceFilter = fi.InvoiceFilter):
            return [t.Invoice.objectify(x) for x in self.conn.list_resource('invoices', filter.get_qs())]
    
        def get(self, id: str):
            return t.Invoice.objectify(self.conn.get_resource('invoices', id))
        
        def list_items(self, id: str, filter: fi.InvoiceItemFilter = fi.InvoiceItemFilter):
            return [t.InvoiceItem.objectify(x) for x in self.conn.list_nested_resource('invoices', id, 'items', filter.get_qs())]

    class UsageSummaryClient(ResourceClient):
        def list(self, subscription_id: str, filter: fi.UsageSummaryFilter = fi.UsageSummaryFilter):
            return [t.UsageSummary.objectify(x) for x in self.conn.list_nested_resource('subscriptions', subscription_id, 'usage-summaries', filter.get_qs())]
    
        def get(self, summary_id: str):
            return t.UsageSummary.objectify(self.conn.get_resource('usage-summaries', id))
        
        def usage_lines(self, summary_id: str, filter: fi.UsageSummaryLineFilter = fi.UsageSummaryLineFilter):
            return [t.UsageSummaryLine.objectify(x) for x in self.conn.list_nested_resource('usage-summaries', summary_id, 'usage-lines', filter.get_qs())]
