def F(n):
  if n < 8:
    F(n + 3)
    F(2 * n)
    print(n)

F(1)