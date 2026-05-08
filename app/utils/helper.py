from datetime import timedelta

def calculate_delivery_date(payment_date):
    """
    Assigns delivery to the next available Monday (0) or Thursday (3)
    after the payment_date.
    """
    # 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
    current_weekday = payment_date.weekday()
    
    if current_weekday < 3:
        days_ahead = 3 - current_weekday
    else:
        days_ahead = 7 - current_weekday
        
    return payment_date + timedelta(days=days_ahead)
