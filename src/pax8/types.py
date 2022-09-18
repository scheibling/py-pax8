from dataclasses import dataclass
from enum import Enum, EnumMeta
import json
from typing import List
from datetime import datetime
from datetime import date
from . import enums as en


@dataclass
class Pax8Resource:
    IGNORE_EMPTY = []
    NESTED_TYPES = {}
    RESOURCE = None

    class JsonDecoder(json.JSONDecoder):
        pass

    class JsonEncoder(json.JSONEncoder):
        pass

    @classmethod
    def objectify(cls, jdict: dict) -> "Pax8Resource":
        for key, typ in cls.NESTED_TYPES.items():
            if key in jdict and jdict[key] is not None:
                if isinstance(typ, type) and issubclass(typ, Pax8Resource):
                    jdict[key] = typ(**jdict[key])
                elif isinstance(typ, EnumMeta):
                    jdict[key] = typ(jdict[key])
                elif typ.__name__ == "List" and issubclass(
                    typ.__args__[0], Pax8Resource
                ):
                    jdict[key] = [typ.__args__[0](**item) for item in jdict[key]]

        return cls(**jdict)

    @classmethod
    def deserialize(cls, jstr: str) -> "Pax8Resource":
        jsdata = json.loads(jstr, cls=cls.JsonDecoder)
        return cls.objectify(jsdata)

    def __iter__(self) -> str:
        self_dict = self.__dict__
        for key in getattr(self, "IGNORE_EMPTY", []):
            if self_dict.get(key, False) is None:
                del self_dict[key]

        for key, value in self_dict.items():
            if isinstance(value, Pax8Resource):
                self_dict[key] = value.serialize()
            if isinstance(value, Enum):
                self_dict[key] = value.value

        yield from self_dict.items()

    def serialize(self) -> str:
        return json.dumps(dict(self), cls=self.JsonEncoder, sort_keys=True)


@dataclass
class Pax8Page(Pax8Resource):
    size: int
    totalElements: int
    totalPages: int
    number: int


@dataclass
class CompanyAddress(Pax8Resource):
    IGNORE_EMPTY = ["street2", "stateOrProvince"]
    street: str
    city: str
    postalCode: str
    country: str
    street2: str = None
    stateOrProvince: str = None


@dataclass
class Company(Pax8Resource):
    IGNORE_EMPTY = ["id", "externalId", "status"]
    NESTED_TYPES = {"address": CompanyAddress, "status": en.CompanyStatus}
    RESOURCE = "companies"
    name: str
    address: CompanyAddress
    website: str
    billOnBehalfOfEnabled: bool
    orderApprovalRequired: bool
    selfServiceAllowed: bool = None
    phone: str = None
    id: str = None
    externalId: str = None
    status: en.CompanyStatus = None


@dataclass
class CompanyMSTenantID(Pax8Resource):
    clientId: str
    tenantId: str


@dataclass
class ContactType(Pax8Resource):
    NESTED_TYPES = {"type": en.ContactTypes}
    type: en.ContactTypes
    primary: bool


@dataclass
class Contact(Pax8Resource):
    RESOURCE = "contacts"
    NESTED_TYPES = {"types": List[ContactType]}
    firstName: str
    lastName: str
    email: str
    types: List[ContactType] = None
    phone: str = None
    phoneNumber: str = None
    phoneCountryCode: str = None
    phoneCountryCallingCode: str = None
    id: str = None
    createdDate: date = None


@dataclass
class Product(Pax8Resource):
    RESOURCE = "products"
    id: str
    name: str
    vendorName: str
    shortDescription: str
    sku: str
    vendorSku: str


@dataclass
class ProvisioningDetail(Pax8Resource):
    IGNORE_EMPTY = ["description", "possibleValues", "partnerShellTemplateId"]
    NESTED_TYPES = {"type": en.ProvisioningDetailTypes}
    RESOURCE = "provision-details"
    label: str
    key: str
    valueType: en.ProvisioningDetailTypes = None
    description: str = None
    possibleValues: list = None
    partnerShellTemplateId: int = None


@dataclass
class CommitmentDependency(Pax8Resource):
    id: str
    term: str
    autoRenew: bool
    renewalWindowDaysBeforeTermEnd: int
    renewalWindowDaysAfterTermEnd: int
    allowForQuantityIncrease: int
    allowForQuantityDecrease: int
    allowForEarlyCancellation: bool
    cancellationFeeApplied: bool
    isTransferable: bool


@dataclass
class ProductDependency(Pax8Resource):
    NESTED_TYPES = {"products": Product}
    name: str
    products: List[Product]


@dataclass
class Dependencies(Pax8Resource):
    RESOURCE = "dependencies"
    NESTED_TYPES = {
        "commitmentDependencies": List[CommitmentDependency],
        "productDependencies": List[ProductDependency],
    }
    productDependencies: List[ProductDependency]
    commitmentDependencies: List[CommitmentDependency]


