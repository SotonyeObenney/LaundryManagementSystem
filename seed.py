from app import create_app
from app.extensions import db
from app.models import Service

app = create_app()
with app.app_context():
    # Clear existing if any
    db.session.query(Service).delete()
    
    services = [
        Service(service_type="Wash & Iron", price_per_unit=500.0, description="Cleaned and pressed"),
        Service(service_type="Wash & Fold", price_per_unit=350.0, description="Cleaned and neatly folded"),
        Service(service_type="Ironing Only", price_per_unit=200.0, description="Professional pressing only"),
        Service(service_type="Dry Cleaning", price_per_unit=1200.0, description="For suits and delicate fabrics")
    ]
    
    db.session.add_all(services)
    db.session.commit()
    print("Services seeded successfully!")