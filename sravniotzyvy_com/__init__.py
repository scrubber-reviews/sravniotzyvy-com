# -*- coding: utf-8 -*-

"""Top-level package for sravniotzyvy."""
from .sravniotzyvy_com import SravniOtzyvyCom, Rating

__author__ = """Melis Nurlan"""
__email__ = 'melis.zhoroev+scrubber@gmail.com'
__version__ = '0.1.3'
__name__ = __title__ = 'СравниОтзывы'
__slug_img_link__ = 'https://i.ibb.co/Yjf69bH/image.png'
__description__ = 'СравниВыбери - Мы знаем где лучше! ' \
                  'Теперь Вы знаете куда идти, ' \
                  'прежде чем пользоваться услугами какой-либо компании. ' \
                  'Мы предлагаем Вашему вниманию каталог компаний с отзывами ' \
                  'и полной информацией о ней. Если Вы пользовались услугами' \
                  ' одной из компаний, оставьте свой отзыв,' \
                  ' чтобы другим было легче осуществить свой выбор'
__how_get_slug__ = """
Надо скопировать цифры с url как показано в скришоте
<img src="{}" alt="image" border="0">
""".format(__slug_img_link__)


provider = SravniOtzyvyCom
rating = Rating

