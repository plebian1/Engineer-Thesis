import pygame
import pygame_menu
from Node import Node
from GameTree import *
from Player import *
from moves import *
from Settings import *
import sys


import time
import csv

# kolory
global white
white = (255, 255, 255)
global black
black = (0, 0, 0)
global red
red = (255, 0, 0)
global blue
blue = (0, 0, 255)
global green
green = (0, 255, 0)
global orange
orange = (255, 165, 0)
global yellow
yellow = (255, 255, 0)
global cyan
cyan = (50, 200, 200)  # background
global magenta
magenta = (255, 0, 255)
# rozdzielczosc
global width
width = 1820
global height
height = 1000


def check_player_game_over(player, all_nodes):
    for node in all_nodes:
        if player.id == node.owner_id:  # jezeli jakikolwiek node jest kontrolowany przez gracza to nie koniec gry
            return False
    return True


def message(msg, color, surface):
    surface.fill(white)
    mesg = pygame.font.SysFont(None, 50).render(msg, True, color)
    surface.blit(mesg, [int(width / 4), int(height / 2) - 60])


def check_game_over(all_nodes):
    for node in all_nodes:
        one = node.owner_id
        break
    for node in all_nodes:
        if node.owner_id != one:
            return False

    return True


def node_from_group(id, all_sprites):
    for node in all_sprites:
        if node.id == id:
            return node


def get_board_nodes_from_file(all_sprites, file):
    with open(file)as f:
        lines = f.readlines()
    iterator = 0
    for line in lines:
        if iterator == 0:
            rows = int(line)
        elif iterator ==1:
            columns = int(line)
        elif iterator < rows*columns +2:
            one_line_split = line.split("\t")
            one_line_split[3] = one_line_split[3][0]

            all_sprites.add(
                Node(int(one_line_split[0]), int(one_line_split[1]), int(one_line_split[2]), int(one_line_split[3])))
        iterator += 1

    game_treex = GameTree(rows, columns)
    remove_start = 2+ rows * columns
    nodes_ids_list = []
    #nodes_iter =0
    for line in lines[remove_start:]:
        nodes_ids_list.append(int(line))


    nodes_list = []
    for node in all_sprites:
        if node.id in nodes_ids_list:
            nodes_list.append(node)

    for node in nodes_list:
        game_treex.remove_node(node,all_sprites)

    # usuwanie nodow, da sie to zrobic lepiej
    # single_node = node_from_group(27,all_sprites)
    # game_treex.remove_node(single_node,all_sprites)

    return game_treex

def zasady(surface):
    petla = True
    while petla:
        surface.fill(orange)
        tekst = pygame.font.SysFont(None, 40).render(("Celem gry jest zajęcie całej planszy"), True, black)
        surface.blit(tekst, [100, 20])
        tekst = pygame.font.SysFont(None, 40).render(("Gra posiada faze ruchu i poruszania jednostek"), True, black)
        surface.blit(tekst, [100, 60])
        tekst = pygame.font.SysFont(None, 40).render(("Gracz kontroluje czarne pola "), True, black)
        surface.blit(tekst, [100, 100])
        tekst = pygame.font.SysFont(None, 40).render(("Gra zaczyna się w fazie ruchu, spacja przechodzi do drugiej fazy"), True, black)
        surface.blit(tekst, [100, 140])
        tekst = pygame.font.SysFont(None, 40).render(("W drugiej fazie spacja konczy ture"), True, black)
        surface.blit(tekst, [100, 180])
        tekst = pygame.font.SysFont(None, 40).render(("W fazie ruchu z posiadanego pola z wiecej niż 1 jednostką można przesuwać jednostki obok"), True, black)
        surface.blit(tekst, [100, 220])
        tekst = pygame.font.SysFont(None, 40).render(("Na polu jest maksymalnie 12 jednostek"), True, black)
        surface.blit(tekst, [100, 260])
        tekst = pygame.font.SysFont(None, 40).render(("W fazie rozstawiania kliknięcie na zaznaczone pole powoduje dodanie jednostki "), True, black)
        surface.blit(tekst, [100, 300])
        tekst = pygame.font.SysFont(None, 40).render(("Jednostki można też dodawać poprzez kilknięcie A co doda 1 jednostke, i klikniecie M co doda maksymalna liczbe jednostek"), True, black)
        surface.blit(tekst, [100, 340])
        tekst = pygame.font.SysFont(None, 40).render(("Escape kończy grę i cofa do menu"), True, black)
        surface.blit(tekst, [100, 380])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    petla = False
        pygame.display.update()
    pass




