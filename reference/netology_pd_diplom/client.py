import requests
import json
from pprint import pprint

## регистрация нового пользователя
#
# response = requests.post("http://localhost:8000/api/v1/user/register",
#                         json={
#                               "first_name": "Paul",
#                               "last_name": "ZV",
#                               "email": "paul_zv@mail.ru",
#                               "password": "Wow002265",
#                               "company": "svyaznoi",
#                               "position": "manager"
#
#                               }
#                         )
# print(response.status_code)
# print(response.text)

## регистрация нового пользователя/поставщика
#
# response = requests.post("http://localhost:8000/api/v1/user/register",
#                         json={
#                               "first_name": "Alex",
#                               "last_name": "grey",
#                               "email": "alex_grey@mail.ru",
#                               "password": "Wow112265",
#                               "company": "vendor",
#                               "position": "director",
#                               "is_active": True,
#                               "type": "shop"
#
#                               }
#                         )
# print(response.status_code)
# print(response.text)

## подтверждение регистрации нового пользователя
#
# response = requests.post("http://localhost:8000/api/v1/user/register/confirm",
#                         json={
#                             "email": "paul_zv@mail.ru",
#                             "token": "5beb6e1adf8117760847994e12d60c5130da6", ## используется токен email подтверждения
#                         }
#                         )
# print(response.status_code)
# print(response.text)


# Логин покупателем

response = requests.post("http://localhost:8000/api/v1/user/login",
                        json={"email": "paul_zv@mail.ru", "password": "Wow002267"}
                        )
print(response.status_code)
print(response.text)
#
## получение информации о пользователе
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "Token 3a5e07a98278d59ccb67de7bd1a50459916d6d5f" ## используется токен авторизации
# }
# response = requests.post("http://localhost:8000/api/v1/user/details",
#                         json={
#                                 "email": "paul_zv@mail.ru",
#                                 "password": "Wow002267",
#                                 "company": "Huawei",
#                                 "position": "director",
#                                 "type": "shop"
#                               }, headers=headers
#                         )
# print(response.status_code)
# print(response.text)

# загрузка данных о магазинах/товарах

# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "Token 3a5e07a98278d59ccb67de7bd1a50459916d6d5f" ## используется токен авторизации
# }
#
# file_path = r"D:\Netology\Diploma\python-final-diplom_PZ\reference\netology_pd_diplom\shop1.yaml"
#
# data = {
#     "email": "paul_zv@mail.ru",
#     "password": "Wow002267",
#     "url": file_path
# }
#
# response = requests.post("http://localhost:8000/api/v1/partner/update",
#                         json=data,
#                          headers=headers
#                         )
# print(response.status_code)
# print(response.text)

## добавление товаров в корзину
#
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "Token 3a5e07a98278d59ccb67de7bd1a50459916d6d5f" ## используется токен авторизации
# }
# data = {
#     "items": [{
#         "product_info": 4,
#         "quantity": 1
#     }],
# }
#
#
# response = requests.post("http://localhost:8000/api/v1/basket",
#                         json=data,
#                         headers=headers)
# print(response.status_code)
# print(response.text)

# добавление товара в корзину (обновление):

# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "Token 3a5e07a98278d59ccb67de7bd1a50459916d6d5f" ## используется токен авторизации
# }
# data = {
#     "items": [
#         {
#         "id": 1,
#         "quantity": 2,
#         # "order": 1,
#     }
#     ],
# }
#
# response = requests.put("http://localhost:8000/api/v1/basket",
#                         json=data,
#                         headers=headers)
# print(response.status_code)
# pprint(response.text)

## удаление товара из корзины

# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "Token 3a5e07a98278d59ccb67de7bd1a50459916d6d5f" ## используется токен авторизации
# }
# data = {
#     "items": "1"
#
# }
#
# response = requests.delete("http://localhost:8000/api/v1/basket",
#                         json=data,
#                         headers=headers)
# print(response.status_code)
# pprint(response.text)

# # просмотр магазина
#
# response = requests.get("http://localhost:8000/api/v1/shops")
# print(response.status_code)
# print(response.text)
#
## просмотр товаров
# #
# response = requests.get("http://localhost:8000/api/v1/products")
# print(response.status_code)
# print(response.text)
#
# # просмотр категорий)
#
# response = requests.get("http://localhost:8000/api/v1/categories")
# print(response.status_code)
# print(response.text)

# просмотр корзины (только залогиненным)
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "Token 3a5e07a98278d59ccb67de7bd1a50459916d6d5f" ## используется токен авторизации
# }
# response = requests.get("http://localhost:8000/api/v1/basket",
#                         headers=headers)
# print(response.status_code)
# pprint(response.text)

## добавление контактов

# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "Token 3a5e07a98278d59ccb67de7bd1a50459916d6d5f" ## используется токен авторизации
# }
# data = {
#     "city": "Moscow",
#     "street": "Tverskaya street",
#     "phone": "123"
# }
#
# response = requests.post("http://localhost:8000/api/v1/user/contact",
#                         json=data,
#                         headers=headers
#                         )
# print(response.status_code)
# print(response.text)

# ## просмотр контакта
#
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "Token 3a5e07a98278d59ccb67de7bd1a50459916d6d5f" ## используется токен авторизации
# }
# data = {
#     "user": 4,
#
# }
#
# response = requests.get("http://localhost:8000/api/v1/user/contact",
#                         json=data,
#                         headers=headers
#                         )
# print(response.status_code)
# print(response.text)

## Обновление контактов
#
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "Token 3a5e07a98278d59ccb67de7bd1a50459916d6d5f" ## используется токен авторизации
# }
# data = {
#     "id": "1",
#     "city": "Moscow",
#     "street": "Tverskaya street",
#     "phone": "125"
# }
#
# response = requests.put("http://localhost:8000/api/v1/user/contact",
#                         json=data,
#                         headers=headers
#                         )
# print(response.status_code)
# print(response.text)

## удаление контактов
#
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "Token 3a5e07a98278d59ccb67de7bd1a50459916d6d5f" ## используется токен авторизации
# }
# data = {
#     "items": "1",
#
# }
#
# response = requests.delete("http://localhost:8000/api/v1/user/contact",
#                         json=data,
#                         headers=headers
#                         )
# print(response.status_code)
# print(response.text)

## размещение заказа

# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "Token 3a5e07a98278d59ccb67de7bd1a50459916d6d5f" ## используется токен авторизации
# }
#
# # Get basket data
# response = requests.get("http://localhost:8000/api/v1/basket", headers=headers)
# basket_data = response.json()
#
# # Check if there are items in the basket
# if basket_data:
#     # Extract relevant information (you may need to adjust this based on your actual data structure)
#     basket_item = basket_data[0]['ordered_items'][0]
#     order_data = {
#         "id": str(basket_item['product_info']['id']),  # Convert to string before checking isdigit
#         "contact": basket_data[0]['contact']['id']
#     }
#
#     # Place an order
#     response = requests.post("http://localhost:8000/api/v1/order", json=order_data, headers=headers)
#     print(response.status_code)
#     print(response.text)
# else:
#     print("Basket is empty.")


headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 3a5e07a98278d59ccb67de7bd1a50459916d6d5f" ## используется токен авторизации
}
data = {
    "id": "4",
    "contact": 2
}

response = requests.post("http://localhost:8000/api/v1/order", json=data, headers=headers)
print(response.status_code)
print(response.text)
