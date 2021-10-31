# Advisor Network API

## Index

| **SR** | **Endpoint**                              | **Desciption**          |
| ------ | ----------------------------------------- | ----------------------- |
| 1      | /admin/advisor/                           | Add Advisor             |
| 2      | /user/register/                           | Register User           |
| 3      | /user/login/                              | User Login              |
| 4      | /user/\<user_id\>/advisor                 | Show Advisors           |
| 5      | /user/\<user_id\>/advisor/\<advisor-id\>/ | Book Advisor            |
| 6      | /user/\<user_id\>/advisor/booking/        | List of Advisors Booked |

## Add Advisor

Add a new advisor

**Request**
**Method** | **Url**
------------ | -------------
POST | api/admin/advisor/

| **Type** | **Params**   | **Values** |
| -------- | ------------ | ---------- |
| POST     | advisor_name | string     |
| POST     | advisor_img  | File       |

**Response**
**Status**| **Description**
-------- | ------------
200 | Successful
400 | Bad Request

## Register User

Register User

**Request**
**Method** | **Url**
------------ | -------------
POST | api/user/register

| **Type** | **Params** | **Values** |
| -------- | ---------- | ---------- |
| POST     | name       | string     |
| POST     | email      | string     |
| POST     | password   | string     |

**Response**
**Status**| **Description**
-------- | ------------
200 | Successful
400 | Bad Request

## Login User

Login your registered user

**Request**
**Method** | **Url**
------------ | -------------
POST | api/user/login

| **Type** | **Params** | **Values** |
| -------- | ---------- | ---------- |
| POST     | email      | string     |
| POST     | password   | string     |

**Response**
**Status**| **Description**
-------- | ------------
200 | Successful
400 | Bad Request

## Show all Advisor

To show all the advisor

**Request**
**Method** | **Url**
------------ | -------------
GET | api/user/\<user_id\>/advisor

| **Type** | **Params**     | **Values**                                                       |
| -------- | -------------- | ---------------------------------------------------------------- |
| Header   | x-access-token | token string given when a user is registered or after user login |

**Response**
|**Status**| **Description**|
|-------- | ------------|
|200 | Successful|
|400 | Bad Request|

## Book Advisor

To book advisor

**Request**
**Method** | **Url**
------------ | -------------
POST | api/user/\<user_id\>/advisor/\<advisor_id\>/

| **Type** | **Params**     | **Values**                                                       |
| -------- | -------------- | ---------------------------------------------------------------- |
| Header   | x-access-token | token string given when a user is registered or after user login |
| POST     | booking_date   | string (dd-mm-yyyy)                                              |

**Response**
**Status**| **Description**
-------- | ------------
200 | Successful
400 | Bad Request

## Show all Bookings

Shows all the bookings made by the user

**Request**
**Method** | **Url**
------------ | -------------
GET | api/user/\<user_id\>/advisor/booking

| **Type** | **Params**     | **Values**                                                       |
| -------- | -------------- | ---------------------------------------------------------------- |
| Header   | x-access-token | token string given when a user is registered or after user login |

**Response**
**Status**| **Description**
-------- | ------------
200 | Successful
400 | Bad Request
