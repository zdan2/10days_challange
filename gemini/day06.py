try:
    a=input()
    b=input()
    if a.isdigit()==False or b.isdigit()==False:
        raise ValueError
    if int(b)==0:
        raise ZeroDivisionError

    print(int(a)/int(b))
except ValueError:
    print('数値以外が入力されました')
except ZeroDivisionError:
    print('0では割れません')