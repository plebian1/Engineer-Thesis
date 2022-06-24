import random
import time
import numpy as np
from Player import *
import pygame


def make_computer_move(player, game_tree, all_nodes):
    # policzenie kotrolowanych pol i dodanie jednostek
    player.count_player_nodes(all_nodes)
    # player.unit_store += player.controlled_nodes

    # znalezienie posiadanych nodow
    owned_nodes = get_owned_nodes(all_nodes, player)

    # znalezienie sasiedztwa wszystkich nodow tego gracza, ktore nie naleza do niego
    neighbours_list = get_neighbour_nodes(all_nodes, player, owned_nodes, game_tree)
    full_neighbours_list = get_full_neighbour_nodes(all_nodes, player, owned_nodes, game_tree)

    # rozmieszczenie jednostek, po 1 w kazdy nodzie
    # assign_units(player,owned_nodes)

    # Przesuwanie jednostek do zewnatrz wlasnych nodow

    move_friendly_units_outside(player, owned_nodes, neighbours_list, full_neighbours_list, all_nodes)

    running = True
    end = False
    while running:
        # 1. Pobierz aktualny stan
        # 2. Policz 3 wspolczynniki dla kazdego ruchu: centralizacja, kondensacja i wartosc/sens ataku
        # 3. powtarzaj do warunku stopu ( jaki warunek?, brak zmian od poprzedniej pozycji oznacza ze komputer nie znalazl zadnego dobrego ruchu), ewentualnie jakis override do tego
        # 4. po warunku stopu koniec tury, to juz jest jakby
        player.count_player_nodes(all_nodes)  # ile nodow kontroluje
        owned_nodes = get_owned_nodes(all_nodes, player)
        neighbours_list = get_neighbour_nodes(all_nodes, player, owned_nodes, game_tree)
        full_neighbours_list = get_full_neighbour_nodes(all_nodes, player, owned_nodes, game_tree)
        # wyliczanie wartosci dla ruchu
        condensation_table = player.evaluate_condensation(neighbours_list, owned_nodes, game_tree, neighbours_list,
                                                          full_neighbours_list, all_nodes)
        centralization_table = player.evaluate_centralization(neighbours_list, owned_nodes, game_tree)
        attacks_table = player.evaluate_attack(neighbours_list, owned_nodes, game_tree)
        units_backup_table = []
        for i in owned_nodes:
            units_backup_table.append(int(i.units_amount))
        moves_number = len(centralization_table)
        final_eval_table = np.zeros(moves_number)
        for i in range(moves_number):
            final_score = condensation_table[i] * centralization_table[i] * attacks_table[i]
            final_eval_table[i] = final_score
        try:
            best_move = np.argmax(final_eval_table)

            if final_eval_table[best_move] > player.threshold:
                iterator = 0
                node_iter = 0
                for one_node_neighbours in neighbours_list:
                    for node in one_node_neighbours:
                        if iterator == best_move:
                            move_units(node, owned_nodes[node_iter])
                        iterator += 1
                    node_iter += 1
        except ValueError:  # to jest koniec gry, juz nie ma mozliwych ruchow bo wszystko zajal
            running = False
            break

        player.count_player_nodes(all_nodes)  # ile nodow kontroluje

        if player.controlled_nodes == len(all_nodes):
            end = True
            running = False
            break
        new_owned_nodes = get_owned_nodes(all_nodes, player)

        if is_the_same(owned_nodes, new_owned_nodes, units_backup_table):
            # sprawdz czy nie zajal wszystkiego, jak tak to koniec gry
            if player.controlled_nodes == len(all_nodes):
                running = False
                end = True
                break

            # sprobuj przemiescic jednostki z zewnatrz

            owned_nodes = get_owned_nodes(all_nodes, player)
            neighbours_list = get_neighbour_nodes(all_nodes, player, owned_nodes, game_tree)
            full_neighbours_list = get_full_neighbour_nodes(all_nodes, player, owned_nodes, game_tree)

            move_friendly_units_outside(player, owned_nodes, neighbours_list, full_neighbours_list, all_nodes)
            if is_the_same(owned_nodes, new_owned_nodes, units_backup_table):
                running = False
                break
    if not end:
        owned_nodes = get_owned_nodes(all_nodes, player)
        neighbours_list = get_neighbour_nodes(all_nodes, player, owned_nodes, game_tree)
        full_neighbours_list = get_full_neighbour_nodes(all_nodes, player, owned_nodes, game_tree)
        player.count_player_nodes(all_nodes)
        player.unit_store += player.controlled_nodes
        # set_nodes_outside_score(player, owned_nodes, neighbours_list, full_neighbours_list)
        assign_units(player, owned_nodes, neighbours_list, full_neighbours_list)
        # move_friendly_units_outside(player, owned_nodes, neighbours_list, full_neighbours_list, all_nodes)


