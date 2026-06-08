import csv
import time
import prettytable as pt
import colorama
from colorama import init, Fore, Back, Style

# arquivos de dados de entrada
FILE_PLAYERS = 'players.csv'
FILE_RATINGS = 'minirating.csv'
FILE_TAGS = 'tags.csv'


TAM_HASH = 12007 # 0.75 is the load factor (18944/0.75)
TAM_HASH_USER = 120011 
MIN_RATING = 0

###############################################################################
#Estrutura 1: Creating a hash table for rating.csv with the user_id as acess key
###############################################################################
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_function(self, key):
        return int(key) % self.size

    def insert(self, key, info, flag):
        index = self.hash_function(key)
        left = 0
        right = len(self.table[index]) - 1

        while left <= right:
            mid = (left + right) // 2
            if flag:
                if self.table[index][mid].user_id == key:
                    return
                elif self.table[index][mid].user_id < key:
                    left = mid + 1
                else:
                    right = mid - 1
            elif not flag:
                if self.table[index][mid].sofifa_id == key:
                    return
                elif self.table[index][mid].sofifa_id < key:
                    left = mid + 1
                else:
                    right = mid - 1

        self.table[index].insert(left, info)

    def search(self, key, flag):
        index = self.hash_function(key)
        left = 0
        right = len(self.table[index]) - 1

        while left <= right:
            mid = (left + right) // 2
            if flag:
                if self.table[index][mid].user_id == key:
                    return self.table[index][mid]
                elif self.table[index][mid].user_id < key:
                    left = mid + 1
                else:
                    right = mid - 1
            elif not flag:
                if self.table[index][mid].sofifa_id == key:
                    return self.table[index][mid]
                elif self.table[index][mid].sofifa_id < key:
                    left = mid + 1
                else:
                    right = mid - 1
        return None

    def update(self, key, info):
        index = self.hash_function(key)
        for i, item in enumerate(self.table[index]):
            if item[0] == key:
                self.table[index][i] = info
                return True
        return False

    def delete(self, key):
        index = self.hash_function(key)
        for i, item in enumerate(self.table[index]):
            if item[0] == key:
                del self.table[index][i]
                return True
        return False

class Player:
    def __init__(self, sofifa_id, short_name, long_name, player_positions, nationality, club_name, league_name):
        self.sofifa_id = sofifa_id
        self.short_name = short_name
        self.long_name = long_name
        self.player_positions = player_positions
        self.nationality = nationality
        self.club_name = club_name
        self.league_name = league_name
        self.count = 0
        self.rating = 0
class Node:
    def __init__(self, char):
        self.char = char
        self.children = [None] * 256
        self.player_ids = []
        self.is_end_of_tag = False
###############################################################################
#Estrutura 2: Radix tree implementation
###############################################################################
class RadixTree:
    def __init__(self):
        self.root = Node('')

    def insert(self, word, player_id):
        node = self.root
        for char in word:
            if node.children[ord(char)] is None:
                node.children[ord(char)] = Node(char)
            node = node.children[ord(char)]
        node.player_ids.append(player_id)
        node.is_end_of_tag = True

    def search(self, prefix):
        node = self.root
        for char in prefix:
            if node.children[ord(char)] is None:
                return []
            node = node.children[ord(char)]
        return self.get_all_ids(node)

    def get_all_ids(self, node):
        ids = []
        if node.is_end_of_tag:
            ids.extend(node.player_ids)
        for child_node in node.children:
            if child_node is not None:
                ids.extend(self.get_all_ids(child_node))
        return ids

    def print_tree(self):
        self.print_radix_tree(self.root)

    def print_radix_tree(self, node, prefix=''):
        if node is None:
            return
        print(prefix + node.char)
        for char, child_node in node.children.items():
            self.print_radix_tree(child_node, prefix + '  ')
###############################################################################
#Estrutura 3: Creating a Class for User table for rating.csv with the user_id as acess key
###############################################################################
class User:
    def __init__(self, user_id, sofifa_id, rating):
        self.user_id = user_id
        self.sofifa_ids = [sofifa_id]
        self.ratings = [rating]
    def add_rating(self, sofifa_id, rating): #dado um usuario adiciona uma sofifa_id e uma rating na sua classe
        self.sofifa_ids.insert(0,sofifa_id)
        self.ratings.insert(0,rating)
