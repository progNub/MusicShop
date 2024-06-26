import os
import random
from slugify import slugify
from django import setup

"""Run administrative tasks."""
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MusicalStore.settings')
setup()
from common_models.models import ProductSubFeature
from products.models import Product, ProductImage
from characteristic.models import Feature, SubFeature, Brand
from django.contrib.auth import get_user_model
from catalog.models import CatalogItem
from card.models import Order, Deliveryman

from accounts.models import AddressUser
from faker import Faker

User = get_user_model()
fake = Faker('ru-RU')


def create_admin():
    print('Creating Admin')
    user = User.objects.filter(username='admin').first()
    if user:
        user.delete()
    user = User(username='admin', is_superuser=True, is_staff=True)
    user.set_password('admin')
    user.save()


def create_user():
    print('Creating User')
    user = User.objects.filter(username='user').first()
    if user:
        user.delete()
    user = User(username='user', is_superuser=False, is_staff=False)
    user.set_password('user')
    user.save()


def create_users(count=10, delete_all=False):
    if delete_all:
        print('Delete all Users')
        User.objects.all().delete()
    print(f'Creating Users {str(count)}')
    users = []
    for i in range(count):
        user = User()
        user.username = 'user_' + fake.unique.word()
        user.first_name = fake.name()
        user.last_name = fake.name()
        user.email = fake.unique.email()
        user.phone = fake.msisdn()
        user.set_password('<PASSWORD>')
        users.append(user)
        print(user)
    User.objects.bulk_create(users)


def create_features(count: int = 10):
    print(f'Creating Features {str(count)}')
    Feature.objects.all().delete()
    features = []
    for i in range(count):
        feature = Feature()
        feature.name = 'Feature_' + fake.unique.word()
        feature.slug = slugify(feature.name)
        features.append(feature)
    Feature.objects.bulk_create(features)


def create_sub_features(count: int = 10):
    print(f'Creating SubFeatures{str(count)}')

    SubFeature.objects.all().delete()
    sub_features = []
    parent_features = list(Feature.objects.all())
    for i in range(count):
        sub_feature = SubFeature()
        sub_feature.name = 'SubFeatures_' + fake.unique.word()
        sub_feature.feature = random.choice(parent_features)
        sub_feature.slug = slugify(str(sub_feature.feature.name + '-' + sub_feature.name))
        sub_features.append(sub_feature)
    SubFeature.objects.bulk_create(sub_features)


def create_all_features():
    create_features(10)
    create_sub_features(10)


def create_brands(count: int = 10, delete_all=True):
    print('Creating Brands')
    if delete_all:
        print('Delete all Brands')
        Brand.objects.all().delete()

    Brand.objects.all().delete()
    brands = []
    for i in range(count):
        brand = Brand()
        brand.name = 'Brand_' + fake.unique.word()
        brand.slug = slugify(brand.name)
        brands.append(brand)
    Brand.objects.bulk_create(brands)


def _create_catalog_structure(parent=None, depth=3, current_level=1):
    print('Creating Catalog Structure')

    if depth < 1 or current_level > depth:
        return

    # Определяем количество элементов каталога на текущем уровне
    num_items = random.randint(2, 5)  # Например, от 2 до 5 элементов на каждом уровне

    for _ in range(num_items):
        catalog_item = CatalogItem()
        name = fake.unique.word()
        print(name)
        if len(name) > 49:
            name = name[:49]
        catalog_item.name = name
        catalog_item.parent = parent
        catalog_item.save()  # Сохраняем элемент, чтобы получить его slug и возможность добавления дочерних элементов

        # Рекурсивно создаем дочерние элементы, если не достигнута максимальная глубина
        if current_level < depth:
            _create_catalog_structure(parent=catalog_item, depth=depth, current_level=current_level + 1)


def create_catalog(delete_all=True):
    if delete_all:
        print('Delete all Catalog')
        CatalogItem.objects.all().delete()
    _create_catalog_structure()


