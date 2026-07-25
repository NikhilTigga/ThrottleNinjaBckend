from django.test import TestCase


class GraphQLEndpointTests(TestCase):
    def test_graphql_endpoint_accepts_json_posts_without_csrf(self):
        response = self.client.post(
            "/graphql/graphql/",
            data='{"query": "query { __typename }"}',
            content_type="application/json",
        )

        self.assertNotEqual(response.status_code, 403)
