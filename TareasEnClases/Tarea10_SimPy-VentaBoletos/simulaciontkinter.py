from mimetypes import init
from tkinter import * 
import collections
import random
import simpy
from PIL import ImageTk, Image
import matplotlib.pyplot as plt


class Cinema:
  
  ##Creacion de ventana
  ventana=Tk()
  frame=Frame(ventana)
  ##Alto y ancho de la ventana
  WIDTH, HEIGHT = 1280, 960
  canvas=Canvas(ventana, width=WIDTH, height=HEIGHT, bg = "white")

  ##Configuraciones de pantalla
  ventana.title('WELCOME TO CINEMA')
  ventana.resizable(False, False)
  ventana.config(bg="#fff")
  frame.pack(side="right", expand = False)
  canvas.pack(side='right', expand = False)

  ##Variables para simulacion ejemplo proporcionado por Diego Quisi
  NUM_BOLETO = 100
  TIEMPO_SIMULACION = 60*3
  boletos={}

  ##Lectura de imagenes
  imgConjuro = ImageTk.PhotoImage(Image.open("conjuro3.jpg").resize((160,240)))
  imgRF = ImageTk.PhotoImage(Image.open("RF.jpg").resize((160,240)))
  imgPF = ImageTk.PhotoImage(Image.open("PF.jpg").resize((160,240)))
  
  ##Creando interfaz grafica aplicacion
  titulo1=canvas.create_text(200, 30, text="Conjuro 3", fill="black", font=('Helvetica 25'))
  titulo2=canvas.create_text(600, 30, text="Rapidos y Furiosos 10", fill="black", font=('Helvetica 25'))
  titulo3=canvas.create_text(1050, 30, text="Pulp Fictions", fill="black", font=('Helvetica 25'))

  peliculaPost1=canvas.create_image(120, 60, image=imgConjuro, anchor="nw")
  peliculaPost2=canvas.create_image(525, 60, image=imgRF, anchor="nw")
  peliculaPost3=canvas.create_image(975, 60, image=imgPF, anchor="nw")

  titulo4=canvas.create_text(150, 350, text="Boletos Disponibles: ", fill="black", font=('Helvetica 17 bold'))

  contador1=canvas.create_text(185, 400, text=(str(NUM_BOLETO) + " Boletos"), fill="black", font=('Helvetica 18'))
  contador2=canvas.create_text(600, 400, text=(str(NUM_BOLETO) + " Boletos"), fill="black", font=('Helvetica 18'))
  contador3=canvas.create_text(1050, 400, text=(str(NUM_BOLETO) + " Boletos"), fill="black", font=('Helvetica 18'))
  
  titulo5=canvas.create_text(205, 450, text="Boletos Agotados en tan solo: ", fill="black", font=('Helvetica 17 bold'))
  agotado1=canvas.create_text(185, 500, text="0.0 minutos", fill="black", font=('Helvetica 18'))
  agotado2=canvas.create_text(600, 500, text="0.0 minutos", fill="black", font=('Helvetica 18'))
  agotado3=canvas.create_text(1050, 500, text="0.0 minutos", fill="black", font=('Helvetica 18'))

  titulo6=canvas.create_text(285, 550, text="Personas que salieron de la fila/renegados: ", fill="black", font=('Helvetica 17 bold'))
  renegados1=canvas.create_text(185, 600, text="0, personas", fill="black", font=('Helvetica 18'))
  renegados2=canvas.create_text(600, 600, text="0, personas", fill="black", font=('Helvetica 18'))
  renegados3=canvas.create_text(1050, 600, text="0, personas", fill="black", font=('Helvetica 18'))

  titulo7=canvas.create_text(150, 675, text="Pedidos de Clientes: ", fill="black", font=('Helvetica 17 bold'))
  titulo8=canvas.create_text(650, 675, text="Respuesta: ", fill="black", font=('Helvetica 17 bold'))
  pedidoCliente=canvas.create_text(210, 725, text="0 entradas para: \n peliculas", fill="black", font=('Helvetica 18'))
  confirmacionEmpleado=canvas.create_text(650, 725, text="Agotado", fill="black", font=('Helvetica 18'))


  tiempo=canvas.create_text(1100, 900, text="Tiempo: 0.0", fill="black", font=('Helvetica 35 bold'))

  ##Definicion de funciones para actualizar valores de canvas
  def notificacion_pedido_cliente(self,boletos,funcion):

    self.canvas.delete(self.pedidoCliente)    
    self.pedidoCliente=self.canvas.create_text(210, 725, text=str(boletos)+" entradas para: \n"+ str(funcion), fill="black", font=('Helvetica 18'))
    self.canvas.update()

  def notificacion_confirmacion_empleado(self,env,tipo_notificacion):
    self.canvas.delete(self.confirmacionEmpleado) 
    if(tipo_notificacion==1):
      self.confirmacionEmpleado=self.canvas.create_text(650, 725, text="Entradas agotadas \n  a las: "+str(round(env.now,1)), fill="black", font=('Helvetica 18'))
    if(tipo_notificacion==2):
      self.confirmacionEmpleado=self.canvas.create_text(650, 725, text="Stock no disponible\n a las: "+str(round(env.now,1)), fill="black", font=('Helvetica 18'))
    if (tipo_notificacion==3):
      self.confirmacionEmpleado=self.canvas.create_text(650, 725, text="Vendiendo Entradas\nFin a las: "+str(round(env.now,1)), fill="black", font=('Helvetica 18'))
    self.canvas.update

  def stock_venta_boletos(self,pelicula,boletos):
    if(pelicula=="Conjuro 3"):
      self.canvas.delete(self.contador1)
      self.contador1=self.canvas.create_text(185, 400, text=(str(boletos) + " Boletos"), fill="black", font=('Helvetica 18'))
    if(pelicula=='Rapidos y Furiosos 10'):
      self.canvas.delete(self.contador2)
      self.contador2=self.canvas.create_text(600, 400, text=(str(boletos) + " Boletos"), fill="black", font=('Helvetica 18'))
    if(pelicula=='Pulp Fictions'):
      self.canvas.delete(self.contador3)
      self.contador3=self.canvas.create_text(1050, 400, text=(str(boletos) + " Boletos"), fill="black", font=('Helvetica 18'))
    self.canvas.update()

  def aumentar_numero_renegados(self,pelicula,renegados):
    if(pelicula=="Conjuro 3"):
      self.canvas.delete(self.renegados1)
      self.renegados1=self.canvas.create_text(185, 600, text=str(renegados)+', personas', fill="black", font=('Helvetica 18'))
    if(pelicula=='Rapidos y Furiosos 10'):
      self.canvas.delete(self.renegados2)
      self.renegados2=self.canvas.create_text(600, 600, text=str(renegados)+', personas', fill="black", font=('Helvetica 18'))
    if(pelicula=='Pulp Fictions'):
      self.canvas.delete(self.renegados3)
      self.renegados3=self.canvas.create_text(1050, 600, text=str(renegados)+', personas', fill="black", font=('Helvetica 18'))
    self.canvas.update()
  

  def registrar_hora_terminacion_Stock(self,pelicula,hora):
    if(pelicula=="Conjuro 3"):
      self.canvas.delete(self.agotado1)
      self.agotado1=self.canvas.create_text(185, 500, text=str(round(hora,1))+" minutos", fill="black", font=('Helvetica 18'))
    if(pelicula=='Rapidos y Furiosos 10'):
      self.canvas.delete(self.agotado2)
      self.agotado2=self.canvas.create_text(600, 500, text=str(round(hora,1))+" minutos", fill="black", font=('Helvetica 18'))
    if(pelicula=='Pulp Fictions'):
      self.canvas.delete(self.agotado3)
      self.agotado3=self.canvas.create_text(1050, 500, text=str(round(hora,1))+" minutos", fill="black", font=('Helvetica 18'))
    self.canvas.update()

  def ventaBoletos(self,env, num_boletos, pelicula, teatro):
    with teatro.contador.request() as turno:      
      resultado = yield turno | teatro.sold_out[pelicula]

      self.notificacion_pedido_cliente(num_boletos,pelicula)
      if turno not in resultado:
        teatro.num_renegados[pelicula] += 1
        self.notificacion_confirmacion_empleado(env, 1)
        self.aumentar_numero_renegados(pelicula,teatro.num_renegados[pelicula])
        return
      if teatro.num_boletos[pelicula] < num_boletos:
        yield env.timeout(0.5)
        self.notificacion_confirmacion_empleado(env, 2)
        return
      
      elif pelicula in list(self.boletos.keys()):
        peliculaObtenida=self.boletos.get(pelicula)
        peliculaObtenida.append([num_boletos, round(env.now,1)])
        self.boletos[pelicula]=peliculaObtenida

      else:
        self.boletos[pelicula]=[[num_boletos, round(env.now,1)]]
      
      self.notificacion_confirmacion_empleado(env, 3)
      teatro.num_boletos[pelicula] -= num_boletos
      self.stock_venta_boletos(pelicula,teatro.num_boletos[pelicula])
      
      if teatro.num_boletos[pelicula] < 1:
        teatro.sold_out[pelicula].succeed()
        teatro.tiempo_agotado[pelicula] = env.now
        teatro.num_boletos[pelicula] = 0
        self.registrar_hora_terminacion_Stock(pelicula,env.now)
      yield env.timeout(1)

  def llegadaClientes(self,env, teatro):  
    while True:      
      yield env.timeout(random.expovariate(1/0.5))    
      pelicula = random.choices(teatro.peliculas, teatro.probabilidad, k=1)    
      num_boletos = random.randint(1, 6)
      if teatro.num_boletos[pelicula[0]]:
        env.process(self.ventaBoletos(env, num_boletos, pelicula[0], teatro))

  def proceso_reloj(self,env):
    while True:
      yield env.timeout(0.001)        
      self.canvas.delete(self.tiempo)
      self.tiempo=self.canvas.create_text(1000, 900, text="Minutos Desde lanzamiento: "+str(round(env.now,1)), fill="black", font=('Helvetica 20 bold'))
      self.canvas.update()
  ############################Graficas de resultados de boletos####################
  def graficas(self):
    listConjutoX = []
    listConjutoY = []

    listRFX = []
    listRFY = []

    listPFX = []
    listPFY = []

    for key in self.boletos:
      valoresX = []
      valoresY = []
      for x in  self.boletos[key]:
        valoresX.append(x[0])
        valoresY.append(x[1])
      if(key == 'Conjuro 3'):    
        listConjutoX = valoresX
        listConjutoY = valoresY
      elif(key == 'Pulp Fictions'):
        listPFX = valoresX
        listPFY = valoresY
      elif(key == 'Rapidos y Furiosos 10'):
        listRFX = valoresX
        listRFY = valoresY
    
    plt.figure(figsize=(20,10), )
    ancho_barras = 0.80
    plt.bar(listConjutoY, listConjutoX, width=ancho_barras, align='center', label='Conjuro 3')
    plt.bar(listPFY, listPFX, width=ancho_barras, align='center', label='Pulp Fictions')
    plt.bar(listRFY, listRFX, width=ancho_barras, align='center', label='Rapidos y Furiosos 10')
    plt.legend(loc='best')
    plt.show()


  def __init__(self):    
    print('Teatro Carlos Crespi - UPS')    
    ##Generado para almacenar resultados de simulacion
    Teatro = collections.namedtuple('Teatro', 'contador, peliculas, probabilidad, num_boletos, sold_out, tiempo_agotado, num_renegados')
    ##Creando entorno de simpy
    env = simpy.Environment()
    ##Recurso contador para paliculas
    contador = simpy.Resource(env,capacity=1)
    ##Peliculas seleccionadas para simulacion
    peliculas = ['Conjuro 3', 'Rapidos y Furiosos 10', 'Pulp Fictions']
    ##Probabilidad de eleccion de cada pelicula
    probabilidad=[0.1, 0.3, 0.6]
    ##Agregamos que cada pelicula tiene una cantidad de 100 boletos
    num_boletos = {pelicula: self.NUM_BOLETO for pelicula in peliculas}
    ##Diccionario para marca de evento cuando ya no hay boletos
    sold_out = {pelicula: env.event() for pelicula in peliculas}
    ##Variable que obtiene el momento en el cual se terminan boletos
    tiempo_agotado = {pelicula: None for pelicula in peliculas}
    ##Cantidad de personas a las cuales se len niega la funcion por limite de boletos
    num_renegados = {pelicula: 0 for pelicula in peliculas}

    #Creando teatro con varibles de almacenamiento
    teatro = Teatro(contador, peliculas, probabilidad, num_boletos, sold_out, tiempo_agotado, num_renegados)
    
    env.process(self.llegadaClientes(env, teatro))
    env.process(self.proceso_reloj(env))
    env.run(until=self.TIEMPO_SIMULACION)  
    self.ventana.mainloop()

    for pelicula in peliculas:
      if teatro.sold_out[pelicula]:
        print('Pelicula: %s se agoto en el tiempo %.1f despues de salir a la venta' %(pelicula, teatro.tiempo_agotado[pelicula]))
        print('Numero de personas que salieron de la fila/renegados %s' %teatro.num_renegados[pelicula])  
    print(self.boletos)
    self.graficas()

    
if __name__ == '__main__':
  print("INICIAR SIMULACION")
  cine = Cinema()
  