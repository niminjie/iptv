def dfs(matrix, p, n, connect, visited):
    if not visited[p]:
        # visit node
        connect.append(p)
        #print p
        visited[p] = True
        for i in range(1, n + 1):
            if matrix[p][i] != 0 and not visited[i]:
                dfs(matrix, i, n, connect, visited)

def find_connection(matrix):
    n = len(matrix[0]) - 1
    visited = [False for i in range(n + 1)]
    connect = []
    for i in range(1, n + 1):
        nodes = []
        dfs(matrix, i, n, nodes, visited)
        if len(nodes) != 0:
            connect.append(nodes)
    return connect

def test():
    matrix = [[0, 0, 0, 0, 0, 0],
              [0, 0, 1, 0, 0, 0],
              [0, 1, 0, 1, 1, 0],
              [0, 0, 1, 0, 0, 0],
              [0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]
    print find_connection(matrix)

if __name__ == '__main__':
    test()
