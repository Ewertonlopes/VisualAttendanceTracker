# ESP CAM Visual Attendance Tracker

Este é o repositório do desenvolvimento de um sistema de presença automático. Este sistema tem a seguinte pretensão:
* Ser barato para ser reprodutível.
* Ser de simples utilização.
* Capaz de funcionar em Nuvem ou Névoa.

A utilização de sistemas embarcados de baixo custo para a produção de imagem visa simplificar e baratear o sensor final do sistema. Esse sensor deve ser capaz de produzir imagens com dada taxa de reprodução. Enquanto, em outra frente, o sistema deve ser capaz de funcionar em rede local, conhecido como névoa, ou com o uso da internet, conhecido como Nuvem.

Este repositório se divide em duas partes principais:
* espServer: que apresenta um servidor web para um espcam;
* PythonClient: que apresenta um cliente em Python para fazer todo processamento de imagens.

## Hardware

Qualquer hardware com sensores de imagem e capacidade de conexão podem ser utilizados como ponto final do sistema. Abaixo está posto o devkit utilizado para os testes de resposta. Um sistema parecido pode ser encontrado no link a seguir: <https://www.robocore.net/wifi/esp32-cam-esp32-com-camera>

![Microcontrolador Esp32 com camera](https://d229kd5ey79jzj.cloudfront.net/1205/images/1205_1_H.png?20230725094432 "Esp cam")

## Software

O desenvolvimento do software pode ser dividido em duas partes essenciais:
* O firmware a ser embarcado.
* O sistema em nuvem possui capacidades de reconhecimento complexo.

### Firmware

Para o desenvolvimento do sistema embarcado se utilizou a framework da espressif,[Espressif IDF](https://github.com/espressif/esp-idf). Dentro dessa framework se utilizou a [biblioteca adequada](https://github.com/espressif/esp32-camera)  para captura de imagens com a câmera ov2640, uma câmera de baixo custo e consumo.


~~~ c
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
      ESP_ERROR_CHECK(nvs_flash_erase());
      ret = nvs_flash_init();
    }

    if(ESP_OK != init_camera()) {
        return;
    }

    wifi_init_softap();

    init_webserver();
~~~

Todo sistema pode ser simplificado ao programa main. Onde temos o início da leitura em flash, necessário para a framework acessar o wifi, seguido do início da câmera que teve seus parâmetros decididos na função init_camera() e por fim o início do wifi, no caso com a utilização de um softap, por se tratar de um protótipo, e do webserver capaz de fazer o envio das imagens através da intranet ou internet.

### Software em Nuvem

O software em nuvem é baseado em duas bibliotecas principais:

* Opencv
* face_recognition

Ainda foram aplicadas bibliotecas de csv, datetime e numpy.

#### Captura de Imagens

O procedimento de captura de imagem pode ser simplificada pelas linhas de código a seguir:

~~~ python
stream_url = "http://192.168.4.1:80"  

cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Error: Could not open video stream")
    exit()

(...)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error reading frame from the video stream")
        break
~~~

Assim uma estrutura de câmera será captura do webserver, foi possível conseguir taxas superiores a 30 fps com imagem comprimida como jpg dessa forma.

#### Pré-Processamento de Imagens

Pela estrutura do sistema e não necessidade de visualização das imagens se resolveu se utilizar de técnicas de equalização, para isso é necessário operar em YUV ao invés de BGR.

~~~ python
def equalize_color(img):
    frame_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)

    frame_yuv[:,:,0] = cv2.equalizeHist(frame_yuv[:,:,0])

    return cv2.cvtColor(frame_yuv, cv2.COLOR_YUV2BGR)
~~~

![Imagem sem equalização]('/Archives/Images/notequal.jpg' "Not Equal")


#### Processamento das Imagens

A


## Contribuitors

* Ewerton Vasconcelos Lopes 