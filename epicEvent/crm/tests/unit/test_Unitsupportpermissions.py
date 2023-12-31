import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from unittest.mock import Mock
from crm.models import Client,Contract,Event

# Fixtures
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def management_user(db):    
    User = get_user_model()
    return User.objects.create_user(username='manager', password='testpass123', role='management')

# Mocking support user
@pytest.fixture
def support_user(db):    
    User = get_user_model()
    return User.objects.create_user(username='support', password='testpass123', role='support')

@pytest.fixture
def mock_client_object(mocker):    
    mock_client = Mock(spec=Client)
    mock_client.id = 1
    mocker.patch('crm.models.Client.objects.get', return_value=mock_client)
    return mock_client

@pytest.fixture
def mock_contract_object(mocker):
    mock_contract = Mock(spec=Contract)
    mock_contract.id = 1
    mocker.patch('crm.models.Contract.objects.get', return_value=mock_contract)
    return mock_contract

@pytest.fixture
def mock_event_object(mocker, support_user):
    mock_event = Mock(spec=Event)
    mock_event.id = 1
    mock_event.support_contact = support_user
    mocker.patch('crm.models.Event.objects.get', return_value=mock_event)
    return mock_event



def test_support_cannot_create_user(api_client, support_user):
    api_client.force_authenticate(user=support_user)
    
    response = api_client.post(reverse('user-create'), {})
    
    assert response.status_code == status.HTTP_403_FORBIDDEN
    
def test_support_cannot_access_user_list(api_client, support_user):
    api_client.force_authenticate(user=support_user)
    
    response = api_client.get(reverse('user-list'))
    
    assert response.status_code == status.HTTP_403_FORBIDDEN
    
def test_support_cannot_update_user(api_client, support_user):
    api_client.force_authenticate(user=support_user)
    
    url = reverse('user-update', args=[1])  
    response = api_client.patch(url, {})
    
    assert response.status_code == status.HTTP_403_FORBIDDEN
    
def test_support_cannot_delete_user(api_client, support_user):
    api_client.force_authenticate(user=support_user)
    
    url = reverse('user-delete', args=[1])  
    response = api_client.delete(url)
    
    assert response.status_code == status.HTTP_403_FORBIDDEN
   
def test_support_can_see_all_clients(mocker, support_user):
    api_client = APIClient()
    api_client.force_authenticate(user=support_user)
    
    response = api_client.get(reverse('client-list'))
    
    assert response.status_code == status.HTTP_200_OK
   
def test_support_cannot_create_client(mocker, support_user):
    api_client = APIClient()
    api_client.force_authenticate(user=support_user)
    
    response = api_client.post(reverse('client-list'), {
        
    })
    
    assert response.status_code == status.HTTP_403_FORBIDDEN   
    
def test_support_cannot_delete_client(api_client, mock_client_object, support_user):
    api_client.force_authenticate(user=support_user)
    
    
    url = reverse('client-detail', args=[mock_client_object.id])
    response = api_client.delete(url)
    
    assert response.status_code == status.HTTP_403_FORBIDDEN
    
def test_support_cannot_update_client(api_client, mock_client_object, support_user):
    api_client = APIClient()
    api_client.force_authenticate(user=support_user)
    
    response = api_client.patch(reverse('client-detail', args=[mock_client_object.id]), {
        
    })    
    assert response.status_code == status.HTTP_403_FORBIDDEN
    
def test_support_can_read_all_contracts(api_client, support_user):
    api_client.force_authenticate(user=support_user)
    response = api_client.get(reverse('contract-list'))
    assert response.status_code == status.HTTP_200_OK


def test_support_cannot_create_contract(api_client, support_user):
    api_client.force_authenticate(user=support_user)
    response = api_client.post(reverse('contract-list'), {})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    
