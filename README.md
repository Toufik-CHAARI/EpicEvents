# EpicEvents CRM API Documentation


## Table of Contents

- [Installation](#installation)
- [Authentication](#authentication)
- [crm](#crm)
- [Integration and Unit tests coverage report](#Integration-and-Unit-tests-coverage-report)
- [PEP8 Code compliance Report](#pep8-code-compliance-report)




***
## Installation

Please be advised that this api runs with python version 3.10.5 

- create a folder via terminal.
'mkdir YourFolderName'

- Change YourFolderName
'cd YourFolderName'

- Clone the project
'git clone https://github.com/Toufik-CHAARI/EpicEvents.git'

- Create Virtual Environment
'python3.10 -m venv env'

- Activate virtual environment
'source env/bin/activate'

- Check python version is 3.10.5
'python --version'

- Change directory
'cd EpicEvents'

- Change directory
'cd EpicEvent'

- Install dependencies
'pip install -r requirements.txt'

- create a database in postgres with the following settings

        'NAME': 'crm',
        'USER': 'postgres',
        

- Set your database password as an Environment variable in your terminal 

'export DB_PASSWORD=YourDataBasePassword'

- run Migrations
'python manage.py migrate'

- create admin (provide username and password)
'python manage.py createsuperuser'

- Run local server
  'python3 manage.py runserver'



***

## Authentication

### 1. Obtain JWT Token
Endpoint: http://127.0.0.1:8000/api-auth/api/token/

Http Method:
POST: Get JWT Token by providing a valid username and password.

Http parameters : none 
Http Body:
- username 
- password 

### 2. Create user

Endpoint: http://127.0.0.1:8000/api-auth/users/create/

HTTP Method 
POST : Create new user
Header must contain token
Http Parameters : None
Http Body :
- username 
- role 
- password 
- email

Permissions:
Token-based authenticated superusers and users with management role.

### 3. User Detail
Endpoint: http://127.0.0.1:8000/api-auth/users/<int:user_id>/

Http Method: 
GET: Fetch data for a specified user.
Header must contain token
Http parameter : user_id
Http body : none

Permissions:
Superusers and Authenticated users with commercial role.


### 3. User list
Endpoint: http://127.0.0.1:8000/api-auth/users

Http Methods: 
GET: Fetch data of all users.
Header must contain token
Permissions:
Superusers Authenticated users with commercial role.
Superusers can fetch data for all users.

### 4. User update
Endpoint: http://127.0.0.1:8000/api-auth/users/<int:user_id>/update/

Http Methods: 
PUT OR PATCH : Fetch data of all users.
Header must contain token

Parameters (all or partial fields depending http method)

username :
role :
password :
email:

Permissions:
Superusers Authenticated users with commercial role.
Superusers can fetch data for all users.



### 5. User delete
Endpoint: http://127.0.0.1:8000/api-auth/users/<int:user_id>/delete/

Http Method: 
DELETE : delete agiven user.
Header must contain token

Permissions:
Superusers Authenticated users with commercial role.
Superusers can fetch data for all users.

**
## CRM

##Client entity

### Create Client

Endpoint: http://127.0.0.1:8000/api/client/

Http Method: 
POST : create a new client.
Header must contain token

Parameters
full_name:
email:
phone :
company_name :
creation_date :
last_update :

Permissions:
Only token-based authenticated users with commercial role. sales_contact attribute is by default = commercial.user_id 



## Client list

Endpoint: http://127.0.0.1:8000/api/client

Http Method: 
GET : Fetch data of all clientS.
Header must contain token

Parameters
None

Permissions:
All token-based authenticated users.



## Client detail

Endpoint: http://127.0.0.1:8000/api/client/<int:cllient_id>/

Http Method: 
GET : Fetch data of all clientS.
Header must contain token

Parameters
client_id in the url

Permissions:
All token-based authenticated users.

### Update Client 

Endpoint: http://127.0.0.1:8000/api/client/<int:client_id>/

Http Method: 
PUT or PATCH : update all or partial fields of a given client.
Header must contain token
Parameter: client_id

Body 
full_name:
email:
phone :
company_name :
creation_date :
last_update :
sales_contact

Permissions:
Token-based authenticated user assigned as sales_contact in client attributes.


### delete Client 
unauthorized action


## Contract entity

### Contract list

Endpoint: http://127.0.0.1:8000/api/contract/

Http Method: 
GET : fetch data of all the existing contracts.
Header must contain token

Parameters : none

Permissions:
All Token-based authenticated users. 

### Contract details

Endpoint: http://127.0.0.1:8000/api/contract/<int:contract_id>/

Http Method: 
GET : fetch data of a given contract.
Header must contain token

Parameters : contract_id

Permissions:
All Token-based authenticated users.


### Create Contract

Endpoint: http://127.0.0.1:8000/api/contract/

Http Method: 
POST : create a new contract.
Header must contain token

Http Parameter none

Http Body
total_amount:
remaining_amount:
creation_date (YYYY-MM-DD) :
is_signed (boolean):
client (client_id):
sales contact (user_id):


Permissions:
Only token-based authenticated users with management role. 



### Update Contract

Endpoint: http://127.0.0.1:8000/api/contract/<int:contract_id>/

Http Method: 
PUT OR PATCH : partial or total update of an existing contract.
Header must contain token

Parameters contract_id

total_amount:
remaining_amount:
creation_date (YYYY-MM-DD) :
is_signed (boolean):
client (client_id):
sales contact (user_id):

Permissions:
Token-based authenticated users with management role as well as users with commercial roles if commercial_id = sales_contact_id. 

### DELETE Contract 
Unauthorized action


### Fitered view : Unsigned Contracts

Endpoint: http://127.0.0.1:8000/api/contracts/commercial/unsigned/

Http Method: 
GET: fetch all the existing unsigned contracts assigned to the current commercial user.
Header must contain token
Http Parameters : none

Permissions:
Token-based authenticated users with commercial role  if commercial_user.id = sales_contact_id.


### Filtered view : Contracts wit positive remaining amounts

Endpoint: http://127.0.0.1:8000/api/contracts/commercial/remaining-amount/

Http Method: 
GET: fetch all the existing contracts assigned to the current commercial user with remaining amounts greater than 0 .
Header must contain token
Http Parameters : none

Permissions:
Token-based authenticated users with commercial role  if commercial_user.id = sales_contact_id.



**
### Event Entity 


### Event list

Endpoint: http://127.0.0.1:8000/api/event/

Http Method: 
GET : fetch all the existing event.
Header must contain token
Http Parameter : none

Http Body : none

Permissions:
All token-based authenticated users. 

### Event details

Endpoint: http://127.0.0.1:8000/api/event/<int:event_id>/

Http Method: 
GET : fetch all the existing event.
Header must contain token
Http Parameter : event_id
Http Body : none
Permissions:
All token-based authenticated users. 

### Create Event

Endpoint: http://127.0.0.1:8000/api/event/

Http Method: 
POST : create a new event.
Header must contain token
Http Parameter : none

Http Body

start_date (YYYY-MM-DD) :
end_date (YYYY-MM-DD) :
location:
attendees (INT):
notes:
contract(contract_id):
support_contact(user_id):


Permissions:
token-based authenticated users with commercial role if the contract is signed and that commercial_user_id = contract.sales_contact.id. 



### Update Event

Endpoint: http://127.0.0.1:8000/api/event/<int:event_id>/

Http Method: 
PUT OR PATCH : total or partial update an existing event.
Header must contain user token
Http Parameter : event_id

Http Body

start_date (YYYY-MM-DD) :
end_date (YYYY-MM-DD) :
location:
attendees (INT):
notes:
contract(contract_id):
support_contact(user_id):


Permissions:
token-based authenticated users with management role as well as users with support role if user_id = support_contact_id.


### Filtered View : Null Role Event

Endpoint: http://127.0.0.1:8000/api/null-role-events/

Http Method: 
GET : fetch all events where support_contact = null.
Header must contain user token
Http Parameter : none

Permissions:
token-based authenticated users with management role.


### Filtered View : Event assigned to support

Endpoint: http://127.0.0.1:8000/api/support-events

Http Method: 
GET : fetch all events assigned to the authenticated support_contact.
Header must contain user token

Http Parameter : none
Permissions:
token-based authenticated users with support role.

## Integration and Unit tests coverage report

For detailed figures regarding tests coverage please run the following command :

'export DB_PASSWORD=YOURPASSWORD'
'pytest --cov=.'

## PEP8 Code compliance Report

In order to generate the reports please run the following commands

#### Authentication App

- flake8 --format=html --htmldir=flake-report_authentication_admin authentication/admin.py
- flake8 --format=html --htmldir=flake-report_authentication_models authentication/models.py
- flake8 --format=html --htmldir=flake-report_authentication_permissions authentication/permissions.py
- flake8 --format=html --htmldir=flake-report_authentication_serializers authentication/serializers.py
- flake8 --format=html --htmldir=flake-report_authentication_urls authentication/urls.py
- flake8 --format=html --htmldir=flake-report_authentication_views authentication/views.py

#### CRM App

- flake8 --format=html --htmldir=flake-report_crm_admin crm/admin.py
- flake8 --format=html --htmldir=flake-report_crm_models crm/models.py
- flake8 --format=html --htmldir=flake-report_crm_permissions crm/permissions.py
- flake8 --format=html --htmldir=flake-report_crm_serializers crm/serializers.py
- flake8 --format=html --htmldir=flake-report_crm_urls crm/urls.py
- flake8 --format=html --htmldir=flake-report_crm_views crm/views.py

#### Integration tests

- flake8 --format=html --htmldir=flake-report_crm_integration_tests_commercial crm/tests/integration/test_Intcommercialpermissions.py
- flake8 --format=html --htmldir=flake-report_crm_integration_tests_management crm/tests/integration/test_Intmanagementpermissions.py
- flake8 --format=html --htmldir=flake-report_crm_integration_tests_support crm/tests/integration/test_Intsupportpermissions.py

#### Unit tests

- flake8 --format=html --htmldir=flake-report_crm_unit_tests_commercial crm/tests/unit/test_Unitcommercialpermissions.py
- flake8 --format=html --htmldir=flake-report_crm_unit_tests_management crm/tests/integration/test_Unitmanagementpermissions.py
- flake8 --format=html --htmldir=flake-report_crm_unit_tests_support crm/tests/integration/test_Unitsupportpermissions.py

***