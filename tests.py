from shrtn import *
import database as db
import unittest
from pdb import set_trace as st

class ShrtnTestCase(unittest.TestCase):
    """A Super Class to be inherited."""

    def setUp(self):
        pass
    
    def tearDown(self):
        pass

class TestValidShort(ShrtnTestCase):
    """Test the is_valid_short function."""

    def test_is_valid_short(self):
        """Test that we can validate a good short url.
        
        Example: http://shr.tn/h7Ki9a
        """
        result = is_valid_short(good_short)
        self.assertTrue(result)
        
    def test_is_not_valid_short(self):
        """Test that we can invalidate a bad short url.
        
        Example: http://shr.tn/a8CT/bnb
        """
        result = is_valid_short(bad_short)
        self.assertFalse(result)

class TestStandardizeUrl(ShrtnTestCase):
    """Test the standardize_url function."""

    def test_no_http_scheme(self):
        """Test that we add the http scheme when necessary."""
        result = standardize_url("example.com") 
        self.assertTrue(result == standard)
    
    def test_http_scheme(self):
        """Test that we don't alter the url with a scheme.
        
        Only add a trailing slash if necessary.
        """
        result = standardize_url("http://example.com") 
        self.assertTrue(result == standard)
    
    def test_hostname_www(self):
        """Test that we don't alter the hostname with www, only that we add the scheme."""
        hostname = "www.example.com/"
        result = standardize_url(hostname)
        self.assertTrue(result != standard)
        self.assertTrue(result == "http://%s" % hostname)
        
    def test_hostname_odd_subdomain(self):
        """Test that we don't alter the hostname with a subdomain, only that we add the scheme."""
        hostname = "subdomain.example.com/"
        result = standardize_url(hostname)
        self.assertTrue(result != standard)
        self.assertTrue(result == "http://%s" % hostname)

    def test_our_urls(self):
        """Test that we do not shorten our own URLs."""
        result = standardize_url(good_short)
        self.assertTrue(result is None) 
        
    def test_non_http_scheme(self):
        """Test that only http(s) allowed."""
        result = standardize_url("ftp://aserver/afile") 
        self.assertTrue (result is None)

class TestConvertToCode(ShrtnTestCase):

    def test_convert_to(self):
        """Test that we can convert an integer id into the correct hash."""
        id = 78950039
        code = convert_to_code(id)
        result = resolve_to_id(code)
        self.assertTrue(result == id)
        
    def test_convert_negative(self):
        """Test that we convert a negative id to 0."""
        id = -1
        negative = convert_to_code(id)
        zero = convert_to_code(0)
        result1 = resolve_to_id(negative)
        result2 = resolve_to_id(zero)
        self.assertTrue(result1 != negative)
        self.assertTrue(result2 == 0)
        
    def test_convert_to(self):
        """Test that we can convert a large prime integer id into the correct hash."""
        id = 17180131327
        code = convert_to_code(id)
        result = resolve_to_id(code)
        self.assertTrue(result == id)
        
class TestResolveToId(ShrtnTestCase):

    def setUp(self):
        self.id = 78950039
        
    def test_resolve_to(self):
        """Test that we can resolve a hash back to the correct id."""
        code = convert_to_code(self.id)
        result = resolve_to_id(code)
        self.assertTrue(result == self.id)

    def test_vanity_resolve_to(self):
        """Test to prove we could easily do vanity urls."""
        vanity = "torgear"
        id = resolve_to_id(vanity)
        result = convert_to_code(id)
        self.assertTrue(result == vanity)

class TestShortenURL(ShrtnTestCase):
    
    def test_shorten_url(self):
        shortened = shorten_url(standard, conn) 
        lengthened = lengthen_url(shortened, conn)
        self.assertTrue(lengthened == standard)
        
class TestLengthenURL(ShrtnTestCase):

    def test_lengthen_url(self):
        shortened = shorten_url(standard, conn) 
        lengthened = lengthen_url(shortened, conn)
        self.assertTrue(lengthened == standard)
        
class TestDBSearchID(ShrtnTestCase):

    def test_search_id(self):
        id = db.search_url(standard, db.MYTABLE, conn)
        result = db.search_id(id, db.MYTABLE, conn)
        self.assertTrue(result == standard)
    
class TestDBSearchURL(ShrtnTestCase):
    
    def test_search_url(self):
        wiki = "http://en.wikipedia.org/wiki/List_of_prime_numbers"
        shortened = shorten_url(wiki, conn)
        result = lengthen_url(shortened, conn)
        self.assertTrue(result == wiki)
            
if __name__ == "__main__":
    conn = setup_db() #setup connection to database
    assert db.table_exists(db.MYTABLE, conn) == True #check that table is ready
    
    #unit tests for shrtn functions
    our_domain = "http://shr.tn"
    good_short = "%s/h7Ki9a" % our_domain
    bad_short = "%s/a8CT/bnb" % our_domain
    standard = "http://example.com/"
    
    valid_short = unittest.TestLoader().loadTestsFromTestCase(TestValidShort)
    standardize = unittest.TestLoader().loadTestsFromTestCase(TestStandardizeUrl)
    convert_to = unittest.TestLoader().loadTestsFromTestCase(TestConvertToCode)
    resolve_to = unittest.TestLoader().loadTestsFromTestCase(TestResolveToId)
    shorten = unittest.TestLoader().loadTestsFromTestCase(TestShortenURL)
    lengthen = unittest.TestLoader().loadTestsFromTestCase(TestLengthenURL)
    search_id = unittest.TestLoader().loadTestsFromTestCase(TestDBSearchID)
    search_url = unittest.TestLoader().loadTestsFromTestCase(TestDBSearchURL)
    
    testcases = [
        valid_short, 
        standardize, 
        convert_to, 
        resolve_to,
        shorten,
        lengthen,
        search_id,
        search_url,
        ]
    
    all_tests = unittest.TestSuite(testcases)
    unittest.TextTestRunner(verbosity=2).run(all_tests)