def run():
    random.seed()
    # ekran i fps
    FPS = 30
    # pygame init
    pygame.init()
    clock = pygame.time.Clock()
    surface = pygame.display.set_mode((width, height))
    all_sprites = pygame.sprite.Group()

    # menu
    menu = pygame_menu.Menu('Welcome', 1200, 900, theme=pygame_menu.themes.THEME_ORANGE)
    global settings
    settings = Settings()
    menu.add.button('Graj', lambda: start_the_game(clock, FPS, players_list, surface, number_of_players))
    menu.add.text_input('Nazwa :', default='Student')
    menu.add.button('Zasady gry', lambda:zasady(surface))
    menu.add.selector('Map :', [('Duża', 1), ('Mała', 2), ('Brakujące pola',3)], onchange=set_difficulty)
    menu.add.button('Wyjście', pygame_menu.events.EXIT)


    # to nie jest do ustawiania w ramach ustawien xD
    """condesation_test_table = [[50, 50, 50, 100], [50, 50, 50, 100],[50, 50, 50, 100],[50, 50, 50, 100],
                              [50, 50, 50, 75],[50, 50, 50, 75],[50, 50, 50, 75],[50, 50, 50, 75],
                              [50, 50, 50, 50],[50, 50, 50, 50],[50, 50, 50, 50],[50, 50, 50, 50]]

    centralization_test_table = [[50, 50, 50, 1], [50,50, 50, 20], [50, 50, 50, 35],[50, 50, 50, 50],
                                 [50, 50, 50, 1], [50,50, 50, 20], [50, 50, 50, 35],[50, 50, 50, 50],
                                 [50, 50, 50, 1], [50,50, 50, 20], [50, 50, 50, 35],[50, 50, 50, 50]]

    threshold_test_table = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                            [0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],
                            [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]"""

    final_score_tab = []
    final_score_tab.append(['kondensacja', 'centralizacja', 'chec ataku', '1','2','3'])
    # to do testow
    for j in range(1):
        number_of_players = 4
        starting_units = 0
        players_list = []
        #condensation = condesation_test_table[j]
        #centralization = centralization_test_table[j]
        #threshold = threshold_test_table[j]

        for i in range(number_of_players):
            players_list.append(Player(i + 1, True, starting_units, "gracz " + str(i + 1)))

        for i in range(number_of_players):
            players_list[i].centralization = random.randint(1,60)
            players_list[i].condensation = random.randint(50,90)
            players_list[i].threshold = 0
            #players_list[i].unit_store -= int(1 * (number_of_players - 1 - i))
        # pierwszy gracz to czlowiek
        players_list[0].computer_controlled = False
        menu.mainloop(surface)
        game_score = start_the_game(clock, FPS, players_list, surface, number_of_players)

        for s in range(4):
            final_score_tab.append([])
            final_score_tab[s + 4 * j +1].extend([players_list[s].condensation, players_list[s].centralization,0])
            final_score_tab[s + 4 * j +1].extend(game_score[s])
    #print(final_score_tab)
    #print(final_score_tab[1])
    #print(final_score_tab[1][1])

    with open('results.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows((final_score_tab))

def set_difficulty(value, size):
    if size == 1:
        settings.map = 'planszatxt2.txt'
    elif size == 2:
        settings.map = 'planszatxt.txt'
    elif size == 3:
        settings.map = 'planszatxtmissingnodes.txt'
    pass


def start_the_game(clock, FPS, players_list, surface, number_of_players):
    single_game_score = [[] for y in range(4)]

    all_sprites = pygame.sprite.Group()
    game_over_text = pygame.font.SysFont(None, 180).render("GAME OVER", True, orange)
    game_over_text2 = pygame.font.SysFont(None, 180).render(" ", True, orange)
    gameover = False
    turn = 0
    current_player = 1
    move_mode = True

    game_map = settings.map
    game_tree = get_board_nodes_from_file(all_sprites, game_map)

    # wyzerowanie startowych jednostek, bo jak sie uruchamia poraz drugi z menu, to bylo to co zostalo z poprzedniej gry
    for player in players_list:
        player.unit_store =0


    all_sprites.update()
    for s in all_sprites:
        if s.owner_id != 0:
            s.units_amount = 2

    while not gameover:
        #pygame.event.get()
        clock.tick(FPS)
        for s in all_sprites:
            prev_clicked_node = s
        # znalezienie poprzednio kliknietego noda
        # events = pygame.event.get()
        if players_list[current_player - 1].computer_controlled == False:
            for s in all_sprites:
                if s.chosen:
                    prev_clicked_node = s

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gameover = True
                    if event.key == pygame.K_m:
                        for node in all_sprites:
                            if node.chosen == True:
                                while node.units_amount < 12 and player.unit_store >0 :
                                    add_unit(player, node)
                    if event.key == pygame.K_a:
                        for node in all_sprites:
                            if node.chosen == True:
                                add_unit(player, node)
                    if event.key == pygame.K_SPACE:
                        if move_mode:
                            move_mode = False
                            player = players_list[current_player - 1]
                            player.count_player_nodes(all_sprites)
                            player.unit_store += player.controlled_nodes
                        else:
                            current_player = end_turn(current_player, number_of_players)

                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    clicked_sprites = [s for s in all_sprites if s.rect.collidepoint(pos)]

                    for node in clicked_sprites:
                        # ruch jednostek
                        if move_mode:
                            # ruch tylko jezeli poruszamy sie do sasiadujacego
                            if node.marked_neighbour:
                                # ruch tylko swoimi jednostkami
                                if current_player == prev_clicked_node.owner_id:
                                    move_units(node, prev_clicked_node)
                        # dodawanie jednostek do pola
                        else:
                            if current_player == prev_clicked_node.owner_id:
                                # jezeli drugi raz kliknelismy na to samo
                                if node.chosen:
                                    add_unit(players_list[current_player - 1], node)

                    for s in all_sprites:
                        s.clicked(False)
                        s.set_neighbour(False)
                    # clicked_sprites = [s for s in all_sprites if s.rect.collidepoint(pos)]
                    for i in clicked_sprites:
                        i.clicked(True)
                        neighbours = game_tree.Adjacency_list[i.id]

                        for node in all_sprites:
                            if node.id in neighbours:
                                node.set_neighbour(True)
        else:
            players_list[current_player - 1].count_player_nodes(all_sprites)
            if players_list[current_player - 1].controlled_nodes != 0:
                make_computer_move(players_list[current_player - 1], game_tree, all_sprites)

            current_player = end_turn(current_player, number_of_players)

            # dodawanie jednostek do gracza ludzkiego
            player = players_list[current_player - 1]
            if player.id == 1:
                for p in range(4):
                    single_game_score[p].append(players_list[p].count_player_score(all_sprites))
                turn += 1
            if player.computer_controlled == False:
                move_mode = True

        surface.fill(cyan)

        if move_mode:
            mode = "RUCH"
        else:
            mode = "ROZMIESZCZANIE"

        tryb = pygame.font.SysFont(None, 40).render("Tryb: " + mode, True, black)
        bank = pygame.font.SysFont(None, 40).render(
            "Jednostki w banku: " + str(players_list[current_player - 1].unit_store), True, black)
        tura = pygame.font.SysFont(None, 40).render("Tura: " + str(turn), True, black)
        surface.blit(tryb, [10, 970])
        surface.blit(bank, [400, 970])
        surface.blit(tura, [750, 970])
        all_sprites.update()
        all_sprites.draw(surface)
        if check_player_game_over(players_list[current_player - 1], all_sprites) and players_list[current_player - 1].computer_controlled == False:
            gameover = True
            game_over_text = pygame.font.SysFont(None, 180).render("GAME OVER", True, orange)
            game_over_text2 = pygame.font.SysFont(None, 180).render("YOU LOSE", True, orange)
            # surface.blit(game_over_text, [400, 400])
            # surface.blit(game_over_text2, [400, 600])

        if check_game_over(all_sprites):
            gameover = True
            game_over_text = pygame.font.SysFont(None, 180).render("GAME OVER", True, orange)
            game_over_text2 = pygame.font.SysFont(None, 180).render("YOU WIN", True, orange)
            # surface.blit(game_over_text, [400, 400])
            # surface.blit(game_over_text2, [400, 600])
        # Update the display
        pygame.display.flip()
        # time.sleep(0.2)
    time.sleep(1)
    surface.fill(cyan)
    surface.blit(game_over_text, [600, 300])
    surface.blit(game_over_text2, [600, 500])
    pygame.display.update()
    time.sleep(4)
    return single_game_score