def generate_image_url(width=1280, height=720, text='hello world'):
    """Generate random image url."""
    width = random.randint(width // 3, width)
    height = random.randint(height // 3, height)
    src = f"https://fakeimg.pl/{width}x{height}/?text={text}"
    return src


def download_image(url):
    """Download image from url and return as django File object."""
    print(f"Download image: {url}")
    from tempfile import NamedTemporaryFile
    import requests
    from django.core.files import File

    # Создаем временный файл без использования контекстного менеджера
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(requests.get(url).content)
    img_temp.flush()

    # Возвращаем объект File Django, не закрывая временный файл
    django_file = File(img_temp, name=os.path.basename(url))
    return django_file


def create_products(count: int = 10, delete_all=True):
    print('Creating Products')
    Product.objects.all().delete()

    brands = list(Brand.objects.all())
    categories = list(CatalogItem.objects.all())
    all_sub_features = list(SubFeature.objects.all())

    products = []
    for i in range(count):
        product = Product()
        product.name = 'Product_' + fake.unique.word()
        product.description = fake.text(max_nb_chars=500)
        product.slug = slugify(product.name)
        product.brand = random.choice(brands)
        product.price = random.randint(100, 50000)
        product.category = random.choice(categories)
        product.save()  # Сначала сохраняем продукт

        # Создаем новую связь между продуктом и характеристикой с заданным значением
        random.shuffle(all_sub_features)
        for sub_feature in all_sub_features[:random.randint(1, len(all_sub_features) // 2)]:
            product_sub_feature = ProductSubFeature(product=product,
                                                    sub_feature=sub_feature,
                                                    value=fake.text(max_nb_chars=100))
            product_sub_feature.save()

        for i in range(random.randint(1, 5)):  # Допустим, от 1 до 5 изображений на продукт
            product_image = ProductImage(product=product,
                                         image=download_image(generate_image_url(text=product.slug + '_' + str(i))))
            product_image.save()


def create_orders(count=10, delete_all=True):
    print('Creating Orders')
    if delete_all:
        print('Delete all Orders')
        Order.objects.all().delete()
    users = list(User.objects.all())
    products = list(Product.objects.all())
    orders = []
    unique = []
    for i in range(count):
        order = Order()
        user = random.choice(users)
        product = random.choice(products)
        result = str(user) + str(product)

        if result in unique:
            continue
        else:
            unique.append(result)

        order.user = user
        order.product = product
        order.quantity = random.randint(1, 3)
        order.payment_status = False
        order.status = 'pending'
        orders.append(order)

    Order.objects.bulk_create(orders)


def create_address(count=2, delete_all=False):
    print('Creating Address')
    if delete_all:
        AddressUser.objects.all().delete()

    users = list(User.objects.all())

    addresses = []
    for user in users:
        for i in range(count):
            address = AddressUser()
            address.user = user
            address.city = fake.city()
            address.street = fake.street_name()
            address.home = fake.building_number()
            addresses.append(address)
    AddressUser.objects.bulk_create(addresses)


def create_deliveryman(count=5, delete_all=False):
    print('Creating Deliveryman ', count)
    if delete_all:
        Deliveryman.objects.all().delete()
    deliveryman_list = []
    for i in range(count):
        deliveryman = Deliveryman()
        deliveryman.first_name = fake.unique.first_name()
        deliveryman.last_name = fake.unique.last_name()
        deliveryman.phone = fake.unique.msisdn()
        deliveryman_list.append(deliveryman)
    Deliveryman.objects.bulk_create(deliveryman_list)


if __name__ == '__main__':
    create_all_features()
    create_catalog(delete_all=True)
    create_brands(count=10, delete_all=True)
    create_products(20, False)
    create_users(10, True)
    create_orders(10, True)
    create_user()
    create_admin()
    create_address(3, True)
    create_deliveryman(count=5, delete_all=True)
