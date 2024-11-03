import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from random import choice, randint

import django
from django.conf import settings

DJANGO_BASE_DIR = Path(__file__).parent.parent
NUMBER_OF_OBJECTS = 1000

sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
settings.USE_TZ = False

django.setup()

if __name__ == '__main__':
    import faker

    from home.models import Produto  # Altere 'seu_app' para o nome correto do seu aplicativo

    Produto.objects.all().delete()

    fake = faker.Faker('pt_BR')
    setores = ['A1', 'B2', 'C3', 'D4']  # Exemplos de setores de armazenamento

    django_produtos = []

    for _ in range(NUMBER_OF_OBJECTS):
        nome = fake.word().capitalize()  # Gera um nome de produto
        lote = fake.uuid4()  # Gera um lote único (você pode ajustar para o que preferir)
        quantidade = randint(1, 100)  # Gera uma quantidade aleatória entre 1 e 100
        vencimento = fake.date_between(start_date='today', end_date='+1y')  # Data de vencimento dentro de um ano
        setor_armazenamento = choice(setores)  # Escolhe um setor aleatório
        codigo_barra = fake.unique.ean13()  # Gera um código de barras único

        django_produtos.append(
            Produto(
                nome=nome,
                lote=lote,
                quantidade=quantidade,
                vencimento=vencimento,
                setor_armazenamento=setor_armazenamento,
                codigo_barra=codigo_barra,
            )
        )

    if len(django_produtos) > 0:
        Produto.objects.bulk_create(django_produtos)
