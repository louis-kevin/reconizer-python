# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
import numpy as np

class Interface():
    def Captura(self):
        self.filename = askopenfilename()
        self.image = Image.open(self.filename)
        self.photo = ImageTk.PhotoImage(self.image)
        label = Label(self.root, image=self.photo).grid(row=1, column=0, padx=15, pady=5)    
     
    def Treinamento(self):
        self.rede = Sequential()
        
        self.rede.add(Conv2D(64, (3,3), input_shape=(64, 64, 3), activation='relu'))
        self.rede.add(BatchNormalization())
        self.rede.add(MaxPooling2D(pool_size=(2, 2)))
        
        self.rede.add(Flatten())
        
        self.rede.add(Dense(units=100, activation='relu'))
        self.rede.add(Dense(units=100, activation='relu'))
        self.rede.add(Dense(units=1, activation='sigmoid'))
        
        self.rede.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        
        gerador_treinamento = ImageDataGenerator(rescale=1. /255, rotation_range=7, horizontal_flip=True, shear_range=0.2, height_shift_range=0.07, zoom_range=0.2)
        
        
        gerador_teste = ImageDataGenerator(rescale=1. / 255)
        
        base_treinamento = gerador_treinamento.flow_from_directory('images', target_size=(64, 64), batch_size = 32, class_mode = 'binary')
        base_teste = gerador_teste.flow_from_directory('images', target_size=(64, 64), batch_size = 32, class_mode = 'binary')
        
        self.rede.fit_generator(base_treinamento, steps_per_epoch=60, epochs=5, validation_data = base_teste, validation_steps=20)
        
        
    
    def ClassificarImagens(self):
        imagem_teste = image.load_img(self.filename, target_size=(64,64))
        imagem_teste = image.img_to_array(imagem_teste)
        imagem_teste /= 255
        imagem_teste = np.expand_dims(imagem_teste, axis=0)
        
        previsao = self.rede.predict(imagem_teste)
        
        if previsao > 0.5:
            print('floresta')
            Label(self.root, text='floresta').grid(row=1, column=0)
        elif previsao < 0.5:
            print('deserto')
            Label(self.root, text='deserto').grid(row=1, column=0)
 
    
    def __init__(self):
        self.root = Tk()
        self.root.title('Classificador de Imagens')
        
        Button(self.root, text='Seleciona a Imagem', command=self.Captura).grid(row=0, column=0, pady=5)
        Button(self.root, text='Treinar', command=self.Treinamento).grid(row=0, column=1, pady=5)
        Button(self.root, text='Classificar', command=self.ClassificarImagens).grid(row=1, column=1, pady=5)
        
        self.root.mainloop()
        
Interface()