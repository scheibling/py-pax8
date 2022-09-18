# Pax8 Partner API Library
This is a python implementation of the Pax8 Partner API. It is still somewhat a work in progress, but is usable. Please report any errors you come along under Issues, or submit a pull request, and I'll get it fixed.

## Functionality
The following section gives an overview of the implemented functionality up to this point, and a roadmap of what's still to be implemented.
There are some differences between the API implementation and the official documentation, see the section Pax8 API Errors for more information.

### General
* Get Access Token
* Access Token Caching (To Disk)
* <strike>Access Token Caching (To Redis/Memcache)</strike> (To Do)
* <strike>Encrypted Access Token Caching</strike> (To Do)
* <strike>Automatic rate limiting</strike> (To Do)

### API Resources
Struck resources are not yet implemented. Resources marked Experimental are a part of the undocumented Pax8 API, see more information below.
* <b> ```client.Company ```</b>
    * ```.list(filter=filters.CompanyFilter)```
    * ```.get(id: uuid)```
    * <strike>```.create(company: types.Company)```</strike>
    * ```.get_ms_tenant_id(id: uuid)``` **EXPERIMENTAL**
    * ```.list_contacts(id: uuid)```
    * ```.get_contact(id: uuid, contact_id: uuid)```
    * <strike>```.create_contact(contact: types.Contact)```</strike>
    * <strike>```.update_contact(contact: types.Contact)```</strike>	
    * <strike>```.delete_contact(id: uuid, contact_id: uuid)```</strike>

* <b> ```client.Product ```</b>
    * ```.list(filter: filters.ProductFilter)```
    * ```.get(id: uuid)```
    * ```.list_provisioning_details(id: uuid)```
    * ```.list_dependencies(id: uuid)```
    * ```.list_pricing(id: uuid)```
* <b>```client.Order```</b>
    * ```.list(filter: filters.OrderFilter)```
    * ```.get(id: uuid)```
    * <strike>```.create(order: types.Order)```</strike>

* <b>```client.Subscription```</b>
    * ```.list(filter: filters.SubscriptionFilter)```
    * ```.get(id: uuid)```
    * ```.get_history(id: uuid)```
    * <strike>```.update(subscription: types.Subscription)```</strike>
    * <strike>```.delete(id: uuid)```</strike>
    * ```.list_usage_summaries(id: uuid, filter: filters.UsageSummaryFilter)```

* <b>```client.Invoice```</b>
    * ```.list(filter: filters.InvoiceFilter)```
    * ```.get(id: uuid)```
    * ```.list_items(id: uuid, filter: filters.InvoiceItemFilter)```

* <b>```client.UsageSummary```</b>
    * ```.list(subscription_id: uuid, filter: filters.UsageSummaryFilter)```
    * ```.get(id: uuid)```
    * ```.get_usage_lines(id: uuid, filter: filters.UsageSummaryLineFilter)```

### V3 API Resources (Undocumented APIs)
There are several undocumented APIs used to implement the functionality of the Pax8 Partner Portal (https://app.pax8.com) that have been implemented into this library, marked Experimental above due to their undocumented nature. These APIs are not guaranteed to be stable, and may change at any time. Use at your own risk.

If there are any undocumented APIs you would like to see implemented, please open an issue and I'll get to it as soon as I can. You can find the full list of available endpoints here: https://app.pax8.com/p8p/api/v3/

## Installation
### From PyPi
```bash
pip3 install pax8
```

### From Source
```bash
git clone https://github.com/scheibling/py-pax8.git
cd py-pax8
python3 setup.py install
```

## Usage
### Creating an API token
To be able to use the API, you must first create a token in the Pax8 Partner Application (https://app.pax8.com). to be able to see the option for doing this, you must first register a partner shell under Tools -> Partner Shells -> Pax8 Partner API Partner Shell. Once this is done, you can create a new client ID and secret under Profile Picture -> Edit Profile -> Developer Apps -> Create.

### Usage Examples
#### Importing the library and retrieving resources
```python
from pax8 import Pax8Client
from pax8 import filters
from pax8 import enums

client = Pax8Client(
    client_id='your_client_id',
    client_secret='your_client_secret',
    cache_token=True,
    cache_location='~/pax8_token.json'
)

# List all customers (companies)
client.Company.list()

# List all customers (companies) with pagination and the following options
# First Page
# Page Size 10
# Sort by Name (Ascending)
# Filter by city = 'New York'
companies = client.Company.list(
    filters.CompanyFilter(
        page=0,
        size=10,
        sort=enums.CompanySortBy.NAME,
        sort_direction=enums.SortDirection.ASCENDING,
        city='New York'
    )
)

# Recursively get all contacts and the MS Partner ID for the companies retrieved above
for company in companies:
    print(f'Company: {company.name}')
    print(f'MS Partner ID: {client.Company.get_ms_tenant_id(company.id)}')
    print('Contacts:')
    for contact in client.Company.list_contacts(company.id):
        print(f'\t{contact.first_name} {contact.last_name} ({contact.phoneNumber})')
```


## Pax8 API Errors
### Subscriptions
- Subscriptions does not contain a "commitmentTerm" field as stated in the documentation, but instead contains a "commitment" field

### Orders
- When an order retrieved from the API and order is placed by the partner, the API returns "Pax8Partner" instead of "Pax8 Partner". When creating a new order, the required value is "Pax8 Partner".

### Contacts
- Contacts contains an undocumented field "phoneNumber" in addition to the field called "phone".
- Contacts contains an undocumented field "phoneCountryCode"
- Contacts contains an undocumented field "phoneCountryCallingcode"

### Invoice
- InvoiceItem.rateType values are documented as lowercase, but are first-letter-uppercase in the API (at least for Flat, not been able to verify the others)

### Usage Summaries
- List Usage Summary Lines does not specify any pagination options for the API call, but the API does support pagination.

## Acknowledgements
- [dkschruteBeets](https://github.com/dkschruteBeets) for the [Powershell implementation of the API](https://github.com/dkschruteBeets/Pax8-API), which was a great reference for this (especially for the undocumented APIs)