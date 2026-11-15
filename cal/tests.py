from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import ColorCode, CreateCode, ItemType, MaterialGroup


class DependencyUpgradeTests(TestCase):
    """Exercise authentication, calculator APIs, and persistence after upgrades."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user('operator', password='test-only-password')
        cls.admin = get_user_model().objects.create_superuser('administrator', password='test-only-password')
        cls.materials = {}
        for pk, name, group, hierarchy in [
            (1, 'Yes', 'A', ''), (2, 'Liquid', 'L', 'L'),
            (3, 'Solvent', 'S', 'S'), (4, 'Additive type', 'T', ''),
            (13, 'Blue', 'B', ''),
        ]:
            item_type = ItemType.objects.create(pk=pk, name=name)
            cls.materials[pk] = MaterialGroup.objects.create(
                pk=pk, item_name=name, material_group=group,
                product_hierarchy_a=hierarchy, product_hierarchy_b=hierarchy,
                item_type_choice=item_type,
            )
        cls.color = ColorCode.objects.create(
            color_code='BLUE-01', material_group='B01', color_type_choice=cls.materials[13]
        )

    def test_home_and_login_render(self):
        self.assertEqual(self.client.get(reverse('index')).status_code, 200)
        self.assertContains(self.client.get(reverse('login')), 'name="username"')

    def test_login_and_post_logout(self):
        response = self.client.post(reverse('login'), {'username': 'operator', 'password': 'test-only-password'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.get(reverse('create_code')).status_code, 200)
        self.assertEqual(self.client.post(reverse('logout')).status_code, 302)
        self.assertEqual(self.client.get(reverse('create_code')).status_code, 302)

    def test_protected_routes_require_authentication(self):
        for name in ['create_code', 'code_list', 'populate-fields', 'get-value', 'get-color-choice']:
            with self.subTest(route=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 302)

    def test_operator_pages_and_material_access(self):
        self.client.force_login(self.user)
        for name in ['create_code', 'code_list']:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)
        self.assertEqual(self.client.get(reverse('material_list')).status_code, 403)

    def test_admin_material_forms_render(self):
        self.client.force_login(self.admin)
        for name in ['material_list', 'create_item', 'create_color_code']:
            with self.subTest(route=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_dependent_selection_api(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('populate-fields'), {'additive': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['swu'][0]['id'], 3)
        self.assertEqual(response.json()['additive_type'][0]['id'], 4)

    def test_generated_material_and_hierarchy(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('get-value'), {
            'additive': '1', 'liquied_narrow': '2', 'swu': '3', 'additive_type': '4'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['material_group'], 'L-ATX')
        self.assertEqual(response.json()['product_hierarchy_a'], '0LS')

    def test_color_choices(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('get-color-choice'), {'color_type': '13'})
        self.assertEqual(response.json(), [{'id': self.color.pk, 'color_code': 'BLUE-01'}])

    def test_calculated_code_can_be_saved_and_viewed(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('create_code'), {
            'additive': '1', 'liquied_narrow': '2', 'swu': '3', 'additive_type': '4',
            'mg_code': 'L-ATX', 'ph_code': '0LS',
        })
        self.assertEqual(CreateCode.objects.count(), 1)
        code = CreateCode.objects.get()
        self.assertRedirects(response, reverse('code_detail', args=[code.pk]))
        self.assertEqual(code.mg_code, 'L-ATX')
        self.assertContains(self.client.get(reverse('code_list')), 'L-ATX')
