from django.contrib.auth.models import Group, Permission
from users.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from blogs.models import Blog
from mailings.models import Mailing, Client, Message


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.create_groups()
        self.create_users()
        self.create_clients()
        self.create_messages()
        self.create_mailings()
        self.create_blogs()
        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))

    def create_groups(self):
        manager_group, created = Group.objects.get_or_create(name='Manager')

        mailing_content_type = ContentType.objects.get_for_model(Mailing)
        mailing_permissions = [
            Permission.objects.get(codename=perm[0], content_type=mailing_content_type)
            for perm in Mailing._meta.permissions
        ]
        manager_group.permissions.add(*mailing_permissions)

        content_manager_group, created = Group.objects.get_or_create(name='Content manager')

        blog_content_type = ContentType.objects.get_for_model(Blog)
        blog_permissions = [
            Permission.objects.get(codename=perm[0], content_type=blog_content_type)
            for perm in Blog._meta.permissions
        ]
        content_manager_group.permissions.add(*blog_permissions)

    def create_users(self):
        self.user1 = User.objects.create_user(email='user1@gmail.com', password='password1')
        self.user1.groups.add(Group.objects.get(name='Manager'))

        self.user2 = User.objects.create_user(email='user2@gmail.com', password='password2')
        self.user2.groups.add(Group.objects.get(name='Content manager'))

        self.user3 = User.objects.create_user(email='user3@gmail.com', password='password3')

    def create_clients(self):
        self.client1 = Client.objects.create(email='client1@gmail.com', name='Client 1')
        self.client2 = Client.objects.create(email='client2@gmail.com', name='Client 2')

    def create_messages(self):
        self.message = Message.objects.create(subject='Test message', body='Test')

    def create_mailings(self):
        self.mailing = Mailing.objects.create(
            periodicity='daily', status='created', message=self.message, owner=self.user3)
        self.mailing.clients.add(self.client1, self.client2)

    def create_blogs(self):
        self.blog = Blog.objects.create(title='Test title', content='Test content', author=self.user2)
