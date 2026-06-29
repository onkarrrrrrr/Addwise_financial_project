from django.test import TestCase
from django.urls import reverse

class SEORoutingTestCase(TestCase):
    """
    Tests to verify that SEO and AIEO endpoints are fully operational,
    accessible, and output correct structures.
    """
    def test_sitemap_xml_status_and_content(self):
        # Fetch sitemap.xml
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/xml')
        
        # Verify it includes the XML sitemap structure
        content = response.content.decode('utf-8')
        self.assertIn('<urlset', content)
        self.assertIn('<loc>', content)
        self.assertIn('<priority>', content)
        
        # Check that main public endpoints are listed
        self.assertIn('/about/', content)
        self.assertIn('/services/', content)
        self.assertIn('/careers/', content)
        self.assertIn('/calculators/', content)
        self.assertIn('/appointment/', content)

    def test_robots_txt_status_and_content(self):
        # Fetch robots.txt
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/plain')
        
        # Verify it lists key crawler directives and sitemaps
        content = response.content.decode('utf-8')
        self.assertIn('User-agent: *', content)
        self.assertIn('Disallow: /admin/', content)
        self.assertIn('Disallow: /superadmin/', content)
        
        # Verify AI bots are explicitly mentioned
        self.assertIn('User-agent: GPTBot', content)
        self.assertIn('User-agent: PerplexityBot', content)
        self.assertIn('User-agent: Google-Extended', content)
        self.assertIn('User-agent: ClaudeBot', content)
        self.assertIn('User-agent: Applebot-Extended', content)
        
        # Verify Sitemap reference exists
        self.assertIn('Sitemap:', content)
        self.assertIn('sitemap.xml', content)

