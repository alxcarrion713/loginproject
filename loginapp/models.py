from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
   

    def registrationValidator(self, forminfo):
        validationErrors= {}
        print('printing form info in validator')
        print(forminfo)
        if len (forminfo['fname'])<2:
            validationErrors['firstName']="First name must be at least 2 characters"
        if len (forminfo['lname'])<2:
            validationErrors['lastName']="Last name must be at least 2 characters"
        if len (forminfo['email']) <1:
            validationErrors['email']= "Email is required"
        elif not EMAIL_REGEX.match(forminfo['email']):
            validationErrors['emailformat']= "Email is not valid"
        else:
            userswithemail = User.objects.filter(email = forminfo['email'])
            if len(userswithemail)>0:
                validationErrors['emailtaken']= "Email is already in use, please try another email"

        if len (forminfo['pw'])<8:
            validationErrors['password']="Password must be at least 8 characters"
        if forminfo['pw'] != forminfo['cfw']:
            validationErrors['confirm']="Password and confirm password must match"
        return validationErrors


    def loginValidator(self,forminfo):
        errors = {}
        if len(forminfo['email']) <1:
            errors['email'] = "Email is required"
        else:

            emailsExist = User.objects.filter(email=forminfo['email'])
            print(emailsExist)
            if len(emailsExist) == 0:
                errors['emailNotFound'] = "This email was not found. Please register first."
            else:
                user = emailsExist[0]
            if not bcrypt.checkpw(forminfo['pw'].encode(), user.password.encode()):
                errors['pw']= "Password does not match."


        return errors




class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


