# Controle do Computador por Gestos

Sistema de controle do mouse por meio de gestos das mãos, utilizando visão computacional e reconhecimento de movimentos em tempo real. O projeto permite interagir com o computador sem a necessidade de utilizar um mouse físico, usando apenas uma webcam.

Desenvolvido em Python, o sistema utiliza **OpenCV** e **MediaPipe** para detectar e rastrear as mãos, enquanto o **PyAutoGUI** transforma os gestos reconhecidos em comandos de mouse.

## Sobre o projeto

O objetivo deste projeto é explorar aplicações de visão computacional e interação humano-computador (IHC), desenvolvendo uma alternativa de controle que utiliza movimentos naturais das mãos.

A aplicação captura imagens da webcam, identifica os pontos de referência das mãos e interpreta determinados gestos para executar ações no sistema operacional.

O processamento da câmera é executado em uma thread separada da interface gráfica, permitindo que a captura e o reconhecimento ocorram paralelamente à atualização da janela.

## Funcionalidades

- **Controle do mouse:** movimentação do cursor utilizando o gesto de pinça entre o polegar e o dedo indicador.
- **Clique esquerdo:** reconhecimento da mão fechada para executar um clique.
- **Reconhecimento de duas mãos:** detecção e rastreamento de até duas mãos simultaneamente.
- **Detecção facial:** identificação de rostos utilizando classificadores Haar Cascade do OpenCV.
- **Suavização de movimentos:** aplicação de interpolação para reduzir oscilações no movimento do cursor.
- **Processamento paralelo:** utilização de threads para separar o processamento da câmera da interface gráfica.
- **Feedback visual:** exibição dos pontos de referência das mãos, quantidade de dedos identificados e indicação de clique.

## Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Linguagem principal |
| OpenCV | Captura e processamento de imagens |
| MediaPipe | Detecção e rastreamento das mãos |
| PyAutoGUI | Controle do mouse |
| Tkinter | Interface gráfica |
| Pillow (PIL) | Conversão e exibição de imagens |
| Threading | Execução paralela do processamento |

## Como funciona

O funcionamento do sistema é dividido em algumas etapas:

1. **Captura de imagem:** a webcam captura os movimentos do usuário.
2. **Processamento:** o OpenCV converte e prepara os quadros para análise.
3. **Reconhecimento:** o MediaPipe identifica as mãos e seus pontos de referência (*landmarks*).
4. **Interpretação dos gestos:** o sistema calcula a distância entre os dedos e identifica a posição da mão.
5. **Execução dos comandos:** o PyAutoGUI transforma os gestos reconhecidos em movimentos e cliques do mouse.
6. **Exibição:** a interface Tkinter apresenta o vídeo processado em tempo real.

## Controles por gestos

| Gesto | Ação |
|---|---|
| Pinça entre polegar e indicador | Movimenta o cursor |
| Mão fechada | Executa clique esquerdo |
| Mão aberta | Não executa clique |

**Observação:** o movimento do cursor é ativado enquanto a pinça permanece formada. O clique é realizado quando todos os dedos são identificados como fechados, respeitando um intervalo mínimo entre cliques.

## Instalação

### 1. Pré-requisitos

- Python 3.9 ou superior.
- Webcam funcional.
- Sistema operacional compatível com as bibliotecas utilizadas.

### 2. Clone o repositório

```bash
git clone https://github.com/gabeswk/Visao-Computacional.git
```

Entre na pasta do projeto:

```bash
cd Visao-Computacional
```

### 3. Instale as dependências

```bash
pip install opencv-python mediapipe pyautogui pillow
```

### 4. Execute a aplicação

```bash
python main.py
```

## Requisitos de execução

- Uma webcam conectada ao computador.
- Iluminação adequada para facilitar o reconhecimento das mãos.
- Mãos visíveis dentro do campo de visão da câmera.
- Ambiente com espaço suficiente para realizar os gestos.

O desempenho depende da capacidade de processamento do computador, da qualidade da webcam e das condições de iluminação.

## Segurança e limitações

- O sistema utiliza a webcam para capturar imagens durante sua execução.
- A detecção facial é utilizada apenas para identificação visual de rostos, sem reconhecimento de identidade.
- A movimentação do cursor pode apresentar pequenas oscilações dependendo da iluminação e da posição das mãos.
- O reconhecimento de gestos pode apresentar falhas em determinadas posições ou condições de captura.
- O PyAutoGUI está configurado com `FAILSAFE = False`, desativando o mecanismo de segurança que normalmente permite interromper a execução ao mover o cursor para o canto superior esquerdo da tela.

**Atenção:** recomenda-se utilizar o botão de saída ou a tecla `ESC` para encerrar a aplicação.

## Possíveis melhorias

- Implementação de gestos para clique direito e duplo clique.
- Controle de rolagem utilizando movimentos dos dedos.
- Ajuste de sensibilidade e velocidade do cursor.
- Calibração da área de movimentação.
- Interface para configuração dos gestos.
- Melhorias na estabilidade e precisão do reconhecimento.

## Autor

**Gabriel Holanda Cunha**

Estudante de Engenharia de Software, interessado em desenvolvimento de software, Python e aplicações de visão computacional.

- GitHub: [@gabeswk](https://github.com/gabeswk)
- LinkedIn: [Gabriel Holanda Cunha](https://www.linkedin.com/in/gabriel-holanda-cunha-18a1352ab/)

---

Desenvolvido como projeto de estudo e experimentação com Python, visão computacional e interação humano-computador.
