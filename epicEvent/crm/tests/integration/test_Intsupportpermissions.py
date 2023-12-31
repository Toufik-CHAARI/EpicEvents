import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.contrib.contenttypes.models import ContentType
from crm.models import Client,CustomUser, Contract,Event  
from datetime import date
import datetime
from django.utils import timezone


@pytest.mark.django_db
class TestSupportUserClientAccess:
    @pytest.fixture(autouse=True)
    def setup_class(self, db, django_user_model):
        self.client = APIClient()        
        self.support_user = django_user_model.objects.create_user(
            username='support', password='password', is_staff=True
        )
        client_content_type = ContentType.objects.get_for_model(Client)
        view_client_permission = Permission.objects.get(
            codename='view_client', content_type=client_content_type
        )
        self.support_user.user_permissions.add(view_client_permission)
        self.client.force_authenticate(user=self.support_user)
        
        def test_support_can_see_all_clients(self):
            url = reverse('client-list')
            response = self.client.get(url)
            assert response.status_code == status.HTTP_200_OK
        def test_support_cannot_create_client(self):
            url = reverse('client-list')
            response = self.client.post(url, {'name': 'New Client'})  
            assert response.status_code == status.HTTP_403_FORBIDDEN
        def test_support_cannot_update_client(self):        
            url = reverse('client-detail', args=[1])
            response = self.client.patch(url, {'name': 'Updated Client'})  
            assert response.status_code == status.HTTP_403_FORBIDDEN

        def test_support_cannot_delete_client(self):
        
            url = reverse('client-detail', args=[1])
            response = self.client.delete(url)
            assert response.status_code == status.HTTP_403_FORBIDDEN
            
            
