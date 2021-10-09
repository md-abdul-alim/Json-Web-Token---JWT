from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext as _


'''
gettext_lazy is imported as _, gettext is imported as gettext.
You’d generally want to use the lazy variant, but this returns a proxy object and not a string,
 so if you have a context where you need a string immediately, you may also need access to the non-lazy version.
The lazy version is probably used more often, so it’s aliased to a nice short name. 
'''
# Create your models here.
'''
This user model is fully customizable.
We can add new field. Like phone number inside the user table.
Or we can also remove default username field from user table.

'''
'''
*args vs **kwargs
*args passes variable number of non-keyworded arguments list and on which operation of the list can be performed.
list = ["l", 5, "alim']
**kwargs passes variable number of keyword arguments dictionary to function on which operation of a dictionary can be performed.
dict = {"key1": "value1", "key2": 2, "key3": "value3"}
'''

# https://dev.to/koladev/django-rest-authentication-cmh


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email can not be empty.")
        if not password:
            raise ValueError("This given password must be set")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # user.set_password(password)
        user.password = make_password(password)
        user.save(using=self._db)
        '''
        https://docs.djangoproject.com/en/3.2/topics/db/multi-db/
        https://stackoverflow.com/questions/57667334/what-is-the-value-of-self-db-by-default-in-django
        use of using = self._db
        Django default managers use using parameter to define which database underlying the manager should use for operation.
        This will optionally use. This is used in case you have multiple databases by which you define which database you need to use for operation.
        An example user.save(using=self._db) usually defined as "default" from your database configuration in settings.py.
        Behind the scene self._db set as None. If user.save(using=None), then it will use default database.
        '''
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Now add an extra validation layer for superuser. We are adding this layer because if anyone
        # try to change superuser default behaviour, we can raise and error
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomAbstractUser(AbstractBaseUser, PermissionsMixin):  # AbstractUser

    '''
    db_index=True
    https://en.wikipedia.org/wiki/Database_index
    https://stackoverflow.com/questions/14786413/add-indexes-db-index-true

    This is not really django specific; more to do with databases. You add indexes on columns when you want to speed up searches on that column.
    Typically, only the primary key is indexed by the database. This means look ups using the primary key are optimized.
    If you do a lot of lookups on a secondary column, consider adding an index to that column to speed things up.
    Keep in mind, like most problems of scale, these only apply if you have a statistically large number of rows (10,000 is not large).
    Additionally, every time you do an insert, indexes need to be updated. So be careful on which column you add indexes.
    As always, you can only optimize what you can measure - so use the EXPLAIN statement and your database logs (especially any slow query logs) to find out where indexes can be useful.

    A database index is a data structure that improves the speed of data retrieval operations on a database table at the cost of additional writes and storage space to maintain the index data structure.
    Indexes are used to quickly locate data without having to search every row in a database table every time a database table is accessed.
    Indexes can be created using one or more columns of a database table, providing the basis for both rapid random lookups and efficient access of ordered records.
    '''
    # username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        # unique=True,
        help_text=_('Optional. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        # validators=[username_validator],
        # error_messages={
        #     'unique': _("A user with that username already exists."),
        # },
        blank=True
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(db_index=True, unique=True, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone = models.CharField(max_length=255, blank=True, null=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(CustomAbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Email and password are required. Other fields are optional.
    """
    class Meta(CustomAbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'