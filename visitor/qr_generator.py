import qrcode
from django.http import HttpResponse
from io import BytesIO

def generate_qr_code(request):
    
    # URL of the phone number form
    data = request.build_absolute_uri('/number_form')
    
    # generate qr code 
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    #create an image
    img = qr.make_image(fill_color="black", back_color="white")

    #save image to a BytesIO object
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Create an HTTP response with the image
    return HttpResponse(buffer, content_type='image/png')