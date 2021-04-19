# Write your code here
from itertools import combinations_with_replacement, chain
from random import shuffle, randint


def doubles(domino_set):
    return [double for double in domino_set if double[0] == double[-1]]


class DominoGame:
    def __init__(self):
        first_double = ''
        self.snake = []
        self.game_end = False
        # generate a set with at least one double
        while not first_double:
            self.full_set = list(list(domino) for domino in combinations_with_replacement(range(7), 2))
            shuffle(self.full_set)
            self.computer_set = self.full_set[:7]
            self.player_set = self.full_set[7:14]
            self.stock_set = self.full_set[14:]
            doubles_computer = doubles(self.computer_set)
            doubles_player = doubles(self.player_set)
            if doubles_player or doubles_computer:
                first_double = sorted(chain(doubles_player, doubles_computer))[-1]
        # pop the highest double from one of the players and start the snake
        if first_double in self.player_set:
            i_start = self.player_set.index(first_double)
            self.snake.append(self.player_set.pop(i_start))
            self.status = 'computer'
        else:
            i_start = self.computer_set.index(first_double)
            self.snake.append(self.computer_set.pop(i_start))
            self.status = 'player'

    def print_snake(self):
        out, front, back = '', '', ''
        if len(self.snake) < 7:
            for item in self.snake:
                out += str(item)
        else:
            for k in range(3):
                front += str(self.snake[k])
                back += str(self.snake[k - 3])
                out = front + '...' + back
        print(out + '\n')

    def grow_snake(self, domino, coll):
        if domino < 0:
            piece = coll.pop(-domino - 1)
            if piece[-1] == self.snake[0][0]:
                self.snake.insert(0, piece)
            else:
                piece.reverse()
                self.snake.insert(0, piece)
        elif domino > 0:
            piece = coll.pop(domino - 1)
            if piece[0] == self.snake[-1][-1]:
                self.snake.append(piece)
            else:
                piece.reverse()
                self.snake.append(piece)

    def get_from_stock(self, coll):
        coll.append(self.stock_set.pop())

    def display_status(self):
        header = '=' * 70
        print(header)
        print(f'''Stock size: {len(self.stock_set)}
Computer pieces: {len(self.computer_set)}
''')
        # print(f'{self.snake[0]}\n')
        self.print_snake()
        print(f'Your pieces:')
        for i, piece in enumerate(self.player_set, start=1):
            print(f'{i}:{piece}')
        print('')

    def player_move(self):
        domino = 0
        # Get a valid input
        choice = input("Status: It's your turn to make a move. Enter your command.\n")
        while True:
            if ((choice[0] == '-' and choice[1:].isdigit()) or choice.isdigit()) \
                    and abs(int(choice)) <= len(self.player_set):
                domino = int(choice)
                if self.is_legal_move(domino, self.player_set):
                    break
                else:
                    choice = input('Illegal move. Please try again.\n')
            else:
                choice = input('Invalid input. Please try again.\n')
        if domino == 0:
            self.get_from_stock(self.player_set)
        else:
            self.grow_snake(domino, self.player_set)

    def computer_move(self):
        domino = 0
        self.computer_set = self.rank_pieces(self.computer_set)
        for i in range(1, len(self.computer_set) + 1):
            # domino = randint(-len(self.computer_set), len(self.computer_set))
            domino = i
            if self.is_legal_move(domino, self.computer_set):
                break
            elif self.is_legal_move(-domino, self.computer_set):
                break
        # print(domino)
        if domino == 0:
            self.get_from_stock(self.computer_set)
        else:
            self.grow_snake(domino, self.computer_set)

    def make_move(self):
        if self.status == 'computer':
            key = input("Status: Computer is about to make a move. Press Enter to continue...\n")
            self.computer_move()
            self.status = 'player'
        else:
            self.player_move()
            self.status = 'computer'

    def is_legal_move(self, domino, coll):
        if domino == 0:
            return True
        elif domino > 0:
            if self.snake[-1][-1] in coll[domino - 1]:
                return True
            else:
                return False
        else:
            if self.snake[0][0] in coll[-domino - 1]:
                return True
            else:
                return False

    def is_draw(self):
        first = self.snake[0][0]
        last = self.snake[-1][-1]
        count = 0
        if first == last:
            for piece in self.snake:
                if first in piece:
                    count += 1
        if count == 8:
            return True
        else:
            return False

    def get_count(self, coll):
        count = dict.fromkeys(range(7), 0)
        for piece in chain(coll, self.snake):
            for num in piece:
                count[num] += 1
        return count

    def rank_pieces(self, coll):
        count = self.get_count(coll)
        ranked_coll = [[x, count[x[0]] + count[x[1]]] for x in coll]
        ranked_coll = sorted(ranked_coll, key=lambda piece: piece[-1], reverse=True)
        return [x[0] for x in ranked_coll]


    def is_end(self):
        # print(self.player_set)
        if not self.player_set:
            self.display_status()
            print("Status: The game is over. You won!")
            self.game_end = True
        elif not self.computer_set:
            self.display_status()
            print("Status: The game is over. The computer won!")
            self.game_end = True
        elif self.is_draw() or not self.stock_set:
            self.display_status()
            print("Status: The game is over. It's a draw!")
            self.game_end = True
        else:
            self.game_end = False


# Start Game
new_game = DominoGame()
while not new_game.game_end:
    new_game.display_status()
    new_game.make_move()
    # print(len(new_game.snake))
    new_game.is_end()












