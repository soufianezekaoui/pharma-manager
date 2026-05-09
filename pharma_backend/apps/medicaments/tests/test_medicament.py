"""
Tests for the Medicament module.
"""
from decimal import Decimal

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.categories.models import Categorie
from apps.medicaments.models import Medicament
from apps.users.models import User


def make_user(role="pharmacist", username="test_ph"):
    return User.objects.create_user(
        username=username, email=f"{username}@test.ma",
        password="Test1234!", role=role
    )


def auth_header(user):
    token = RefreshToken.for_user(user)
    return {"HTTP_AUTHORIZATION": f"Bearer {token.access_token}"}


def make_categorie(nom="Antibiotiques"):
    return Categorie.objects.create(nom=nom, description="Test")


def make_medicament(categorie=None, **kwargs):
    defaults = dict(
        nom="Amoxicilline",
        prix_achat=Decimal("10.00"),
        prix_vente=Decimal("15.00"),
        stock_actuel=100,
        stock_minimum=10,
    )
    defaults.update(kwargs)
    if categorie:
        defaults["categorie"] = categorie
    return Medicament.objects.create(**defaults)


class MedicamentModelTest(TestCase):
    def test_str(self):
        m = Medicament(nom="Paracetamol", dosage="500mg")
        self.assertIn("Paracetamol", str(m))

    def test_is_low_stock(self):
        m = Medicament(stock_actuel=5, stock_minimum=10)
        self.assertTrue(m.is_low_stock)

    def test_not_low_stock(self):
        m = Medicament(stock_actuel=50, stock_minimum=10)
        self.assertFalse(m.is_low_stock)

    def test_is_expired(self):
        from datetime import date
        m = Medicament(date_expiration=date(2020, 1, 1))
        self.assertTrue(m.is_expired)

    def test_not_expired(self):
        from datetime import date, timedelta
        future = date.today() + timedelta(days=30)
        m = Medicament(date_expiration=future)
        self.assertFalse(m.is_expired)


class MedicamentAPITest(TestCase):
    def setUp(self):
        self.api = APIClient()
        self.pharmacist = make_user("pharmacist", "ph1")
        self.client_user = make_user("client", "cl1")
        self.cat = make_categorie()
        self.med = make_medicament(self.cat)

    def _auth(self, user):
        token = RefreshToken.for_user(user)
        self.api.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

    def test_list_active(self):
        self._auth(self.pharmacist)
        resp = self.api.get("/api/medicaments/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_success(self):
        self._auth(self.pharmacist)
        resp = self.api.post("/api/medicaments/", {
            "nom": "Ibuprofene",
            "prix_achat": "8.00",
            "prix_vente": "12.00",
            "stock_actuel": 50,
            "stock_minimum": 5,
            "categorie": self.cat.pk,
        }, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_create_prix_vente_less_than_achat(self):
        self._auth(self.pharmacist)
        resp = self.api.post("/api/medicaments/", {
            "nom": "Bad Drug",
            "prix_achat": "20.00",
            "prix_vente": "10.00",
            "stock_actuel": 10,
            "stock_minimum": 2,
        }, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_client_cannot_create(self):
        self._auth(self.client_user)
        resp = self.api.post("/api/medicaments/", {
            "nom": "X", "prix_achat": "1", "prix_vente": "2",
            "stock_actuel": 5, "stock_minimum": 1,
        }, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_soft_delete(self):
        self._auth(self.pharmacist)
        resp = self.api.delete(f"/api/medicaments/{self.med.pk}/")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.med.refresh_from_db()
        self.assertFalse(self.med.est_actif)

    def test_restock(self):
        self._auth(self.pharmacist)
        initial = self.med.stock_actuel
        resp = self.api.post(
            f"/api/medicaments/{self.med.pk}/restock/",
            {"quantite": 20}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.med.refresh_from_db()
        self.assertEqual(self.med.stock_actuel, initial + 20)

    def test_alertes_stock(self):
        self._auth(self.pharmacist)
        # Create a low-stock medication
        make_medicament(self.cat, nom="LowDrug", stock_actuel=2, stock_minimum=10)
        resp = self.api.get("/api/medicaments/alertes-stock/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(resp.data["count"], 1)
