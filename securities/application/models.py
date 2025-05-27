from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms


class Application(models.Model):
    STATUS_CHOICES = [
        ('PENDING', '審核中'),
        ('APPROVED', '已通過'),
        ('REJECTED', '已拒絕'),
        ('MISSING_DOCUMENTS', '待補件'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    account_name = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reason = models.TextField(blank=True, null=True)  # reason for MISSING_DOCUMENTS

    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user.username} - {self.status}"