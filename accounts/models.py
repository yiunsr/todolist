#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


# Create your models here.

# https://wikidocs.net/10294
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
         이메일, 비밀번호로 생성
        """
        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        주어진 이메일, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여한다. 
        """
        user = self.create_user(
            email=email,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Djanog User model 에 대한 재정의
    """
    email = models.EmailField(
        verbose_name=_('Email address'),
        max_length=30,
        unique=True,
    )
    
    is_active = models.BooleanField(
        verbose_name=_('Is active'),
        default=True
    )
    date_joined = models.DateTimeField(
        verbose_name=_('Date joined'),
        default=timezone.now
    )
    # 이 필드는 레거시 시스템 호환을 위해 추가할 수도 있다.
    salt = models.CharField(
        verbose_name=_('Salt'),
        max_length=10,
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('accounts')
        ordering = ('-date_joined',)

    def __str__(self):
        return self.email

    def get_full_name(self):        
        return self.email

    def get_short_name(self):
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All superusers are staff
        return self.is_superuser

    get_full_name.short_description = _('Full name')
        