from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Optional

# Форма для добавления нового поставщика
class SupplierForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    contact_phone = StringField('Contact Phone', validators=[DataRequired()])
    cooperation_date = DateField('Cooperation Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Confirm')  # Кнопка отправки формы

# Форма для добавления нового сотрудника
class EmployeeForm(FlaskForm):
    employee_name = StringField('Employee Name', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    salary = DecimalField('Salary', validators=[DataRequired()])
    contract_date = DateField('Contract Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Confirm')  # Кнопка отправки формы

 # Форма для добавления нового элемента доставки
class DeliveryForm(FlaskForm):
    delivery_date = DateField('Delivery Date', format='%Y-%m-%d', validators=[DataRequired()])
    supplier_id = IntegerField('Supplier ID', validators=[DataRequired()])
    employee_id = IntegerField('Employee ID', validators=[DataRequired()])
    submit = SubmitField('Confirm')  # Кнопка отправки формы

# Форма для добавления нового букета
class BouquetForm(FlaskForm):
    name = StringField('Bouquet Name', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Confirm')  # Кнопка отправки формы

# Форма для добавления нового цветка
class FlowerForm(FlaskForm):
    shelf_life = IntegerField('Shelf Life', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    submit = SubmitField('Confirm')  # Кнопка отправки формы

# Форма для добавления дополнительного материала
class AdditionalMaterialForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Confirm')  # Кнопка отправки формы

# Форма для добавления нового продукта
class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    unit_price = DecimalField('Unit Price', validators=[DataRequired()])
    bouquet_id = IntegerField('Bouquet ID', validators=[Optional()])
    flower_id = IntegerField('Flower ID', validators=[Optional()])
    material_id = IntegerField('Material ID', validators=[Optional()])
    submit = SubmitField('Confirm')  # Кнопка отправки формы

# Форма для добавления нового клиента
class ClientForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    first_order_date = DateField('First Order Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Confirm')  # Кнопка отправки формы

# Форма для добавления нового заказа
class OrderForm(FlaskForm):
    order_date = DateField('Order Date', format='%Y-%m-%d', validators=[DataRequired()])
    order_status = StringField('Order Status', validators=[DataRequired()])
    employee_id = IntegerField('Employee ID', validators=[DataRequired()])
    client_id = IntegerField('Client ID', validators=[DataRequired()])
    submit = SubmitField('Confirm')  # Кнопка отправки формы

# Форма для добавления детали заказа
class OrderDetailForm(FlaskForm):
    order_id = IntegerField('Order ID', validators=[DataRequired()])
    product_id = IntegerField('Product ID', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    purchase_price = DecimalField('Purchase Price', validators=[DataRequired()])
    submit = SubmitField('Confirm')  # Кнопка отправки формы

# Форма для добавления нового платежа
class PaymentForm(FlaskForm):
    order_id = IntegerField('Order ID', validators=[DataRequired()])
    payment_date = DateField('Payment Date', format='%Y-%m-%d', validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired()])
    payment_method = StringField('Payment Method', validators=[DataRequired()])
    submit = SubmitField('Confirm')  # Кнопка отправки формы

# Форма для добавления нового элемента доставки
class DeliveryDetailForm(FlaskForm):
    delivery_id = IntegerField('Delivery ID', validators=[DataRequired()])
    product_id = IntegerField('Product ID', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    purchase_price = DecimalField('Purchase Price', validators=[DataRequired()])
    submit = SubmitField('Confirm')  # Кнопка отправки формы
