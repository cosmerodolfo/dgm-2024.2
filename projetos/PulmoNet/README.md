# `PulmoNet: Rede Neuronal Generativa para Imagens Tomográficas Pulmonares`
# `PulmoNet: Generative Neuronal Network for Pulmonary Tomographic Images`

## Apresentação

O presente projeto foi originado no contexto das atividades da disciplina de pós-graduação *IA376N - IA generativa: de modelos a aplicações multimodais*, 
oferecida no segundo semestre de 2024, na Unicamp, sob supervisão da Profa. Dra. Paula Dornhofer Paro Costa, do Departamento de Engenharia de Computação e Automação (DCA) da Faculdade de Engenharia Elétrica e de Computação (FEEC).

 |Nome  | RA | Especialização|
 |--|--|--|
 | Arthur Matheus Do Nascimento | 290906 | Eng. Elétrica |
 | Júlia Castro de Paula | 219193 | Eng. Elétrica |
 | Letícia Levin Diniz | 201438  | Eng. Elétrica |


## Descrição Resumida do Projeto

As tomografias computadorizadas (CT) pulmonares, juntamente com a segmentação das vias aéreas, desempenham um papel crucial no diagnóstico preciso de doenças pulmonares. Ao gerar imagens detalhadas da região torácica, ela permite que médicos mapeiem a anatomia das vias aéreas antes de procedimentos cirúrgicos, avaliando a extensão de lesões e facilitando o acompanhamento da progressão de doenças respiratórias [[2]](#2). Além disso, a CT é fundamental para monitorar a eficácia de tratamentos e detectar seus possíveis efeitos colaterais [[5]](#5).

A complexidade e diversidade do corpo humano dificultam a obtenção de grandes volumes de dados médicos para treinar modelos de aprendizado de máquina, como as redes neurais. Essa escassez de dados pode levar a diagnósticos imprecisos, comprometendo a qualidade do atendimento aos pacientes [[6]](#6). Com as redes generativas é possível criar dados de forma a compensar essa escassez, permitindo que as redes aprendam muito mais detalhes do que utilizando apenas aqueles obtidos de exames reais.

Este projeto visa gerar imagens sintéticas de tomografia computadorizada (CT) da região torácica de alta fidelidade, também produzindo máscaras de segmentação das vias aéreas. O modelo generativo proposto terá como saída volumes de CT da região do tórax, ou seja, uma combinação de fatias que juntas formarão o equivalente a um exame real.

[Link para o vídeo de apresentação](https://drive.google.com/file/d/1TlpQOlCh_lAI0-jPPMPWOzGZ_werCo3d/view?usp=sharing)

[Link para a apresentação de slides](https://docs.google.com/presentation/d/1b8W0Cw1eiTbWlJ0CJJ8eMRA4zyu2iLhYvggi55-mOb0/edit?usp=sharing)

## Metodologia Proposta

Este projeto usará como inspiração inicial o trabalho desenvolvido em [[1]](#1), o qual propõe duas arquiteturas baseadas em GANs para a síntese de imagens CT pulmonares a partir de máscaras binárias que segmentam a região pulmonar. Das arquiteturas propostas, inspirar-se-á na arquitetura Pix2Pix, na qual o gerador é composto de um encoder que aumenta a profundidade da imagem enquanto diminui suas dimensões, seguido de um decoder que realiza o processo oposto. Tal arquitetura também utiliza conexões residuais. Na arquitetura Pix2Pix, o discriminador é composto por cinco camadas convolucionais, onde as quatro primeiras são seguidas por uma camada de ativação *LeakyReLu*, enquanto a última é seguida de uma função *sigmoide*. 

Apesar de inspirar-se no artigo [[1]](#1), para o desenvolvimento deste projeto será usada a base de dados ATM'22, a qual possui 500 volumes CTs nos quais as vias aéreas estão completamente anotadas, i.e., delimitadas [[2]](#2). Tal base de dados não foi usada no desenvolvimento do projeto em [[1]](#1), mas foi escolhida no presente projeto devido a sua amplitude, a presença de dados volumétricos e em razão das imagens possuírem a delimitação das vias aéreas obtidas através de especialistas. Os volumes da base ATM'22 foram adquiridos em diferentes clínicas e considerando diferentes contextos clínicos. Construída para a realização de um desafio de segmentação automática de vias aéria utilizando IA, a base de dados está dividida em 300 volumes para treino, 50 para validação e 150 para teste. 

Além do artigo [[1]](#1), também serão considerados os trabalhos realizados em [[3]](#3) e [[4]](#4). No primeiro, desenvolveu-se uma GAN condicional para a geração de imagens CT pulmonares a partir de imagens de ressonância magnética. Já no segundo, utiliza-se um modelo baseado em GAN para a segmentação do pulmão em imagens CT que contém anomalias no tecido pulmonar. Apesar dos objetivos de tais trabalhos não serem os mesmos objetivos propostos para o presente projeto, eles servirão de apoio para proposição de modificações na arquitetura, estratégias de treino e de validação de resultados.   

A ferramenta escolhida para o desenvolvimento da arquitetura dos modelos e de treinamento é o PyTorch, em função de sua relevância na área e familiaridade por parte dos integrantes do grupo.
Ademais, para o desenvolvimento colaborativo dos modelos entre os estudantes, opta-se pela ferramenta de programação Google Collaboratory.
Já para o versionamento dos modelos e para ajustar seus hiperparâmetros, decidiu-se pela ferramenta Wandb AI dentre as opções disponíveis no mercado. E, além disso, a ferramenta do GitHub também auxiliará no versionamento dos algoritmos desenvolvidos.

Como resultado desta implementação, espera-se gerar amostras de imagens de tomografias pulmonares em 2D realistas o suficiente para possibilitar a segmentação das vias aéreas.
Caso este resultado se concretize antes do prazo estipulado pelo cronograma e ainda reste tempo para o aprofundamento do projeto, buscar-se-á a geração de imagens 3D de tomografias pulmonares, isto é, espera-se aumentar o escopo do projeto para gerar volumes com a mesma estratégia da síntese de imagens, com as devidas adequações necessárias a esta nova estrutura.

Por fim, para avaliar a qualidade dos resultados obtidos com o modelo de síntese, propõe-se três tipos de avaliação: análise qualitativa, análise quantitativa e análise frente a um benchmark.
No caso da análise qualitativa, os próprios estudantes irão observar os resultados sintéticos, sejam eles imagens e/ou  volumes, e compararão com os dados reais esperados.
Já a análise quantitativa trata de uma avaliação sobre as imagens a partir dos métodos Fréchet Inception Distance (FID) e Structural Similarity Index (SSIM), os quais são utilizados para avaliação de qualidade das imagens sintéticas e de similaridade com dados reais. Ambas estratégias foram utilizadas pelos pesquisadores do artigo [[1]](#1), o que permite uma avaliação dos nossos resultados frente a esta outra pesquisa.
Por último, a análise de benchmark, que também pode ser considerada um estratégia quantitativa, tem como proposta a comparação das saídas de uma rede de segmentação já consolidada a partir dos dados gerados pela PulmoNet e de dados reais. Feito isso, compara-se ambas as saídas da rede, por meio do cálculo do coeficiente DICE (obtido a partir da precisão e recall da predição) e da quantidade de ramificações (métricas escolhidas com base na referência do artigo [[2]](#2)) e avalia-se se os dados sintéticos são bons o suficiente em uma aplicação real, isto é, avalia-se a utilidade do modelo generativo proposto.

## Cronograma


| Nº da Tarefa | Descrição                                                                 | Data Prevista de Finalização | Semanas Entre Etapas |
|--------------|---------------------------------------------------------------------------|------------------------------|----------------------|
| 1            | Leitura de artigos, familiarização com a base de dados e GANs              | 10/09                        |                      |
| 2            | Primeira versão da GAN (inspirada no artigo de referência)                | 24/09                        | 2 semanas            |
| 3            | Estrutura de avaliação bem delimitada                                     | 07/10                        | 2 semanas            |
| 4            | E2                                                                        | 08/10                        | 1 dia                |
| 5            | Primeiros resultados com imagens segmentadas e valores para validação     | 15/10                        | 1 semana             |
| 6            | Fine-tuning e aperfeiçoamento do modelo                                   | 29/10                        | 2 semanas            |
| 7            | Evoluir para redes 3D ou continuar aperfeiçoando o modelo                 | 05/11                        | 1 semana             |
| 8            | E3                                                                        | 25/11                        | 3 semanas            |



## Referências Bibliográficas
> Apontar nesta seção as referências bibliográficas adotadas no projeto.

<a id="1">[1]</a> : José Mendes et al., Lung CT image synthesis using GANs, Expert Systems with Applications, vol. 215, 2023, pp. 119350., https://www.sciencedirect.com/science/article/pii/S0957417422023685.

<a id="2">[2]</a> : Minghui Zhang et al., Multi-site, Multi-domain Airway Tree Modeling (ATM'22): A Public Benchmark for Pulmonary Airway Segmentation, https://arxiv.org/abs/2303.05745.

<a id="3">[3]</a> :  Jacopo Lenkowicz et al., A deep learning approach to generate synthetic CT in low field MR-guided radiotherapy for lung cases, Radiotherapy and Oncology, vol. 176, 2022, pp. 31-38, https://www.sciencedirect.com/science/article/pii/S0167814022042608.

<a id="4">[4]</a> : Swati P. Pawar and Sanjay N. Talbar, LungSeg-Net: Lung field segmentation using generative adversarial network, Biomedical Signal Processing and Control, vol. 64, 2021, 102296, https://www.sciencedirect.com/science/article/pii/S1746809420304158.

<a id="5">[5]</a> : Tekatli, Hilâl et al. “Artificial intelligence-assisted quantitative CT analysis of airway changes following SABR for central lung tumors.” Radiotherapy and oncology : journal of the European Society for Therapeutic Radiology and Oncology vol. 198 (2024): 110376. doi:10.1016/j.radonc.2024.110376, https://pubmed.ncbi.nlm.nih.gov/38857700/

<a id="6">[6]</a> : Zhang, Ling et al. “Generalizing Deep Learning for Medical Image Segmentation to Unseen Domains via Deep Stacked Transformation.” IEEE transactions on medical imaging vol. 39,7 (2020): 2531-2540. doi:10.1109/TMI.2020.2973595, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7393676/

Documento com as referências extras identificadas: https://docs.google.com/document/d/1uatPj6byVIEVrvMuvbII6J6-5usOjf8RLrSxLHJ8u58/edit?usp=sharing
