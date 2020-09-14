import glob
import sys
import os
import os.path
import struct
import re
import time

#拆分bin文件，每个文件大小200K
def split_bin_file(dest_fileName):
	try:
		audio_bin = open(dest_fileName,'wb')
		#print("hello world")
		
		"""
		pos_start = voice.tell()
		for line in voice.readlines():
			pass
		pos_end = voice.tell()
		voice.seek(0)
		"""
		#写地址,seek(0)
		print(hex(v_bin.tell()))
		audio_index = hex(v_bin.tell())
		audio_index = audio_index[2:]
		audio_bin.seek(0)
		#print(audio_index)
		if len(audio_index) <= 2:
			a = struct.pack('B', int(audio_index, 16))
			audio_bin.write(a)
		else:
			i = 0
			cnt = len(audio_index)%2+int(len(audio_index)/2)
			#print(cnt)
			while i < cnt:
				wb = audio_index[-2::]
				a = struct.pack('B', int(wb, 16))
				audio_bin.write(a)
				audio_index = audio_index[0:(len(audio_index)-2)]
				#print(wb)
				i = i + 1
		audio_bin.seek(8)
		#从bin捞出来写拆分文件
		while (audio_bin.tell() <=  (FILE_SIZE - 1)) and (v_bin.tell() != v_end):
			audio_bin.write(v_bin.read(1))
		"""
		for line in v_bin.readlines():
			audio.write(line)
			#print(v_bin.tell())
			if(audio.tell() >=  204808):
				#v_bin.seek(audio.tell())
				break
		"""
		#audio.seek(4)
		#写文件大小，seek(4)
		audio_len = hex(audio_bin.tell())
		audio_len = audio_len[2:]
		audio_bin.seek(4)
		#print(audio_len)
		if len(audio_len) <= 2:
			a = struct.pack('B', int(audio_len, 16))
			audio_bin.write(a)
		else:
			i = 0
			cnt = len(audio_len)%2+int(len(audio_len)/2)
			#print(cnt)
			while i < cnt:
				wb = audio_len[-2::]
				a = struct.pack('B', int(wb, 16))
				audio_bin.write(a)
				audio_len = audio_len[0:(len(audio_len)-2)]
				#print(wb)
				i = i + 1
				
		audio_bin.close()
	finally:
		if audio_bin:
			audio_bin.close()

#读单个音频文件的函数
def read_voice_file(fileName,wav):
	try:
		voice = open(fileName,'rb+')
		
		voice.seek(0)
		pos_start = voice.tell()
		for line in voice.readlines():
			pass
		pos_end = voice.tell()
		#看是否四字对齐
		sup = 4 - ((pos_end - pos_start) % 4)
		while sup > 0 and sup != 4:
			voice.write(struct.pack('B', int('0', 16)))
			sup -= 1
			
		voice.seek(0)
		for line in voice.readlines():
			#print(v_bin.tell())
			v_bin.write(line)
	finally:
		if voice:
			voice.close()

#main 函数开始
print('*******************************')
print('******** Please Input *********')
print('*******************************')
#voice_p = input('Voice path:')
voice_p = './all_bin'
version_id = input('Version id:')
ISOTIMEFORMAT = '%Y-%m-%d %X'
Time = time.strftime( ISOTIMEFORMAT, time.localtime() )
print('version -【版本 %s】- %s' %(version_id,Time))
#BinName = 'voice_V' + version_id + '.wav'

#audioVx.x.audio_num
version_len = 4
file_cnt_len = 4
files = os.listdir(voice_p)
fileNames = []
fileNames1 = []
fileNames2 = []
fileNames3 = []
hex_index_txt = []
index_p = {}
flag = 0
vp = 0
audio_num = 0
for fileName in files:
	audio_num = audio_num +1
	#fileNames.append(int(fileName.split('.')[0]))
	fileNames1.append(fileName)
	#fileNames[fileName.split('_')[0]] = fileName.split('_')[1] 
#audio_num = len(fileNames)
#print(audio_num)
BinName = 'audioV' + version_id + '_audio_num' + str(audio_num) + '.bin'
fileNames2 = sorted(fileNames1,key = lambda i:int(re.match(r'(\d+)',i).group()))
print(fileNames2)
FILE_SIZE = 1024*200 + 8

#p = 0x830000 + 0x44#index address  0x44 = 68 0x64 = 100 
#p = 0x64+version_len+file_cnt_len#index address  0x44 = 68 0x64 = 100 #100个字节
p = 0x400+version_len+file_cnt_len #1024个字节

