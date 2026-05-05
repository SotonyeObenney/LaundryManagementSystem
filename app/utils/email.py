from flask_mail import Message
from ..extensions import mail
from flask import current_app
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_verification_alert(user_email, order_id, mismatches):
    """Sends email if items exceed limit or mismatch."""
    app = current_app._get_current_object()
    msg = Message(f"Action Required: Laundry Order #{order_id}",
                  recipients=[user_email],
                  sender="admin@nilelaundry.com")
    
    msg.body = f"Hello, your order #{order_id} has been processed. \n\n"
    msg.body += "Issues found during verification:\n" + "\n".join(mismatches)
    msg.body += "\n\nPlease visit the laundry office as your order exceeds the 30-item limit."
    
    Thread(target=send_async_email, args=(app, msg)).start()