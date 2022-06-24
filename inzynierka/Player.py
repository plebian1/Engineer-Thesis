import numpy as np
import time


class Player:
    def __init__(self, player_id, computer_controlled, unit_store_start, player_name):
        self.__set_id(player_id)
        self.__set_computer_controlled(computer_controlled)
        self.__set_unit_store(unit_store_start)
        self.__set_name(player_name)
        self.__set_own_turn(False)
        self.__set_controlled_nodes(4)
        self.__set_condensation(1)
        self.__set_centralization(80)
        self.__set_threshold(500)

    def __get_id(self):
        return self.__id

    def __set_id(self, player_id):
        self.__id = player_id

    id = property(__get_id, __set_id)

    def __get_unit_store(self):
        return self.__unit_store

    def __set_unit_store(self, unit_store):
        self.__unit_store = unit_store

    unit_store = property(__get_unit_store, __set_unit_store)

    def __get_computer_controlled(self):
        return self.__computer_controlled

    def __set_computer_controlled(self, computer_controlled):
        self.__computer_controlled = computer_controlled

    computer_controlled = property(__get_computer_controlled, __set_computer_controlled)

    def __get_name(self):
        return self.__name

    def __set_name(self, player_name):
        self.__name = player_name

    name = property(__get_name, __set_name)

    def __get_own_turn(self):
        return self.__own_turn

    def __set_own_turn(self, x):
        self.__own_turn = x

    own_turn = property(__get_own_turn, __set_own_turn)

    def __get_controlled_nodes(self):
        return self.__controlled_nodes

    def __set_controlled_nodes(self, nodes):
        self.__controlled_nodes = nodes

    controlled_nodes = property(__get_controlled_nodes, __set_controlled_nodes)

    # to do AI od tego momentu

    def __get_condensation(self):
        return self.__condensation

    def __set_condensation(self, condensation):
        self.__condensation = condensation

    # skupienie/zwarcie, od 1 do 100, 100 to maksymalnie skupiony (kształt kwadratu), 1 to wydłuzony ( kreska)
    condensation = property(__get_condensation, __set_condensation)

    def __get_centralization(self):
        return self.__centralization

    def __set_centralization(self, centralization):
        self.__centralization = centralization

    # centralizacja, przy 100 priorytezuje punkty centralne, przy 1 bandowe
    centralization = property(__get_centralization, __set_centralization)

    def __get_threshold(self):
        return self.__threshold

    def __set_threshold(self, threshold):
        self.__threshold = threshold

    # centralizacja, przy 100 priorytezuje punkty centralne, przy 1 bandowe
    threshold = property(__get_threshold, __set_threshold)

    # na wejsciu tablica ruchow, na wyjsciu tablica z wynikiem przypisanym do kazdego ruchu
    def evaluate_condensation(self,move_table,owned_nodes, game_tree, neighbours_list, full_neighbours_list,all_nodes):
        eval_move_table = []
        scores = []
        for single_node_moves in move_table:
            for move in single_node_moves:  # move to obiekt klasy node
                neighbours_amount = len(game_tree.Adjacency_list[move.id])
                player_neighbours_amount = 0
                # policz ile ma sasiadow aktualnego gracza
                for node in all_nodes:
                    if node.id in game_tree.Adjacency_list[move.id]:  # jezeli jest sasiadem tego punktu
                        if node.owner_id == self.id:
                            player_neighbours_amount += 1
                # policz ile ma innych sasiadow
                other_neighbours_amount = neighbours_amount - player_neighbours_amount

                scores.append(other_neighbours_amount - player_neighbours_amount)  # maksymalnie 4, minimalnie -6
        delta = 10
        # przejscie na skale 0 do 100, 100 to najbardziej skondensowany, czyli najmniejszy wynik
        for score in scores:
            score += 6
            score = (delta - score) / delta * 100
            final_eval = ((self.condensation - 50) * (score - 50)) / 50 + 50
            eval_move_table.append(final_eval + 1)
        return eval_move_table

    def evaluate_centralization(self, move_table, owned_nodes, game_tree):
        # maksymalny score dla miejsc nodow centralnych czyli dla 8x12 to bedzie (3,5) (3,6), (4,5), (4,6)
        # do zapisu wynikow
        eval_move_table = []
        x_len = game_tree.columns
        y_len = game_tree.rows
        x_centre = float(x_len / 2) - 0.5  # centralny punkt poziomo
        y_centre = float(y_len / 2) - 0.5  # centralny punkt pionowo
        max_length = float((x_len + y_len) / 2)  # maksymalna odleglosc od srodka
        for single_node_moves in move_table:
            for move in single_node_moves:  # move to obiekt klasy node
                move_cords = move.manhattan_pos(game_tree)
                score = manhattan_score([y_centre, x_centre], move_cords)  # i mniej tym bardziej centralne
                score_adjusted = (
                                             max_length - score) / max_length * 100  # im wiecej tym bardziej centralne, od 0 do 100

                final_eval = ((self.centralization - 50) * (score_adjusted - 50)) / 50 + 50
                eval_move_table.append(final_eval + 1)
        return eval_move_table

    def evaluate_attack(self, move_table, owned_nodes, game_tree):
        eval_move_table = []
        node_iterator = 0
        for single_node_moves in move_table:
            for move in single_node_moves:  # move to obiekt klasy node
                if owned_nodes[node_iterator].units_amount > 1:
                    # print("node ", owned_nodes[node_iterator].id, " jednostek: " ,owned_nodes[node_iterator].units_amount)
                    attackers = owned_nodes[node_iterator].units_amount
                    if move.units_amount == 0:  # podboj bez strat
                        eval_move_table.append(1 * attackers)
                    elif owned_nodes[node_iterator].units_amount > move.units_amount + 1:  # pewny podboj, ze stratami
                        # attackers = owned_nodes[node_iterator].units_amount -1
                        defenders = move.units_amount
                        # loss =  defenders
                        # score = 1 - 0.05* defenders
                        eval_move_table.append((1 - 0.05 * defenders) * attackers)
                    elif owned_nodes[node_iterator].units_amount == move.units_amount + 1:  # 50/50
                        eval_move_table.append(0.5)
                    else:  # mniej jednostek, czyli przegrana bitwa
                        defenders = move.units_amount
                        eval_move_table.append((0.75 - 0.05 * defenders) * attackers)
                else:
                    eval_move_table.append(0)
            node_iterator += 1
        return eval_move_table

    def count_player_nodes(self, all_sprites):
        nodes_count = 0
        for s in all_sprites:
            if s.owner_id == self.id:
                nodes_count += 1
        self.controlled_nodes = nodes_count
        return nodes_count

    def count_player_score(self, all_nodes):
        score_count = 0
        for s in all_nodes:
            if s.owner_id == self.id:
                score_count += s.units_amount
        return score_count


