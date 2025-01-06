from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Supplier, Employee, Delivery, Bouquet, Flower, AdditionalMaterial, Product, Client, Order, OrderDetail, Payment, DeliveryDetail
from forms import (
    SupplierForm, EmployeeForm,DeliveryForm, BouquetForm, FlowerForm,
    AdditionalMaterialForm, ProductForm, ClientForm, OrderForm,
    OrderDetailForm, PaymentForm, DeliveryDetailForm
)
from datetime import datetime
from decimal import Decimal

# Создание экземпляра приложения Flask
app = Flask(__name__)

# Загрузка конфигурации
app.config.from_object('config')

# Инициализация SQLAlchemy
db.init_app(app)

# Инициализация Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Настройка страницы логина
login_manager.login_view = 'login'

# Функция загрузки пользователя
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))  # Если пользователь уже залогинен, направляем его на главную страницу
    return redirect(url_for('login'))  # Если пользователь не залогинен, редиректим на страницу логина


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:  # Проверка пароля без хэширования
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin_action'))  # Редиректим на страницу выбора действий
            else:
                return redirect(url_for('user_dashboard'))  # Для пользователей редирект на их страницу
        else:
            flash('Invalid credentials, try again.')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('user_dashboard'))


@app.route('/admin_action')
@login_required
def admin_action():
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('login'))

    return render_template('admin_action.html')  # Убедитесь, что этот файл существует


@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('login'))

    # Данные для администратора
    suppliers = Supplier.query.all()
    employees = Employee.query.all()
    deliveries = Delivery.query.all()
    bouquets = Bouquet.query.all()
    flowers = Flower.query.all()
    materials = AdditionalMaterial.query.all()
    products = Product.query.all()
    clients = Client.query.all()
    orders = Order.query.all()
    order_details = OrderDetail.query.all()
    payments = Payment.query.all()
    delivery_details = DeliveryDetail.query.all()


    return render_template(
        'admin_dashboard.html',
        suppliers=suppliers,
        employees=employees,
        deliveries=deliveries,
        bouquets=bouquets,
        flowers=flowers,
        additional_materials=materials,
        products=products,
        clients=clients,
        orders=orders,
        order_details=order_details,
        payments=payments,
        delivery_details=delivery_details,
    )

#-------------------------------------------------------------------------------------------------------------


@app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    supplier_form = SupplierForm()

    if supplier_form.validate_on_submit():
        # Создание нового поставщика
        new_supplier = Supplier(
            company_name=supplier_form.company_name.data,
            contact_phone=supplier_form.contact_phone.data,
            cooperation_date=supplier_form.cooperation_date.data,
        )
        # Сохранение в базе данных
        db.session.add(new_supplier)
        db.session.commit()

        # Уведомление и возврат на панель администратора
        flash('Supplier added successfully!')
        return redirect(url_for('admin_dashboard') + "#suppliers")

    # Отображение страницы добавления поставщика
    return render_template('add_supplier.html', supplier_form=supplier_form)

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    employee_form = EmployeeForm()

    if employee_form.validate_on_submit():
        new_employee = Employee(
            employee_name=employee_form.employee_name.data,
            position=employee_form.position.data,
            salary=employee_form.salary.data,
            contract_date=employee_form.contract_date.data
        )
        db.session.add(new_employee)
        db.session.commit()
        flash('Employee added successfully!')
        return redirect(url_for('admin_dashboard') + "#employees")

    # Отображение страницы добавления поставщика
    return render_template('add_employee.html', employee_form=employee_form,)

@app.route('/add_delivery', methods=['GET', 'POST'])
def add_delivery():
    delivery_form = DeliveryForm()

    if delivery_form.validate_on_submit():
        new_delivery = Delivery(
            delivery_date=delivery_form.delivery_date.data,
            supplier_id=delivery_form.supplier_id.data,  # предполагается, что supplier соответствует supplier_id
            employee_id=delivery_form.employee_id.data  # предполагается, что employee соответствует employee_id
        )
        db.session.add(new_delivery)
        db.session.commit()
        flash('Delivery added successfully!')
        return redirect(url_for('admin_dashboard') + "#deliveries")

    # Отображение страницы добавления поставщика
    return render_template('add_delivery.html', delivery_form=delivery_form,)

