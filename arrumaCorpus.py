from os import listdir
from os import path

segmentation_path = 'corpus/paragraphs'
filenames = listdir(segmentation_path)
contador_segmento = 1

for filename in filenames:
    if 'xml' in filename:
        arquivo_segmentacao = open(path.join(segmentation_path, filename), 'r').read()
        segmentos = arquivo_segmentacao.split('</unit>')

        novo_arquivo = open(path.join(segmentation_path, filename), 'w')

        for (id_segmento, segmento) in enumerate(segmentos):
            if '</document>' not in segmento:
                novo_arquivo.write(segmento + '</unit id="' + str(contador_segmento).zfill(4) + '">')
                contador_segmento += 1

        novo_arquivo.close()
