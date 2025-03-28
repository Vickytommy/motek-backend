from django.db import models
import qrcode
import os
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
import arabic_reshaper
from bidi.algorithm import get_display


logo_path = os.path.join(settings.STATIC_ROOT, "images/Logo_Motek.png")

# Get the absolute path to the font file inside your project
arial_font_path = os.path.join(os.path.dirname(__file__), "fonts", "arial.ttf")

class UserLimit(models.Model):
    ticket_day = models.CharField(max_length=50, default='')
    ticket_time = models.CharField(max_length=50, default='')
    cycle_count = models.IntegerField(default=2000)
    current_count = models.IntegerField(default=0)
    color_code = models.CharField(max_length=50, default='#5ec6cc')
    image = models.CharField(max_length=50, default='')
    
class RegisteredUser(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15, unique=True)
    mail = models.EmailField(unique=True)
    id_card = models.CharField(max_length=50, unique=True)
    city = models.CharField(max_length=50)
    number_of_tickets = models.PositiveIntegerField()
    date = models.CharField(max_length=50, default='')
    time = models.CharField(max_length=50, default='')


    # Tickets (Optional, up to 6)
    extra_name1 = models.CharField(max_length=50, blank=True, null=True)
    extra_name2 = models.CharField(max_length=50, blank=True, null=True)
    extra_name3 = models.CharField(max_length=50, blank=True, null=True)
    extra_name4 = models.CharField(max_length=50, blank=True, null=True)
    extra_name5 = models.CharField(max_length=50, blank=True, null=True)
    extra_name6 = models.CharField(max_length=50, blank=True, null=True)

    ticket = models.ImageField(upload_to="ticket/", blank=True, null=True)
    extra_ticket1 = models.ImageField(upload_to="ticket/", blank=True, null=True)
    extra_ticket2 = models.ImageField(upload_to="ticket/", blank=True, null=True)
    extra_ticket3 = models.ImageField(upload_to="ticket/", blank=True, null=True)
    extra_ticket4 = models.ImageField(upload_to="ticket/", blank=True, null=True)
    extra_ticket5 = models.ImageField(upload_to="ticket/", blank=True, null=True)
    extra_ticket6 = models.ImageField(upload_to="ticket/", blank=True, null=True)


    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.mail})"

    def get_tickets(self):
        """Return all non-empty tickets as a list."""
        return [name for name in [
            self.extra_name1, self.extra_name2, self.extra_name3,
            self.extra_name4, self.extra_name5, self.extra_name6
        ] if name]


    # def save(self, *args, **kwargs):
    #     # Load the pre-designed ticket template
    #     image_type = UserLimit.objects.filter(ticket_day=self.date, ticket_time=self.time).first().image
    #     ticket_template_path = os.path.join(settings.MEDIA_ROOT, image_type)
    #     ticket = Image.open(ticket_template_path).convert("RGB")
        
    #     # Generate QR code
    #     qr = qrcode.QRCode(
    #         version=1,
    #         error_correction=qrcode.constants.ERROR_CORRECT_L,
    #         box_size=10,
    #         border=2,
    #     )
    #     qr.add_data(self.mail)
    #     qr.make(fit=True)
        
    #     qrcode_img = qr.make_image(fill="black", back_color="white").convert("RGB")

    #     # Resize QR code (optional, adjust to fit your template)
    #     qr_code_size = (1250, 1250)  # Adjust this based on your ticket design
    #     qrcode_img = qrcode_img.resize(qr_code_size)

    #     # Define the QR code position (adjust this based on your ticket template)
    #     qr_x, qr_y = 510, 1980  # Example values; adjust to your template

    #     # Paste QR code onto the ticket
    #     ticket.paste(qrcode_img, (qr_x, qr_y))

    #     # Save image to buffer
    #     fname = f"ticket-{self.id_card}.png"
    #     buffer = BytesIO()
    #     ticket.save(buffer, format="PNG")

    #     # Save to model field
    #     self.ticket.save(fname, File(buffer), save=False)

    #     ticket.close()
    #     super().save(*args, **kwargs)


    def save(self, *args, **kwargs):
        # Generate tickets for the main user and additional tickets
        self.generate_ticket(self.mail, f"{self.firstname} {self.lastname}", 0)
        
        # Check through the number of tickets and generate for each extra ticket
        extra_names = [
            self.extra_name1, self.extra_name2, self.extra_name3,
            self.extra_name4, self.extra_name5, self.extra_name6
        ]
        
        for i, extra_name in enumerate(extra_names, start=1):
            if extra_name:  # Only generate tickets for non-empty extra names
                self.generate_ticket(self.mail, extra_name, i)
        
        super().save(*args, **kwargs)


    def generate_ticket(self, mail, name, num):
        image_type = UserLimit.objects.filter(ticket_day=self.date, ticket_time=self.time).first().image
        ticket_template_path = os.path.join(settings.MEDIA_ROOT, image_type)
        ticket = Image.open(ticket_template_path).convert("RGB")
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(f"Name: {name}, Email: {mail}")
        qr.make(fit=True)
        
        qrcode_img = qr.make_image(fill="black", back_color="white").convert("RGB")

        # Resize QR code (optional, adjust to fit your template)
        qr_code_size = (1250, 1250)  # Adjust this based on your ticket design
        qrcode_img = qrcode_img.resize(qr_code_size)

        # Define the QR code position (adjust this based on your ticket template)
        qr_x, qr_y = 510, 1980  # Example values; adjust to your template

        # Paste QR code onto the ticket
        ticket.paste(qrcode_img, (qr_x, qr_y))
        
        # Reduce the entire image size by 50%
        new_size = (ticket.width // 2, ticket.height // 2)
        ticket = ticket.resize(new_size, Image.ANTIALIAS)  # Smooth resizing

        # Save image to buffer
        fname = f"ticket-{self.id_card}-{name}.png"
        buffer = BytesIO()
        ticket.save(buffer, format="PNG")

        # Save to model field
        if num == 0:
            self.ticket.save(fname, File(buffer), save=False)
        elif num == 1:
            self.extra_ticket1.save(fname, File(buffer), save=False)
        elif num == 2:
            self.extra_ticket2.save(fname, File(buffer), save=False)
        elif num == 3:
            self.extra_ticket3.save(fname, File(buffer), save=False)
        elif num == 4:
            self.extra_ticket4.save(fname, File(buffer), save=False)
        elif num == 5:
            self.extra_ticket5.save(fname, File(buffer), save=False)
        elif num == 6:
            self.extra_ticket6.save(fname, File(buffer), save=False)

        ticket.close()