@app.route('/add_bouquet', methods=['GET', 'POST'])
def add_bouquet():
    bouquet_form = BouquetForm()

    if bouquet_form.validate_on_submit():
        new_bouquet = Bouquet(
            name=bouquet_form.name.data,
            price=bouquet_form.price.data,
            description=bouquet_form.description.data
        )
        db.session.add(new_bouquet)
        db.session.commit()
        flash('Bouquet added successfully!')
        return redirect(url_for('admin_dashboard') + "#bouquets")

    # Отображение страницы добавления поставщика
    return render_template('add_bouquet.html', bouquet_form=bouquet_form,)

@app.route('/add_flower', methods=['GET', 'POST'])
def add_flower():
    flower_form = FlowerForm()
    if flower_form.validate_on_submit():
        new_flower = Flower(
            shelf_life=flower_form.shelf_life.data,
            description=flower_form.description.data,
            price=flower_form.price.data
        )
        db.session.add(new_flower)
        db.session.commit()
        flash('Flower added successfully!')
        return redirect(url_for('admin_dashboard') + "#flowers")

    # Отображение страницы добавления поставщика
    return render_template('add_flower.html', flower_form=flower_form,)

@app.route('/add_material', methods=['GET', 'POST'])
def add_material():
    material_form = AdditionalMaterialForm()
    if material_form.validate_on_submit():
        new_material = AdditionalMaterial(
            description=material_form.description.data
        )
        db.session.add(new_material)
        db.session.commit()
        flash('Material added successfully!')
        return redirect(url_for('admin_dashboard') + "#additional_materials")

    # Отображение страницы добавления поставщика
    return render_template('add_material.html', material_form=material_form,)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    product_form = ProductForm()
    if product_form.validate_on_submit():
        try:
            new_product = Product(
                product_name=product_form.product_name.data,
                unit_price=product_form.unit_price.data,
                bouquet_id=product_form.bouquet_id.data,
                flower_id=product_form.flower_id.data,
                material_id=product_form.material_id.data
            )
            db.session.add(new_product)
            db.session.commit()
            flash('Product added successfully!')
            return redirect(url_for('admin_dashboard') + "#products")
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding product: {e}')
    else:
        if product_form.errors:
            flash(f'Form validation errors: {product_form.errors}')

    return render_template('add_product.html', product_form=product_form)

@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    client_form = ClientForm()
    if client_form.validate_on_submit():
        new_client = Client(
            full_name=client_form.full_name.data,
            age=client_form.age.data,
            phone_number=client_form.phone_number.data,
            first_order_date=client_form.first_order_date.data
        )
        db.session.add(new_client)
        db.session.commit()
        flash('Client added successfully!')
        return redirect(url_for('admin_dashboard') + "#clients")

    return render_template('add_client.html', client_form=client_form,)

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    order_form = OrderForm()
    if order_form.validate_on_submit():
        new_order = Order(
            order_date=order_form.order_date.data,
            employee_id=order_form.employee_id.data,
            client_id=order_form.client_id.data,
            order_status=order_form.order_status.data
        )
        db.session.add(new_order)
        db.session.commit()
        flash('Order added successfully!')
        return redirect(url_for('admin_dashboard') + "#orders")

    return render_template('add_order.html',order_form=order_form,)

@app.route('/add_payment', methods=['GET', 'POST'])
def add_payment():
    payment_form = PaymentForm()
    if payment_form.validate_on_submit():
        new_payment = Payment(
            order_id=payment_form.order_id.data,
            payment_date=payment_form.payment_date.data,
            amount=payment_form.amount.data,
            payment_method=payment_form.payment_method.data
        )
        db.session.add(new_payment)
        db.session.commit()
        flash('Payment added successfully!')
        return redirect(url_for('admin_dashboard') + "#payments")

    return render_template('add_payment.html', payment_form=payment_form,)