def manhattan_score(start, end):
    x_dif = abs(start[0] - end[0])
    y_dif = abs(start[1] - end[1])
    score = x_dif + y_dif
    return score


def set_nodes_outside_score(player, owned_nodes, neighbours_list, full_neighbour_list):
    nodes_number = player.controlled_nodes
    # wyzerowanie wartosci w nodach, takie rozwiazanie wydaje sie najprostrze
    for node in owned_nodes:
        node.outside_score = 0
    for i in range(nodes_number):
        val = len(neighbours_list[i])  # przypisanie wartosci
        owned_nodes[i].outside_score = val
    run = True
    while run:
        # nie chce odrazu zmieniac pola, bo wplyneloby to na inne wyniki w tej "warstwie", wiec dodaje po przejsciu calej warstwy
        results_list = []
        id_list = []
        for i in range(nodes_number):
            if owned_nodes[i].outside_score == 0:
                score_sum = 0
                non_zeros = 0
                for node in full_neighbour_list[i]:
                    score_sum += node.outside_score
                    if node.outside_score > 0:
                        non_zeros += 1
                if non_zeros > 0:
                    results_list.append(
                        score_sum / (6 * non_zeros))  # jezeli nie jest w wartswie zewnetrznej to bedzie <0
                    id_list.append(owned_nodes[i].id)
        for node_id in id_list:
            for node in owned_nodes:
                if node.id == node_id:
                    res_id = id_list.index(node_id)
                    node.outside_score = results_list[res_id]
        # Sprawdz czy zostaly jakies zerowe
        run = False
        for node in owned_nodes:
            if node.outside_score == 0:
                run = True
                break


def count_outside_score(owned_nodes):
    score = 0
    for node in owned_nodes:
        score += node.outside_score
    return score


def get_neighbour_nodes(all_nodes, player, owned_nodes, game_tree):
    """
    Zwraca liste sasiadow dla kazdego noda kontrolowanego przez tego gracza, usuwa z listy wlasne nody tego gracza
    """

    neighbours_list = [[] for y in range(player.controlled_nodes)]
    iterator = 0
    for w in owned_nodes:
        for node in all_nodes:
            if node.id in game_tree.Adjacency_list[w.id]:
                neighbours_list[iterator].append(node)
        iterator += 1

    # usuwanie wlasnych pol
    for w in owned_nodes:
        for k in neighbours_list:
            if w in k:
                k.remove(w)

    return neighbours_list


def get_full_neighbour_nodes(all_nodes, player, owned_nodes, game_tree):
    """
    Zwraca liste sasiadow dla kazdego noda kontrolowanego przez tego gracza, wlacznie z wlasnymi polami
    """

    neighbours_list = [[] for y in range(player.controlled_nodes)]
    iterator = 0
    for w in owned_nodes:
        for node in all_nodes:
            if node.id in game_tree.Adjacency_list[w.id]:
                neighbours_list[iterator].append(node)
        iterator += 1

    return neighbours_list


def get_owned_nodes(all_nodes, player):
    owned_nodes = []
    for node in all_nodes:
        if player.id == node.owner_id:
            owned_nodes.append(node)
    return owned_nodes
