from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from . import bookings_bp
from .forms import OrderForm
from ..models import Service, Order, OrderItem
from ..extensions import db

@bookings_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_order():
    form = OrderForm()
    # Dynamically fill the dropdown from our Service table
    services = db.session.execute(db.select(Service)).scalars().all()
    form.service_type.choices = [(s.id, f"{s.service_type} (₦{s.price_per_unit}/item)") for s in services]

    if form.validate_on_submit():
        # 1. Check the 30-item constraint
        total_items = (form.shirts_tops.data + form.trousers_bottoms.data + 
                       form.traditional_wear.data + form.light_wear.data + form.heavy_wear.data)
        
        if total_items > 30:
            flash("Order exceeds the 30-item limit!", "danger")
            return render_template("bookings/create.html", form=form)
        
        if total_items == 0:
            flash("You cannot place an empty order.", "warning")
            return render_template("bookings/create.html", form=form)

        # 2. Get the selected service
        selected_service = db.session.get(Service, form.service_type.data)
        
        try:
            # 3. Create the Order (The Container)
            new_order = Order(
                customer_id=current_user.id,
                service_type=selected_service.service_type,
                status="pending",
                delivery_fee=500.0  # Standard Nile Campus fee
            )
            db.session.add(new_order)
            db.session.flush() # This gives us new_order.id without committing yet

            # 4. Create OrderItems for categories with quantity > 0
            categories = {
                "Shirts & Tops": form.shirts_tops.data,
                "Trousers & Bottoms": form.trousers_bottoms.data,
                "Traditional Wear": form.traditional_wear.data,
                "Light Wear": form.light_wear.data,
                "Heavy Wear": form.heavy_wear.data
            }

            running_total = 0
            for item_name, qty in categories.items():
                if qty > 0:
                    cost = qty * selected_service.price_per_unit
                    item = OrderItem(
                        order_id=new_order.id,
                        service_id=selected_service.id,
                        item_type=item_name,
                        quantity=qty,
                        price=selected_service.price_per_unit
                    )
                    db.session.add(item)
                    running_total += item.calculate_cost()

            # 5. Finalize Order price
            new_order.total_price = running_total + new_order.delivery_fee
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            flash("An error occurred while placing your order. Please try again.", "danger")
            return render_template("bookings/create.html", form=form)
        
        
        flash("Order placed successfully! Please wait for staff verification.", "success")
        return redirect(url_for('auth.register')) # Change to Dashboard later

    return render_template("bookings/create.html", form=form)