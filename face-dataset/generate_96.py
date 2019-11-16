import os
import numpy as np
import cv2

def generate_structure():
	structure = []
	keys      = None

	currdir   = "." 

	for root, dirs, files in os.walk(currdir):
		# print("root  : " + root)
		# print("dirs  : " + str(dirs))

		if len(dirs) != 0:
			keys = dirs

		temp = []

		for name in files:
			if root != currdir:
				temp.append(os.path.join(root, name))
				
			# print(os.path.join(root, name))

		if len(temp) != 0:
			structure.append(temp)

	return (structure, keys)

def read_image(filepath):
	return cv2.imread(filepath, -1)

def write_image(im, dest):
	return cv2.imwrite(dest, im)

def resize_image(face, size):
	return cv2.resize(face, size)

def draw_image(imdest, imfrom, x, y):
	# Extract the alpha mask of the RGBA image, convert to RGB 
	b,g,r = cv2.split(imfrom)
	overlay_color = cv2.merge((b,g,r))
	
	# Apply some simple filtering to remove edge noise
	# mask = cv2.medianBlur(a,5)

	h, w, _ = overlay_color.shape
	rows, cols, _ = imdest.shape
	# y, x = (y - h // 2, x - w // 2)
	y, x = (y - h, x - w)
	# roi = image[y-h//2:y+h//2, x-w//2:x+w//2]

	# # Black-out the area behind the logo in our original ROI
	# img1_bg = cv2.bitwise_and(roi.copy(),roi.copy(),mask = cv2.bitwise_not(mask))
	
	# # Mask out the logo from the logo image.
	# img2_fg = cv2.bitwise_and(overlay_color,overlay_color,mask = mask)

	# # Update the original image with our new ROI
	# image[y-h//2:y+h//2, x-w//2:x+w//2] = cv2.add(img1_bg, img2_fg)

	for i in range(w):
		for j in range(h):
			if x + i >= cols or y + j >= rows:
				continue
			# alpha = float(imfrom[j][i][3] / 255.0)  # read the alpha channel
			# imdest[y + j][x + i] = imfrom[j][i] + imdest[y + j][x + i]
			imdest[y + j][x + i] = imfrom[j][i]

	return imdest

def main():
	ext = "jpg"
	struct, keys = generate_structure()

	# print(str(struct))
	# print(str(keys))
	size   = 96
	# ssheet = 8
	# wsheet = ssheet * size
	for i, data in enumerate(struct):
		# hsheet = (len(data) // ssheet) * size
		# blank = 255 * np.ones(shape=[hsheet, wsheet, 3], dtype=np.uint8)
		# sh, sw, _ = blank.shape
		# sy, sx = (0, 0)
		basedir = os.path.join('.', keys[i], "96x96")
		if not os.path.exists(basedir):
			os.makedirs(basedir)

		for j, fp in enumerate(data):
			face = read_image(fp)
			face = resize_image(face, (size, size))

			print("Drawing " + str(j) + " face of " + keys[i] + "\r")
			write_image(face, os.path.join(basedir, fp[(fp.rfind("/") + 1):]))

			# ry, cx, _ = face.shape
				
			# sy = size * (j // ssheet)

			# if j % ssheet == 0:
			# 	sx = 0

			# blank = draw_image(blank, face, sx, sy)

			# sx += size
			# break

			# for y1 in range(ry): 
			# 	for x1 in range(cx):						 	
			# 		blank[sy][sx] = face[y1][x1]
			# 		sx += 1

			# 	sy += 1

			# print("Draw image " + fp + " on " + keys[i] + '.' + ext)



if __name__ == '__main__':
	main()