from dataclasses import dataclass
from enum import Enum, EnumMeta
import json
from this import d
from typing import List, Dict
from datetime import datetime
from datetime import date

class ResponseType(Enum):
    OK=200
    BAD_REQUEST=400
    UNAUTHORIZED=401
    FORBIDDEN=403
    NOT_FOUND=404
    UNPROCESSABLE_ENTITY=422
    TOO_MANY_REQUESTS=429
    INTERNAL_SERVER_ERROR=500
    NOT_IMPLEMENTED=501
    BAD_GATEWAY=502
    SERVICE_UNAVAILABLE=503
    GATEWAY_TIMEOUT=504
    VERSION_NOT_SUPPORTED=505
    VARIANT_ALSO_NEGOTIATES=506
    INSUFFICIENT_STORAGE=507

@dataclass
class Pax8Resource:
    IGNORE_EMPTY=[]
    NESTED_TYPES={}
    GET_NAME=None
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
                elif typ.__name__ == 'List' and issubclass(typ.__args__[0], Pax8Resource):
                    jdict[key] = [typ.__args__[0](**item) for item in jdict[key]]
                    
        return cls(**jdict)
    
    @classmethod
    def deserialize(cls, jstr: str) -> "Pax8Resource":
        jsdata = json.loads(jstr, cls=cls.JsonDecoder)
        return cls.objectify(jsdata)

    def __iter__(self) -> str:
        self_dict = self.__dict__
        for key in getattr(self, "IGNORE_EMPTY", []) + getattr(self, "IGNORE_EMPTY_ALWAYS", []):
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

class SortBy(Enum):
    pass

class SortDirection(Enum):
    ASCENDING='asc'
    DESCENDING='desc'

