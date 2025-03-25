from django.db import models
import qrcode
import os
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

logo_path = os.path.join(settings.STATIC_ROOT, "images/Logo_Motek.png")

class RegisteredUser(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15, unique=True)
    mail = models.EmailField(unique=True)
    id_card = models.CharField(max_length=50, unique=True)
    city = models.CharField(max_length=50)
    number_of_tickets = models.PositiveIntegerField()

    # Tickets (Optional, up to 6)
    ticket1 = models.CharField(max_length=50, blank=True, null=True)
    ticket2 = models.CharField(max_length=50, blank=True, null=True)
    ticket3 = models.CharField(max_length=50, blank=True, null=True)
    ticket4 = models.CharField(max_length=50, blank=True, null=True)
    ticket5 = models.CharField(max_length=50, blank=True, null=True)
    ticket6 = models.CharField(max_length=50, blank=True, null=True)

    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.mail})"

    def get_tickets(self):
        """Return all non-empty tickets as a list."""
        return [ticket for ticket in [
            self.ticket1, self.ticket2, self.ticket3,
            self.ticket4, self.ticket5, self.ticket6
        ] if ticket]

    # def save(self, *args, **kwargs):
    #     # Generate QR code
    #     qr = qrcode.QRCode(
    #         version=1,
    #         error_correction=qrcode.constants.ERROR_CORRECT_L,
    #         box_size=10,
    #         border=4,
    #     )
    #     qr.add_data(self.mail)
    #     qr.make(fit=True)
        
    #     qrcode_img = qr.make_image(fill="black", back_color="white").convert("RGB")

    #     # Create a white canvas with the same size as the QR code
    #     canvas = Image.new("RGB", qrcode_img.size, "white")

    #     # Paste the QR code onto the canvas
    #     canvas.paste(qrcode_img, (0, 0))  

    #     # Save the image to a buffer
    #     fname = f"qr_code-{self.id_card}.png"
    #     buffer = BytesIO()
    #     canvas.save(buffer, format="PNG")

    #     # Save the QR code to the model field
    #     self.qr_code.save(fname, File(buffer), save=False)
        
    #     canvas.close()
    #     super().save(*args, **kwargs)



    def save(self, *args, **kwargs):
        print('\n\n PATH - ', logo_path, '\n\n')
        # Load assets
        # logo_path = "path/to/logo.png"  # Replace with the actual path to your logo
        font_path = "path/to/font.ttf"  # Replace with an actual TTF font file

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(self.mail)
        qr.make(fit=True)
        
        qrcode_img = qr.make_image(fill="black", back_color="white").convert("RGB")

        # Define sizes
        ticket_width = max(qrcode_img.width + 40, 400)
        ticket_height = qrcode_img.height + 500  # Adjust height for header and texts
        header_height = 70
        logo_size = (int(qrcode_img.width*.8), int(qrcode_img.height*.8))
        text_height = 50

        # Create ticket canvas
        ticket = Image.new("RGB", (ticket_width, ticket_height), "lightblue")
        draw = ImageDraw.Draw(ticket)

        # Load and paste logo
        logo = Image.open(logo_path).resize(logo_size)
        logo_x = (ticket_width - logo.width) // 2
        ticket.paste(logo, (logo_x, header_height), logo if logo.mode == "RGBA" else None)

        # Load font
        try:
            font = ImageFont.truetype("arial.ttf", 32) 
        except:
            font = ImageFont.load_default()

        # Draw event details
        # date_text = f"מועד: {self.event_date}"  # Example: "17.04.25"
        # time_text = f"שעה: {self.event_time}"   # Example: "14:00-17:30"

        date_text = f"מועד: 17.04.25"
        time_text = f"שעה: 14:00-17:30"

        # Header text
        header_text = f"Header text"
        header_text_bbox = draw.textbbox((0, 0), header_text, font=font)
        header_text_width = header_text_bbox[2] - header_text_bbox[0]
        draw.text(((ticket_width - header_text_width) // 2, 20), header_text, fill="white", font=font)


        # Calculate text width to center it
        date_text_bbox = draw.textbbox((0, 0), date_text, font=font)
        date_text_width = date_text_bbox[2] - date_text_bbox[0]
        time_text_bbox = draw.textbbox((0, 0), time_text, font=font)
        time_text_width = time_text_bbox[2] - time_text_bbox[0]

        # Draw event details centered
        draw.text(((ticket_width - date_text_width) // 2, header_height + logo_size[1]), date_text, fill="white", font=font)
        draw.text(((ticket_width - time_text_width) // 2, header_height + logo_size[1] + text_height), time_text, fill="white", font=font)

        # Paste QR code
        qr_x = (ticket_width - qrcode_img.width) // 2
        ticket.paste(qrcode_img, (qr_x, header_height + logo_size[1] + text_height*2))

        # Save image to buffer
        fname = f"ticket-{self.id_card}.png"
        buffer = BytesIO()
        ticket.save(buffer, format="PNG")

        # Save to model field
        self.qr_code.save(fname, File(buffer), save=False)

        ticket.close()
        super().save(*args, **kwargs)




