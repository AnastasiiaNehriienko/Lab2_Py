import pickle
import os
def create_schedule(name_f):
	contin=True #умова для циклу
	file=open(name_f, 'ab')
	acts=[] #розклад
	while contin:
		act=[] #пункт розкладу
		name=input("Enter the name of the act: ") #умовна назва
		act.append(name) #додання
		time=input("Enter the beginning (hours and minutes with a space between them): ")
		h_m=time.split() #розділення годин і хвилин, уведених користувачем
		if len(h_m)!=2:  #якщо введено тільки години
			h_m.append(0)
		beg_m = int(h_m[0]) * 60 + int(h_m[1]) #розрахунок та запис часу у хвилинах
		act.append(beg_m) #додання
		time=input("Enter the end (hours and minutes with a space between them): ")
		h_m=time.split()
		if len(h_m)!=2:
			h_m.append(0)
		end_m = int(h_m[0]) * 60 + int(h_m[1]) #час закінчення
		act.append(end_m)
		ch=yes_or_no("Do you want to continue ? (Y / N) ") #перевірка, чи вводить користувач правильний знак
		if ch.upper() == 'Y':  #умова продовження
			contin = True
		else:
			contin = False
		acts.append(act)
	pickle.dump(acts, file)  #додавання у файл
	file.close()	#закриття файлу
def yes_or_no(ask):
	fail = True #для неправильних даних
	while fail:
		ch=input(ask)
		if ch.upper() == "Y" or ch.upper() == "N": #якщо користувач уводить потрібний символ
			fail = False
	return ch #повертає, так чи ні
def read_schedule(name):
	with open(name, 'rb') as file:
		acts_def=pickle.load(file) #завантаження із файлу
		a=file.tell()
		while file.tell()!=file.seek(0, 2):
			file.seek(a, 0)
			act1=pickle.load(file)
			acts_def+=act1
			a=file.tell()
		acts=sorted(acts_def, key=lambda x: x[1])  #розставляє справи за часом початку
		for act in acts:
			dur=act[2]-act[1]  #вираховує тривалість
			print("{:15s}    from {:02d}:{:02d} till {:02d}:{:02d}. Duration is {}h {}m".format(act[0], act[1]//60, act[1]%60,
																  act[2]//60, act[2]%60, dur//60, dur%60))
	return acts
def next(acts):
	time_now=input("What time is it now? (hours and minutes with a space between them): ");
	h_m=time_now.split()
	if len(h_m)!=2:
			h_m.append(0)
	time=int(h_m[0])*60+int(h_m[1])  #теперішній час
	next_time=24*60  #останній можливий час у дні
	next_act="Nothing"  #якщо нічого більше немає
	for act in acts:
		if act[1]>time and act[1]<next_time:  #пошук найближчої справи
			next_time=act[1]
			next_act=act[0]
	print("Next is "+next_act)
def spaces(acts):
	spaces=[]
	time_post=13*60  #пункт перевірки 13:00
	for act in acts:
		if act[1]<=time_post and act[2]>time_post:  #за наявності дії, що починається раніше, а закінчується пізніше
			time_post=act[2]
		if act[1]>time_post:
			dur=act[1]-time_post  #тривалість перерви
			spaces.append("Space from {:02d}:{:02d} to {:02d}:{:02d}. Duration is {}h {}m.".format(
				time_post//60, time_post%60, act[1]//60, act[1]%60, dur//60, dur%60))
			time_post=act[2]
	if time_post<24*60:  #остання перерва -- до кінця дня
		dur=24*60-time_post
		spaces.append("Space from {:02d}:{:02d} to 24:00. Duration is {}h {}m.".format(
				time_post//60, time_post%60, dur//60, dur%60))
	return spaces
def spaces_file(name, info):
	with open(name, "wb") as file:
		pickle.dump(info, file)  #запис у файл
def print_spaces(name):
	with open(name, "rb") as file:
		info=pickle.load(file)  #читання з файлу
		for space in info:      #виведення
			print(space)