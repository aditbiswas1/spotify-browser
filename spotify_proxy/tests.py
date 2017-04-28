from django.test import TestCase, Client
from django.urls import reverse
# Create your tests here.

class IndexViewTest(TestCase):
    
    def setUp(self):
        self.view_endpoint = reverse('index')
        self.client = Client()

    def generic_valid_search(self, q, query_filter):
        '''
        Tests the context of any valid query with any valid filter
        response filter should match the input filter
        response query should match the input query
        results count and number of items should be greater than 0
        '''
        params = {
            'q' : q,
            'filter': query_filter,
        }

        response = self.client.get(self.view_endpoint, params)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.context['count']>0)
        self.assertTrue(len(response.context['items'])>0)
        self.assertEqual(response.context['q'], params['q'])
        self.assertEqual(response.context['filter'], params['filter'])

        message = '<p class="message">Found {count} results for "{q}" in {filter}s</p>'.format(
            count=response.context['count'],
            q=q,
            filter=query_filter
            )
        self.assertContains(response, message)
        return response

    def test_landing_page(self):
        '''
        Tests the main landing page of the music browser
        by default we search with the track filter
        count, item and query should be empty values
        '''
        response = self.client.get(self.view_endpoint)
        
        self.assertEqual(response.status_code , 200)

        self.assertEqual(response.context['count'], 0)
        self.assertEqual(response.context['items'], [])
        self.assertEqual(response.context['q'], None)
        self.assertEqual(response.context['filter'], 'track')
        self.assertContains(response, '<p class="error message">Please fill out the form.</p>')

    def test_track_search(self):
        '''
        Tests the default search functionality with a popular track name
        results of querying with 'track' and no filter should be the same
        '''
        q = 'stronger'

        with_track_response = self.generic_valid_search(q, 'track')
        
        default_search_response = self.client.get(self.view_endpoint, {'q': q})

        self.assertEqual(with_track_response.context['count'], default_search_response.context['count'])
        self.assertEqual(with_track_response.context['items'], default_search_response.context['items'])
        self.assertEqual(with_track_response.context['q'], default_search_response.context['q'])
        self.assertEqual(with_track_response.context['filter'], default_search_response.context['filter'])

        message = '<p class="message">Found {count} results for "{q}" in {filter}s</p>'.format(
            count=default_search_response.context['count'],
            q=q,
            filter='track'
            )
        self.assertContains(with_track_response, message)
        self.assertContains(default_search_response, message)

    def test_filters_search(self):
        '''
        Test the results of searching a given query in all the valid filters
        '''
        q = 'kanye'

        valid_filters = ['track', 'playlist', 'artist', 'album']
        for query_filter in valid_filters:
            self.generic_valid_search(q, query_filter)

    def test_invalid_filter(self):
        '''
        Tests the results when user manually enters an invalid filter parameter in url
        should return empty results 
        '''
        q = 'kanye'
        query_filter = 'song'
        response = self.client.get(self.view_endpoint, {'q': q , 'filter': query_filter})

        self.assertEqual(response.context['count'], 0)
        self.assertEqual(response.context['items'], [])
        self.assertEqual(response.context['q'], q)
        self.assertEqual(response.context['filter'], query_filter)
        message = '<p class="message">Found {count} results for "{q}" in {filter}s</p>'.format(
            count=response.context['count'],
            q=q,
            filter=query_filter
            )
        self.assertContains(response, message)

    def test_null_results(self):
        '''
        Tests the results of a nonsensical query
        should be empty results
        '''
        q = 'adfadfadsafsa'
        response = self.client.get(self.view_endpoint, {'q': q})

        self.assertEqual(response.context['count'], 0)
        self.assertEqual(response.context['items'], [])
        self.assertEqual(response.context['q'], q)
        self.assertEqual(response.context['filter'], 'track')
        message = '<p class="message">Found {count} results for "{q}" in {filter}s</p>'.format(
            count=response.context['count'],
            q=q,
            filter='track'
            )
        self.assertContains(response, message)
