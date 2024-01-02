import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from crm.models import Client, Contract
import datetime
from authentication.models import CustomUser


@pytest.fixture
def api_client():
    return APIClient()


# Fixtures
@pytest.fixture
def commercial_user(db):
    return get_user_model().objects.create_user(
        username="commercial", password="testpass123", role="commercial"
    )


@pytest.fixture
def support_user(db):
    return get_user_model().objects.create_user(
        username="support", password="testpass123", role="support"
    )


@pytest.fixture
def management_user(db):
    return get_user_model().objects.create_user(
        username="management", password="testpass123", role="management"
    )


@pytest.fixture
def client_data():
    return {
        "full_name": "Test Client",
        "email": "client@example.com",
        "phone": "1234567890",
        "company_name": "Test Company",
        "creation_date": "2021-01-01",
        "last_update": "2021-01-01",
    }


@pytest.mark.django_db
def test_commercial_create_client(
    commercial_user, api_client, client_data
):
    api_client.force_authenticate(user=commercial_user)
    response = api_client.post(reverse("client-list"), client_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Client.objects.count() == 1
    client = Client.objects.first()
    assert client.full_name == "Test Client"
    assert client.sales_contact == commercial_user


@pytest.mark.django_db
def test_commercial_update_client(
    commercial_user, api_client, client_data
):
    client = Client.objects.create(
        **client_data, sales_contact=commercial_user
    )
    api_client.force_authenticate(user=commercial_user)
    updated_data = {"full_name": "Updated Client"}
    response = api_client.patch(
        reverse("client-detail", args=[client.id]), updated_data
    )
    assert response.status_code == status.HTTP_200_OK
    client.refresh_from_db()
    assert client.full_name == "Updated Client"


@pytest.mark.django_db
def test_support_user_read_only_access(
    support_user, api_client, client_data, commercial_user
):
    client = Client.objects.create(
        **client_data, sales_contact=commercial_user
    )
    api_client.force_authenticate(user=support_user)
    response = api_client.get(
        reverse("client-detail", args=[client.id])
    )
    assert response.status_code == status.HTTP_200_OK
    # Attempt to update client
    updated_data = {"full_name": "Unauthorized Update"}
    response = api_client.patch(
        reverse("client-detail", args=[client.id]), updated_data
    )
    assert response.status_code in [
        status.HTTP_403_FORBIDDEN,
        status.HTTP_401_UNAUTHORIZED,
    ]


@pytest.mark.django_db
def test_management_user_read_only_access(
    management_user, api_client, client_data, commercial_user
):
    client = Client.objects.create(
        **client_data, sales_contact=commercial_user
    )
    api_client.force_authenticate(user=management_user)
    response = api_client.get(
        reverse("client-detail", args=[client.id])
    )
    assert response.status_code == status.HTTP_200_OK
    # Attempt to update client
    updated_data = {"full_name": "Unauthorized Update"}
    response = api_client.patch(
        reverse("client-detail", args=[client.id]), updated_data
    )
    assert response.status_code in [
        status.HTTP_403_FORBIDDEN,
        status.HTTP_401_UNAUTHORIZED,
    ]


@pytest.mark.django_db
def test_authenticated_user_view_client_details(
    api_client, client_data, commercial_user
):
    client = Client.objects.create(
        **client_data, sales_contact=commercial_user
    )
    api_client.force_authenticate(user=commercial_user)
    response = api_client.get(
        reverse("client-detail", args=[client.id])
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["full_name"] == "Test Client"


@pytest.mark.django_db
def test_unauthenticated_user_actions(api_client, client_data):
    response = api_client.post(reverse("client-list"), client_data)
    assert response.status_code in [
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    ]

    commercial_user = get_user_model().objects.create_user(
        username="temp_commercial", password="pass", role="commercial"
    )
    client = Client.objects.create(
        **client_data, sales_contact=commercial_user
    )

    response = api_client.get(
        reverse("client-detail", args=[client.id])
    )
    assert response.status_code in [
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    ]

    updated_data = {"full_name": "Unauthorized Update"}
    response = api_client.patch(
        reverse("client-detail", args=[client.id]), updated_data
    )
    assert response.status_code in [
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    ]

    response = api_client.delete(
        reverse("client-detail", args=[client.id])
    )
    assert response.status_code in [
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    ]


@pytest.fixture
def create_contracts(db, commercial_user):
    Client.objects.create(
        full_name="Test Client",
        email="client@example.com",
        sales_contact=commercial_user,
        creation_date=datetime.date.today(),
        last_update=datetime.date.today(),
    )


@pytest.mark.django_db
def test_commercial_user_view_unsigned_contracts(
    commercial_user, api_client
):
    api_client.force_authenticate(user=commercial_user)

    client = Client.objects.create(
        full_name="Test Client",
        email="client@example.com",
        sales_contact=commercial_user,
        creation_date="2023-01-01",
        last_update="2023-01-01",
    )

    Contract.objects.create(
        client=client,
        sales_contact=commercial_user,
        is_signed=False,
        total_amount=1000.00,
        remaining_amount=500.00,
        creation_date="2023-01-01",
    )

    response = api_client.get(reverse("commercial-unsigned-contracts"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_commercial_user_view_remaining_amount_contracts(
    commercial_user, api_client
):
    api_client.force_authenticate(user=commercial_user)

    client = Client.objects.create(
        full_name="Test Client",
        email="client@example.com",
        sales_contact=commercial_user,
        creation_date="2023-01-01",
        last_update="2023-01-01",
    )

    Contract.objects.create(
        client=client,
        sales_contact=commercial_user,
        is_signed=True,
        total_amount=1000.00,
        remaining_amount=500.00,
        creation_date="2023-01-01",
    )

    response = api_client.get(
        reverse("commercial-remaining-amount-contracts")
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


#
@pytest.mark.django_db
@pytest.mark.parametrize(
    "view_name",
    [
        "commercial-unsigned-contracts",
        "commercial-remaining-amount-contracts",
    ],
)
def test_non_commercial_user_no_contracts(
    support_user, api_client, create_contracts, view_name
):
    api_client.force_authenticate(user=support_user)
    response = api_client.get(reverse(view_name))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


@pytest.fixture
def commercial_user_for_contract_test(db):
    return CustomUser.objects.create_user(
        username="commercial_user_contract_test",
        password="testpass123",
        role="commercial",
    )


@pytest.fixture
def client_data_for_contract_test(commercial_user_for_contract_test):
    return Client.objects.create(
        full_name="Test Client",
        email="client@example.com",
        phone="1234567890",
        company_name="Test Company",
        creation_date="2023-01-01",
        last_update="2023-01-01",
        sales_contact=commercial_user_for_contract_test,
    )


@pytest.fixture
def contract_data_for_contract_test(client_data_for_contract_test):
    return Contract.objects.create(
        client=client_data_for_contract_test,
        sales_contact=client_data_for_contract_test.sales_contact,
        total_amount=1000.00,
        remaining_amount=500.00,
        creation_date=datetime.date.today(),
        is_signed=False,
    )


@pytest.mark.django_db
def test_commercial_user_update_contract(
    commercial_user_for_contract_test,
    api_client,
    contract_data_for_contract_test,
):
    api_client.force_authenticate(
        user=commercial_user_for_contract_test
    )

    updated_data = {
        "client": contract_data_for_contract_test.client.id,
        "sales_contact": contract_data_for_contract_test.sales_contact.id,
        "total_amount": 1200.00,
        "remaining_amount": 600.00,
        "creation_date": contract_data_for_contract_test.creation_date,
        "is_signed": True,
    }

    response = api_client.put(
        reverse(
            "contract-detail",
            kwargs={"pk": contract_data_for_contract_test.id},
        ),
        updated_data,
    )
    assert response.status_code == status.HTTP_200_OK
    contract_data_for_contract_test.refresh_from_db()
    assert (
        contract_data_for_contract_test.total_amount
        == updated_data["total_amount"]
    )
    assert (
        contract_data_for_contract_test.remaining_amount
        == updated_data["remaining_amount"]
    )
    assert (
        contract_data_for_contract_test.is_signed
        == updated_data["is_signed"]
    )


@pytest.fixture
def client_assigned_to_commercial(commercial_user):
    return Client.objects.create(
        full_name="Test Client",
        email="client@example.com",
        sales_contact=commercial_user,
        creation_date=datetime.date.today(),
        last_update=datetime.date.today(),
    )


@pytest.fixture
def signed_contract(client_assigned_to_commercial, commercial_user):
    return Contract.objects.create(
        client=client_assigned_to_commercial,
        sales_contact=commercial_user,
        total_amount=1000.00,
        remaining_amount=0.00,
        creation_date=datetime.date.today(),
        is_signed=True,
    )


@pytest.fixture
def unsigned_contract(client_assigned_to_commercial, commercial_user):
    return Contract.objects.create(
        client=client_assigned_to_commercial,
        sales_contact=commercial_user,
        total_amount=1000.00,
        remaining_amount=500.00,
        creation_date=datetime.date.today(),
        is_signed=False,
    )


@pytest.fixture
def event_data(signed_contract):
    return {
        "contract": signed_contract.id,
        "event_date": "2023-01-10",
        "start_date": "2023-01-15",
        "end_date": "2023-01-20",
        "location": "Test Location",
        "attendees": 50,
        "client_name": signed_contract.client.id,
        "notes": "Test Event",
    }


@pytest.mark.django_db
def test_create_event_signed_contract(
    commercial_user, api_client, event_data
):
    api_client.force_authenticate(user=commercial_user)
    response = api_client.post(reverse("event-list"), event_data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_event_unsigned_contract(
    commercial_user, api_client, event_data, unsigned_contract
):
    api_client.force_authenticate(user=commercial_user)
    response = api_client.post(reverse("event-list"), event_data)
    print(response.data)  # Add this line for debugging
    assert response.status_code == status.HTTP_201_CREATED
