from json import dumps as jsdump_str
from datetime import date
from dataclasses import dataclass
from . import enums as pe


@dataclass
class ListFilter:
    page: int = None
    size: int = None

    def serialize(self) -> str:
        return jsdump_str(dict(self), sort_keys=True)

    def __post_init__(self):
        self.get_qs = self.__get_qs

    # pylint: disable=method-hidden
    @staticmethod
    def get_qs(*args, **kwargs) -> dict:
        return {}

    def __get_qs(self) -> dict:
        return dict(self)

    def __iter__(self) -> dict:
        self_dict = {}
        for key, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, pe.Enum):
                    value = value.value
                self_dict[key] = value

        yield from self_dict.items()


@dataclass
class CompanyFilter(ListFilter):
    sort_direction: pe.SortDirection = None
    sort: pe.CompanySortBy = None
    city: str = None
    country: str = None
    stateOrProvince: str = None
    postalCode: str = None
    selfServiceAllowed: bool = None
    billOnBehalfOfEnabled: bool = None
    orderApprovalRequired: bool = None
    status: pe.CompanyStatus = None


@dataclass
class ProductFilter(ListFilter):
    sort: pe.ProductSortBy = None
    sortDirection: pe.SortDirection = None
    vendorName: str = None


@dataclass
class OrderFilter(ListFilter):
    companyId: str = None


@dataclass
class SubscriptionFilter(ListFilter):
    sort: pe.SubscriptionSortBy = None
    sort_direction: pe.SortDirection = None
    status: pe.SubscriptionStatus = None
    billingTerm: pe.BillingTerm = None
    companyId: str = None
    productId: str = None


@dataclass
class ContactFilter(ListFilter):
    pass


@dataclass
class InvoiceFilter(ListFilter):
    sort: pe.InvoiceSortBy = None
    sort_direction: pe.SortDirection = None
    status: pe.InvoiceStatus = None
    invoiceDate: date = None
    invoiceDateRangeStart: date = None
    invoiceDateRangeEnd: date = None
    dueDate: date = None
    total: float = None
    balance: float = None
    carriedBalance: float = None
    companyId: str = None


@dataclass
class InvoiceItemFilter(ListFilter):
    pass


@dataclass
class UsageSummaryFilter(ListFilter):
    sort: pe.UsageSummarySortBy = None
    sort_direction: pe.SortDirection = None
    resourceGroup: str = None
    companyId: str = None


@dataclass
class UsageSummaryLineFilter(ListFilter):
    pass
