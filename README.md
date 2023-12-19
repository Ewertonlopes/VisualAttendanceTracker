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


'''
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
'''

Todo sistema pode ser simplificado ao programa main. Onde temos o início da leitura em flash, necessário para a framework acessar o wifi, seguido do início da câmera que teve seus parâmetros decididos na função init_camera() e por fim o início do wifi, no caso com a utilização de um softap, por se tratar de um protótipo, e do webserver capaz de fazer o envio das imagens através da intranet ou internet.

### Software em Nuvem

O software em nuvem deve ser 

#### Pré-Processamento de Imagens




## Contribuitors

* Ewerton Vasconcelos Lopes 