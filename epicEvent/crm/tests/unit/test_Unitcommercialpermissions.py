import pytest
from django.urls import reverse
from rest_framework import status
from crm.models import Client, Contract
from rest_framework.test import APIClient
from unittest.mock import Mock
from django.contrib.auth import get_user_model
from crm.serializers import ClientSerializer
from unittest.mock import MagicMock
from rest_framework.response import Response


@pytest.fixture
def api_client():
    return APIClient()


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


@pytest.fixture
def commercial_user(db):
    User = get_user_model()
    return User.objects.create_user(
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


def test_commercial_create_client_unit(
    mocker, commercial_user, api_client, client_data
):
    mocked_serializer_instance = mocker.Mock(spec=ClientSerializer)
    mocked_serializer_instance.data = {"id": 1, **client_data}
    mock_save = mocker.patch(
        "crm.serializers.ClientSerializer.save",
        return_value=mocked_serializer_instance,
    )

    api_client.force_authenticate(user=commercial_user)

    response = api_client.post(reverse("client-list"), client_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["full_name"] == "Test Client"
    mock_save.assert_called_once()


def test_commercial_update_client_unit(
    mocker, commercial_user, api_client, client_data
):
    mock_client = Mock(
        id=1, **client_data, sales_contact=commercial_user
    )

    mocker.patch(
        "crm.views.ClientViewSet.get_object", return_value=mock_client
    )
    mock_serializer = mocker.Mock(spec=ClientSerializer)
    mocker.patch.object(mock_serializer, "is_valid", return_value=True)
    mocker.patch.object(mock_serializer, "save")
    mock_serializer.data = {"id": mock_client.id, **client_data}
    mocker.patch(
        "crm.views.ClientViewSet.get_serializer",
        return_value=mock_serializer,
    )
    api_client.force_authenticate(user=commercial_user)

    updated_data = {"full_name": "Updated Client"}

    response = api_client.patch(
        reverse("client-detail", args=[mock_client.id]), updated_data
    )
    assert response.status_code == status.HTTP_200_OK
    mock_serializer.is_valid.assert_called_once()
    mock_serializer.save.assert_called_once()


def test_support_user_read_only_access_unit(
    mocker, support_user, api_client, client_data, commercial_user
):
    mock_client = Mock(
        id=1, **client_data, sales_contact=commercial_user
    )

    mocker.patch(
        "crm.views.ClientViewSet.get_object", return_value=mock_client
    )

    mock_serializer = mocker.Mock(spec=ClientSerializer)
    mock_serializer.data = {"id": mock_client.id, **client_data}

    mocker.patch(
        "crm.views.ClientViewSet.get_serializer",
        return_value=mock_serializer,
    )

    api_client.force_authenticate(user=support_user)

    response = api_client.get(
        reverse("client-detail", args=[mock_client.id])
    )

    assert response.status_code == status.HTTP_200_OK

    updated_data = {"full_name": "Unauthorized Update"}

    response = api_client.patch(
        reverse("client-detail", args=[mock_client.id]), updated_data
    )

    assert response.status_code in [
        status.HTTP_403_FORBIDDEN,
        status.HTTP_401_UNAUTHORIZED,
    ]
    mock_serializer.is_valid.assert_not_called()
    mock_serializer.save.assert_not_called()


def test_management_user_read_only_access_unit(
    mocker, management_user, api_client, client_data
):
    mock_client = Mock(id=1, **client_data, sales_contact=mocker.Mock())

    mocker.patch(
        "crm.views.ClientViewSet.get_object", return_value=mock_client
    )

    mock_serializer = mocker.Mock(spec=ClientSerializer)
    mocker.patch.object(mock_serializer, "is_valid", return_value=True)
    mocker.patch.object(mock_serializer, "save")
    mock_serializer.data = {"id": mock_client.id, **client_data}

    mocker.patch(
        "crm.views.ClientViewSet.get_serializer",
        return_value=mock_serializer,
    )

    api_client.force_authenticate(user=management_user)

    response = api_client.get(
        reverse("client-detail", args=[mock_client.id])
    )
    assert response.status_code == status.HTTP_200_OK

    updated_data = {"full_name": "Unauthorized Update"}
    response = api_client.patch(
        reverse("client-detail", args=[mock_client.id]), updated_data
    )

    assert response.status_code in [
        status.HTTP_403_FORBIDDEN,
        status.HTTP_401_UNAUTHORIZED,
    ]

    mock_serializer.save.assert_not_called()


def test_authenticated_user_view_client_details_unit(
    mocker, api_client, client_data, commercial_user
):
    mock_client = Mock(
        id=1, **client_data, sales_contact=commercial_user
    )

    mocker.patch(
        "crm.views.ClientViewSet.get_object", return_value=mock_client
    )

    mock_serializer = mocker.Mock(spec=ClientSerializer)
    mock_serializer.data = {"id": mock_client.id, **client_data}

    mocker.patch(
        "crm.views.ClientViewSet.get_serializer",
        return_value=mock_serializer,
    )

    api_client.force_authenticate(user=commercial_user)

    response = api_client.get(
        reverse("client-detail", args=[mock_client.id])
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["full_name"] == "Test Client"


def test_unauthenticated_user_actions_unit(
    mocker, api_client, client_data
):
    mocker.patch("crm.views.ClientViewSet.create")

    response = api_client.post(reverse("client-list"), client_data)
    assert response.status_code in [
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    ]

    mock_client = Mock(id=1, **client_data)

    mocker.patch(
        "crm.views.ClientViewSet.get_object", return_value=mock_client
    )

    response = api_client.get(
        reverse("client-detail", args=[mock_client.id])
    )
    assert response.status_code in [
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    ]

    updated_data = {"full_name": "Unauthorized Update"}
    response = api_client.patch(
        reverse("client-detail", args=[mock_client.id]), updated_data
    )
    assert response.status_code in [
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    ]

    response = api_client.delete(
        reverse("client-detail", args=[mock_client.id])
    )
    assert response.status_code in [
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    ]


def test_commercial_user_view_unsigned_contracts_unit(
    mocker, commercial_user, api_client
):
    mock_response_data = [
        {
            "id": 1,
            "client_id": 1,
            "sales_contact_id": commercial_user.id,
            "is_signed": False,
            "total_amount": 1000.00,
            "remaining_amount": 500.00,
            "creation_date": "2023-01-01",
        }
    ]

    mock_method = mocker.patch(
        "crm.views.CommercialUnsignedContractsView.list",
        return_value=Response(
            mock_response_data, status=status.HTTP_200_OK
        ),
    )

    api_client.force_authenticate(user=commercial_user)

    response = api_client.get(reverse("commercial-unsigned-contracts"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data == mock_response_data
    mock_method.assert_called_once()


@pytest.fixture
def client_assigned_to_commercial(mocker, commercial_user):
    mock_client = MagicMock()
    mock_client.sales_contact = commercial_user
    return mock_client


@pytest.fixture
def signed_contract(
    mocker, client_assigned_to_commercial, commercial_user
):
    mock_signed_contract = MagicMock()
    mock_signed_contract.id = int(1)
    mock_signed_contract.client = client_assigned_to_commercial
    mock_signed_contract.sales_contact = commercial_user
    mock_signed_contract.is_signed = True
    return mock_signed_contract


@pytest.fixture
def unsigned_contract(
    mocker, client_assigned_to_commercial, commercial_user
):
    mock_unsigned_contract = MagicMock()
    mock_unsigned_contract.id = int(1)
    mock_unsigned_contract.client = client_assigned_to_commercial
    mock_unsigned_contract.sales_contact = commercial_user
    mock_unsigned_contract.is_signed = False
    return mock_unsigned_contract


@pytest.fixture
def event_data():
    def _event_data(contract):
        return {
            "contract": int(contract.id) if contract else None,
            "event_date": "2023-01-10",
            "start_date": "2023-01-15",
            "end_date": "2023-01-20",
            "location": "Test Location",
            "attendees": 50,
            "client_name": int(contract.client.id)
            if contract and contract.client
            else None,
            "notes": "Test Event",
        }

    return _event_data


@pytest.fixture
def test_client(db):
    return Client.objects.create(
        full_name="Test Client",
        email="testclient@example.com",
        phone="1234567890",
        company_name="Test Company",
        creation_date="2023-01-15",
        last_update="2023-01-15",
    )


@pytest.fixture
def test_contract(db, test_client, commercial_user):
    test_client.sales_contact = commercial_user
    test_client.save()
    return Contract.objects.create(
        client=test_client,
        sales_contact=commercial_user,
        total_amount=1000,
        remaining_amount=0,
        creation_date="2023-01-15",
        is_signed=True,
    )


def test_create_event_signed_contract(
    api_client, test_contract, commercial_user
):
    api_client.force_authenticate(user=commercial_user)
    event_data = {
        "contract": test_contract.id,
        "event_date": "2023-01-10",
        "start_date": "2023-01-15",
        "end_date": "2023-01-20",
        "location": "Test Location",
        "attendees": 50,
        "client_name": test_contract.client.id,
        "notes": "Test Event",
    }
    response = api_client.post(reverse("event-list"), event_data)
    print(response.data)
    assert response.status_code == status.HTTP_201_CREATED


def test_create_event_unsigned_contract(
    mocker, commercial_user, api_client, event_data, unsigned_contract
):
    unsigned_event_data = event_data(unsigned_contract)
    mocker.patch("crm.models.Event.objects.create")
    api_client.force_authenticate(user=commercial_user)
    response = api_client.post(
        reverse("event-list"), unsigned_event_data
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_commercial_user_cannot_access_user_list(
    commercial_user, api_client
):
    api_client.force_authenticate(user=commercial_user)
    url = reverse("user-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_commercial_user_cannot_create_user(
    commercial_user, api_client
):
    api_client.force_authenticate(user=commercial_user)
    url = reverse("user-create")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_commercial_user_cannot_access_user_detail(
    commercial_user, api_client
):
    api_client.force_authenticate(user=commercial_user)
    url = reverse("user-detail", args=[commercial_user.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_commercial_user_cannot_update_user(
    commercial_user, api_client
):
    api_client.force_authenticate(user=commercial_user)
    url = reverse("user-update", args=[commercial_user.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_commercial_user_cannot_delete_user(
    commercial_user, api_client
):
    api_client.force_authenticate(user=commercial_user)
    url = reverse("user-delete", args=[commercial_user.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
