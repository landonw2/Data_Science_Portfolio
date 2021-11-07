# Initialize the playing board using dictionary
theBoard = {'A1': ' ' , 'B1': ' ' , 'C1': ' ' ,
            'A2': ' ' , 'B2': ' ' , 'C2': ' ' ,
            'A3': ' ' , 'B3': ' ' , 'C3': ' ' }


# Function to print 'theBoard'    
def printBoard(board):
    print(board['A1'] + '|' + board['B1'] + '|' + board['C1'])
    print('-+-+-')
    print(board['A2'] + '|' + board['B2'] + '|' + board['C2'])
    print('-+-+-')
    print(board['A3'] + '|' + board['B3'] + '|' + board['C3'])

# Initializing an indicator used to determine whose turn it is
player_indicator = 'X'

# While with logic of game implemented
while theBoard['A1'] == ' ' or theBoard['A2'] == ' ' or theBoard['A3'] == ' ' or theBoard['B1'] == ' ' or theBoard['B2'] == ' ' or theBoard['B3'] == ' ' or theBoard['C1'] == ' ' or theBoard['B3'] == ' ' or theBoard['C3'] == ' ':

    # Empty board is printed
    printBoard(theBoard)
    
    # Player is prompted to choose a position with Input function
    placement = str(input("Please choose a position player " + str(player_indicator) + ": ")) 
    
    # Conditional that requires the space on board to be empty
    if placement in theBoard:

        if theBoard[placement] == ' ':
            
            # Places the player indicator in the dictionary (theBoard)
            theBoard[placement] = player_indicator
            
            # If/else used to switch the player
            if player_indicator == 'X':
                player_indicator = 'O'
            else: player_indicator = 'X'
        else:
            
            # If the space is not empty, then someone already played there
            print("\nInvalid selection - someone already played there. Please try again.\n")
            continue
        
        # If statement to determine if a player wins (specifically looking at top row)
        if theBoard['A1'] == theBoard['B1'] == theBoard['C1']:
            
            # If statement to determine any empty spaces (specifically looking at top row)
            if theBoard['A1'] != ' ' or theBoard['B1'] != ' ' or theBoard['C1'] != ' ':
                
                # If there are empty spaces, then the turn switches
                if player_indicator == 'X':
                    player_indicator = 'O'
                else: player_indicator = 'X'
                printBoard(theBoard)
                print("\nPlayer " + str(player_indicator) + " wins!\n")
                break
        
        # Same thing as above but for first column
        elif theBoard['A1'] == theBoard['A2'] == theBoard['A3']:
            if theBoard['A2'] != ' ' or theBoard['B2'] != ' ' or theBoard['C2'] != ' ':
                if player_indicator == 'X':
                    player_indicator = 'O'
                else: player_indicator = 'X'
                printBoard(theBoard)
                print("\nPlayer " + str(player_indicator) + " wins!\n")
                break
            
        # Same thing as above but for second row
        elif theBoard['A2'] == theBoard['B2'] == theBoard['C2']:
            if theBoard['A2'] != ' ' or theBoard['B2'] != ' ' or theBoard['C2'] != ' ':
                if player_indicator == 'X':
                    player_indicator = 'O'
                else: player_indicator = 'X'
                printBoard(theBoard)
                print("\nPlayer " + str(player_indicator) + " wins!\n")
                break
        
        # Same thing as above but for third row
        elif theBoard['A3'] == theBoard['B3'] == theBoard['C3']:
            if theBoard['A3'] != ' ' or theBoard['B3'] != ' ' or theBoard['C3'] != ' ':
                if player_indicator == 'X':
                    player_indicator = 'O'
                else: player_indicator = 'X'
                printBoard(theBoard)
                print("\nPlayer " + str(player_indicator) + " wins!\n")
                break
        
        # Same thing as above but for top left to bottom right diagonal
        elif theBoard['A1'] == theBoard['B2'] == theBoard['C3']:
            if theBoard['A1'] != ' ' or theBoard['B2'] != ' ' or theBoard['C3'] != ' ':
                if player_indicator == 'X':
                    player_indicator = 'O'
                else: player_indicator = 'X'
                printBoard(theBoard)
                print("\nPlayer " + str(player_indicator) + " wins!\n")
                break
        
        # Same thing as above but for top right to bottom left diagonal
        elif theBoard['A3'] == theBoard['B2'] == theBoard['C1']:
            if theBoard['A3'] != ' ' or theBoard['B2'] != ' ' or theBoard['C1'] != ' ':
                if player_indicator == 'X':
                    player_indicator = 'O'
                else: player_indicator = 'X'
                printBoard(theBoard)
                print("\nPlayer " + str(player_indicator) + " wins!\n")
                break
        # Same thing as above but for second column    
        elif theBoard['B1'] == theBoard['B2'] == theBoard['B3']:
             if theBoard['B1'] != ' ' or theBoard['B2'] != ' ' or theBoard['B3'] != ' ':
                if player_indicator == 'X':
                    player_indicator = 'O'
                else: player_indicator = 'X'
                printBoard(theBoard)
                print("\nPlayer " + str(player_indicator) + " wins!\n")
                break
        # Same thing as above but for third column   
        elif theBoard['C1'] == theBoard['C2'] == theBoard['C3']:
            if theBoard['C1'] != ' ' or theBoard['C2'] != ' ' or theBoard['C3'] != ' ':
                if player_indicator == 'X':
                    player_indicator = 'O'
                else: player_indicator = 'X'
                printBoard(theBoard)
                print("\nPlayer " + str(player_indicator) + " wins!\n")
                break
            
        # Checking for a tie   
        if theBoard['A1'] != ' ' and theBoard['A2'] != ' ' and theBoard['A3'] != ' ' and theBoard['B1'] != ' ' and theBoard['B2'] != ' ' and theBoard['B3'] != ' ' and theBoard['C1'] != ' ' and theBoard['B3'] != ' ' and theBoard['C3'] != ' ':
            printBoard(theBoard)
            print("\nIt's a tie...\n")
            break
        
    # Check if the player needs to capitalize          
    else:
        if placement == 'a1' or placement == 'a2' or placement == 'a3' or placement == 'b1' or placement == 'b2' or placement == 'b3' or placement == 'c1' or placement == 'c2' or placement == 'c3':
            print('\nInvalid selection - please capitalize. Try again.\n' )
            continue
        
        # If none of the above, then it was an invalid selection thta does not exist
        else: 
            print('\nInvalid selection - ' + str(placement) + ' does not exist. Try again.\n')
            continue    