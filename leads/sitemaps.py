from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    """
    Sitemap for the static pages of the Addwise Financials website.
    Enables traditional search engines and AI web crawlers to discover
    and index all public endpoints correctly.
    """
    changefreq = 'weekly'

    def items(self):
        # List of tuples: (url_name, priority)
        return [
            ('home', 1.0),
            ('services', 0.9),
            ('about', 0.8),
            ('career', 0.7),
            ('appointment', 0.8),
            ('contact', 0.8),
            ('calculators', 0.7),
            ('disclaimer', 0.3),
            ('privacy_policy', 0.3),
            ('disclosure', 0.3),
        ]

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]
