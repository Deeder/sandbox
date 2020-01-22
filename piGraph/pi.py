import math
from PIL import Image, ImageDraw
import seaborn
import matplotlib.pyplot as plt


# Colors
colorPalettes = {
	'pastel': ['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd'],
	'blue'  : ['#e3fafc','#c5f6fa','#99e9f2','#66d9e8','#3bc9db','#22b8cf','#15aabf','#1098ad','#0c8599','#0b7285'],
	'lime'  : ['#f4fce3','#e9fac8','#d8f5a2','#c0eb75','#a9e34b','#94d82d','#82c91e','#74b816','#66a80f','#5c940d'],
	'redtoblue' : seaborn.color_palette("RdBu_r", n_colors=10, desat=.5).as_hex(),
	'creamblue' : seaborn.cubehelix_palette(10, start=.5, rot=-.75).as_hex(),
	'darkpastel': seaborn.cubehelix_palette(10, start=1.0, rot=-5, light=0.7, dark=0.3, hue=1.0, gamma=1/2.2).as_hex(),
	'muted'     : seaborn.color_palette("muted", n_colors=10).as_hex()
}
palette      = 'muted'
dotColor     = '#CCCCCC'
imageColor   = 'white'
showPalette  = False

if showPalette:
	seaborn.palplot(seaborn.color_palette(colorPalettes[palette]))
	plt.show()

# Format parameters
nColumns   = 10
nRows      = 10
zoomFactor = 10
nMaxColors = 10

# Relative size of design elements
widthSquare   = 6   * zoomFactor
heightSquare  = 6   * zoomFactor
heightEllipse = 3   * zoomFactor
widthEllipse  = 3   * zoomFactor
spaceSize     = 1.5 * zoomFactor

# Output image name
output = "test_{}x{}_{}_{}colors".format(nColumns, nRows, palette, nMaxColors)

# Load pi decimals
with open('pi.txt') as f:
	pi = f.read(nColumns*nRows)
nChiffres = len(pi)
assert(nChiffres >= nColumns*nRows)

print("Generating image")
heightImage = int(spaceSize + (widthSquare+spaceSize) * min(int(nChiffres/float(nRows)+1), nColumns) + 0.5)
widthImage  = int(spaceSize + nRows * (widthSquare + spaceSize) + 0.5)
im   = Image.new("RGB", (widthImage, heightImage), imageColor)
draw = ImageDraw.Draw(im)
squareColors = colorPalettes[palette]
mod = min(len(squareColors), nMaxColors)


for i, n in enumerate(pi):
	if i/nRows < nColumns:
		y = i // nRows
		x = i % nRows
		if n != '.':
			draw.rectangle([
				(widthSquare+spaceSize)*x+spaceSize, 
				y*(heightSquare+spaceSize)+spaceSize, 
				spaceSize*x+widthSquare*(x+1)+spaceSize, 
				spaceSize*y+(y+1)*heightSquare+spaceSize
			], fill=squareColors[eval(n)%mod])
		else:

			draw.ellipse(
				[
					(widthSquare+spaceSize)*x + (heightSquare-heightEllipse)/2+spaceSize, 
					y*(heightSquare+spaceSize)+(widthSquare-widthEllipse)+spaceSize, 
					spaceSize*x+widthSquare*(x+1) - (heightSquare-heightEllipse)/2+spaceSize, 
					spaceSize*y+(y+1)*heightSquare+spaceSize#-(widthSquare-widthEllipse)/2
				], fill=dotColor
			)
del draw

# Save image
im.save(output+".png", "PNG")
print("Image saved")