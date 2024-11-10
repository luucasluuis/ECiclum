import os
import sys
from pathlib import Path
from random import randint, choice

import django
from django.conf import settings

DJANGO_BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'  # Altere para o nome do seu projeto
settings.USE_TZ = False

django.setup()

if __name__ == '__main__':
    import faker
    from home.models import Produto, Categoria, Fornecedor, Lote, Estoque

    fake = faker.Faker('pt_BR')

    total_produtos = 500

    # Limpa os dados para evitar duplicação
    Produto.objects.all().delete()
    Categoria.objects.all().delete()
    Fornecedor.objects.all().delete()
    Lote.objects.all().delete()
    Estoque.objects.all().delete()

    # Criação de categorias e fornecedores fictícios
    categorias = ["Bebidas", "Laticínios", "Carnes", "Grãos", "Higiene"]
    fornecedores = ["Fornecedor A", "Fornecedor B", "Fornecedor C"]
    categoria_objs = [Categoria.objects.create(nome_categoria=categoria) for categoria in categorias]
    fornecedor_objs = [Fornecedor.objects.create(nome_fornecedor=fornecedor, contato=fake.name(), telefone=fake.phone_number()[:15], email=fake.email(), endereco=fake.address()) for fornecedor in fornecedores]

    # Criação de produtos e estoque
    for _ in range(total_produtos):
        produto = Produto.objects.create(
            nome_produto=fake.word().capitalize(),
            categoria=choice(categoria_objs),
            fornecedor=choice(fornecedor_objs),
            codigo_barras=fake.unique.ean13(),
            descricao=fake.sentence(),
            unidade_medida=choice(['unidade', 'kg', 'litro']),
            preco_custo=round(randint(5, 100) * 1.15, 2),
            preco_venda=round(randint(10, 150) * 1.20, 2),
            ativo=True
        )

        # Criando lotes e entradas no estoque para cada produto
        for _ in range(randint(1, 5)):  # Cada produto com 1 a 5 lotes
            lote = Lote.objects.create(
                produto=produto,
                quantidade=randint(50, 200),
                data_recebimento=fake.date_between(start_date='-1y', end_date='today'),
                data_validade=fake.date_between(start_date='today', end_date='+1y'),
                preco_custo=produto.preco_custo,
                status=choice(['ativo', 'em promoção', 'vencido'])
            )

            # Criando entradas no estoque
            Estoque.objects.create(
                produto=produto,
                lote=lote,
                tipo_movimento='entrada',
                quantidade=lote.quantidade
            )

    print("Produtos, lotes e entradas de estoque gerados com sucesso!")