@app.route('/add_delivery_detail', methods=['GET', 'POST'])
def add_delivery_detail():
    delivery_detail_form = DeliveryDetailForm()
    if delivery_detail_form.validate_on_submit():
        new_delivery_detail = DeliveryDetail(
            delivery_id=delivery_detail_form.delivery_id.data,
            product_id=delivery_detail_form.product_id.data,
            quantity=delivery_detail_form.quantity.data,
            purchase_price=delivery_detail_form.purchase_price.data
        )
        db.session.add(new_delivery_detail)
        db.session.commit()
        flash('Delivery detail added successfully!')
        return redirect(url_for('admin_dashboard') + "#delivery_details")

    return render_template('add_delivery_detail.html', delivery_detail_form=delivery_detail_form)

@app.route('/add_order_detail', methods=['GET', 'POST'])
def add_order_detail():
    order_detail_form = OrderDetailForm()
    if order_detail_form.validate_on_submit():
        new_order_detail = OrderDetail(
            order_id=order_detail_form.order_id.data,
            product_id=order_detail_form.product_id.data,
            quantity=order_detail_form.quantity.data,
            purchase_price=order_detail_form.purchase_price.data
        )
        db.session.add(new_order_detail)
        db.session.commit()
        flash('Order detail added successfully!')
        return redirect(url_for('admin_dashboard') + "#order_details")

    return render_template('add_order_detail.html', order_detail_form=order_detail_form,)

#-------------------------------------------------------------------------------------------------------------
@app.route('/edit_supplier/<int:supplier_id>', methods=['GET', 'POST'])
def edit_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    form = SupplierForm(obj=supplier)  # Заполнение формы текущими данными поставщика

    if form.validate_on_submit():
        supplier.company_name = form.company_name.data
        supplier.contact_phone = form.contact_phone.data
        supplier.cooperation_date = form.cooperation_date.data

        # Обновление зависимых записей, если необходимо
        for delivery in supplier.deliveries:
            delivery.company_name = supplier.company_name  # Если это поле существует

        db.session.commit()
        flash('Supplier updated successfully!', 'success')
        return redirect(url_for('admin_dashboard') + "#suppliers")

    return render_template('edit_supplier.html', form=form, supplier=supplier)