try:
	v_bin = open(BinName,'wb+')
	v_bin.seek(p)
	vp_start, vp_end = 0, 0
	if voice_p:
		print('path: %s!' % voice_p)
		"""
		for fileName in files:
			fileNames.append(int(fileName.split('.')[0]))
		"""
		#
		for f in fileNames2:
			#print (f)
			fileNames3.append(voice_p + '/' + f)#+ '.' +  f.split('.')[1])
		for fileName in fileNames3:
			#print(fileName)
			p += vp
			hex_p = hex(p)
			add_zero_cnt =8 - len(hex(p)) % 8
			hex_p1 = hex_p[:2]
			hex_p2 = hex_p[2:]
			while add_zero_cnt != 0 and add_zero_cnt != 8:
				hex_p1 = hex_p1 + '0'
				add_zero_cnt -= 1
			hex_p = hex_p1 +hex_p2
			
			i = 1
			while i < 4: 
				hex_index_txt.append(re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", hex_p).split(' ')[i])
				i += 1
			#print(len(hex_index_txt))
			str1 = ''
			hex_index_txt = hex_index_txt[::-1]
			for i in hex_index_txt:
				str1 = str1 + str(i)
				#print()
			index_p[fileName.split('/')[2]] = str1
			vp_start = v_bin.tell()
			read_voice_file(fileName,v_bin)
			vp_end = v_bin.tell()
			vp = vp_end - vp_start
			hex_index_txt = []
		v_end = v_bin.tell()#生成的bin文件大小
		#将index写入index.txt文件
		try:
			index_f = open('index.txt', 'w')
			for k in index_p:
				print(k + ': ' + index_p[k])
				index_str = str(k) +':' + str(index_p[k]) + '\n'
				index_f.writelines(index_str)
		finally:
			if index_f:
				index_f.close()
				
		v_bin.seek(0)
		#增加语音条目数
		file_cnt = audio_num#len(fileNames)
		hex_cnt = hex(file_cnt)
		hex_cnt = hex_cnt[2:]
		if len(hex_cnt) <= 2:
			a = struct.pack('B', int(hex_cnt, 16))
			v_bin.write(a)
		else:
			i = 0
			cnt = len(hex_cnt)%2+int(len(hex_cnt)/2)
			print(cnt)
			while i < cnt:
				wb = hex_cnt[-2::]
				a = struct.pack('B', int(wb, 16))
				v_bin.write(a)
				hex_cnt = hex_cnt[0:(len(hex_cnt)-2)]
				#print(wb)
				i = i + 1
		#增加版本号码
		v_bin.seek(4)
		vs_id = int(version_id)
		hex_id = hex(vs_id)
		hex_id = hex_id[2:]
		if len(hex_id) <= 2:
			a = struct.pack('B', int(hex_id, 16))
			v_bin.write(a)
		else:
			i = 0
			cnt = len(hex_id)%2+int(len(hex_id)/2)
			print(cnt)
			while i < cnt:
				wb = hex_id[-2::]
				a = struct.pack('B', int(wb, 16))
				v_bin.write(a)
				hex_id = hex_id[0:(len(hex_id)-2)]
				#print(wb)
				i = i + 1
		'''
		j = 0
		hex_id = hex(vs_id)
		hex_id = hex_id[2:]
		if len(hex_id)%2 == 1:
			cnt = int(len(hex_id)/2)+1
		else:
			cnt = int(len(hex_id)/2)
		print(cnt,hex_id[0])
		while j < cnt:
			if len(hex_id) == 1:
				a = struct.pack('B', int(hex_id, 16))
				v_bin.write(a)
				break;
			b = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", hex_id).split(' ')[i]
			a = struct.pack('B', int(hex_id, 16))
			v_bin.write(a)
			print(hex_id)
			j = j + 1
		'''
		v_bin.seek(version_len+file_cnt_len)
		
		for k in index_p:
			index = []
			i = 0
			while i < 3: 
				index.append(re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", str(index_p[k])).split(' ')[i])
				i += 1
				
			#flag = 3
			#index_re = index[::-1]
			for i in index:
				#print(i)
				if i == '0x':
					#flag = 0
					continue
				a = struct.pack('B', int(i, 16))
				v_bin.write(a)
				
			v_bin.seek(v_bin.tell()+1)
			
		#拆分bin文件，每个文件大小200K
		v_bin.seek(0)
		
		if (v_end / 204800) - (v_end // 204800)  > 0:
			i = v_end // 204800 + 1
		else:
			i = v_end // 204800
		k=0
		while k < i:
			k = k + 1
			audio_name = "audio" + str(k) + "_" + str(hex(v_bin.tell())) + ".bin"
			split_bin_file(audio_name)
			#dex = str(hex(v_bin.tell()))
			#print(dex)
			#print("k = "  + str(k))
		
	else:
		print('NO voice path!')
finally:
	if v_bin:
		v_bin.close()