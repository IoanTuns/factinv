from django.test import TestCase, Client
from my_company.models import MyCompany

class GraphQLTest(TestCase):
    def test_list_my_company(self):
        MyCompany.objects.all()
        query = """
        query{
            my_companies{
                id
                cui
                nrRegCom
                denumire
                }
            }
        """
        response = Client().post(
            "/graphql/",
            {"query": query},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("errors"), None)
        mycompany = response.json()["data"]["mycompany"]
        self.assertEqual(len(mycompany), 1)
        self.assertEqual(mycompany[0]["cui"], "CUI")
