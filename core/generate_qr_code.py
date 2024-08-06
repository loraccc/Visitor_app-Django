# generate_qr_code.py

import qrcode

def generate_qr_code():
    # Construct the URL for the review form
    review_url = "http://127.0.0.1:8000/submit-review/"  # Local development URL

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(review_url)
    qr.make(fit=True)

    # Create the QR code image
    img = qr.make_image(fill_color="white", back_color="red")

    # Save or display the QR code image as needed
    img.save("qr_code_review_form.png")

# Generate the QR code for the review form
generate_qr_code()
