import os
import requests
from django.core.management.base import BaseCommand
from faker import Faker, providers

from api.models import Section, Category, Advertisement, AdImage

SECTIONS = [
    'Children',
    'Property',
    'Vehicles',
    'Jobs',
    'Pets',
    'Home',
    'Gadges',
    'Business',
    'Magazines',
    'Flowers',
    'Cleaning',
    'Baking',
    'Beauty',
    'Stationary',
    'Spices'
]

def download_image(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded successfully as {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")


def generate_long_lorem(fake, min_length=500):
    text = ""
    while len(text) < min_length:
        text += fake.paragraph()
    return text


class Provider(providers.BaseProvider):
    def ec_section(self):
        return self.random_element(SECTIONS)


class Command(BaseCommand):
    help = "Populates the database with random data"

    def handle(self, *args, **options):
        print("Populating the database with Faker...")

        fake = Faker()
        fake.add_provider(Provider)

        # section
        secs_len = len(SECTIONS)
        secs_count = Section.objects.all().count()
        if not secs_count >= secs_len:
            for _ in range(len(SECTIONS)):
                d = fake.unique.ec_section()
                Section.objects.create(name=d)

            check_section = Section.objects.all().count()
            print(f"{check_section} sections has been inserted")

        # advertisement
        for _ in range(50):
            ad = Advertisement.objects.create(
                title = fake.text(max_nb_chars=70),
                description = generate_long_lorem(fake, min_length=1000),
                price = fake.random_int() * 100
            )

            # ad images
            pic_path =  "ad/images/pic" + fake.pystr() + ".jpeg"
            download_image("https://picsum.photos/1600/900", "media/" + pic_path)
            AdImage.objects.create(ad=ad, image=pic_path)
            
        
