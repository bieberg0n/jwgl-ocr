from PIL import Image
import collections
import glob
import sys
#n = 1
#for i in glob.glob('p/*.jpg'):
#img = Image.open(i)

def jo(filename):
	#读取字库
	fonts = []
	for i in glob.glob('pp/*.png'):
		fonts.append((i.replace('pp/','').replace('.png',''),Image.open(i).load()))

	#print(fonts[0][1])

	img = Image.open(filename)
	#img = img.convert('RGB')
	img = img.convert('RGB')
	pixdata = img.load()

	#print(pixdata[0,0])
	#l = [pixdata[x,y] for x in range(img.size[0]) for y in range(img.size[1])]
	#l.sort()
	#print(l[1])
	#边框
	for x in range(img.size[0]):
		pixdata[x,0] = (255, 255, 255)
	for y in range(img.size[1]):
		pixdata[0,y] = (255, 255, 255)
	for x in range(img.size[0]):
		pixdata[x,img.size[1]-1] = (255, 255, 255)
	for y in range(img.size[1]):
		pixdata[img.size[0]-1,y] = (255, 255, 255)

	#纯白
	for y in range(img.size[1]):
		for x in range(img.size[0]):
			#if pixdata[x,y][0] >= 200 and pixdata[x,y][1] >= 200 and pixdata[x,y][2] >= 200 or pixdata[x,y][0] <= 110 and pixdata[x,y][1] <= 110 and pixdata[x,y][2] <= 110:
			if pixdata[x,y][0] >= 175 and pixdata[x,y][1] >= 175 and pixdata[x,y][2] >= 175:
				pixdata[x,y] = (255, 255, 255)

	#去噪
	for i in range(2):
		for y in range(img.size[1]):
			for x in range(img.size[0]):
				try:
					if pixdata[x,y] != (255,255,255) and (pixdata[x-1,y] == pixdata[x+1,y] == (255,255,255) or pixdata[x,y-1] == pixdata[x,y+1] == (255,255,255)):
						pixdata[x,y] = (255, 255, 255)
					elif pixdata[x,y] != (255,255,255) and pixdata[x+1,y] != (255,255,255) and pixdata[x,y+1] != (255,255,255) and pixdata[x+1,y+1] != (255,255,255) and pixdata[x-1,y] == pixdata[x-1,y+1] == pixdata[x,y-1] == pixdata[x+1,y-1] == pixdata[x+2,y] == pixdata[x+2,y+1] == pixdata[x,y+2] == pixdata[x+1,y+2] == (255,255,255):
						pixdata[x,y] = pixdata[x+1,y] = pixdata[x,y+1] = pixdata[x+1,y+1]= (255, 255, 255)
				except IndexError:
					continue

	#img = img.convert('P')
	#print(pixdata[20,17])
	#img.save('c.png')

	#img.save('b.png')
	#img.show()

	#分割
	#内容区块
	db = []
	for x in range(img.size[0]):
		for y in range(img.size[1]):
			if pixdata[x,y] != (255,255,255):
				db.append(x)
				break

	j = len(db)-1
	k = 0
	for i in reversed(db):
		if i == db[j-1]+1:
			k += 1
		else:
			k = 0
		if k >= 2:
			del db[j]
		j -= 1

	def tooshort(l):
		for v in l[::2]:
			i = l.index(v)
			if db[i+1] - db [i] <= 2:
				return True

	if len(db) > 8 or tooshort(db):
		db = []
		for x in range(img.size[0]):
			nowhite = 0
			for y in range(img.size[1]):
				if pixdata[x,y] != (255,255,255):
					nowhite += 1
				if nowhite == 3:
					db.append(x)
					break

		db1 = []
		for i,v in enumerate(db):
			if i == 0 or i == len(db)-1:
				continue
			if db[i-1]+1 == v == db[i+1]-1 or db[i-1]+1 != v != db[i+1]-1:
				db1.append(i)

		for i in db1[::-1]:
			del db[i]

		while len(db) > 8:
			for v in db[1:-1:2]:
				i = db.index(v)
				if v - db[i-1] <=10:
					del db[i+1],db[i]
					break

	#while len(db) < 8:
	#	for v in db[::2]:
	#		i = db.index(v)
	#		if db[i+1] - v > 40:
	#			db.insert(i+1,v+24)
	#print(db)
	#exit()

	#切割对比
	answer = []
	n = 1
	def eye(v,v1,n):
		img0 = img.crop((v,0,v1,img.size[1]))
		pixdata = img0.load()
		dby = []
		for y in range(img0.size[1]):
			nowhite = 0
			for x in range(img0.size[0]):
				if pixdata[x,y] != (255,255,255):
					nowhite += 1
				if nowhite == 3:
					dby.append(y)
					break

		j = len(dby)-1
		k = 0
		for i in reversed(dby):
			if i == dby[j-1]+1:
				k += 1
			else:
				k = 0
			if k >= 2:
				del dby[j]
			j -= 1
		#img0.crop((0,dby[0],img0.size[0],dby[-1])).save('{}.png'.format(n))
		#n += 1
		#print(dby)
		if dby[-1] - dby[0] > 25:
			while len(dby) > 2:
				if len(dby) == 3:
					del dby[-1]
				for v in dby[1::2]:
					i = dby.index(v)
					if v - dby[i-1] <= 4:
						del dby[i],dby[i-1]
						break
		#print(dby)

		#for x in list(range(img0.size[0]))[:4]:
		dbx = 0
		#print(123123,n)
		#img0.crop((0,dby[0],img0.size[0],dby[-1])).save('{}.png'.format(n))
		#n += 1
		img0 = img0.crop((0,dby[0],img0.size[0],dby[-1]))
		pixdata = img0.load()

		for x in range(5):
			#white = img0.size[1]
			nowhite = 0
			#for y in list(range(img0.size[1]))[3:]:
			for y in range(img0.size[1]):
				if y <= 3 and pixdata[x,y] != (255,255,255):
					break
				if y > 3 and pixdata[x,y] != (255,255,255):
					nowhite += 1
			if 2 <= nowhite <= 3:
					#for y in range(img0.size[1])[3:]:
						#pixdata[x,y] = (255,255,255)
				dbx += 1
			else:
				break
			#print(nowhite)
					#break
		#img0.crop((dbx,dby[0],img0.size[0],dby[-1])).save('{}.png'.format(n))
		#img0.crop((dbx,0,img0.size[0],img0.size[1])).save('{}.png'.format(n))
		#print(dbx,dby)
		#imgl.append(img0.crop((0,db1[0],img0.size[0],db1[-1])))
		img0 = img0.crop((dbx,0,img0.size[0],dby[-1]))
		pixdata = img0.load()
		diffl = []
		for i in fonts:
			diff = 0
			for y in range(img0.size[1]):
				for x in range(img0.size[0]):
					try:
						if pixdata[x,y] != (255,255,255) and i[1][x,y] == (255,255,255) or pixdata[x,y] == (255,255,255) and i[1][x,y] != (255,255,255):
							diff += 1
					except IndexError:
						continue
			diffl.append((i[0],diff))

		min = ['',360]
		for i in diffl:
			if min[1] >= i[1]:
				min = i
		#print(sorted(diffl))
		#print(min[0].split('_')[0])
		return min[0].split('_')[0]


	#imgl = []
	#for i,v in enumerate(db[::2]):
	#print(db)
	for v in db[::2]:
		i = db.index(v)
		#print(i,v)
		if db[i+1] - v > 40:
			font = eye(v,v+29,n)
			answer.append(font)
			n += 1
			if font == 'b':
				font = eye(v+25,db[i+1],n)
				#img.crop((v+25,0,db[i+1],img.size[1])).save('t.png')
				#print(v+19)
			elif font == 'm':
				font = eye(v+28,db[i+1],n)
			elif font == 'h' or font == 'q':
				font = eye(v+26,db[i+1],n)
			else:
				font = eye(v+31,db[i+1],n)
		else:
			font = eye(v,db[i+1],n)
		answer.append(font)
		n += 1
		#if db[i+1] - v > 40:
		#	#db.insert(i+1,v+29)
		#	#db.insert(i+2,v+30)
		#	print(db)
		#	font = eye(v+31,db[i+1],n)
		#	answer.append(font)
		#	n += 1
		#answer.append(min[0].split('_')[0])
		#print(min)

	return ''.join(answer)

if __name__ == '__main__':
	for i in sys.argv[1:]:
		print(jo(i),end=' ')
	print()
	#print(jo('p/35.jpg'))
	#print(tesser('a.jpg'))

