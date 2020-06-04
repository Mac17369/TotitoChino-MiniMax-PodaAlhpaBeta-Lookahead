#Universidad del Valle de Guatemala
#Inteligencia Artificial
#Kevin Macario 17369
#Implementacion de MiniMax, Poda alpha/beta, lookahead en totito
#
import socketio
from TotitoMacFun import *

#Direccion
host_address = 'localhost'
port_address = '5000'
address = 'http://' + host_address + ':' + port_address
idTorneo = 123456

gan = 0
per = 0

#Conexion
socket = socketio.Client()
socket.connect(address)

#Conexion
@socket.on('connect')
def on_connect():
	print('Conectando a servidor...')
	socket.emit('signin',
		{
			'user_name': 'Kevin Macario',
        	'tournament_id': idTorneo,
        	'user_role': 'player'
		}
	)
	print('Conexion exitosa...\n')


#Listo para jugar
@socket.on('ready')
def on_ready(data):
	print("Listo para jugar, esganando movida de oponente... \n")
	print(humanBoard(data['board']))

	movement = jugadaSegura(data["board"],data["player_turn_id"])

	socket.emit('play', 
		{	
			'tournament_id': idTorneo,
			'player_turn_id': data['player_turn_id'],
			'game_id': data['game_id'],
			'movement': movement
        }
    )

#Partida concluida
@socket.on('finish')
def finish(data): 

	global gan
	global per

	if (data['player_turn_id'] == data ['winner_turn_id']):
		print("Ganaste :) \n")
		gan = gan + 1
	else:
		print("gandiste :( \n")
		per = per + 1
	
	games_counter=per + gan
	print('Juego ', games_counter, 'concluido')
	print('Resumen de torneo:')
	print('Partidas gandas :) : ', gan)
	print('Partidas gandidas :( :', per)

	socket.emit('player_ready', 
		{
        	"tournament_id":idTorneo,
        	"game_id":data['game_id'],
        	"player_turn_id":data['player_turn_id']
        }
    )
	print('Partida terminada, esganando nueva partida...')
