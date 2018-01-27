from __future__ import unicode_literals

from django.db import models
import bcrypt, re
from datetime import datetime

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+.[^@\s]+$")


class UserManager(models.Manager):
    def validate_register(self, postData):    
        errors = {}
        
        if not len(postData['name']):
            errors['name'] = "What's your name."
        elif len(postData['name']) < 3:
            errors['name'] = "name field must be at least 3 characters"
        
        if not len(postData['alias']):
            errors['alias'] = "Input your Alias."
        elif len(postData['alias']) < 3:
            errors['alias'] = "Alias field must be at least 3 characters"
        elif self.filter(alias = postData['alias']):
            errors['alias'] = "please enter a new one,Alias is already in use."
        
        if not len(postData['email']):
            errors['email'] = "Input your email."
        elif not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = "Invalid email! Please input the right format like: kedirzgreat@mail.com"
        elif self.filter(email = postData['email']):
            errors['email'] = "please enter a new Email, this one is already in use."

        if not len(postData['password']):
            errors['password'] = "Password field can not be empty."
        elif len(postData['password']) < 8:
            errors['password'] = "password should be >= 8 characters"
        elif postData['password'] != postData['confirm_pass']:
            errors['confirm_pass'] = "Password you entered is not same as registration password "
        
        if not postData['birthday']:
            errors['birthday'] = "What's your birthday."
        else:
            now = datetime.today().date()
            birthday = datetime.strptime(postData['birthday'], "%Y-%m-%d").date()
            if birthday >= now:
                errors['birthday'] = "Birthday can not be earlier than the current day."

        if len(errors):
            return (False, errors)
        else:
            password = postData['password'].encode()
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            self.create(name = postData['name'], alias = postData['alias'], email = postData['email'], password = hashed, birthday = birthday)
            return (True, postData['name'])

    def validate_login(self, postData):
        errors_login = {}
        if not len(postData['email']):
            errors_login['login_email_error'] = "Please provide an email."
        else:
            if not self.filter(email = postData['email']):
                errors_login['login_error'] = "The Email or password you have entered is wrong."
        
        if not len(errors_login):
            user = self.filter(email = postData['email'])
            if not len(postData['password']):
                errors_login['login_password_error'] = "Please provide password."
            else:
                password = postData['password'].encode()
                hashed = self.filter(email = postData['email'])[0].password.encode()
                if not bcrypt.checkpw(password, hashed):
                    errors_login['login_error'] = "Email or password wrong."

        
        if len(errors_login):
            return (False, errors_login)
        else:
            return (True, self.filter(email = postData['email']))


class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    birthday = models.DateField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
