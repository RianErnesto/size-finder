# size-finder
Integrantes: Rian Ernesto, Lucas Gabriel e Matheus Dourado
---
Esse repositório possui um arquivo em **Python** que toma como referência uma imagem com um objeto de tamanho conhecido para calcular o tamanho de outros objetos.

Sabemos que medições são imprescindíveis para um projeto funcionar de uma maneira ideal, seja na área da construção civil ou na área mecânica. Dessa forma, medir distância é indispensável para um engenheiro, mas sabemos também que em ocasiões excepcionais não temos esses equipamentos em mãos, então ao analisar essa situação, foi desenvolvido uma aplicação que tem como objetivo medir distâncias de um ponto ao outro, justamente para servir como auxílio em momentos que não tem esses equipamentos de medições. 

O objetivo é servir como auxílio em momentos excepcionais, como podemos citar quando um grupo de estudante da universidade estava desenvolvendo um projeto de robô sumô e não tinha equipamentos de medições, então a aplicação irá solucionar essa problemática, também incentivando o uso de escala de medidas de distância para desenvolver projetos.

Para rodar o código basta entra na pasta onde o arquivo se encontra e digitar o seguinte comando no CLI:
`python object_size.py --image object_size_image.jpeg --width 3`

Caso queira utilizar seu próprio exemplo, faça o upload de uma imagem com o mesmo nome e mesma extensão de arquivo e passe na flag _--width_ o tamanho do objeto de referência em centímetros.

**Obs.:** _o objeto referência deve ser aquele mais à esquerda da imagem e deve ter tamanho conhecido pelo usuário._
