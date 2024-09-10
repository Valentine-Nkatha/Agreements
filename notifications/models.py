from django.db import models

# Create your models here.
class Notifications(models.Model):
    # land = models.ForeignKey('Land', on_delete=models.CASCADE)
    # buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_interests')
    # seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_interests')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    objects = models.Manager()
    def __str__(self):
        return f"{self.message},{self.created_at},{self.is_read}"
 
