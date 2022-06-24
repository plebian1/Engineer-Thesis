
class GameTree:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.Adjacency_list = [[] for y in range(self.rows*self.columns)]
        node_counter = 0

        #pierwszy node
        self.Adjacency_list[0].append(1)
        self.Adjacency_list[0].append(self.columns)
        node_counter +=1
        # pierwsza linia bez ostatniego
        for i in range(self.columns-2):
            self.Adjacency_list[node_counter].append(i+1 + 1)  # dodaj po prawej
            self.Adjacency_list[node_counter].append(i+1 - 1)  # dodaj po lewej
            self.Adjacency_list[node_counter].append(i+1 + self.columns)  # dodaj po prawej u dolu
            self.Adjacency_list[node_counter].append(i+1 - 1 + self.columns)  # dodaj po lewej u dołu
            node_counter +=1
        # ostatni w pierwszej lini
        self.Adjacency_list[self.columns-1].append(self.columns-2)
        self.Adjacency_list[self.columns-1].append(2*self.columns-2)
        self.Adjacency_list[self.columns-1].append(2*self.columns-1)
        node_counter += 1
        #linie srodkowe
        row_counter = 2
        for w in range(self.rows-2):
            if row_counter % 2 ==0:
                row_adjustment = 1
            else:
                row_adjustment = 0

            for k in range(self.columns):
                if k != 0 and k!= self.columns-1:
                    self.Adjacency_list[node_counter].append(node_counter + 1)  # dodaj po prawej
                    self.Adjacency_list[node_counter].append(node_counter - 1)  # dodaj po lewej
                    self.Adjacency_list[node_counter].append(node_counter + self.columns + row_adjustment)  # dodaj po prawej u dolu
                    self.Adjacency_list[node_counter].append(node_counter - 1 + self.columns + row_adjustment)  # dodaj po lewej u dołu
                    self.Adjacency_list[node_counter].append(node_counter - self.columns + row_adjustment)  # dodaj po prawej u gory
                    self.Adjacency_list[node_counter].append(node_counter -1 -  self.columns + row_adjustment)  # dodaj po lewej u gory
                elif k ==0:
                    if row_adjustment == 1:
                        self.Adjacency_list[node_counter].append(node_counter - 1 + self.columns + row_adjustment)  # dodaj po lewej u dołu
                        self.Adjacency_list[node_counter].append(node_counter - 1 - self.columns + row_adjustment)  # dodaj po lewej u gory
                    self.Adjacency_list[node_counter].append(node_counter + 1)  # dodaj po prawej
                    self.Adjacency_list[node_counter].append(node_counter + self.columns + row_adjustment)  # dodaj po prawej u dolu
                    self.Adjacency_list[node_counter].append(node_counter - self.columns + row_adjustment)  # dodaj po prawej u gory
                else:
                    if row_adjustment == 0 :
                        self.Adjacency_list[node_counter].append(node_counter + self.columns + row_adjustment)  # dodaj po prawej u dolu
                        self.Adjacency_list[node_counter].append(node_counter - self.columns + row_adjustment)  # dodaj po prawej u gory
                    self.Adjacency_list[node_counter].append(node_counter - 1)  # dodaj po lewej
                    self.Adjacency_list[node_counter].append(node_counter - 1 + self.columns + row_adjustment)  # dodaj po lewej u dołu
                    self.Adjacency_list[node_counter].append(node_counter - 1 - self.columns + row_adjustment)  # dodaj po lewej u gory
                node_counter +=1
            row_counter +=1

        # ostatni rzad
        row_adjustment =(self.rows + 1 ) %2
        for k in range(self.columns):
            if k != 0 and k != self.columns-1:
                self.Adjacency_list[node_counter].append(node_counter + 1)  # dodaj po prawej
                self.Adjacency_list[node_counter].append(node_counter - 1)  # dodaj po lewej
                self.Adjacency_list[node_counter].append(node_counter - self.columns + row_adjustment)  # dodaj po prawej u gory
                self.Adjacency_list[node_counter].append(node_counter - 1 - self.columns + row_adjustment)  # dodaj po lewej u gory
            elif k == 0:
                self.Adjacency_list[node_counter].append(node_counter + 1)  # dodaj po prawej
                self.Adjacency_list[node_counter].append(node_counter - self.columns + row_adjustment)  # dodaj po prawej u gory
                self.Adjacency_list[node_counter].append(node_counter - 1 - self.columns + row_adjustment)  # dodaj po lewej u gory
            else:
                self.Adjacency_list[node_counter].append(node_counter - 1)  # dodaj po lewej
                self.Adjacency_list[node_counter].append(node_counter - 1 - self.columns + row_adjustment)  # dodaj po lewej u gory
            node_counter += 1


    def remove_node(self,node, all_nodes):
        id = node.id
        for list in self.Adjacency_list:
            for i in list:
                if i == id:
                    list.remove(i)
        del self.Adjacency_list[id]
        all_nodes.remove(node)

        for i in all_nodes:
            if i.id > id:
                i.adjust_id()

        for w in range(len(self.Adjacency_list)):
            for k in range(len(self.Adjacency_list[w])):
                if self.Adjacency_list[w][k] > id:
                    self.Adjacency_list[w][k] -= 1










