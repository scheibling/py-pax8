"""
This is some module information

.. include:: ../../README.md
"""
from abc import abstractmethod, ABC
from typing import List
from .rest import RestClient
from . import types as t
from . import filters as fi

# pylint: disable=abstract-class-instantiated,too-few-public-methods
class Pax8Client:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        cache_token: bool = True,
        cache_location: str = "~/pax8_token.json",
    ):
        self.conn = RestClient(client_id, client_secret, cache_token, cache_location)

        self.Company = self.CompanyClient(self.conn)
        self.Invoice = self.InvoiceClient(self.conn)
        self.Product = self.ProductClient(self.conn)
        self.Order = self.OrderClient(self.conn)
        self.Subscription = self.SubscriptionClient(self.conn)
        self.UsageSummary = self.UsageSummaryClient(self.conn)

    # pylint: disable=unused-private-member
    class ResourceClient(ABC):
        conn: RestClient
        resource: type = t.Pax8Resource

        def __init__(self, conn):
            self.conn = conn

        @abstractmethod
        def list(self, filter: fi.ListFilter = fi.ListFilter) -> List[t.Pax8Resource]:
            return [
                self.resource.objectify(item)
                for item in self.conn.list_resource(
                    self.resource.RESOURCE, filter.get_qs()
                )
            ]

        @abstractmethod
        def get(self, id: str) -> t.Pax8Resource:
            return self.resource.objectify(
                self.conn.get_resource(self.resource.RESOURCE, id)
            )

        def _list_nested(
            self, id: str, resource: type, filter: fi.ListFilter = fi.ListFilter
        ):
            return [
                resource.objectify(item)
                for item in self.conn.list_nested_resource(
                    self.resource.RESOURCE, id, resource.RESOURCE, filter.get_qs()
                )
            ]

        def _get_nested(self, id: str, resource: type, resource_id: str):
            return resource.objectify(
                self.conn.get_nested_resource(
                    self.resource.RESOURCE, id, resource.RESOURCE, resource_id
                )
            )

    class CompanyClient(ResourceClient):
        resource: type = t.Company

        def list(self, filter: fi.CompanyFilter = fi.CompanyFilter) -> List[t.Company]:
            return super().list(filter)

        def get(self, id: str) -> t.Company:
            return super().get(id)

        def get_ms_tenant_id(self, id: str) -> t.CompanyMSTenantID:
            return t.CompanyMSTenantID.objectify(self.conn.get_tenant_id(id))

        def list_contacts(
            self, id: str, filter: fi.ContactFilter = fi.ContactFilter
        ) -> List[t.Contact]:
            return super()._list_nested(id, t.Contact, filter)

        def get_contact(self, id: str, contact_id: str) -> t.Contact:
            return super()._get_nested(id, t.Contact, contact_id)

    class ProductClient(ResourceClient):
        resource: type = t.Product

        def list(self, filter: fi.ProductFilter = fi.ProductFilter) -> List[t.Product]:
            return super().list(filter)

        def get(self, id: str) -> t.Product:
            return super().get(id)

        def list_provisioning_details(self, id: str) -> List[t.ProvisioningDetail]:
            return super()._list_nested(id, t.ProvisioningDetail)

        def list_dependencies(self, id: str) -> t.Dependencies:
            return t.Dependencies.objectify(
                self.conn.list_nested_resource(
                    "products", id, "dependencies", content_only=False
                )
            )

        def list_pricing(self, id: str) -> List[t.ProductPricing]:
            return super()._list_nested(id, t.ProductPricing)

    class OrderClient(ResourceClient):
        resource: type = t.Order

        def list(self, filter: fi.OrderFilter = fi.OrderFilter) -> List[t.Order]:
            return super().list(filter)

        def get(self, id: str) -> t.Order:
            return super().get(id)

    class SubscriptionClient(ResourceClient):
        resource: type = t.Subscription

        def list(
            self, filter: fi.SubscriptionFilter = fi.SubscriptionFilter
        ) -> List[t.Subscription]:
            return super().list(filter)

        def get(self, id: str) -> t.Subscription:
            return super().get(id)

        def get_history(self, id: str) -> t.SubscriptionHistory:
            return t.SubscriptionHistory.objectify(
                self.conn.list_nested_resource(
                    "subscriptions", id, "history", content_only=False
                )
            )

        def list_usage_summaries(self, id: str) -> List[t.UsageSummary]:
            return super()._list_nested(id, t.UsageSummary)

    class InvoiceClient(ResourceClient):
        resource: type = t.Invoice

        def list(self, filter: fi.InvoiceFilter = fi.InvoiceFilter) -> List[t.Invoice]:
            return super().list(filter)

        def get(self, id: str) -> t.Invoice:
            return super().get(id)

        def list_items(
            self, id: str, filter: fi.InvoiceItemFilter = fi.InvoiceItemFilter
        ):
            return super()._list_nested(id, t.InvoiceItem, filter)

    class UsageSummaryClient(ResourceClient):
        resource: type = t.UsageSummary

        def list(self, *args, **kwargs) -> None:
            pass

        def list_for_subscription(
            self,
            subscription_id: str,
            filter: fi.UsageSummaryFilter = fi.UsageSummaryFilter,
        ) -> List[t.UsageSummary]:
            return [
                self.resource.objectify(item)
                for item in self.conn.list_nested_resource(
                    "subscriptions", subscription_id, "usage_summaries", filter.get_qs()
                )
            ]

        def get(self, id: str) -> t.UsageSummary:
            return super().get(id)

        def list_usage_lines(
            self, id: str, filter: fi.UsageSummaryLineFilter = fi.UsageSummaryLineFilter
        ) -> List[t.UsageSummaryLine]:
            return super()._get_nested(id, t.UsageSummaryLine, filter)
