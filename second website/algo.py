def foo(page_no,limit):
    a = (page_no-1)*limit
    b = page_no*limit
    return a,b


