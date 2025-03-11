from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Image, Rating, Reply, Order, OrderItem, Payment
from .forms import ProductCreateForm
from django.contrib import messages
from django.http import Http404
from django.utils import timezone
from datetime import timedelta
import json
from django.http import JsonResponse

User = get_user_model()

def home_page(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'main/index.html', {'products': products})


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.is_active == False and request.user != product.seller:
        messages.error(request, 'Продукт не актуален')
        return redirect('home_page')
    images = product.images.all()
    similar_products = Product.objects.filter(category=product.category.id).exclude(id=product.id)[:8]
    form = ProductCreateForm(instance=product)
    reviews = product.ratings.all()
    return render(request=request,
                  template_name='main/product_details.html',
                  context={'product': product,
                           'images': images,
                           'similar_products': similar_products,
                           'form': form,
                           'reviews': reviews,
                           }
                  )

def all_products_in_category(request, category_id):
    products = Product.objects.filter(category=category_id, is_active='True')
    category = get_object_or_404(Category, id=category_id)
    return render(request, 'main/all_in_category.html',{'products': products, 'category': category})


def profile_page(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_products = user.products.all().order_by('-is_active')
    return render(
        request=request,
        template_name='main/profile.html',
        context={'user': user, 'user_products': user_products}
    )

def create_product(request):
    if not request.user.is_authenticated:
        raise Http404
    if request.method == 'POST':
        form = ProductCreateForm(request.POST)
        if form.is_valid():
            product_obj = form.save(commit=False)
            product_obj.seller = request.user
            product_obj.save()
            print(request.POST, request.FILES)
            images = request.FILES.getlist('images')
            main_image_id = request.POST.get('main_image')
            for idx, image in enumerate(images):
                is_main = str(idx) == main_image_id
                Image.objects.create(product=product_obj,file=image, is_main=is_main)

            messages.success(request, 'Успешно создано!')
            return redirect('profile_page', request.user.id)

    form = ProductCreateForm()
    return render(request, 'main/create_product.html', {'form': form})



def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.seller != request.user:
        messages.error(request, 'У вас нет доступа!')
        return redirect('home_page')

    if request.method == "POST":
        form = ProductCreateForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()

            # Убираем статус главной у всех старых изображений
            Image.objects.filter(product=product).update(is_main=False)

            # Получаем ID выбранного главного изображения
            main_image_id = request.POST.get('main_image')
            print(request.POST)
            print(request.FILES)

            if main_image_id:
                try:
                    main_image = Image.objects.get(id=main_image_id, product=product)
                    main_image.is_main = True
                    main_image.save()
                except Image.DoesNotExist:
                    pass

            new_images = request.FILES.getlist('images')
            for idx, image in enumerate(new_images):
                img_obj = Image.objects.create(product=product, file=image)

            return redirect('product_details', product_id=product.id)

    raise Http404

def delete_image(request):
    if request.method == "POST":
        data = json.loads(request.body)
        image_id = data.get("image_id")
        try:
            image = Image.objects.get(id=image_id)
            if image.product.seller != request.user:
                return JsonResponse({"success": False, "error": "У вас нет доступа к удалению этого фото!"}, status=403)
            image.delete()
            return JsonResponse({"success": True})
        except Image.DoesNotExist:
            return JsonResponse({"success": False, "error": "Фото не найдено"}, status=404)

    return JsonResponse({"success": False, "error": "Некорректный запрос"}, status=400)


def delete_product(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        if product.seller != request.user:
            return JsonResponse({"success": False, "error": "У вас нет доступа для удаления!"}, status=403)
        product.delete()
        return JsonResponse({"success": True})

    raise Http404


def add_review(request, product_id):
    if request.method == "POST":
        user = request.user
        product = get_object_or_404(Product, id=product_id)
        if product.seller == request.user:
            messages.error(request, 'Вы не можете оставлять отзыв самому себе! ')
            return redirect('product_details', product_id=product.id)
        # Проверяем, что данные есть в запросе
        count = request.POST.get("rating")
        text = request.POST.get("comment", "").strip()

        if not count or not text:
            messages.error(request, "Пожалуйста, заполните все поля!")
            return redirect("product_details", product_id=product.id)

        # Создаём отзыв
        Rating.objects.create(user=user, product=product, count=int(count), text=text)
        messages.success(request, "Отзыв успешно сохранён!")
        return redirect("product_details", product_id=product.id)
    raise Http404


def reply_review(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        if product.seller != request.user:
            messages.error(request, 'У вас нет доступа! ')
            return redirect('product_details', product_id=product_id)

        rating_id = request.POST.get('review_id')
        rating = get_object_or_404(Rating, id=rating_id)
        seller = request.user
        text = request.POST.get('text')
        Reply.objects.create(rating=rating, seller=seller, text=text)
        return redirect('product_details', product_id=product_id)

def edit_reply(request, product_id):
    if request.method == 'POST':
        reply_id = request.POST.get('reply_id')
        reply = get_object_or_404(Reply, id=int(reply_id))
        if reply.seller != request.user:
            messages.error(request, 'У вас нет доступа!')
            return redirect('product_details', product_id=product_id)
        print(reply.created_at)
        print(timezone.now())
        print(timezone.now() - reply.created_at)
        if timezone.now() - reply.created_at > timedelta(hours=3):
            messages.error(request, 'К сожалению вы можете исправить сообщение только в первые 3 часа')
            return redirect('product_details', product_id=product_id)
        text = request.POST.get('text')
        reply.text = text
        reply.save()
        messages.success(request, 'Успешно изменено!')
        return redirect('product_details', product_id=product_id)
    raise Http404


def delete_reply(request, product_id):
    if request.method == 'POST':
        reply_id = request.POST.get('reply_id')
        reply = get_object_or_404(Reply, id=reply_id)
        if reply.seller != request.user:
            messages.error(request, 'У вас нет доступа!')
            return redirect('product_details', product_id=product_id)
        reply.delete()
        messages.success(request, 'Ответ успешно удален!')
        return redirect('product_details', product_id=product_id)

    raise Http404


def cart_page(request):
    user = request.user
    orders_in_cart = user.orders.filter(status='in_cart')
    total_price = sum(order.total_price for order in orders_in_cart)
    return render(request=request,
                  template_name='main/cart.html',
                  context={'orders_in_cart':orders_in_cart, 'total_price': total_price}

                  )


def add_to_cart(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    if user == product.seller:
        messages.error(request, 'Вы не можете купить свой же товар! ')
        return redirect('home_page')
    order, created = Order.objects.get_or_create(buyer=user, seller=product.seller, status='in_cart')
    order_item = order.items.filter(product=product).first()
    if order_item:
        order_item.quantity += 1
        order_item.save()
    else:
        OrderItem.objects.create(order=order, product=product, quantity=1, price_at_purchase=product.price)

    messages.success(request, 'Успешно добавлено в корзину!')
    return redirect('product_details', product_id=product.id)


def update_cart_ajax(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            item_id = data.get("item_id")
            new_quantity = data.get("quantity")

            item = get_object_or_404(OrderItem, id=item_id, order__buyer=request.user)

            if new_quantity < 1:
                item.delete()
            else:
                item.quantity = new_quantity
                item.save()

            order = item.order
            order_deleted = False

            if not order.items.exists():
                order.delete()
                order_deleted = True
                order_total = 0
            else:
                order_total = sum(i.product.price * i.quantity for i in order.items.all())

            grand_total = sum(o.total_price for o in Order.objects.filter(buyer=request.user, status="in_cart"))

            return JsonResponse({
                "success": True,
                "order_deleted": order_deleted,
                "item_total": new_quantity * item.product.price if new_quantity > 0 else 0,
                "order_total": order_total,
                "grand_total": grand_total
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False}, status=400)


def delete_cart_item_ajax(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            item_id = data.get("item_id")

            item = get_object_or_404(OrderItem, id=item_id, order__buyer=request.user)
            order = item.order
            item.delete()

            order_deleted = False
            if not order.items.exists():
                order.delete()
                order_deleted = True
                order_total = 0
            else:
                order_total = sum(i.product.price * i.quantity for i in order.items.all())

            grand_total = sum(o.total_price for o in Order.objects.filter(buyer=request.user, status="in_cart"))

            return JsonResponse({
                "success": True,
                "order_deleted": order_deleted,
                "grand_total": grand_total
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False}, status=400)

def payment_page(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    orders = user.orders.filter(status='in_cart')
    if not orders:
        messages.error(request, 'У вас нет заказов для оплаты! ')
        return redirect('home_page')
    price = sum(order.total_price for order in orders)
    return render(request=request,
                  template_name='main/payment.html',
                  context={'orders':orders, 'price':price}

                  )

def process_orders(request):
    if request.method == "POST":
        user = request.user
        orders = user.orders.filter(status='in_cart')
        amount = sum(order.total_price for order in orders)
        if not 'receipt' in request.FILES:
            messages.error(request, 'Загрузите чек!')
            return redirect('payment')
        if not orders.exists():
            messages.error(request, 'У вас нет заказов для обработки')
            return redirect('home_page')
        receipt = request.FILES['receipt']
        payment= Payment.objects.create(
            user=user,
            amount=amount,
            status='pending',
            receipt=receipt
        )
        orders.update(payment=payment, status='pending')
        messages.success(request, 'Ваша оплата отправлена на рассмотрение, ожидайте!')
        return redirect('home_page')

    raise Http404

def orders_page(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    payments = Payment.objects.filter(user=user).order_by('-created_at')
    return render(request, 'main/orders.html', {'payments':payments})