###############################################################################
#Estrutura 4 & 5: tags.csv, support to string-based query, Trie Tree
###############################################################################
class TrieNode:
    def __init__(self, char):
        self.char = char
        self.children = [None] * 256
        self.player_ids = []
        self.is_end_of_tag = False

class Trie:
    def __init__(self):
        self.root = TrieNode('')

    def insert(self, tag, player_id):
        node = self.root
        for char in tag:
            if node.children[ord(char)] is None:
                node.children[ord(char)] = TrieNode(char)
            node = node.children[ord(char)]
        node.player_ids.append(player_id)
        node.is_end_of_tag = True

    def search(self, tag):
        node = self.root
        for char in tag:
            if node.children[ord(char)] is None:
                return []
            node = node.children[ord(char)]
        return node.player_ids if node.is_end_of_tag else []
    
    def print_tree(self):
        self.print_trie(self.root)

    def print_trie(self, node, prefix=''):
        if node is None:
            return
        print(prefix + node.char)
        for caractere, child_node in enumerate(node.children):
            if child_node is not None:
                self.print_trie(child_node, prefix)
        
    def get_all_positions(self):
        return self.get_all_positions_from_node(self.root, "")

    def get_all_positions_from_node(self, node, prefix):
        positions = []
        if node.is_end_of_tag:
            positions.append(prefix)
        for caractere, child_node in enumerate(node.children):
            if child_node is not None:
                char = chr(caractere)
                positions.extend(self.get_all_positions_from_node(child_node, prefix + char))
        return positions
###############################################################################
#Pesquisa 1: Prefixos nomes dos jogadores, ordenar por rating global
###############################################################################

