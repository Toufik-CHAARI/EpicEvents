from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
import pytest
from django.urls import reverse
from unittest.mock import Mock
from crm.models import Client, Contract, Event


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def mock_client_object(mocker):
    mock_client = Mock(spec=Client)
    mock_client.id = 1
    mocker.patch(
        "crm.models.Client.objects.get", return_value=mock_client
    )
    return mock_client


@pytest.fixture
def management_user(db):
    User = get_user_model()
    return User.objects.create_user(
        username="manager", password="testpass123", role="management"
    )


def test_management_can_see_all_clients(mocker, management_user):
    api_client = APIClient()
    api_client.force_authenticate(user=management_user)

    response = api_client.get(reverse("client-list"))

    assert response.status_code == status.HTTP_200_OK


def test_management_cannot_create_client(mocker, management_user):
    api_client = APIClient()
    api_client.force_authenticate(user=management_user)

    response = api_client.post(reverse("client-list"), {})

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_management_cannot_delete_client(
    api_client, mock_client_object, management_user
):
    api_client.force_authenticate(user=management_user)

    url = reverse("client-detail", args=[mock_client_object.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_management_cannot_update_client(
    api_client, mock_client_object, management_user
):
    api_client = APIClient()
    api_client.force_authenticate(user=management_user)

    response = api_client.patch(
        reverse("client-detail", args=[mock_client_object.id]), {}
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_management_can_read_all_users(mocker):
    api_client = APIClient()
    User = get_user_model()
    management_user = User.objects.create_user(
        username="manager", password="password", role="management"
    )
    api_client.force_authenticate(user=management_user)

    url = reverse("user-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_management_can_create_user(mocker):
    api_client = APIClient()
    User = get_user_model()
    management_user = User.objects.create_user(
        username="manager", password="password", role="management"
    )
    api_client.force_authenticate(user=management_user)

    url = reverse("user-create")
    user_data = {
        "username": "newuser",
        "password": "newpass123",
        "role": "support",
        "email": "newuser@gmail.com",
    }
    response = api_client.post(url, user_data)

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_management_can_update_user(mocker):
    api_client = APIClient()
    User = get_user_model()
    management_user = User.objects.create_user(
        username="manager", password="password", role="management"
    )
    api_client.force_authenticate(user=management_user)

    user_to_update = User.objects.create_user(
        username="existinguser", password="password", role="commercial"
    )

    url = reverse("user-update", args=[user_to_update.id])

    update_data = {
        "username": "updateduser",
        "role": "support",
        "password": "password",
    }
    response = api_client.put(url, update_data, format="json")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_management_can_delete_user(mocker):
    api_client = APIClient()
    User = get_user_model()
    management_user = User.objects.create_user(
        username="manager", password="password", role="management"
    )
    api_client.force_authenticate(user=management_user)
    user_to_delete = User.objects.create_user(
        username="deleteuser", password="password", role="user_role"
    )
    url = reverse("user-delete", args=[user_to_delete.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_management_can_read_all_contracts(mocker):
    api_client = APIClient()
    mocked_user = mocker.patch(
        "rest_framework.request.Request.user", create=True
    )
    mocked_user.return_value.is_authenticated = True
    mocked_user.return_value.role = "management"

    mocked_queryset = mocker.patch(
        "crm.views.ContractViewSet.get_queryset"
    )
    mocked_queryset.return_value = mocker.MagicMock()

    url = reverse("contract-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_management_can_create_contracts():
    api_client = APIClient()
    User = get_user_model()
    management_user = User.objects.create_user(
        username="manager", password="password", role="management"
    )
    api_client.force_authenticate(user=management_user)

    url = reverse("contract-list")

    client = Client.objects.create(
        full_name="Test Client",
        email="testclient@example.com",
        phone="1234567890",
        company_name="Test Company",
        creation_date="2023-01-15",
        last_update="2023-01-15",
    )

    contract_data = {
        "total_amount": 15000.00,
        "remaining_amount": 5000.00,
        "creation_date": "2023-12-17",
        "is_signed": True,
        "client": client.id,
        "sales_contact": management_user.id,
    }

    response = api_client.post(url, contract_data, format="json")
    print(response.data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_management_can_update_contracts():
    api_client = APIClient()
    User = get_user_model()
    management_user = User.objects.create_user(
        username="manager", password="password", role="management"
    )
    api_client.force_authenticate(user=management_user)

    client = Client.objects.create(
        full_name="Test Client",
        email="testclient@example.com",
        phone="1234567890",
        company_name="Test Company",
        creation_date="2023-01-15",
        last_update="2023-01-15",
    )

    contract = Contract.objects.create(
        sales_contact=management_user,
        total_amount=15000.00,
        remaining_amount=5000.00,
        creation_date="2023-12-17",
        is_signed=True,
        client=client,
    )

    url = reverse("contract-detail", args=[contract.id])

    update_data = {
        "total_amount": 20000.00,
        "remaining_amount": 3000.00,
        "creation_date": "2023-12-17",
        "client": client.id,
    }

    response = api_client.put(url, update_data, format="json")
    print(response.data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_management_cannot_delete_contracts():
    api_client = APIClient()
    User = get_user_model()
    management_user = User.objects.create_user(
        username="manager", password="password", role="management"
    )
    api_client.force_authenticate(user=management_user)

    client = Client.objects.create(
        full_name="Test Client",
        email="testclient@example.com",
        phone="1234567890",
        company_name="Test Company",
        creation_date="2023-01-15",
        last_update="2023-01-15",
    )
    contract = Contract.objects.create(
        sales_contact=management_user,
        total_amount=15000.00,
        remaining_amount=5000.00,
        creation_date="2023-12-17",
        is_signed=True,
        client=client,
    )

    url = reverse("contract-detail", args=[contract.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_management_can_see_all_events():
    api_client = APIClient()
    User = get_user_model()
    management_user = User.objects.create_user(
        username="manager", password="password", role="management"
    )
    api_client.force_authenticate(user=management_user)

    url = reverse("event-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_management_can_update_events():
    api_client = APIClient()
    User = get_user_model()
    management_user = User.objects.create_user(
        username="manager", password="password", role="management"
    )
    api_client.force_authenticate(user=management_user)

    client = Client.objects.create(
        full_name="Test Client",
        email="testclient@example.com",
        phone="1234567890",
        company_name="Test Company",
        creation_date="2023-01-15",
        last_update="2023-01-15",
    )
    contract = Contract.objects.create(
        sales_contact=management_user,
        total_amount=15000.00,
        remaining_amount=5000.00,
        creation_date="2023-12-17",
        is_signed=True,
        client=client,
    )

    event = Event.objects.create(
        support_contact=management_user,
        start_date="2024-02-28T14:46:00Z",
        end_date="2024-03-03T14:46:00Z",
        location="ultime test",
        attendees=2,
        notes="grose soiree ",
        contract=contract,
        client_name=client,
    )

    update_data = {
        "start_date": "2024-02-28T14:46:00Z",
        "end_date": "2024-03-03T14:46:00Z",
        "location": "Mexico",
        "attendees": 200,
        "notes": "grosse soiree arrosée ",
        "contract": contract.id,
        "client_name": client.id,
    }

    url = reverse("event-detail", args=[event.id])
    response = api_client.put(url, update_data, format="json")
    print(response.data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_management_cannot_create_events():
    api_client = APIClient()
    User = get_user_model()
    management_user = User.objects.create_user(
        username="manager", password="password", role="management"
    )
    api_client.force_authenticate(user=management_user)

    url = reverse("event-list")
    event_data = {
        "start_date": "2024-02-28T14:46:00Z",
        "end_date": "2024-03-03T14:46:00Z",
        "location": "Principauté de Monaco",
        "attendees": 25,
        "notes": "Hello Sed convallis tellus at urna iaculis",
        "contract": 7,
        "client_name": 3,
    }

    response = api_client.post(url, event_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_management_cannot_delete_events():
    api_client = APIClient()
    User = get_user_model()
    management_user = User.objects.create_user(
        username="manager", password="password", role="management"
    )
    api_client.force_authenticate(user=management_user)

    client = Client.objects.create(
        full_name="Test Client",
        email="testclient@example.com",
        phone="1234567890",
        company_name="Test Company",
        creation_date="2023-01-15",
        last_update="2023-01-15",
    )
    contract = Contract.objects.create(
        sales_contact=management_user,
        total_amount=15000.00,
        remaining_amount=5000.00,
        creation_date="2023-12-17",
        is_signed=True,
        client=client,
    )

    event = Event.objects.create(
        support_contact=management_user,
        start_date="2024-02-28T14:46:00Z",
        end_date="2024-03-03T14:46:00Z",
        location="Principauté de Monaco",
        attendees=25,
        notes="Hello Sed convallis tellus at urna iaculis ultrices.",
        contract=contract,
        client_name=client,
    )

    url = reverse("event-detail", args=[event.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