@dataclass
class ProductRate(Pax8Resource):
    NESTED_TYPES = {"chargeType", en.ChargeType}
    partnerBuyRate: float
    suggestedRetailPrice: float
    startQuantityRange: int = None
    endQuantityRange: int = None
    chargeType: en.ChargeType = None


@dataclass
class ProductPricing(Pax8Resource):
    RESOURCE = "pricing"
    NESTED_TYPES = {
        "billingTerm": en.BillingTerm,
        "type": en.PricingType,
        "rates": List[ProductRate],
    }
    billingTerm: en.BillingTerm
    commitmentTerm: str = None
    commitmentTermInMonths: int = None
    type: en.PricingType = None
    unitOfMeasurement: str = None
    rates: List[ProductRate] = None


@dataclass
class ProvisioningSetting(Pax8Resource):
    key: str
    value: List[str]


@dataclass
class OrderLineItem(Pax8Resource):
    NESTED_TYPES = {"provisioningDetails": List[ProvisioningDetail]}
    id: str
    productId: str
    subscriptionId: str
    provisionStartDate: datetime
    billingTerm: en.BillingTerm
    quantity: int
    commitmentTermId: str = None
    lineItemNumber: int = None
    parentSubscriptionId: str = None
    parentLineItemNumber: int = None
    provisioningDetails: List[ProvisioningDetail] = None


@dataclass
class Order(Pax8Resource):
    NESTED_TYPES = {"lineItems": List[OrderLineItem], "orderedBy": en.OrderedBy}
    RESOURCE = "orders"
    companyId: str
    createdDate: str
    lineItems: List[OrderLineItem]
    id: str = None
    orderedBy: en.OrderedBy = None
    orderedByUserId: str = None
    orderedByUserEmail: str = None

    """
    Added due to inconsistencies in Pax8 API, where creation requires "Pax8 Partner"
    and retrieval returns "Pax8Partner"
    """

    @classmethod
    def objectify(cls, jdict: dict):
        if "orderedBy" in jdict and jdict["orderedBy"] == "Pax8Partner":
            jdict["orderedBy"] = "Pax8 Partner"

        return super().objectify(jdict)


@dataclass
class CommitmentTerm(Pax8Resource):
    id: str
    term: str
    endDate: date


@dataclass
class Subscription(Pax8Resource):
    RESOURCE = "subscriptions"
    NESTED_TYPES = {
        "status": en.SubscriptionStatus,
        "billingTerm": en.BillingTerm,
        "commitment": CommitmentTerm,
    }
    companyId: str
    productId: str
    quantity: str
    startDate: date
    createdDate: date
    billingStart: date
    status: en.SubscriptionStatus
    price: int
    billingTerm: en.BillingTerm
    commitment: CommitmentTerm = None
    endDate: date = None
    updatedDate: date = None
    id: str = None

@dataclass
class SubscriptionHistory(Pax8Resource):
    RESOURCE = "history"
    NESTED_TYPES = {"content": List[Subscription]}
    content: List[Subscription]


@dataclass
class InvoiceItem(Pax8Resource):
    RESOURCE = "items"
    NESTED_TYPES = {
        "rateType": en.InvoiceItemRateTypes,
        "chargeType": en.InvoiceItemChargeTypes,
    }
    id: str
    purchaseOrderNumber: str
    type: en.InvoiceItemType
    companyId: str
    externalId: str
    companyName: str
    startPeriod: date
    endPeriod: date
    quantity: int
    unitOfMeasure: str
    term: en.InvoiceItemTerm
    sku: str
    description: str
    rateType: en.InvoiceItemRateTypes
    chargeType: en.InvoiceItemChargeTypes
    price: float
    subTotal: float
    cost: float
    costTotal: float
    offeredBy: str
    billedByPax8: bool
    total: float
    productId: str
    productName: str
    billingFee: float
    billingFeeRate: float
    amountDue: float
    currencyCode: str
    details: str = None


@dataclass
class Invoice(Pax8Resource):
    RESOURCE = "invoices"
    NESTED_TYPES = {"status": en.InvoiceStatus}
    id: str
    status: en.InvoiceStatus
    invoiceDate: date
    dueDate: date
    balance: float
    carriedBalance: float
    total: float
    partnerName: str
    companyId: str
    externalId: str


@dataclass
class UsageSummary(Pax8Resource):
    RESOURCE = "usage-summaries"
    id: str
    companyId: str
    productId: str
    resourceGroup: str
    vendorName: str
    currentCharges: float
    partnerTotal: float
    isTrial: bool


@dataclass
class UsageSummaryLine(Pax8Resource):
    RESOURCE = "usage-lines"
    usageSummaryId: str
    usageDate: date
    productName: str
    productId: str
    unitOfMeasure: str
    quantity: int
    currentCharges: float
    currentProfit: float
    partnerTotal: float
    unitPrice: float
    isTrial: bool
