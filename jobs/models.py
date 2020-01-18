from django.db import models

# Create your models here.
class JobConfig(models.Model):
    job_type = models.SmallIntegerField(primary_key=True)
    job_type_desc = models.CharField(max_length=200, blank=True, null=True)
    job_rate = models.FloatField(blank=True, null=True)
    job_api = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.job_type_desc)

    class Meta:
        managed = False
        db_table = 'job_config'


class JobLogs(models.Model):
    uuid = models.UUIDField(primary_key=True)
    business_id = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.SmallIntegerField(blank=True, null=True)
    job_status = models.SmallIntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    job_message = models.CharField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.uuid)

    class Meta:
        managed = False
        db_table = 'job_logs'
