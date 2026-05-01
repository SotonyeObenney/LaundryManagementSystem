from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class OrderForm(FlaskForm):
    # Service selection (Wash & Fold, Ironing, Dry Clean)
    service_type = SelectField("Service Type", choices=[], coerce=int, validators=[DataRequired()])
    
    # Quantities for the 5 SRS Categories
    shirts_tops = IntegerField("Shirts & Tops", default=0, validators=[NumberRange(min=0)])
    trousers_bottoms = IntegerField("Trousers & Bottoms", default=0, validators=[NumberRange(min=0)])
    traditional_wear = IntegerField("Traditional Wear", default=0, validators=[NumberRange(min=0)])
    light_wear = IntegerField("Light Wear (Underwear/Socks)", default=0, validators=[NumberRange(min=0)])
    heavy_wear = IntegerField("Heavy Wear (Jackets/Bedding)", default=0, validators=[NumberRange(min=0)])
    
    submit = SubmitField("Place Order")