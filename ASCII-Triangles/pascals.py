# the first function is to derive the elements in each row
def rowOfTriangle(n):
    if n == 1:
        # Enter base case and remove pass
        pass
    else:
        #TODO: enter code to generate rows of pascal's triangle and remove pass
        pass
    return #enter your returned value

# the second function is to concatenate all rows together and reshape them
#Nothing to be changed in this function
def concatRows(n):
    line = []
    for j in range(1, n + 1):
        list_line = rowOfTriangle(j)
        for k in range(1, j + j - 1):
            if k % 2 != 0:
                list_line.insert(k, ' ')
        line.append([' '] * (n - j) + list_line + [' '] * (n - j))

    return line


def main():
    n=int(input("Enter the number of rows for Pascal\'s triangle:"))
    # print out each list inside a list
    for i in concatRows(n):
        for element in i:
            print(element,end=' ')
        print()

main()