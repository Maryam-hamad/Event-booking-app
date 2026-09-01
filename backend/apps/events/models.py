from django.db import models


class Event(models.Model):
    # Short human-readable name for the event (required, max 255 chars)
    title = models.CharField(max_length=255)

    # Full text description of the event (required, unlimited length)
    description = models.TextField()

    # Physical or virtual location string (required, max 255 chars)
    location = models.CharField(max_length=255)

    # Exact date and time the event takes place (required)
    date = models.DateTimeField()

    # Maximum number of attendees allowed; enforced as positive integer
    capacity = models.PositiveIntegerField()

    # Timestamp set once when the record is first saved; never updated
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']  # Default ordering: soonest events first

    def __str__(self):
        return f"{self.title} ({self.date:%Y-%m-%d})"
