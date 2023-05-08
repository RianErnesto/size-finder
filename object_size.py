# Pacotes
import cv2
import numpy as np
from scipy.spatial import distance as dist
import imutils
from imutils import perspective
from imutils import contours
import argparse

# Função para calcular o ponto intermediário entre as coordenadas x e y
def calculateMidpoint(a, b):
	return ((a[0] + b[0]) * 0.5, (a[1] + b[1]) * 0.5)

# Para passar os argumentos via terminal
argumentParser = argparse.ArgumentParser()
argumentParser.add_argument("-i", "--image", required=True,
	help="Caminho da imagem")
argumentParser.add_argument("-w", "--width", type=float, required=True,
	help="Comprimento do objeto mais à esquerda, que é o de referência (em centímetros)")
args = vars(argumentParser.parse_args())

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)

edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

# Acha os contornos na imagem
imgContours = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
imgContours = imutils.grab_contours(imgContours)

# Ordena os contornos da esquerda para a direita e inicializa a variável que vai calibrar o sistema
(imgContours, _) = contours.sort_contours(imgContours)
pixelsPerMetric = None

# Loop sobre os contornos existentes na imagem
for cont in imgContours:

	# Ignora os contornos muito pequenos
	if cv2.contourArea(cont) < 80:
		continue

	# Rotaciona o contorno e acha o menor retângulo que o envolve
	orig = image.copy()
	box = cv2.minAreaRect(cont)
	box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
	box = np.array(box, dtype="int")

	# Ordena os pontos do contorno de forma que eles apareça no sentido horário começando do canto superior esquerdo e desenha o contorno do retângulo rotacionado no objeto
	box = perspective.order_points(box)
	cv2.drawContours(orig, [box.astype("int")], -1, (133, 22, 171), 2)

	# Loop sobre os pontos do contorno e desenha um círculo em cada um deles
	for (x, y) in box:
		cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

	# Desempacota o retângulo rotacionado e calcula os pontos médios entre os pontos do retângulo
	(topLeft, topRight, bottomRight, bottomLeft) = box
	(topLeft_topRightX, topLeft_topRightY) = calculateMidpoint(topLeft, topRight)
	(bottomLeft_bottomRightX, bottomLeft_bottomRightY) = calculateMidpoint(bottomLeft, bottomRight)

	# Calcula os pontos médios entre os pontos do retângulo
	(topLeft_bottomLeftX, topLeft_bottomLeftY) = calculateMidpoint(topLeft, bottomLeft)
	(topRight_bottomRightX, topRight_bottomRightY) = calculateMidpoint(topRight, bottomRight)

	# Desenha os pontos médios na imagem
	cv2.circle(orig, (int(topLeft_topRightX), int(topLeft_topRightY)), 5, (29, 30, 89), -1)
	cv2.circle(orig, (int(bottomLeft_bottomRightX), int(bottomLeft_bottomRightY)), 5, (29, 30, 89), -1)
	cv2.circle(orig, (int(topLeft_bottomLeftX), int(topLeft_bottomLeftY)), 5, (29, 30, 89), -1)
	cv2.circle(orig, (int(topRight_bottomRightX), int(topRight_bottomRightY)), 5, (29, 30, 89), -1)

	# Desenha as linhas entre os pontos médios
	cv2.line(orig, (int(topLeft_topRightX), int(topLeft_topRightY)), (int(bottomLeft_bottomRightX), int(bottomLeft_bottomRightY)),
		(59, 173, 164), 2)
	cv2.line(orig, (int(topLeft_bottomLeftX), int(topLeft_bottomLeftY)), (int(topRight_bottomRightX), int(topRight_bottomRightY)),
		(59, 173, 164), 2)
	



	# Calcula a distância Euclidiana entre os pontos médios
	dA = dist.euclidean((topLeft_topRightX, topLeft_topRightY), (bottomLeft_bottomRightX, bottomLeft_bottomRightY))
	dB = dist.euclidean((topLeft_bottomLeftX, topLeft_bottomLeftY), (topRight_bottomRightX, topRight_bottomRightY))

	# Se a variável que calibra o sistema não foi inicializada, então calcula ela como a razão entre os pixels e a métrica fornecida (neste caso, centímetros)
	if pixelsPerMetric is None:
		pixelsPerMetric = dB / args["width"]

	# Cálculo do tamanho do objeto
	dimA = dA / pixelsPerMetric
	dimB = dB / pixelsPerMetric

	# Desenha o tamanho do objeto na imagem
	cv2.putText(orig, "{:.1f}cm".format(dimB),
		(int(topLeft_topRightX - 15), int(topLeft_topRightY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (255, 255, 255), 2)
	cv2.putText(orig, "{:.1f}cm".format(dimA),
		(int(topRight_bottomRightX + 10), int(topRight_bottomRightY)), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (255, 255, 255), 2)
	
	# Mostra a imagem
	cv2.imshow("Size detector", orig)
	cv2.waitKey(0)