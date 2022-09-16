from src.pax8.types import *
# import json

# test = CompanyAddress(
#     street="Street", city="City", postalCode="PostalCode", country="country"
# )

# print(test.serialize())

# # testPage = json.dumps({
#     "size": 1,
#     "totalElements": 100,
#     "totalPages": 100,
#     "number": 999
# })

# page = Pax8Page.deserialize(testPage)

# print(page)

# class Test:
#     @staticmethod
#     def get_qs():
#         return {}
    
#     def __get_qs(self):
#         return {"Hello": "World"}

#     def __init__(self):
#         self.get_qs = self.__get_qs
    
    # def __init__(self):
    #     delattr(self, "get_qs")
    #     setattr(self, "get_qs", self.__get_qs)


from src.pax8.rest import Pax8RestClient

cli = Pax8RestClient('', '')

# cpnlist = cli.list_companies(CompanyFilter(page=0, size=1))
# print(len(cpnlist))

# prodlist = cli.list_products(ProductFilter(page=0, size=5))
# print(len(prodlist))

provdet = cli.list_dependencies('9c773c32-9871-4a12-a592-b2ee129fef61')
print(provdet)

print("Hold")



# cpnlist = cli.list_companies(
#     CompanyFilter(
#         page=0,
#         size=1,
#         sort=CompanySortBy.NAME,
#         sort_direction=SortDirection.ASCENDING,
#         city="Helsingborg"
#     )
# )
# cpnlist2 = cli.list_companies()
# print(cpnlist)
# print(cpnlist2)
# cpn = cli.get_company("87e22dab-0a0f-451e-a5fa-f2d85c2ff4df")
# print(cpn)
# prod = cli.get_product("fbde4e32-6e38-4d26-88fc-3b5cdab42ab6")
# print(prod)
# # con = cli.get_contact("")
# print("Hold")