def quicksort(vetor, key=lambda a: a, reverse=False):
    if len(vetor) <= 1:
        return vetor
    else:
        pivot = key(vetor[len(vetor) // 2])
        left = [a for a in vetor if key(a) < pivot]
        middle = [a for a in vetor if key(a) == pivot]
        right = [a for a in vetor if key(a) > pivot]
        if reverse:
            return quicksort(right, key, reverse) + middle + quicksort(left, key, reverse)
        else:
            return quicksort(left, key, reverse) + middle + quicksort(right, key, reverse)

# Inicializa o colorama
init(autoreset=True)

# Função para aplicar cores aos cabeçalhos
def color_headers(headers, color):
    return [color + header + Style.RESET_ALL for header in headers]

# Função para aplicar cores ao texto das células
def color_text(text, color):
    return color + str(text) + Style.RESET_ALL

def quicksort(vetor, key=lambda x: x, reverse=False):
    if len(vetor) <= 1:
        return vetor
    pivot = key(vetor[len(vetor) // 2])
    left = [a for a in vetor if key(a) < pivot]
    middle = [a for a in vetor if key(a) == pivot]
    right = [a for a in vetor if key(a) > pivot]
    if reverse:
        return quicksort(right, key, reverse) + middle + quicksort(left, key, reverse)
    else:
        return quicksort(left, key, reverse) + middle + quicksort(right, key, reverse)

def encontrar_player(prefix):
    prefix = prefix.lower()
    matching_ids = radix_tree.search(prefix)
    matching_players = [players_hash.search(player_id, False) for player_id in matching_ids]
    return matching_players

def print_players(prefix, header_color=Back.CYAN, text_color=Fore.CYAN):
    sorted_players = quicksort(encontrar_player(prefix), key=lambda player: player.rating, reverse=True)
    table = pt.PrettyTable()
    headers = ["SOFIFA_ID:", "SHORT_NAME:", "LONG_NAME:", "POSITIONS:", "RATING:", "COUNT:"]
    table.field_names = color_headers(headers, header_color)
    table.align["SOFIFA_ID:"] = "c"
    table.align["SHORT_NAME:"] = "c"
    table.align["LONG_NAME:"] = "c"
    table.align["POSITIONS:"] = "c"
    table.align["RATING:"] = "c"
    table.align["COUNT:"] = "c"
    for player in sorted_players:
        table.add_row([
            color_text(player.sofifa_id, text_color),
            color_text(player.short_name, text_color),
            color_text(player.long_name, text_color),
            color_text(player.player_positions, text_color),
            color_text(player.rating, text_color),
            color_text(player.count, text_color)
        ])
    print(table)


###############################################################################
#Pesquisa 2: N, melhores jogadores de um usuário
###############################################################################

def top_players(user_id, num):
    user = user_ratings_hash.search(user_id, True)
    matching_players = [players_hash.search(player_id, False) for player_id in user.sofifa_ids]
    sorted_players = quicksort(matching_players, key=lambda player: (user.ratings[user.sofifa_ids.index(player.sofifa_id)], player.rating), reverse=True)[:num]
    table = pt.PrettyTable()
    headers = ["SOFIFA_ID:", "SHORT_NAME:", "LONG_NAME:", "POSITIONS:", "RATING:", "COUNT:", "USER_RATING:"]
    table.field_names = color_headers(headers, Back.YELLOW)
    table.align["SOFIFA_ID:"] = "c"
    table.align["SHORT_NAME:"] = "c"
    table.align["LONG_NAME:"] = "c"
    table.align["POSITIONS:"] = "c"
    table.align["RATING:"] = "c"
    table.align["COUNT:"] = "c"
    table.align["USER_RATING:"] = "c"
    for player in sorted_players:
        table.add_row([
            color_text(player.sofifa_id, Fore.YELLOW),
            color_text(player.short_name, Fore.YELLOW),
            color_text(player.long_name, Fore.YELLOW),
            color_text(player.player_positions, Fore.YELLOW),
            color_text(player.rating, Fore.YELLOW),
            color_text(player.count, Fore.YELLOW),
            color_text(user.ratings[user.sofifa_ids.index(player.sofifa_id)], Fore.YELLOW)
        ])
    print(table)
###############################################################################
#Pesquisa 3: N, melhores jogadores com uma tag específica
###############################################################################

def top_players_tag(num, tag, header_color=Back.GREEN, text_color=Fore.GREEN):
    tag = tag.upper()
    matching_ids = trie_position.search(tag)
    matching_players = [players_hash.search(player_id, False) for player_id in matching_ids]
    sorted_players = quicksort(matching_players, key=lambda player: player.rating, reverse=True)[:num]
    table = pt.PrettyTable()
    headers = ["SOFIFA_ID:", "SHORT_NAME:", "LONG_NAME:", "POSITIONS:", "RATING:", "COUNT:"]
    table.field_names = color_headers(headers, header_color)
    table.align["SOFIFA_ID:"] = "c"
    table.align["SHORT_NAME:"] = "c"
    table.align["LONG_NAME:"] = "c"
    table.align["POSITIONS:"] = "c"
    table.align["RATING:"] = "c"
    table.align["COUNT:"] = "c"
    for player in sorted_players:
        table.add_row([
            color_text(player.sofifa_id, text_color),
            color_text(player.short_name, text_color),
            color_text(player.long_name, text_color),
            color_text(player.player_positions, text_color),
            color_text(player.rating, text_color),
            color_text(player.count, text_color)
        ])
    print(table)

###############################################################################
#Pesquisa 4: Lista de tags, listar jogadores com intersecao de tags
###############################################################################

def get_players_with_intersection(tags):

    matching_ids = set.intersection(*[set(tag_trie.search(tag)) for tag in tags])
    players = [players_hash.search(player_id, False) for player_id in matching_ids]
    
    sorted_players = quicksort(players, key=lambda player: player.rating, reverse=True)
    table = pt.PrettyTable()
    headers = ["SOFIFA_ID:", "SHORT_NAME:", "LONG_NAME:", "POSITIONS:", "RATING:", "COUNT:"]
    table.field_names = color_headers(headers, Back.MAGENTA)
    table.align["SOFIFA_ID:"] = "c"
    table.align["SHORT_NAME:"] = "c"
    table.align["LONG_NAME:"] = "c"
    table.align["POSITIONS:"] = "c"
    table.align["RATING:"] = "c"
    table.align["COUNT:"] = "c"
    for player in sorted_players:
        table.add_row([
            color_text(player.sofifa_id, Fore.MAGENTA),
            color_text(player.short_name, Fore.MAGENTA),
            color_text(player.long_name, Fore.MAGENTA),
            color_text(player.player_positions, Fore.MAGENTA),
            color_text(player.rating, Fore.MAGENTA),
            color_text(player.count, Fore.MAGENTA)
        ])
    print(table)
    return players
###############################################################################
#Pesquisa EXTRA: Dream team, melhor jogador de cada posição
###############################################################################

def best_team():
    positions = trie_position.get_all_positions()
    dream_team = []
    all_players = []
    print("DREAM TEAM: ")
    for position in positions:
        find = True
        player_ids = trie_position.search(position)
        players = [players_hash.search(player_id, False) for player_id in player_ids]
        all_players = quicksort(players, key=lambda player: player.rating, reverse=True)
        while find and all_players:
            player = all_players.pop(0)
            if player not in dream_team:
                dream_team.append(player)
                find = False
        table = pt.PrettyTable()
        headers = ["SOFIFA_ID:", "SHORT_NAME:", "LONG_NAME:", "POSITIONS:", "NATIONALITY:", "LEAGUE_NAME:", "RATING:", "COUNT:"]
        table.field_names = color_headers(headers, Back.RED)
        table.align["SOFIFA_ID:"] = "c"
        table.align["SHORT_NAME:"] = "c"
        table.align["LONG_NAME:"] = "c"
        table.align["POSITIONS:"] = "c"
        table.align["NATIONALITY:"] = "c"
        table.align["LEAGUE_NAME:"] = "c"
        table.align["RATING:"] = "c"
        table.align["COUNT:"] = "c"
        for player in dream_team:
            table.add_row([
                color_text(player.sofifa_id, Fore.RED),
                color_text(player.short_name, Fore.RED),
                color_text(player.long_name, Fore.RED),
                color_text(player.player_positions, Fore.RED),
                color_text(player.nationality, Fore.RED),
                color_text(player.league_name, Fore.RED),
                color_text(player.rating, Fore.RED),
                color_text(player.count, Fore.RED)
            ])
    print(table)

#Pesquisa EXTRA2: Dream team, por pais pesquisado

def best_selecao(pais):
    positions = trie_position.get_all_positions()
    dream_team = []
    all_players = []
    print(f"DREAM TEAM {pais}:")
    table = pt.PrettyTable()
    headers = ["SOFIFA_ID:", "SHORT_NAME:", "LONG_NAME:", "POSITIONS:", "NATIONALITY:", "LEAGUE_NAME:", "RATING:", "COUNT:"]
    table.field_names = color_headers(headers, Back.BLUE)
    table.align["SOFIFA_ID:"] = "c"
    table.align["SHORT_NAME:"] = "c"
    table.align["LONG_NAME:"] = "c"
    table.align["POSITIONS:"] = "c"
    table.align["NATIONALITY:"] = "c"
    table.align["LEAGUE_NAME:"] = "c"
    table.align["RATING:"] = "c"
    table.align["COUNT:"] = "c"
    for position in positions:
        find = True
        player_ids = tag_trie.search(pais)
        players = [players_hash.search(player_id, False) for player_id in player_ids]
        all_players = quicksort(players, key=lambda player: player.rating, reverse=True)
        player = None
        while find and all_players:
            player = all_players.pop(0)
            if player not in dream_team:
                dream_team.append(player)
                find = False
        if player:
            table.add_row([
                color_text(player.sofifa_id, Fore.BLUE),
                color_text(player.short_name, Fore.BLUE),
                color_text(player.long_name, Fore.BLUE),
                color_text(position, Fore.BLUE),
                color_text(pais, Fore.BLUE),
                color_text(player.league_name, Fore.BLUE),
                color_text(player.rating, Fore.BLUE),
                color_text(player.count, Fore.BLUE)
            ])
    print(table)

###############################################################################

players_hash = HashTable(TAM_HASH)
radix_tree = RadixTree()
user_ratings_hash = HashTable(TAM_HASH_USER)
tag_trie = Trie()
trie_position = Trie()

###############################################################################
# Import players.csv file into a hash table and position trie
###############################################################################

print("Iniciando processamento dos dados: ")
start = time.time()

with open(FILE_PLAYERS, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        sofifa_id = int(row['sofifa_id'])
        short_name = str(row['short_name'])
        long_name = str(row['long_name'])
        player_positions = str(row['player_positions'])
        nationality = str(row['nationality'])
        club_name = str(row['club_name'])
        league_name = str(row['league_name'])

        # Adicionar cada posição do jogador na árvore trie
        positions = player_positions.split(',')
        for position in positions:
            trie_position.insert(position.strip().upper(), sofifa_id)

        player = Player(sofifa_id, short_name, long_name, player_positions, nationality, club_name, league_name)
        players_hash.insert(sofifa_id, player, False)
        lower_long_name = long_name.lower()
        radix_tree.insert(lower_long_name, sofifa_id)

end = time.time()
decorrido = end - start
print(f"Players_hash, trie_positions e Radix_tree feitos em: {decorrido:.2f} segundos")

###############################################################################
#Import tags.csv file into a tag trie and radix tree
###############################################################################


start = time.time()

with open(FILE_TAGS, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        tag = str(row['tag'])
        player_id = int(row['sofifa_id'])
        tag_trie.insert(tag, player_id)


end = time.time()
decorrido = end - start
print(f"Tag_trie em: {decorrido:.2f} segundos")

###############################################################################
#Import the rating.csv file into a hash table with user_id as the access key
###############################################################################

start = time.time()

with open(FILE_RATINGS, 'r') as RatingFile:
    rating_csv = csv.DictReader(RatingFile)

    for line in rating_csv:
        user_id = int(line["user_id"])
        sofifa_id = int(line["sofifa_id"])
        rating = float(line['rating'])

        # Check if the user_id already exists in the hash table
        existing_user = user_ratings_hash.search(user_id, flag=True)
        if existing_user:
            existing_user.add_rating(sofifa_id, rating)
        else:
            # Create a new User object and insert it into the user_ratings_hash
            user = User(user_id, sofifa_id, rating)
            user_ratings_hash.insert(user_id, user, flag=True)

        # Check if the sofifa_id exists in the players_hash
        existing_player = players_hash.search(sofifa_id, flag=False)
        if existing_player:
            existing_player.count += 1
            existing_player.rating += rating

# Calculate the average rating for each player
for bucket in players_hash.table:
    for player in bucket:
        if player.count > 0:
            player.rating /= player.count
        else:
            player.rating = 0

end = time.time()
decorrido = end - start
print(f"Rating_hash em: {decorrido:.2f} segundos\n")
print("Processamento dos dados finalizado, o que desjas fazer?\n\n")
opcao = -1
while opcao != 7:
    print("Processamento dos dados finalizado, o que desjas fazer?\n\n")
    print("1 - Prefixo dos nomes dos jogadores\n2 - N melhores jogadores de um usuário\n3 - N melhores jogadores com uma tag específica" \
    "\n4 - Lista de tags, listar jogadores com intersecao de tags\n5 - Ver Dream team\n6 - Ver o Dream Team de um país\n7 - Sair")
    opcao = int(input("Digite a opção desejada: "))
    if opcao == 7:
        print("Finalizando...")
        break
    if opcao == 1:
        # Pesquisa 1: Prefixos nomes dos jogadores, ordenar por rating global
        # "Cristiano"
        prefix = input("Digite o prefixo do nome do jogador: ")
        print_players(prefix)
    elif opcao == 2:
        # Pesquisa 2: N, melhores jogadores de um usuário
        # 108952 7
        user_id = int(input("Digite o id do usuário: "))
        num = int(input("Digite a quantidade de jogadores que deseja ver: "))
        top_players(user_id, num)
    elif opcao == 3:
        # Pesquisa 3: N, melhores jogadores com uma tag específica
        # 5 "Acrobat"
        num = int(input("Digite a quantidade de jogadores que deseja ver: "))
        tag = input("Digite a tag que deseja pesquisar: ")
        top_players_tag(num, tag)
    elif opcao == 4:
        # Pesquisa 4: Lista de tags, listar jogadores com intersecao de tags
        # "Speedster,Playmaker"
        tags = input("Digite as tags que deseja pesquisar separadas por vírgula: ")
        tags = tags.split(',')
        get_players_with_intersection(tags)
    elif opcao == 5:
        # Pesquisa 5: Ver Dream team
        best_team()
    elif opcao == 6:
        # Pesquisa 6: Ver o Dream Team de um país
        # "France"
        pais = input("Digite o país que deseja ver o dream team: ")
        best_selecao(pais)