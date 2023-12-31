import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.contrib.contenttypes.models import ContentType
from crm.models import Client,CustomUser, Contract,Event  # Replace with your actual model path
from datetime import date
import datetime
from django.utils import timezone



@pytest.mark.django_db
class TestManagementUserClientAccess:
    @pytest.fixture(autouse=True)
    def setup_class(self, db, django_user_model):
        self.client = APIClient()        
        self.management_user = django_user_model.objects.create_user(
            username='manager', password='password', is_staff=True
        )
        client_content_type = ContentType.objects.get_for_model(Client)
        view_client_permission = Permission.objects.get(
            codename='view_client', content_type=client_content_type
        )
        self.management_user.user_permissions.add(view_client_permission)
        self.client.force_authenticate(user=self.management_user)
        
        def test_management_can_see_all_clients(self):
            url = reverse('client-list')
            response = self.client.get(url)
            assert response.status_code == status.HTTP_200_OK
        def test_management_cannot_create_client(self):
            url = reverse('client-list')
            response = self.client.post(url, {'name': 'New Client'})  
            assert response.status_code == status.HTTP_403_FORBIDDEN
            
        def test_management_cannot_update_client(self):
        
            url = reverse('client-detail', args=[1])
            response = self.client.patch(url, {'name': 'Updated Client'})  # Adjust the payload as needed
            assert response.status_code == status.HTTP_403_FORBIDDEN

        def test_management_cannot_delete_client(self):
        
            url = reverse('client-detail', args=[1])
            response = self.client.delete(url)
            assert response.status_code == status.HTTP_403_FORBIDDEN
            

@pytest.mark.django_db
class TestManagementUserAccess:
    @pytest.fixture(autouse=True)
    def setup_method(self, db, django_user_model):
        self.client = APIClient()
        self.management_user = django_user_model.objects.create_user(
            username='management', password='management123', is_staff=True, role='management'
        )
        self.client.force_authenticate(user=self.management_user)
        
    def test_management_can_read_all_users(self):
        url = reverse('user-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        
    def test_management_can_create_user(self):
        url = reverse('user-create')
        new_user_data = {
            'username': 'newuser',
            'password': 'newpass123',
            'role': 'commercial',
            'email': 'email@email.com'
        }
        response = self.client.post(url, new_user_data)
        assert response.status_code == status.HTTP_201_CREATED
        
    def test_management_can_update_user(self):
        
        user_model = get_user_model()
        user_to_update = user_model.objects.create_user(
            username='updatable', password='password', role='support', email='email@email.com'
        )
        url = reverse('user-update', args=[user_to_update.pk])
        update_data = {
            'username': 'updateduser',
            'role': 'commercial'
        }
        response = self.client.patch(url, update_data)
        assert response.status_code == status.HTTP_200_OK
        
    def test_management_can_delete_user(self):
        # Create a user to delete
        user_model = get_user_model()
        user_to_delete = user_model.objects.create_user(
            username='deletable', password='password', role='commercial', email='email@email.com'
        )
        url = reverse('user-delete', args=[user_to_delete.pk])
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        

@pytest.mark.django_db
class TestManagementUserContractAccess:
    @pytest.fixture(autouse=True)
    def setup_method(self, db, django_user_model):
        self.client = APIClient()
        self.commercial_user = django_user_model.objects.create_user(
            username='commercial', password='commercial123', role='commercial'
        )
        self.management_user = django_user_model.objects.create_user(
            username='management', password='management123', is_staff=True, role='management'
        )
        self.client_obj = Client.objects.create (
        full_name='Test Client',
        email='client@example.com',
        sales_contact=self.commercial_user,
        creation_date=date.today(),
        last_update=date.today()
        )
        self.client.force_authenticate(user=self.management_user)
        
        self.contract = Contract.objects.create(
        client=self.client_obj, 
        sales_contact=self.commercial_user, 
        is_signed=False,
        total_amount=1000.00,  
        remaining_amount=500.00,  
        creation_date='2023-01-01'  
        )
        
    def test_management_can_read_all_contracts(self):
        url = reverse('contract-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        
    def test_management_can_create_contract(self):
        url = reverse('contract-list')
        contract_data = {
        "client":self.client_obj.id, 
        "sales_contact":self.commercial_user.id, 
        "is_signed":'false',
        "total_amount":1000.00,  
        "remaining_amount":500.00,  
        "creation_date":'2023-01-01'  
        }
        response = self.client.post(url, contract_data)
        print(response.data) 
        assert response.status_code == status.HTTP_201_CREATED
    def test_management_can_update_contract(self):
        url = reverse('contract-detail', args=[self.contract.pk])
        update_data = {
            "is_signed":'true',
            "total_amount":10000.00,
        }
        response = self.client.patch(url, update_data)
        assert response.status_code == status.HTTP_200_OK
        
    def test_management_cannot_delete_contract(self):
        url = reverse('contract-detail', args=[self.contract.pk])
        response = self.client.delete(url)
        assert response.status_code in (status.HTTP_403_FORBIDDEN, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        
@pytest.mark.django_db
class TestManagementUserEventAccess:
    @pytest.fixture(autouse=True)
    def setup_method(self, db, django_user_model):
        self.client = APIClient()
        self.management_user = django_user_model.objects.create_user(
            username='management', password='management123', role='management'
        )
        self.commercial_user = django_user_model.objects.create_user(
            username='commercial', password='commercial123', role='commercial'
        )
        self.client_obj= Client.objects.create(
        full_name='Test Client', 
        email='client@example.com', 
        sales_contact=self.commercial_user,
        creation_date=datetime.date.today(),  
        last_update=datetime.date.today()     
    )
        
        self.contract = Contract.objects.create(
        client=self.client_obj, 
        sales_contact=self.commercial_user, 
        is_signed=False,
        total_amount=1000.00,  
        remaining_amount=500.00,  
        creation_date='2023-01-01'  
        )
        
        self.event = Event.objects.create(       
     
        start_date = timezone.make_aware(datetime.datetime(2023, 1, 15)),
        end_date = timezone.make_aware(datetime.datetime(2023, 1, 20)),
        location = 'Test Location',
        attendees = 50,
        client_name = self.client_obj,
        contract=self.contract, 
        )
        assert self.management_user.role == 'management'
        assert self.client.login(username='management', password='management123')
        self.client.force_authenticate(user=self.management_user)
        
    def test_management_can_see_all_events(self):
        url = reverse('event-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK    
    
    def test_management_can_update_events(self):       
        
        url = reverse('event-detail', kwargs={'pk': self.event.id})
        update_data = {
            'notes': 'Updated event notes'
        }
        response = self.client.patch(url, update_data)
        print(response.data)
        assert response.status_code == status.HTTP_200_OK
        
    def test_management_cannot_create_events(self):
        url = reverse('event-list')
        event_data = {        
        'event_date': '2023-01-10',
        'start_date': '2023-01-15',
        'end_date': '2023-01-20',
        'location': 'Test Location',
        'attendees': 50,        
        'notes': 'Test Event',
        'client_name' : self.client_obj,
        'contract':self.contract, 
        }
        response = self.client.post(url, event_data)
        assert response.status_code in (status.HTTP_403_FORBIDDEN, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_management_cannot_delete_events(self):        
        url = reverse('event-detail', kwargs={'pk': self.event.id})
        response = self.client.delete(url)    