def test_support_cannot_delete_contract(api_client, mock_contract_object, support_user):
    api_client.force_authenticate(user=support_user)
    url = reverse('contract-detail', args=[mock_contract_object.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_support_cannot_update_contract(api_client, mock_contract_object, support_user):
    api_client.force_authenticate(user=support_user)
    response = api_client.patch(reverse('contract-detail', args=[mock_contract_object.id]), {})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    
    
    
def test_support_user_can_read_all_events(api_client, support_user):
    api_client.force_authenticate(user=support_user)
    response = api_client.get(reverse('event-list'))
    assert response.status_code == status.HTTP_200_OK
    
@pytest.mark.django_db
def test_support_user_can_update_assigned_event():   
    api_client = APIClient()    
    User = get_user_model()
    support_user = User.objects.create_user(username='support', password='password', role='support')    
    api_client.force_authenticate(user=support_user)    
    client_instance = Client.objects.create(
        full_name="Test Client",
        email="testclient@example.com",
        phone="1234567890",
        company_name="Test Company",
        creation_date="2023-01-15",
        last_update="2023-01-15"
    )
    
    contract_instance = Contract.objects.create(
        sales_contact=support_user,
        total_amount=15000.00,
        remaining_amount=5000.00,
        creation_date='2023-12-17',
        is_signed=True,
        client=client_instance
    )
    
    event_instance = Event.objects.create(
        support_contact=support_user,
        start_date="2024-02-28T14:46:00Z",
        end_date="2024-03-03T14:46:00Z",
        location="Ultimate Test Location",
        attendees=2,
        notes="Great event",
        contract=contract_instance,
        client_name=client_instance
    )   
    
    update_data = {
        "location": "Updated Location",
        "notes": "Updated notes"
    }   
    
    url = reverse('event-detail', args=[event_instance.id])
    response = api_client.patch(url, update_data, format='json')   
    
    assert response.status_code == status.HTTP_200_OK    
    event_instance.refresh_from_db()
    assert event_instance.location == update_data['location']
    assert event_instance.notes == update_data['notes']
    


@pytest.mark.django_db
def test_support_user_cannot_update_unassigned_event(api_client, support_user):    
    
    client_instance = Client.objects.create(
        full_name="Test Client",
        email="testclient@example.com",
        phone="1234567890",
        company_name="Test Company",
        creation_date="2023-01-15",
        last_update="2023-01-15"
    )
    
    contract_instance = Contract.objects.create(
        sales_contact=support_user,
        total_amount=15000.00,
        remaining_amount=5000.00,
        creation_date='2023-12-17',
        is_signed=True,
        client=client_instance
    )      
        
    unassigned_event = Event.objects.create(
        support_contact=None, 
        start_date="2024-02-28T14:46:00Z",
        end_date="2024-03-03T14:46:00Z",
        location="Ultimate Test Location",
        attendees=2,
        notes="Great event",
        contract=contract_instance,
        client_name=client_instance 
    )
    
    api_client.force_authenticate(user=support_user)
    url = reverse('event-detail', args=[unassigned_event.id])
    response = api_client.patch(url, {'notes': 'Updated notes'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    

@pytest.mark.django_db
def test_support_user_cannot_create_event(api_client, support_user):
    api_client.force_authenticate(user=support_user)
    
    client_instance = Client.objects.create(
        full_name="Test Client",
        email="testclient@example.com",
        phone="1234567890",
        company_name="Test Company",
        creation_date="2023-01-15",
        last_update="2023-01-15"
    )
    
    contract_instance = Contract.objects.create(
        sales_contact=support_user,
        total_amount=15000.00,
        remaining_amount=5000.00,
        creation_date='2023-12-17',
        is_signed=True,
        client=client_instance
    ) 
    
    
    event_data = {
        "support_contact":support_user, 
        "start_date":"2024-02-28T14:46:00Z",
        "end_date":"2024-03-03T14:46:00Z",
        "location":"Ultimate Test Location",
        "attendees":2,
        "notes":"Great event",
        "contract":contract_instance,
        "client_name":client_instance 
    }

    response = api_client.post(reverse('event-list'), event_data)
    assert response.status_code in (status.HTTP_403_FORBIDDEN, status.HTTP_405_METHOD_NOT_ALLOWED)
    

@pytest.mark.django_db
def test_support_user_cannot_delete_event(api_client, support_user):
    
    client_instance = Client.objects.create(
        full_name="Test Client",
        email="testclient@example.com",
        phone="1234567890",
        company_name="Test Company",
        creation_date="2023-01-15",
        last_update="2023-01-15"
    )    
    contract_instance = Contract.objects.create(
        sales_contact=support_user,
        total_amount=15000.00,
        remaining_amount=5000.00,
        creation_date='2023-12-17',
        is_signed=True,
        client=client_instance
    )    
       
    event_to_delete = Event.objects.create(
        support_contact=None, 
        start_date="2024-02-28T14:46:00Z",
        end_date="2024-03-03T14:46:00Z",
        location="Ultimate Test Location",
        attendees=2,
        notes="Great event",
        contract=contract_instance,
        client_name=client_instance 
    )
    
    
    api_client.force_authenticate(user=support_user)
    url = reverse('event-detail', args=[event_to_delete.id])
    response = api_client.delete(url)
    assert response.status_code in (status.HTTP_403_FORBIDDEN, status.HTTP_405_METHOD_NOT_ALLOWED)