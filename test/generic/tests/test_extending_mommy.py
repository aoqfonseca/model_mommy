from django.db.models.fields import BooleanField
from django.test import TestCase

from model_mommy import mommy
from model_mommy.generators import gen_from_list
from test.generic.models import Person

__all__ = ['SimpleExtendMommy', 'LessSimpleExtendMommy']


class SimpleExtendMommy(TestCase):

    def test_list_generator_respects_values_from_list(self):
        age_list = range(4, 12)

        class KidMommy(mommy.Mommy):
            attr_mapping = {'age': gen_from_list(age_list)}

        mom = KidMommy(Person)
        kid = mom.make()

        self.assertTrue(kid.age in age_list)


class LessSimpleExtendMommy(TestCase):

    def test_unexistent_required_field(self):
        gen_oposite = lambda x: not x
        gen_oposite.required = ['house']

        class SadPeopleMommy(mommy.Mommy):
            attr_mapping = {'happy': gen_oposite}

        mom = SadPeopleMommy(Person)
        self.assertRaises(AttributeError, mom.make)

    #TODO: put a better name
    def test_string_to_generator_required(self):
        gen_oposite = lambda default: not default
        gen_oposite.required = ['default']

        class SadPeopleMommy(mommy.Mommy):
            attr_mapping = {
                'happy': gen_oposite,
                'unhappy': gen_oposite,
            }

        happy_field = Person._meta.get_field('happy')
        unhappy_field = Person._meta.get_field('unhappy')
        mom = SadPeopleMommy(Person)
        person = mom.make()
        self.assertEqual(person.happy, not happy_field.default)
        self.assertEqual(person.unhappy, not unhappy_field.default)

    def test_fail_pass_non_string_to_generator_required(self):
        gen_age = lambda x: 10

        class MyMommy(mommy.Mommy):
            attr_mapping = {'age': gen_age}

        mom = MyMommy(Person)

        # for int
        gen_age.required = [10]
        self.assertRaises(ValueError, mom.make)

        # for float
        gen_age.required = [10.10]
        self.assertRaises(ValueError, mom.make)

        # for iterable
        gen_age.required = [[]]
        self.assertRaises(ValueError, mom.make)

        # for iterable/dict
        gen_age.required = [{}]
        self.assertRaises(ValueError, mom.make)

        # for boolean
        gen_age.required = [True]
        self.assertRaises(ValueError, mom.make)
