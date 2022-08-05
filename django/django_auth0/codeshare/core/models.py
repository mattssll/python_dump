# codeshare/core/models.py

from django.db import models
class Organization(models.Model):
    """ Company entities in our model """
    orgname = models.CharField(primary_key=True, max_length=100)
    numb_of_ppl = models.IntegerField()
    creation_date = models.DateField()
    sector = models.CharField(max_length=100)
    yearly_revenue = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=None)
    def __str__(self):
        return self.orgname
class Person(models.Model):
    #class Meta:
    """ Company entities in our model """
    personid = models.AutoField(primary_key=True)
    personname = models.CharField(max_length=100)
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=None)
    age = models.IntegerField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    def __str__(self):
        return self.personname

# Create our models here.
class TimeAuditModel(models.Model): # data types and other stuff are in models.Model
    """ To path when the record was created and last modified """
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created At",)
    updated = models.DateTimeField(auto_now=True, verbose_name="Last Modified At")
    class Meta:
        abstract = True # abstract classes have to be inherited


class Post(TimeAuditModel): # inheriting fields from TimeAuditModel
    post_title = models.CharField(max_length=255)
    post_description = models.TextField()
    post_description_markdown = models.TextField(blank=True)
    post_org = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=False, default="Other")
    post_author = models.ForeignKey(Person, on_delete=models.CASCADE, blank=False, default="Other")
    def __str__(self):
        return self.post_title