@app.route('/edit_employee/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    form = EmployeeForm(obj=employee)

    if form.validate_on_submit():
        employee.employee_name = form.employee_name.data
        employee.position = form.position.data
        employee.salary = form.salary.data
        employee.contract_date = form.contract_date.data

        # Обновление зависимых записей, если необходимо
        for delivery in employee.deliveries:
            delivery.employee_name = employee.employee_name  # Если это поле существует

        db.session.commit()
        flash('Employee updated successfully!', 'success')
        return redirect(url_for('admin_dashboard') + "#employees")

    return render_template('edit_employee.html', form=form, employee=employee)

@app.route('/edit_delivery/<int:delivery_id>', methods=['GET', 'POST'])
def edit_delivery(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    form = DeliveryForm(obj=delivery)

    if form.validate_on_submit():
        delivery.delivery_date = form.delivery_date.data
        delivery.supplier_id = form.supplier_id.data
        delivery.employee_id = form.employee_id.data

        # Обновление зависимых записей, если необходимо
        for detail in delivery.delivery_details:
            detail.delivery_date = delivery.delivery_date  # Пример обновления связанных записей

        db.session.commit()
        flash('Delivery updated successfully!', 'success')
        return redirect(url_for('admin_dashboard') + "#deliveries")

    return render_template('edit_delivery.html', form=form, delivery=delivery)

@app.route('/edit_bouquet/<int:bouquet_id>', methods=['GET', 'POST'])
def edit_bouquet(bouquet_id):
    bouquet = Bouquet.query.get_or_404(bouquet_id)
    form = BouquetForm(obj=bouquet)

    if form.validate_on_submit():
        bouquet.name = form.name.data
        bouquet.price = form.price.data
        bouquet.description = form.description.data

        db.session.commit()
        flash('Bouquet updated successfully!', 'success')
        return redirect(url_for('admin_dashboard') + "#bouquets")

    return render_template('edit_bouquet.html', form=form, bouquet=bouquet)

@app.route('/edit_flower/<int:flower_id>', methods=['GET', 'POST'])
def edit_flower(flower_id):
    flower = Flower.query.get_or_404(flower_id)
    form = FlowerForm(obj=flower)

    if form.validate_on_submit():
        # Обновляем только информацию о цветке, не затрагивая связанные продукты
        flower.shelf_life = form.shelf_life.data
        flower.description = form.description.data
        flower.price = form.price.data

        # Продукты, связанные с этим цветком, остаются без изменений
        db.session.commit()
        flash('Flower updated successfully!', 'success')
        return redirect(url_for('admin_dashboard') + "#flowers")

    return render_template('edit_flower.html', form=form, flower=flower)

@app.route('/edit_additional_material/<int:material_id>', methods=['GET', 'POST'])
def edit_additional_material(material_id):
    material = AdditionalMaterial.query.get_or_404(material_id)
    form = AdditionalMaterialForm(obj=material)

    if form.validate_on_submit():
        # Обновляем только информацию о дополнительном материале
        material.description = form.description.data

        # Продукты, связанные с этим дополнительным материалом, остаются без изменений
        db.session.commit()
        flash('Additional Material updated successfully!', 'success')
        return redirect(url_for('admin_dashboard') + "#additional_materials")

    return render_template('edit_additional_material.html', form=form, material=material)

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        product.product_name = form.product_name.data
        product.unit_price = form.unit_price.data
        # Проверяем, возвращает ли форма объект модели или None
        product.bouquet_id = form.bouquet_id.data if form.bouquet_id.data else None
        product.flower_id = form.flower_id.data if form.flower_id.data else None
        product.material_id = form.material_id.data if form.material_id.data else None

        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin_dashboard') + "#products")

    return render_template('edit_product.html', form=form, product=product)

@app.route('/edit_client/<int:client_id>', methods=['GET', 'POST'])
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)
    form = ClientForm(obj=client)

    if form.validate_on_submit():
        # Обновление данных клиента
        client.full_name = form.full_name.data
        client.age = form.age.data
        client.phone_number = form.phone_number.data
        client.first_order_date = form.first_order_date.data

        # Обновление связанных данных, если необходимо
        for order in client.orders:
            order.client_name = client.full_name  # Если имя используется в заказах

        db.session.commit()
        flash('Client updated successfully!', 'success')
        return redirect(url_for('admin_dashboard') + "#clients")

    return render_template('edit_client.html', form=form, client=client)

@app.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    order = Order.query.get_or_404(order_id)
    form = OrderForm(obj=order)

    if form.validate_on_submit():
        # Обновление данных заказа
        order.order_date = form.order_date.data
        order.employee_id = form.employee_id.data
        order.client_id = form.client_id.data
        order.order_status = form.order_status.data

        db.session.commit()
        flash('Order updated successfully!', 'success')
        return redirect(url_for('admin_dashboard') + "#orders")

    return render_template('edit_order.html', form=form, order=order)

@app.route('/edit_payment/<int:payment_id>', methods=['GET', 'POST'])
def edit_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    form = PaymentForm(obj=payment)

    if form.validate_on_submit():
        # Обновление данных платежа
        payment.order_id = form.order_id.data
        payment.payment_date = form.payment_date.data
        payment.amount = form.amount.data
        payment.payment_method = form.payment_method.data

        db.session.commit()
        flash('Payment updated successfully!', 'success')
        return redirect(url_for('admin_dashboard') + "#payments")

    return render_template('edit_payment.html', form=form, payment=payment)

@app.route('/edit_delivery_detail/<int:delivery_detail_id>', methods=['GET', 'POST'])
def edit_delivery_detail(delivery_detail_id):
    delivery_detail = DeliveryDetail.query.get_or_404(delivery_detail_id)
    form = DeliveryDetailForm(obj=delivery_detail)

    if form.validate_on_submit():
        delivery_detail.delivery_id = form.delivery_id.data
        delivery_detail.product_id = form.product_id.data
        delivery_detail.quantity = form.quantity.data
        delivery_detail.purchase_price = form.purchase_price.data

        # Сохранение изменений в базу данных
        db.session.commit()
        flash('Delivery detail updated successfully!', 'success')
        return redirect(url_for('admin_dashboard') + "#delivery_details")

    return render_template('edit_delivery_detail.html', form=form, delivery_detail=delivery_detail)

@app.route('/edit_order_detail/<int:order_detail_id>', methods=['GET', 'POST'])
def edit_order_detail(order_detail_id):
    order_detail = OrderDetail.query.get_or_404(order_detail_id)
    form = OrderDetailForm(obj=order_detail)

    if form.validate_on_submit():
        order_detail.order_id = form.order_id.data
        order_detail.product_id = form.product_id.data
        order_detail.quantity = form.quantity.data
        order_detail.purchase_price = form.purchase_price.data

        # Сохранение изменений в базу данных
        db.session.commit()
        flash('Order detail updated successfully!', 'success')
        return redirect(url_for('admin_dashboard') + "#order_details")

    return render_template('edit_order_detail.html', form=form, order_detail=order_detail)

#--------------------------------------------------------------------------------------------------------------

# Пример маршрута для удаления поставщика
@app.route('/suppliers/delete/<int:supplier_id>', methods=['POST'])
def delete_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    db.session.delete(supplier)
    db.session.commit()
    return redirect(url_for('admin_dashboard') + "#suppliers")  # Возвращаемся к списку поставщиков

# Пример маршрута для удаления сотрудника
@app.route('/employees/delete/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('admin_dashboard') + "#employees")

@app.route('/deliveries/delete/<int:delivery_id>', methods=['POST'])
def delete_delivery(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    db.session.delete(delivery)
    db.session.commit()
    return redirect(url_for('admin_dashboard') + "#deliveries")

@app.route('/bouquets/delete/<int:bouquet_id>', methods=['POST'])
def delete_bouquet(bouquet_id):
    bouquet = Bouquet.query.get_or_404(bouquet_id)
    db.session.delete(bouquet)
    db.session.commit()
    return redirect(url_for('admin_dashboard') + "#bouquets")


@app.route('/flowers/delete/<int:flower_id>', methods=['POST'])
def delete_flower(flower_id):
    flower = Flower.query.get_or_404(flower_id)
    db.session.delete(flower)
    db.session.commit()
    return redirect(url_for('admin_dashboard') + "#flowers")


@app.route('/additional_materials/delete/<int:material_id>', methods=['POST'])
def delete_material(material_id):
    material = AdditionalMaterial.query.get_or_404(material_id)
    db.session.delete(material)
    db.session.commit()
    return redirect(url_for('admin_dashboard') + "#additional_materials")


@app.route('/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('admin_dashboard') + "#products")


@app.route('/clients/delete/<int:client_id>', methods=['POST'])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('admin_dashboard') + "#clients")


@app.route('/orders/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('admin_dashboard') + "#orders")


@app.route('/order_details/delete/<int:order_detail_id>', methods=['POST'])
def delete_order_detail(order_detail_id):
    order_detail = OrderDetail.query.get_or_404(order_detail_id)
    db.session.delete(order_detail)
    db.session.commit()
    return redirect(url_for('admin_dashboard') + "#order_details")


@app.route('/payments/delete/<int:payment_id>', methods=['POST'])
def delete_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    db.session.delete(payment)
    db.session.commit()
    return redirect(url_for('admin_dashboard') + "#payments")


@app.route('/delivery_details/delete/<int:delivery_detail_id>', methods=['POST'])
def delete_delivery_detail(delivery_detail_id):
    delivery_detail = DeliveryDetail.query.get_or_404(delivery_detail_id)
    db.session.delete(delivery_detail)
    db.session.commit()
    return redirect(url_for('admin_dashboard') + "#delivery_details")

#--------------------------------------------------------------------------------------------------------------


@app.route('/user_dashboard')
@login_required
def user_dashboard():
    if current_user.role != 'admin':
      user = Client.query.filter_by(client_id=1).first()  # Получаем пользователя, чей ID равен 1
      return render_template('user_dashboard.html', user=user)
    else:
        return "Вы не имеете прав доступа к этой странице."

@app.route('/user_create_order', methods=['GET', 'POST'])
@login_required
def user_create_order():
    if current_user.role != 'admin':
        employees = Employee.query.filter((Employee.position == 'Флорист') | (Employee.position == 'Менеджер')).all()
        products = Product.query.all()
        if request.method == 'POST':
            order_date = request.form['order_date']
            employee_id = request.form['employee_id']
            payment_method = request.form['payment_method']
            user = Client.query.filter_by(client_id=1).first()
            if user:
                new_order = Order(
                   order_date=datetime.strptime(order_date, '%Y-%m-%d').date(),
                   employee_id=employee_id,
                   client_id=user.client_id,
                   order_status='Новый' # Автоматически устанавливаем статус
                  )
                db.session.add(new_order)
                db.session.commit()
                order_id = new_order.order_id # Получаем ID нового заказа
                total_price = 0 #сумма заказа
                for product in products:
                    quantity_str = request.form.get(f'quantity_{product.product_id}', '0')  # Получаем значение в виде строки и по умолчанию 0
                    try:
                      quantity = int(quantity_str) # Преобразовываем в int
                    except ValueError: # Если не получается преобразовать, значит там пустая строка, то количество 0
                        quantity = 0

                    if quantity > 0:
                      flower = Flower.query.filter_by(flower_id=product.flower_id).first()
                      bouquet = Bouquet.query.filter_by(bouquet_id=product.bouquet_id).first()
                      material = AdditionalMaterial.query.filter_by(material_id=product.material_id).first()

                      if flower is None and bouquet is None and material is None:
                        db.session.rollback()
                        return render_template('create_order.html', employees=employees, products=products, error=f"ID цветка, букета или материала: {product.product_id} не существует.")
                      if flower is None and product.flower_id is not None:
                         db.session.rollback()
                         return render_template('create_order.html', employees=employees, products=products, error=f"ID цветка: {product.flower_id} не существует.")
                      if bouquet is None and product.bouquet_id is not None:
                         db.session.rollback()
                         return render_template('create_order.html', employees=employees, products=products, error=f"ID букета: {product.bouquet_id} не существует.")
                      if material is None and product.material_id is not None:
                        db.session.rollback()
                        return render_template('create_order.html', employees=employees, products=products, error=f"ID материала: {product.material_id} не существует.")
                      new_order_detail = OrderDetail(order_id=order_id, product_id=product.product_id, quantity=quantity, purchase_price=product.unit_price)
                      db.session.add(new_order_detail)
                      total_price += Decimal(product.unit_price) * quantity

                new_payment = Payment(order_id=order_id, payment_date=datetime.now().date(), amount=total_price, payment_method=payment_method)
                db.session.add(new_payment)
                db.session.commit()
                return redirect(url_for('user_dashboard'))
        total_price = 0 #сумма заказа
        return render_template('create_order.html', employees=employees, products=products, total_price = total_price)

@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if current_user.role != 'admin':
        user = Client.query.filter_by(client_id=1).first()
        if request.method == 'POST':
           if user:
               user.full_name = request.form['full_name']
               user.phone_number = request.form['phone_number']
               db.session.commit()
               return redirect(url_for('user_dashboard'))
        return render_template('update_profile.html', user=user)
    else:
        return "Вы не имеете прав доступа к этой странице."

if __name__ == '__main__':
    app.run(debug=True)
