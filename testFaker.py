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
from faker import Faker

User = get_user_model()
fake = Faker('ru-RU')


def create_admin():
    print('Creating Admin')
    User.objects.all().delete()
    user = User(username='admin', is_superuser=True, is_staff=True)
    user.set_password('admin')
    user.save()


def create_features(count: int = 10):
    print('Creating Features')
    Feature.objects.all().delete()
    features = []
    for i in range(count):
        feature = Feature()
        feature.name = fake.unique.word()
        feature.slug = slugify(feature.name)
        features.append(feature)
    Feature.objects.bulk_create(features)


def create_sub_features(count: int = 10):
    print('Creating SubFeatures')
    SubFeature.objects.all().delete()
    sub_features = []
    parent_features = list(Feature.objects.all())
    for i in range(count):
        sub_feature = SubFeature()
        sub_feature.name = fake.unique.word()
        sub_feature.feature = random.choice(parent_features)
        sub_feature.slug = slugify(str(sub_feature.feature.name + '-' + sub_feature.name))
        sub_features.append(sub_feature)
    SubFeature.objects.bulk_create(sub_features)


def create_all_features():
    create_features(10)
    create_sub_features(10)


def create_brands(count: int = 10):
    print('Creating Brands')
    Brand.objects.all().delete()
    brands = []
    for i in range(count):
        brand = Brand()
        brand.name = fake.unique.word()
        brand.slug = slugify(brand.name)
        brands.append(brand)
    Brand.objects.bulk_create(brands)


def create_catalog_structure(parent=None, depth=3, current_level=1):
    print('Creating Catalog Structure')
    if depth < 1 or current_level > depth:
        return

    # Определяем количество элементов каталога на текущем уровне
    num_items = random.randint(2, 5)  # Например, от 2 до 5 элементов на каждом уровне

    for _ in range(num_items):
        catalog_item = CatalogItem()
        catalog_item.name = fake.unique.word()
        catalog_item.parent = parent
        catalog_item.save()  # Сохраняем элемент, чтобы получить его slug и возможность добавления дочерних элементов

        # Рекурсивно создаем дочерние элементы, если не достигнута максимальная глубина
        if current_level < depth:
            create_catalog_structure(parent=catalog_item, depth=depth, current_level=current_level + 1)


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


def create_products(count: int = 10):
    print('Creating Products')
    Product.objects.all().delete()

    brands = list(Brand.objects.all())
    categories = list(CatalogItem.objects.all())
    all_sub_features = list(SubFeature.objects.all())

    products = []
    for i in range(count):
        product = Product()
        product.name = fake.unique.word()
        product.description = fake.text(max_nb_chars=1000)
        product.slug = slugify(product.name)
        product.brand = random.choice(list(brands))
        product.price = random.randint(100, 50000)
        product.category = random.choice(list(categories))
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


if __name__ == '__main__':
    create_admin()
    create_all_features()

    CatalogItem.objects.all().delete()
    create_catalog_structure()
    create_brands()
    create_products()
