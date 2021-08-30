from django.http import response
from django.test import TestCase, Client
from rest_framework import status
from user_api.models import User
from bond_api.models import Bond
# Create your tests here.

class UsuarioTestCase(TestCase):
    
    def setUp(self):
        self.client=Client()
        self.user_seller = User.objects.create_user(
            email='juan@gmail.com',
            username='juan',
            password='1234'
            )
        self.user_buyer = User.objects.create_user(
            email='pablo@gmail.com',
            username='pablo',
            password='1234',
        )

        self.bonds_list_one=[
            {
                "type":"0123456789",
                "total_sell":1,
                "price_total":"1,000.0001"
            }
        ]
        self.bonds_list_many=[
            {
                "type":"0123456789",
                "total_sell":1,
                "price_total":"1,000.0001"
            },
            {
                "type":"nuevo0123456789",
                "total_sell":5,
                "price_total":"0.9991"
            },
            {
                "type":"nuevo0123456789",
                "total_sell":5,
                "price_total":"0.9992"
            }
        ] 

        self.bonds_list_one_type_error=[
            {
                "type":"012345678asd_9",
                "total_sell":1,
                "price_total":"1,000.0001"
            }
        ]

        self.bonds_list_one_total_sell_error=[
            {
                "type":"0123456789",
                "total_sell":'s',
                "price_total":"1,000.0001"
            }
        ]

        self.bonds_list_one_price_total_error=[
            {
                "type":"0123456789",
                "total_sell": 1,
                "price_total":"100,000,000.0001"
            }
        ]


    def test_user_buyer_creation(self):
        self.assertEqual(self.user_buyer.is_active,True)
        self.assertEqual(self.user_buyer.is_staff,False)
        self.assertEqual(self.user_buyer.is_superuser,False)

    def test_user_seller_creation(self):
        self.assertEqual(self.user_seller.is_active,True)
        self.assertEqual(self.user_seller.is_staff,False)
        self.assertEqual(self.user_seller.is_superuser,False)

    def test_login_error(self):
        response= self.client.post(
            '/api/token/',{
                'email':'juan@gmail.com',
                'password':'12345',
                }
        )
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        #print(response.data)


    def test_login_ok(self):
        response= self.client.post(
            '/api/token/',{
                'email':'juan@gmail.com',
                'password':'1234',
                }
        )
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_bonds_list_not_auth(self):
        response=self.client.get('/api/bonds/')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_bonds_list_auth(self):
        login= self.client.post(
            '/api/token/',{
                'email':'juan@gmail.com',
                'password':'1234',
                }
        )

        response=self.client.get(
            '/api/bonds/',
            HTTP_AUTHORIZATION='Bearer {}'.format(login.data['access']),
            content_type='application/json'
            )
        #print(response.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_bonds_list_usd_auth(self):
        login= self.client.post(
            '/api/token/',{
                'email':'juan@gmail.com',
                'password':'1234',
                }
        )

        response=self.client.get(
            '/api/bonds/usd',
            HTTP_AUTHORIZATION='Bearer {}'.format(login.data['access']),
            content_type='application/json'
            )
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        #print(response.data)

    def test_sell_bond_not_auth(self):
        response=self.client.post(
            '/api/sell_bonds/',
            content_type='application/json'
            )
        #print(response.data)

    def test_sell_bond_one_auth(self):
        login= self.client.post(
            '/api/token/',{
                'email':'juan@gmail.com',
                'password':'1234',
                }
        )

        response=self.client.post(
            '/api/sell_bonds/',
            data=self.bonds_list_one,
            HTTP_AUTHORIZATION='Bearer {}'.format(login.data['access']),
            content_type='application/json'
            )
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        #print(response.status_code,response.data)


    def test_sell_bond_many_auth(self):
        login= self.client.post(
            '/api/token/',{
                'email':'juan@gmail.com',
                'password':'1234',
                }
        )

        response=self.client.post(
            '/api/sell_bonds/',
            data=self.bonds_list_many,
            HTTP_AUTHORIZATION='Bearer {}'.format(login.data['access']),
            content_type='application/json'
            )
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        #print(response.status_code,response.data)


    def test_sell_bond_one_type_error(self):
        login= self.client.post(
            '/api/token/',{
                'email':'juan@gmail.com',
                'password':'1234',
                }
        )

        response=self.client.post(
            '/api/sell_bonds/',
            data=self.bonds_list_one_type_error,
            HTTP_AUTHORIZATION='Bearer {}'.format(login.data['access']),
            content_type='application/json'
            )
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

        def test_sell_bond_one_total_sell_error(self):
            login= self.client.post(
                '/api/token/',{
                    'email':'juan@gmail.com',
                    'password':'1234',
                    }
            )

            response=self.client.post(
                '/api/sell_bonds/',
                data=self.bonds_list_one_total_sell_error,
                HTTP_AUTHORIZATION='Bearer {}'.format(login.data['access']),
                content_type='application/json'
                )
            #self.assertEqual(response.status_code,status.HTTP_201_CREATED)

            #print(response.status_code,response.data)

    def test_sell_bond_one_price_total_error(self):
        login= self.client.post(
            '/api/token/',{
                'email':'juan@gmail.com',
                'password':'1234',
                }
        )

        response=self.client.post(
            '/api/sell_bonds/',
            data=self.bonds_list_one_price_total_error,
            HTTP_AUTHORIZATION='Bearer {}'.format(login.data['access']),
            content_type='application/json'
            )
        #print(response.status_code)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)


    def test_buy_bond_auth(self):
        login= self.client.post(
            '/api/token/',{
                'email':'juan@gmail.com',
                'password':'1234',
                }
        )

        response=self.client.post(
            '/api/sell_bonds/',
            data=self.bonds_list_many,
            HTTP_AUTHORIZATION='Bearer {}'.format(login.data['access']),
            content_type='application/json'
            )

        login= self.client.post(
            '/api/token/',{
                'email':'pablo@gmail.com',
                'password':'1234',
                }
        )

        response=self.client.get(
            '/api/bonds/',
            HTTP_AUTHORIZATION='Bearer {}'.format(login.data['access']),
            content_type='application/json'
            )

        bond_id=response.data[0]['id']
        #print(bond_id)

        response=self.client.post(
            '/api/buy_bonds/',
            data={'bond_id':bond_id},
            HTTP_AUTHORIZATION='Bearer {}'.format(login.data['access']),
            content_type='application/json'
        )

        response=self.client.get(
            '/api/bonds/',
            HTTP_AUTHORIZATION='Bearer {}'.format(login.data['access']),
            content_type='application/json'
            )
        self.assertEqual(response.status_code,status.HTTP_200_OK)






        #print(response.status_code,response.data)

  