class CompanyStatus(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    DELETED = "Deleted"

@dataclass
class CompanyAddress(Pax8Resource):
    IGNORE_EMPTY = ['street2', 'stateOrProvince']
    street: str
    city: str
    postalCode: str
    country: str
    street2: str = None
    stateOrProvince: str = None

class CompanySortBy(SortBy):
    NAME='name'
    CITY='city'
    COUNTRY='country'
    STATE_OR_PROVINCE='stateOrProvince'
    POSTAL_CODE='postalCode'

@dataclass
class ListFilter(Pax8Resource):
    IGNORE_EMPTY_ALWAYS = ['page', 'size', 'sort', 'sort_direction']
    page: int = None
    size: int = None
    sort: SortBy = None
    sort_direction: SortDirection = None
    
    def __post_init__(self):
        self.get_qs = self.__get_qs
    
    @staticmethod
    def get_qs(*args, **kwargs) -> dict:
        return {}
    
    def __get_qs(self) -> dict:
        return dict(self)

@dataclass
class CompanyFilter(ListFilter):
    IGNORE_EMPTY = ['city', 'country', 'stateOrProvince', 'postalCode', 'selfServiceAllowed', 'billOnBehalfOfEnabled', 'orderApprovalRequired', 'status']
    sort: CompanySortBy = None
    city: str = None
    country: str = None
    stateOrProvince: str = None
    postalCode: str = None
    selfServiceAllowed: bool = None
    billOnBehalfOfEnabled: bool = None
    orderApprovalRequired: bool = None
    status: CompanyStatus = None

@dataclass
class Company(Pax8Resource):
    IGNORE_EMPTY = ['id', 'externalId', 'status']
    NESTED_TYPES = {'address': CompanyAddress, 'status': CompanyStatus}
    name: str
    address: CompanyAddress
    website: str
    billOnBehalfOfEnabled: bool
    orderApprovalRequired: bool
    selfServiceAllowed: bool = None
    phone: str = None
    id: str = None
    externalId: str = None
    status: CompanyStatus = None

class ProductSortBy(Enum):
    NAME = "name"
    VENDOR = "vendor"

@dataclass
class ProductFilter(ListFilter):
    IGNORE_EMPTY = ['vendorName']
    sort: ProductSortBy = None
    vendorName: str = None

@dataclass
class Product(Pax8Resource):
    id: str
    name: str
    vendorName: str
    shortDescription: str
    sku: str
    vendorSku: str

class ProvisioningDetailTypes(Enum):
    MULTIPLE_CHOICE = 1
    INPUT = 2

@dataclass
class ProvisioningDetail(Pax8Resource):
    IGNORE_EMPTY = ['description', 'possibleValues', 'partnerShellTemplateId']
    NESTED_TYPES = {'type': ProvisioningDetailTypes}
    label: str
    key: str
    valueType: ProvisioningDetailTypes
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
    NESTED_TYPES = {'products': Product}
    name: str
    products: List[Product]

@dataclass
class Dependencies(Pax8Resource):
    NESTED_TYPES = {'commitmentDependencies': List[CommitmentDependency], 'productDependencies': List[ProductDependency]}
    productDependencies: List[ProductDependency]
    commitmentDependencies: List[CommitmentDependency]

class BillingTerm(Enum):
    MONTHLY = "Monthly"
    ANNUAL = "Annual"
    TWO_YEAR = "2-Year"
    THREE_YEAR = "3-Year"
    ONE_TIME = "One-Time"
    TRIAL = "Trial"
    ACTIVATION = "Activation"

class PricingType(Enum):
    FLAT = "Flat"
    VOLUME = "Volume"
    TIERED = "Tiered"
    MARK_UP = "Mark-Up" 

class ChargeType(Enum):
    PER_UNIT = "per_unit"
    FLAT_RATE = "flat_rate"

@dataclass
class ProductRate(Pax8Resource):
    partnerBuyRate: float
    suggestedRetailPrice: float
    startQuantityRange: int
    endQuantityRange: int
    chargeType: ChargeType 

@dataclass
class ProductPricing(Pax8Resource):
    billingTerm: BillingTerm
    type: PricingType
    unitOfMeasurement: str
    rates: List[ProductRate]

class OrderedBy(Enum):
    PAX8_PARTNER = "Pax8 Partner"
    CUSTOMER = "Customer"
    PAX8 = "Pax8"

@dataclass
class ProvisioningSetting(Pax8Resource):
    key: str
    value: List[str]

@dataclass
class OrderLineItem(Pax8Resource):
    productId: str
    subscriptionId: str
    commitmentTermId: str
    provisionStartDate: datetime
    lineItemNumber: int
    billingTerm: BillingTerm
    parentSubscriptionId: str
    parentLineItemNumber: int
    quantity: int
    provisioningDetails: List[ProvisioningDetail]

@dataclass
class Order(Pax8Resource):
    companyId: str
    createdDate: str
    lineItems: List[OrderLineItem]
    id: str = None
    orderedBy: OrderedBy = None
    orderedByUserId: str = None
    orderedByUserEmail: str = None

class SubscriptionStatus(Enum):
    ACTIVE = "Active"
    CANCELLED = "Cancelled"
    PENDING_MANUAL = "PendingManual"
    PENDING_AUTOMATED = "PendingAutomated"
    PENDING_CANCEL = "PendingCancel"
    WAITING_FOR_DETAILS = "WaitingForDetails"
    TRIAL = "Trial"
    CONVERTED = "Converted"
    PENDING_ACTIVATION = "PendingActivation"
    ACTIVATED = "Activated"

class CommitmentTerm(Pax8Resource):
    id: str
    term: str
    endDate: date

@dataclass
class Subscription(Pax8Resource):
    companyId: str
    productId: str
    quantity: str
    startDate: date
    createdDate: date
    billingStart: date
    status: SubscriptionStatus
    price: int
    billingTerm: BillingTerm
    commitmentTerm: CommitmentTerm
    id: str = None

class ContactTypes(Enum):
    BILLING = "Billing"
    ADMIN = "Admin"
    TECHNICAL = "Technical"

@dataclass
class ContactType(Pax8Resource):
    type: ContactTypes
    primary: bool
    
@dataclass
class Contact(Pax8Resource):
    firstName: str
    lastName: str
    email: str
    phone: str
    types: List[ContactType]
    id: str = None
    createdDate: date = None

class InvoiceItemType(Enum):
    REBATE = "rebate"
    PRORATE = "prorate"
    SUBSCRIPTION = "subscription"
    PAYMENT_CREDIT = "payment_credit"
    ONE_TIME = "one_time"
    SERVICE_CHARGE = "service_charge"
    SERVICE_CREDIT = "service_credit"
    INVOICE_CREDIT = "invoice_credit"

class InvoiceItemTerm(Enum):
    THREE_YEAR = "3 Year"
    ANNUAL = "Annual"
    TWO_YEAR = "2 Year"
    ACTIVATION = "Activation"
    ONE_TIME    = "One Time"
    ARREARS = "Arrears"
    TRIAL = "Trial"
    REBATE = "Rebate"
    MONTHLY = "Monthly"

class InvoiceItemRateTypes(Enum):
    MARKUP = "markup"
    FLAT = "flat"
    SINGLE = "single"
    VOLUME = "volume"
    TIERED = "tiered"

class InvoiceItemChargeTypes(Enum):
    PER_UNIT = "per_unit"
    FLAT_RATE = "flat_rate"

@dataclass
class InvoiceItem(Pax8Resource):
    id: str
    purchaseOrderNumber: str
    type: InvoiceItemType
    companyId: str
    externalId: str
    companyName: str
    startPeriod: date
    endPeriod: date
    quantity: int
    unitOfMeasure: str
    term: InvoiceItemTerm
    sku: str
    description: str
    details: str
    rateType: InvoiceItemRateTypes
    chargeType: InvoiceItemChargeTypes
    price: float
    subtotal: float
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

@dataclass
class Invoice(Pax8Resource):
    id: str
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
    id: str
    companyId: str
    productId: str
    resourceGroup: str
    vendorName: str
    currentCharges: float
    partnerTotal: float
    isTrial: bool

@dataclass
class UsageSummaryItem(Pax8Resource):
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