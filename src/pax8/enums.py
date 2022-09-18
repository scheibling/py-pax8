from enum import Enum


class ResponseType(Enum):
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    UNPROCESSABLE_ENTITY = 422
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504
    VERSION_NOT_SUPPORTED = 505
    VARIANT_ALSO_NEGOTIATES = 506
    INSUFFICIENT_STORAGE = 507


class SortBy(Enum):
    pass


class SubscriptionSortBy(SortBy):
    QUANTITY = "quantity"
    START_DATE = "startDate"
    END_DATE = "endDate"
    CREATED_DATE = "createdDate"
    BILLING_START = "billingStart"
    PRICE = "price"


class InvoiceSortBy(SortBy):
    INVOICE_DATE = "invoiceDate"
    DUE_DATE = "dueDate"
    STATUS = "status"
    PARTNER_NAME = "partnerName"
    TOTAL = "total"
    BALANCE = "balance"
    CARRIED_BALANCE = "carriedBalance"


class UsageSummarySortBy(SortBy):
    RESOURCE_GROUP = "resourceGroup"
    CURRENT_CHARGES = "currentCharges"
    PARTNER_TOTAL = "partnerTotal"


class SortDirection(Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"


class CompanyStatus(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    DELETED = "Deleted"


class CompanySortBy(SortBy):
    NAME = "name"
    CITY = "city"
    COUNTRY = "country"
    STATE_OR_PROVINCE = "stateOrProvince"
    POSTAL_CODE = "postalCode"


class ProductSortBy(Enum):
    NAME = "name"
    VENDOR = "vendor"


class ProvisioningDetailTypes(Enum):
    MULTIPLE_CHOICE = 1
    INPUT = 2


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


class OrderedBy(Enum):
    PAX8_PARTNER = "Pax8 Partner"
    CUSTOMER = "Customer"
    PAX8 = "Pax8"


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


class ContactTypes(Enum):
    BILLING = "Billing"
    ADMIN = "Admin"
    TECHNICAL = "Technical"


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
    ONE_TIME = "One Time"
    ARREARS = "Arrears"
    TRIAL = "Trial"
    REBATE = "Rebate"
    MONTHLY = "Monthly"


class InvoiceItemRateTypes(Enum):
    MARKUP = "markup"
    FLAT = "Flat"
    SINGLE = "single"
    VOLUME = "volume"
    TIERED = "tiered"


class InvoiceItemChargeTypes(Enum):
    PER_UNIT = "per"
    FLAT_RATE = "flat"


class InvoiceStatus(Enum):
    UNPAID = "Unpaid"
    PAID = "Paid"
    VOID = "Void"
    CARRIED = "Carried"
    NOTHING_DUE = "Nothing Due"
