from django.test import TestCase

from authentication.tests.factories import UserFactory 
from django.db import IntegrityError
from ..exceptions import DuplicatedSkill
from ..models import Skill, SkillData 
from .factories import SkillFactory, SkillDataFactory
from django.test import Client
from django.core.urlresolvers import reverse 


class SkillModelTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.data = SkillDataFactory(codename='testing')

    def test_user_add_skill_success(self):
        Skill.objects.create(user=self.user, data=self.data)
        self.assertTrue(Skill.objects.get(user=self.user, data=self.data))
        self.assertTrue(self.user.skill_set.get(user=self.user, data=self.data))
        self.assertTrue(self.data.skill_set.get(user=self.user, data=self.data))

    def test_double_skill_error(self):
        Skill.objects.create(user=self.user, data=self.data)
        with self.assertRaises(IntegrityError):
            Skill.objects.create(user=self.user, data=self.data)

    def test_user_can_have_multiple_skills(self):
        data2 = SkillDataFactory(codename='test')

        Skill.objects.create(user=self.user, data=self.data)
        Skill.objects.create(user=self.user, data=data2)
        self.assertEqual(self.user.skill_set.filter().count(), 2)

    def tearDown(self):
        del self.user
        del self.data



class SkillManagerTestCase(TestCase):
    def test_add_skill(self): 
        user = UserFactory()

        skill_ass = Skill.objects.add(user, name='testing')

        self.assertIsInstance(
            skill_ass, Skill,
            msg='The returned value must be an instance of Skill class'
            )
        self.assertTrue(
            SkillData.objects.get(_codename='testing') == skill_ass.data,
            msg='No SkillData instance allocated',
            )

        with self.assertRaises(DuplicatedSkill):
            Skill.objects.add(user, name='testing')

    def test_user_can_have_multiple_skills(self):
        user = UserFactory()
        Skill.objects.add(user, name='testing')
        Skill.objects.add(user, name='test')

        self.assertEqual(user.skill_set.filter().count(), 2)

class SkillViewTestCase(TestCase):
    # views tests
    def setUp(self):
        self.client = Client()
        self.user = UserFactory(email='matt@gmail.com', password='pa55worD')
        self.client.login(username=self.user.email, password='pa55worD')


    def test_get_create_skill(self):
        response = self.client.get(reverse('skill:add_skill'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form']) 


    def test_post_add_skill_redirect(self):
        response = self.client.post(
            reverse('skill:add_skill'),
            {'_codename': 'pippo'},
            follow=True,
            )

        self.assertRedirects(
            response,
            reverse('account:profile_detail',
                args=((self.user.email,)),
                )
            )

    def test_post_add_skil_message_success(self):
        response = self.client.post(
            reverse('skill:add_skill'),
            {'_codename': 'skill'},
            follow=True,
            )

        from django.contrib.messages import SUCCESS
        queue = list(response.context['messages'])
        self.assertEqual(len(queue), 1)
        self.assertEqual(queue[0].level, SUCCESS)

       
