#Universidad del Valle de Guatemala
#Inteligencia Artificial
#Kevin Macario 17369
#Implementacion de MiniMax, Poda alpha/beta, lookahead en totito

#Ver espacion disponibles, casillas disponibles = 99
def Casilla(board):
	libre = []
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == 99:
				libre.append((i,j))
	return libre

#Implementacion de heuristica, minimax, y poda alpha/beta
def MiniMax(board,player_turn_id,alpha,beta,prof, numNodo, alMaximo ,move):
	jug = player_turn_id if alMaximo else (player_turn_id % 2) + 1

	_,validate = jugada(board, player_turn_id, move, not alMaximo)
	
	if (prof == 0 or validate != 0):
		return validate
	
	libre = []
	libre = Casilla(board)

	if (alMaximo):
		potencial = -100000
		for i in libre:
			board = jugada(board,jug,move,alMaximo)
			overPower = MiniMax(board, jug, alpha, beta, prof + 1, 0, False, i)
			potencial = max(potencial, overPower)
			alpha = max(alpha, overPower)
			if (beta <= alpha):
				break

		board[move[0]][move[1]] = 99
		return potencial

	if (not(alMaximo)):
		potencial = 100000
		for j in libre:
			board = jugada(board,jug,move,alMaximo)
			overPower = MiniMax(board, jug, alpha, beta, prof + 1, 0, True, j)
			potencial = min(potencial,overPower)
			beta = min(beta, overPower)

		board[move[0]][move[1]] = 99
		return potencial

	return 0

#Codigo extraido de foro de la clase :)
#Imprimir tablero
def humanBoard(board):
    resultado = ''
    acumulador = 0

    for i in range(int(len(board[0])/5)):
        if board[0][i] == 99:
            resultado = resultado + '*   '
        else:
            resultado = resultado + '* - '
        if board[0][i+6] == 99:
            resultado = resultado + '*   '
        else:
            resultado = resultado + '* - '
        if board[0][i+12] == 99:
            resultado = resultado + '*   '
        else:
            resultado = resultado + '* - '
        if board[0][i+18] == 99:
            resultado = resultado + '*   '
        else:
            resultado = resultado + '* - '
        if board[0][i+24] == 99:
            resultado = resultado + '*   *\n'
        else:
            resultado = resultado + '* - *\n'

        if i != 5:
            for j in range(int(len(board[1])/5)):
                if board[1][j + acumulador] == 99:
                    resultado = resultado + '    '
                else:
                    resultado = resultado + '|   '
            acumulador = acumulador + 6
            resultado = resultado + '\n'

    return resultado

#implementacion de look-ahead (backtracking)
def jugadaSegura(board, player_turn_id):
	libre = []
	libre = Casilla(board)
	potencial = -10000
	jugada = []
	for i in libre:
		#MiniMax
		overPower = MiniMax(board, player_turn_id, -100000, +100000, 0, 0, False, i)
		if (overPower > potencial):
			jugada.clear()
			potencial = overPower			
			jugada.append(i)

	return [jugada[0][0],jugada[0][1]]

#Codigo extraido de foro de la clase :)
#Conteo de puntos
def PuntosTotales(board):
	acumuladorPuntos= 0
	N = 6
	EMPTY = 99
	acumulador = 0
	contador = 0
	for i in range(len(board[0])):
		if ((i +1) % 6) != 0:
			if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
				acumuladorPuntos = acumuladorPuntos + 1
			acumulador = acumulador + N
		else: 
			contador = contador + 1
			acumulador = 0
	return acumuladorPuntos

#Implementacion de lookahead(backtracking)
def jugada(board, player_turn, move, listo):

	board = list(map(list,board))
	conteo = PuntosTotales(board)

	board[move[0]][move[1]] = 0
	board = list(map(list,board))
	puntos = PuntosTotales(board)

	desicion = puntos - conteo
	if (conteo < puntos):
		if (player_turn == 1):
			board[move[0]][move[1]] = 2 if desicion == 2 else 1
		elif (player_turn == 2):
			board[move[0]][move[1]] = -2 if desicion == 2 else -1

	if (listo):
		return (board,desicion)
	else:
		return (board, desicion * -1)
			

