from django.test import TestCase
from catalog.models import Author


# Simple Test class examples
class YourTestClass(TestCase):

    # Note 1:
    # The test classes also have a tearDown() method which we haven't used. 
    # This method isn't particularly useful for database tests, 
    # since the TestCase base class takes care of database teardown for you.

    # Note 2
    # You should not normally include print() functions in your tests as shown above. 
    # We do that here only so that you can see the order that the setup functions 
    # are called in the console (in the following section).

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass
    
    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(True)
        # If you want faile test
        # self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)


class AuthorModelTest(TestCase):

    # Заметка для себя:
    # Возможно можно улучшить функции в этом методе убрав дублирование.
    # А именно вынести "author=Author.objects.get(id=1)" в метод setUpTestData()


    # Class Model - temporary

    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    # date_of_birth = models.DateField(null=True, blank=True)
    # date_of_death = models.DateField('Died', null=True, blank=True)
    # 
    # def get_absolute_url(self):
        # """
        # Returns the url to access a particular author instance.
        # """
        # return reverse('author-detail', args=[str(self.id)])
    # 
    # def __str__(self):
        # """
        # String for representing the Model object.
        # """
        # return '%s %s' % (self.last_name, self.first_name)

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        # Get an author object to test
        author=Author.objects.get(id=1)
        # Get the metadata for the required field and use it to query the required field data
        field_label = author._meta.get_field('first_name').verbose_name
        # Compare the value to the expected result
        self.assertEquals(field_label,'first name')

    def test_last_name_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label,'last name')

    def test_date_of_birth_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEquals(field_label,'date of birth')

    def test_date_of_death_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label,'died')

    def test_first_name_max_length(self):
        author=Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length,100)

    def test_last_name_max_length(self):
        author=Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEquals(max_length,100)

    def test_object_name_is_last_name_comma_first_name(self):
        author=Author.objects.get(id=1)
        expected_object_name = '%s %s' % (author.last_name, author.first_name)
        self.assertEquals(expected_object_name,str(author))

    def test_get_absolute_url(self):
        author=Author.objects.get(id=1)
        #This will also fail if the urlconf is not defined.
        self.assertEquals(author.get_absolute_url(),'/catalog/author/1')
