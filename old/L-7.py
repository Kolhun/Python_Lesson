x = 38

print('hi')
if x < 0:
    print('minus zero')
print('bye')

a, b = 10, 5

if a > b:
    print('a > b')

if a > b and a > 0:
    print('ok')

if (a > b) and (a > 0 or b < 1000):
    print('ok')

if 5 < b and b < 10:
    print('ok')

if '34' > '12':
    print('ok')

if '123' > '12':
    print('ok')

if [1, 2] > [1, 1]:
    print('ok')

if '6' > 5:
    print('ok')

if [5, 6] > 5:
    print('ok')

if "6" != 5:
    print('ok')