@pytest.mark.django_db
class TestSupportUserAccess:
    @pytest.fixture(autouse=True)
    def setup_method(self, db, django_user_model):
        self.client = APIClient()
        self.support_user = django_user_model.objects.create_user(
            username='support', password='support123', role='support'
        )
        self.client.force_authenticate(user=self.support_user)
        
    def test_support_user_cannot_create_user(self):
            url = reverse('user-create')  
            user_data = {
                'username': 'newuser',
                'password': 'newpass123',
                'role': 'support'
            }
            response = self.client.post(url, user_data)
            assert response.status_code == status.HTTP_403_FORBIDDEN
            
    def test_support_user_cannot_access_user_list(self):
        url = reverse('user-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_support_user_cannot_update_user(self):        
        user_model = get_user_model()
        user_to_update = user_model.objects.create_user(
            username='updatable', password='password', role='commercial'
        )
        url = reverse('user-update', args=[user_to_update.pk])  
        update_data = {
            'username': 'updateduser',
            'role': 'commercial'
        }
        response = self.client.patch(url, update_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_support_user_cannot_delete_user(self):        
        user_model = get_user_model()
        user_to_delete = user_model.objects.create_user(
            username='deletable', password='password', role='commercial'
        )
        url = reverse('user-delete', args=[user_to_delete.pk])  
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        

@pytest.mark.django_db
class TestSupportUserContractAccess:
    @pytest.fixture(autouse=True)
    def setup_method(self, db, django_user_model):
        self.client = APIClient()
        self.support_user = django_user_model.objects.create_user(
            username='support', password='support123', role='support'
        )
        self.commercial_user = django_user_model.objects.create_user(
            username='commercial', password='commercial123', role='commercial'
        )
        self.client.force_authenticate(user=self.support_user)

       
        self.client_obj = Client.objects.create (
        full_name='Test Client',
        email='client@example.com',
        sales_contact=self.commercial_user,
        creation_date=date.today(),
        last_update=date.today()
        )
        
        
        self.sample_contract = Contract.objects.create(
        client=self.client_obj, 
        sales_contact=self.commercial_user, 
        is_signed=False,
        total_amount=1000.00,  
        remaining_amount=500.00,  
        creation_date='2023-01-01'  
        )
            
    def test_support_user_can_read_all_contracts(self):
        url = reverse('contract-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        
    def test_support_user_cannot_create_contract(self):
        url = reverse('contract-list')
        contract_data = {           
        "total_amount": "15000.00",
        "remaining_amount": "5000.00",
        "creation_date": "2023-12-17",
        "is_signed": "true",
        "client": self.client_obj,
        "sales_contact": self.commercial_user
        }
        response = self.client.post(url, contract_data)
        assert response.status_code in (status.HTTP_403_FORBIDDEN, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_support_user_cannot_update_contract(self):
        url = reverse('contract-detail', kwargs={'pk': self.sample_contract.pk})
        update_data = {
            "is_signed": "false",
        }
        response = self.client.patch(url, update_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN  
        
    def test_support_user_cannot_delete_contract(self):
        url = reverse('contract-detail', kwargs={'pk': self.sample_contract.pk})
        response = self.client.delete(url)
        assert response.status_code in (status.HTTP_403_FORBIDDEN, status.HTTP_405_METHOD_NOT_ALLOWED)              
        


@pytest.mark.django_db
class TestSupportUserEventAccess:
    @pytest.fixture(autouse=True)
    def setup_method(self, db, django_user_model):
        self.client = APIClient()
        self.support_user = django_user_model.objects.create_user(
            username='support', password='support123', role='support'
        )
        self.commercial_user = django_user_model.objects.create_user(
            username='commercial', password='commercial123', role='commercial'
        )
        self.client.force_authenticate(user=self.support_user)
        
        self.client_obj = Client.objects.create (
        full_name='Test Client',
        email='client@example.com',
        sales_contact=self.commercial_user,
        creation_date=date.today(),
        last_update=date.today()
        )
        self.sample_contract = Contract.objects.create(
            client=self.client_obj, 
            sales_contact=self.commercial_user, 
            is_signed=False,
            total_amount=1000.00,  
            remaining_amount=500.00,  
            creation_date='2023-01-01'  
            )    
       
        self.assigned_event = Event.objects.create(
            
            support_contact=self.support_user,
            start_date = timezone.make_aware(datetime.datetime(2023, 1, 15)),
            end_date = timezone.make_aware(datetime.datetime(2023, 1, 20)),
            location = 'Test Location',
            attendees = 50,
            client_name = self.client_obj,
            contract=self.sample_contract, 
        )
        self.unassigned_event = Event.objects.create(
            
            support_contact=None,
            start_date = timezone.make_aware(datetime.datetime(2023, 1, 15)),
            end_date = timezone.make_aware(datetime.datetime(2023, 1, 20)),
            location = 'Test Location',
            attendees = 50,
            client_name = self.client_obj,
            contract=self.sample_contract, 
            
        )
        
    def test_support_user_can_read_all_events(self):
        url = reverse('event-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK    
        
    def test_support_user_can_update_assigned_event(self):
        url = reverse('event-detail', kwargs={'pk': self.assigned_event.pk})
        update_data = {
            'attendees' : 500,
        }
        response = self.client.patch(url, update_data)
        assert response.status_code == status.HTTP_200_OK
        
    def test_support_user_cannot_update_unassigned_event(self):
        url = reverse('event-detail', kwargs={'pk': self.unassigned_event.pk})
        update_data = {
            'location' : 'Acapulco',
        }
        response = self.client.patch(url, update_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_support_user_cannot_create_event(self):
        url = reverse('event-list')
        event_data = {
            'event_date': '2023-01-10',
            'start_date': '2023-01-15',
            'end_date': '2023-01-20',
            'location': 'Test Location',
            'attendees': 50,        
            'notes': 'Test Event',
            'client_name' : self.client_obj,
            'contract':self.sample_contract, 
        }
        response = self.client.post(url, event_data)
        assert response.status_code in (status.HTTP_403_FORBIDDEN, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_support_user_cannot_delete_event(self):
        url = reverse('event-detail', kwargs={'pk': self.assigned_event.pk})
        response = self.client.delete(url)
        assert response.status_code in (status.HTTP_403_FORBIDDEN, status.HTTP_405_METHOD_NOT_ALLOWED)