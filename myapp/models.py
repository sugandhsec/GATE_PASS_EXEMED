from django.db import models
from random import choices
from secrets import choice
from turtle import position
from django.db import models
from django.utils import timezone


user_type = (
    ("operator", "operator"),
    ("manager", "manager"),
    ("approver", "approver"),
    ("verifier", "verifier")
)
dept = (
    ("admin", "admin"),
    ("HR", "HR"),
    ("QA", "QA"),
    ("QC", "QC"),
    ("PH", "PH"),
    ("WH", "WH"),
    ("ENGG", "ENGG"),
    ("API", "API"),
    ("ADL", "ADL"),
    ("EOHS", "EOHS"),
    ("IT", "IT")
)

# Create your models here.


class User_rgp(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    usertype = models.CharField(max_length=100, choices=user_type)
    department=models.CharField(max_length=100,choices=dept,null=True)
    def __str__(self):
        return self.fname+" "+self.lname+" "+self.department+" "+self.usertype


class Rgp_entry(models.Model):
    rgp_serial = models.CharField(max_length=20, null=True)
    rgp_created = models.ForeignKey(
        User_rgp, on_delete=models.CASCADE, null=True)
    cpname = models.CharField(max_length=100)
    dpname = models.CharField(max_length=100)
    spname = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    qty = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    made_on = models.DateTimeField(default=timezone.now)
    current_status = models.CharField(max_length=10, default="Entry")
    verifier = models.ForeignKey(
        User_rgp, related_name='verifier', null=True, on_delete=models.CASCADE)
    verify_status = models.BooleanField(default=False)
    rgp_verify_time = models.DateTimeField(null=True)
    approver = models.ForeignKey(
        User_rgp, related_name='approver', null=True, on_delete=models.CASCADE)
    approve_status = models.BooleanField(default=False)
    rgp_approve_time = models.DateTimeField( null=True)

    outward_sender = models.ForeignKey(
        User_rgp, related_name='outward_sender', on_delete=models.CASCADE, null=True)
    outward_status = models.BooleanField(default=False)
    outward_mode = models.CharField(max_length=100, null=True)
    outward_reciever_name = models.CharField(max_length=100, null=True)
    rgp_outward_time = models.DateTimeField( null=True)

    inward_receiver = models.ForeignKey(
        User_rgp, related_name='inward_receiver', on_delete=models.CASCADE, null=True)
    inward_status = models.BooleanField(default=False)
    inward_party_challan = models.CharField(max_length=100, null=True)
    inward_mode = models.CharField(max_length=100, null=True)
    rgp_inward_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.rgp_serial


class Nrgp_entry(models.Model):
    nrgp_serial = models.CharField(max_length=20, null=True)
    nrgp_created = models.ForeignKey(
        User_rgp, on_delete=models.CASCADE, null=True)
    cpname = models.CharField(max_length=100)
    dpname = models.CharField(max_length=100)
    spname = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    qty = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    made_on = models.DateTimeField(default=timezone.now)
    current_status = models.CharField(max_length=10, default="Entry")
    nrgp_verifier = models.ForeignKey(
        User_rgp, related_name='nrgp_verifier', null=True, on_delete=models.CASCADE)
    nrgp_verify_status = models.BooleanField(default=False)
    nrgp_verify_time = models.DateTimeField( null=True)
    nrgp_approver = models.ForeignKey(
        User_rgp, related_name='nrgp_approver', null=True, on_delete=models.CASCADE)
    nrgp_approve_status = models.BooleanField(default=False)
    nrgp_approve_time = models.DateTimeField(null=True)
    nrgp_outward_sender = models.ForeignKey(
        User_rgp, related_name='nrgp_outward_sender', on_delete=models.CASCADE, null=True)
    nrgp_outward_status = models.BooleanField(default=False)
    nrgp_outward_mode = models.CharField(max_length=100, null=True)
    nrgp_outward_reciever_name = models.CharField(max_length=100, null=True)
    nrgp_outward_time = models.DateTimeField( null=True)

    def __str__(self):
        return self.nrgp_serial

# class rgp_outward(models.Model):
#     rgp_product = models.ForeignKey(
#         Rgp_entry, on_delete=models.CASCADE, null=True)
#     mode=models.CharField(max_length=100,null=True)
#     reciever_name=models.CharField(max_length=100,null=True)
