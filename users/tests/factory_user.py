import factory
from faker import Factory

from users.models import CustomUser

faker = Factory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
    
    
    email = faker.email()
    password = faker.password()
    type = 'instructor'
    phone = faker.random_number(10)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop("password", None)
        obj = super(UserFactory, cls)._create(model_class, *args, **kwargs)
        # ensure the raw password gets set after the initial save
        obj.set_password(password)
        obj.save()
        return obj
