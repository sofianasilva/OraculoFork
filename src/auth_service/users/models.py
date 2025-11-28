"""
User models for Oráculo Authentication Service.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    
    This model will be extended in future steps to include:
    - Repository permissions
    - Access control lists
    - Integration with GitHub data
    """
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # Future ACL fields (will be added in Step 5)
    # github_username = models.CharField(max_length=255, blank=True, null=True)
    # allowed_repositories = models.ManyToManyField('Repository', blank=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        db_table = 'auth_user'  # Separate from existing user_info table
        
    def __str__(self):
        return self.username