def move_units(final_node, previous_node):
    # prev_clicked_node to node startowy
    # final_node to node docelowy

    # jakis setup
    attackers = previous_node.units_amount - 1  # liczba atakujacych to jednostki stacjonujace - 1
    defenders = final_node.units_amount  # liczba obroncow to wszystkie jednostki stacjonujace


    if attackers > 0:
        # przemieszczenie do wlasnego pola
        if final_node.owner_id == previous_node.owner_id:
            if final_node.units_amount + attackers <=12:
                previous_node.units_amount -= attackers
                final_node.units_amount += attackers


        # przemieszczenie do przeciwnego, czyli jakas walka, moze do rozbudowania kiedys
        else:
            previous_node.units_amount -= attackers
            attack_move(final_node, previous_node, defenders, attackers)


def transport_move(final_node, attackers):
        final_node.units_amount += attackers



def attack_move(final_node, previous_node, defenders, attackers):
    result = defenders - attackers
    if result < 0:
        final_node.units_amount = abs(result)
        final_node.owner_id = previous_node.owner_id
    elif result > 0:
        final_node.units_amount = result
    else:
        rand_number = random.randint(0, 1)  # losowanie kto to zajmie, 0 stary, 1 nowy
        if rand_number == 0:
            final_node.units_amount = 1
        else:
            final_node.units_amount = 1
            final_node.owner_id = previous_node.owner_id


def add_unit(current_player, node):
    bank = current_player.unit_store
    if bank > 0 and node.units_amount < 12:
        node.units_amount += 1
        current_player.unit_store -= 1


def end_turn(cp, number_of_players):
    curr_player = (cp + 1) % number_of_players
    if curr_player == 0:
        curr_player = number_of_players

    return curr_player


def move_friendly_units_outside(player, owned_nodes, neighbours_list, full_neighbour_list, all_nodes):
    # Przypisz wartosc "zewnetrznosci" do kazdego pola, najpierw 1 za kazdy nie wlasny node sasiadujacy, pozniej idac do wenatrz score = suma niezerowych dookola /ilosc /2
    set_nodes_outside_score(player, owned_nodes, neighbours_list, full_neighbour_list)

    # przesun jednostki do zewnatrz, nie trzeba reewaluowac po ruchu, bo nie zajmujemy nowych pol

    run = True

    while run:

        units_backup_table = []
        for i in owned_nodes:
            units_backup_table.append(int(i.units_amount))

        nodes_iterator = 0
        for node in owned_nodes:
            if node.outside_score < 1 and node.units_amount > 1:  # jezeli nie jestesmy na zewnatrz i mamy co przesunac
                neighbour_scores = []  # lista wynikow, posortowac i leciec od gory

                for neighbour in full_neighbour_list[nodes_iterator]:
                    neighbour_scores.append([neighbour.outside_score,
                                             neighbour])  # troche dziwnie to wyglada, ale nie chce tego sortowac na oryginalnej liscie

                neighbour_scores.sort(key=lambda row: (row[0]), reverse=True)

                for neighbour in neighbour_scores:
                    if neighbour[0] > node.outside_score:  # jezeli jest bardziej na zewnatrz
                        if neighbour[
                            1].units_amount + node.units_amount - 1 <= 12:  # zeby przerzucanie jednostek nie przekroczylo 12 w jednym polu
                            move_units(neighbour[1], node)
            nodes_iterator += 1

        new_owned_nodes = get_owned_nodes(all_nodes, player)

        if is_the_same(owned_nodes, new_owned_nodes, units_backup_table):
            running = False
            break


def assign_units(player, owned_nodes, neighbours_list, full_neighbour_list):
    set_nodes_outside_score(player, owned_nodes, neighbours_list, full_neighbour_list)

    rounds_iterator = 0
    while player.unit_store > 0 and rounds_iterator < 12:
        rounds_iterator += 1
        for node in owned_nodes:
            if node.outside_score >= 1:
                add_unit(player, node)

    while player.unit_store > 0:
        for w in owned_nodes:
            add_unit(player, w)
        max_counter = 0
        for i in owned_nodes:
            if i.units_amount == 12:
                max_counter += 1
        if max_counter == len(owned_nodes):
            break


"""def stop_condition_single_units(owned_nodes, neighbours_list):
    # print("     ")
    # print("start: ")
    for i in neighbours_list:
        print(len(i))
    iterator = 0
    for node in owned_nodes:
        if len(neighbours_list[iterator]) != 0:  # jezeli graniczy nie tylko z wlasnymi nodami
            # print("here")
            # print(node.units_amount)
            if node.units_amount != 1:
                return False
        iterator += 1

    return True"""


def is_the_same(owned_nodes, new_owned_nodes, units_backup_table):
    # wszystko jest takie same, jezeli nie zmienila sie przynaleznosc nodow oraz ilosc jednostek jest taka sama jak wczesniej
    iterator = 0
    length1 = len(owned_nodes)
    length2 = len(new_owned_nodes)

    if length1 != length2:  # jezeli sa roznej dlugosci to nie ma co sprawdzac
        return False

    for i in range(length1):
        if units_backup_table[i] != new_owned_nodes[i].units_amount:
            return False

    return True
