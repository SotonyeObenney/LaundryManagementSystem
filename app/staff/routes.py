from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required
from . import staff_bp
from ..models import Order, User
from ..extensions import db
from ..utils.decorators import staff_required 
from ..utils.email import send_verification_alert 


@staff_bp.route("/dashboard")
@login_required
@staff_required
def dashboard():
    """The Command Center: Business Health & Navigation."""
    # Analytics for the 'Health of the Business' (Requirement 1.2 Performance)
    stats = {
        'total_pending': db.session.execute(db.select(db.func.count(Order.id)).where(Order.status.in_(['pending', 'received']))).scalar(),
        'total_verified': db.session.execute(db.select(db.func.count(Order.id)).where(Order.status == 'verified')).scalar(),
        'total_paid': db.session.execute(db.select(db.func.count(Order.id)).where(Order.status == 'paid')).scalar(),
        'today_revenue': db.session.execute(db.select(db.func.sum(Order.total_price)).where(Order.status.in_(['paid', 'out_for_delivery', 'delivered']))).scalar() or 0,
        'active_customers': db.session.execute(db.select(db.func.count(User.id)).where(User.role == 'customer')).scalar()
    }
    return render_template("staff/dashboard.html", stats=stats)


@staff_bp.route("/pending-orders")
@login_required
@staff_required
def get_pending_orders():
    """US 3.1: Admin can view all pending orders."""
    orders = db.session.execute(
        db.select(Order).where(Order.status.in_(['pending', 'received']))
    ).scalars().all()
    return render_template("staff/pending-orders.html", orders=orders)

@staff_bp.route("/receive-order/<int:order_id>", methods=["POST"])
@login_required
@staff_required
def receive_order(order_id):
    order = db.session.get(Order, order_id)
    if order:
        order.status = "received"
        db.session.commit()
        flash(f"Order #{order.id} marked as Received.", "info")
    return redirect(url_for('staff.get_pending_orders'))

@staff_bp.route("/verify-order/<int:order_id>", methods=["GET", "POST"])
@login_required
@staff_required
def verify_order(order_id):
    """US 3.1 & 4.1: Confirm clothes match and generate price."""
    order = db.session.get(Order, order_id)
    
    if request.method == "POST":
        total_items = 0
        mismatched_categories = []

        # Update quantities based on physical count
        for item in order.items:
            physical_count = request.form.get(f"item_{item.id}", type=int)
            if physical_count is not None:
                # Track if there's a mismatch for the email alert
                if physical_count != item.quantity:
                    mismatched_categories.append(f"{item.item_type}: expected {item.quantity}, found {physical_count}")
                
                item.quantity = physical_count
                total_items += physical_count

        # 2. Check 30-item limit (SRS Requirement)
        if total_items > 30:
            order.status = "limit_exceeded"
            flash("Order exceeds 30 items. Student notified.", "warning")
        else:
            # US 3.1 & 4.1: Finalize Verification and Price
            order.status = "verified"
            # Calculate total based on verified items + delivery fee
            item_total = sum(i.quantity * i.price for i in order.items)
            order.total_price = item_total + order.delivery_fee
            flash(f"Order #{order.id} verified. Total: ₦{order.total_price}", "success")

        if total_items > 30 or len(mismatched_categories) > 0: 
            # US 3.1: Trigger email notification
            print(total_items)
            send_verification_alert(order.customer.email, order.id, mismatched_categories, total_items)

        db.session.commit()
        return redirect(url_for('staff.dashboard'))

    return render_template("staff/verify-orders.html", order=order)


@staff_bp.route("/paid-orders")
@login_required
@staff_required
def get_paid_orders():
    """US 4.3: Staff views only paid orders ready for processing."""
    orders = db.session.execute(
        db.select(Order).where(Order.status == 'paid')
    ).scalars().all()
    return render_template("staff/paid-orders.html", orders=orders)

@staff_bp.route("/dispatch-order/<int:order_id>", methods=["POST"])
@login_required
@staff_required
def dispatch_order(order_id):
    """US 5.2: Mark order as Out for Delivery."""
    order = db.session.get(Order, order_id)
    if order and order.status == 'paid':
        order.status = 'out_for_delivery'
        db.session.commit()
        flash(f"Order #{order.id} is now out for delivery!", "success")
        return redirect(url_for('staff.get_paid_orders'))


@staff_bp.route("/delivery-queue")
@login_required
@staff_required
def delivery_queue():
    """US 5.3: The final stage. Orders waiting for handover."""
    orders = db.session.execute(
        db.select(Order).where(Order.status == 'out_for_delivery')
    ).scalars().all()
    return render_template("staff/delivery-queue.html", orders=orders)

@staff_bp.route("/confirm-delivery/<int:order_id>", methods=["POST"])
@login_required
@staff_required
def confirm_delivery(order_id):
    """US 5.3: Verification of Order ID and final handover."""
    order = db.session.get(Order, order_id)
    if order and order.status == 'out_for_delivery':
        order.status = 'delivered'
        db.session.commit()
        flash(f"Order #{order.id} handed over to {order.customer.name}!", "success")
    return redirect(url_for('staff.delivery_queue'))



# ----------- Test email(mailtrap) with fake data --------
# @staff_bp.route("/test-email")
# @staff_required
# def test_email_flow():
#     # Provide fake data
#     recipient = "student-test@example.com"
#     order_id = 12345
#     issues = ["Jeans: Found 5, expected 1", "T-shirts: Found 20, expected 15"]
    
#     try:
#         send_verification_alert(recipient, order_id, issues)
#         return "<h3>Email task started!</h3>Check your Mailtrap Sandbox inbox in a few seconds."
#     except Exception as e:
#         return f"<h3>It failed!</h3> Error: {str(e)}"

