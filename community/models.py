from django.db import models

STATUS = (
    ('PEN', 'Pending'),
    ('APR', 'Approved'),
    ('CAN', 'Cancelled'),
)

class JobPost(models.Model):
    
    artisan = models.ForeignKey("artisan.Artisan", related_name="job_posts", on_delete=models.PROTECT)
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    vacancy = models.PositiveIntegerField()
    prerequisites = models.JSONField(default=list) 
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title

class JobPostApplicationRequest(models.Model):
    
    artisan = models.ForeignKey("artisan.Artisan", related_name="applied_jobs", on_delete=models.PROTECT)
    job_post = models.ForeignKey("community.JobPost", related_name="application_requests", on_delete=models.PROTECT)

    about = models.TextField()
    
    status = models.CharField(choices=STATUS, max_length=20, default="PEN")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.artisan.name

class RentalMachine(models.Model):
    
    artisan = models.ForeignKey("artisan.Artisan", related_name="rental_machines", on_delete=models.PROTECT)
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    rate = models.PositiveIntegerField(default=50) # per hour
    
    starting_time = models.TimeField() 
    ending_time = models.TimeField() 
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title
    
class RentalMachineBookingRequest(models.Model):
    
    artisan = models.ForeignKey("artisan.Artisan", related_name="booked_machines", on_delete=models.PROTECT)
    rental_machine = models.ForeignKey("community.RentalMachine", related_name="booking_requests", on_delete=models.PROTECT)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    purpose = models.TextField(blank=True, null=True)
    
    status = models.CharField(choices=STATUS, max_length=20, default="PEN")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.artisan.name