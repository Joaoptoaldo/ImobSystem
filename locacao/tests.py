from django.test import TestCase, Client
from django.urls import reverse
from .models import Client, Immobile, RegisterLocation
from .forms import ClientForm, ImmobileForm, RegisterLocationForm
from datetime import datetime, timedelta
from django.contrib.auth.models import User

# Create your tests here.
class AuthRedirectTest(TestCase):
    def setUp(self):
        self.immobile = Immobile.objects.create(code='T001', type_item='AP', address='Test Address', price=1000)

    def test_redirect_if_not_logged_in(self):
        """
        verifica se as views protegidas redirecionam para a página de login
        """
        urls = {
            'client-create': None,
            'immobile-create': None,
            'reports': None,
            'location-create': [self.immobile.pk],
        }
        for url_name, args in urls.items():
            url = reverse(url_name, args=args)
            response = self.client.get(url)
            self.assertRedirects(response, f"{reverse('login')}?next={url}")


class FormValidationTest(TestCase):
    def test_duplicate_client_email(self):
        """
        testa que o ClientForm gera um erro de validação para um e-mail duplicado
        """
        Client.objects.create(name='Test User', email='test@test.com', phone='123456789')
        form_data = {'name': 'Another User', 'email': 'test@test.com', 'phone': '987654321'}
        form = ClientForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'][0], 'Este e-mail já está cadastrado em nosso sistema.')

    def test_duplicate_immobile_code(self):
        """
        testa que o ImmobileForm gera um erro de validação para um código duplicado
        """
        Immobile.objects.create(code='T001', type_item='AP', address='Test Address', price=1000)
        form_data = {'code': 'T001', 'type_item': 'CA', 'address': 'Another Address', 'price': 1500}
        form = ImmobileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('code', form.errors)
        self.assertEqual(form.errors['code'][0], 'Este código de imóvel já está cadastrado em nosso sistema.')

    def test_invalid_location_dates(self):
        """
        testa que o RegisterLocationForm gera um erro de validação se a data de início for posterior à data de término
        """
        client = Client.objects.create(name='Test User', email='test@test.com', phone='123456789')
        dt_start = datetime.now()
        dt_end = dt_start - timedelta(days=1)
        form_data = {
            'client': client.pk,
            'dt_start': dt_start.strftime('%Y-%m-%d'),
            'dt_end': dt_end.strftime('%Y-%m-%d'),
        }
        form = RegisterLocationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertEqual(form.errors['__all__'][0], 'A data de início deve ser menor que a data de fim.')


class ReportsViewTest(TestCase):
    def setUp(self):
        # Create user and log in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Create clients
        self.client1 = Client.objects.create(name='John Doe', email='john@test.com', phone='111')
        self.client2 = Client.objects.create(name='Jane Smith', email='jane@test.com', phone='222')

        # Create immobiles
        self.immobile1 = Immobile.objects.create(code='A001', type_item='AP', address='Addr 1', price=1000, is_locate=True)
        self.immobile2 = Immobile.objects.create(code='C002', type_item='CA', address='Addr 2', price=2000, is_locate=True)
        self.immobile3 = Immobile.objects.create(code='A003', type_item='AP', address='Addr 3', price=1500, is_locate=False)

        # Create locations
        self.location1 = RegisterLocation.objects.create(
            client=self.client1,
            immobile=self.immobile1,
            dt_start=datetime.now() - timedelta(days=10),
            dt_end=datetime.now() + timedelta(days=20),
        )
        self.location2 = RegisterLocation.objects.create(
            client=self.client2,
            immobile=self.immobile2,
            dt_start=datetime.now() - timedelta(days=5),
            dt_end=datetime.now() + timedelta(days=25),
        )

    def test_reports_filter_bug(self):
        """
        testa que a view de relatórios filtra corretamente os imóveis por múltiplos critérios
        """
        response = self.client.get(reverse('reports'), {'client': 'John', 'is_locate': 'True', 'type_item': 'AP'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A001')
        self.assertNotContains(response, 'C002')
        self.assertNotContains(response, 'A003')
        self.assertEqual(len(response.context['immobiles']), 1)


class ReportsViewFixTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.client1 = Client.objects.create(name='Client One', email='one@test.com', phone='111')
        self.client2 = Client.objects.create(name='Client Two', email='two@test.com', phone='222')
        self.immobile1 = Immobile.objects.create(code='A001', type_item='APARTAMENTO', address='Addr 1', price=1000, is_locate=True)

        # Location 1: Client 1, created on 2025-01-15
        self.location1 = RegisterLocation.objects.create(
            client=self.client1,
            immobile=self.immobile1,
            dt_start=datetime(2025, 1, 1),
            dt_end=datetime(2025, 1, 31),
            create_at=datetime(2025, 1, 15).date()
        )
        # Location 2: Client 2, created on 2025-03-15
        self.location2 = RegisterLocation.objects.create(
            client=self.client2,
            immobile=self.immobile1,
            dt_start=datetime(2025, 3, 1),
            dt_end=datetime(2025, 3, 31),
            create_at=datetime(2025, 3, 15).date()
        )

    def test_reports_filter_logic_corrected(self):
        """
        testa que o filtro de relatórios filtra corretamente os imóveis por múltiplos critérios
        """
        response = self.client.get(reverse('reports'), {
            'client': 'Client One',
            'dt_start': '2025-03-01',
            'dt_end': '2025-03-31'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['immobiles']), 0)


class FormLocationViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.client_renter = Client.objects.create(name='Renter', email='renter@test.com', phone='333')
        self.immobile_available = Immobile.objects.create(code='AV01', type_item='CASA', address='Available', price=500, is_locate=False)
        self.immobile_located = Immobile.objects.create(code='LOC01', type_item='CASA', address='Located', price=500, is_locate=True)

    def test_form_location_success(self):
        """
        testa a criação bem-sucedida de uma locação
        """
        form_data = {
            'client': self.client_renter.pk,
            'dt_start': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'dt_end': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'),
        }
        response = self.client.post(reverse('location-create', args=[self.immobile_available.pk]), data=form_data)
        self.assertRedirects(response, reverse('list-location'))
        self.immobile_available.refresh_from_db()
        self.assertTrue(self.immobile_available.is_locate)
        self.assertTrue(RegisterLocation.objects.filter(immobile=self.immobile_available, client=self.client_renter).exists())

    def test_form_location_for_already_located_immobile_returns_404(self):
        """
        testa que tentar acessar o formulário de um imóvel já localizado retorna um 404
        """
        response = self.client.get(reverse('location-create', args=[self.immobile_located.pk]))
        self.assertEqual(response.status_code, 404)

