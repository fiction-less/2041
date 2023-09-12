#!/usr/bin/python3 -u

x = "###"
while x != "########":
    y = "#"
    while y != x:
        print(y)
        y = f"{y}#"
    x = f"{x}#"

status = "off"
while status != "on":
    print(f"status is {status}")
    if status == "half on":
        status = "on"
    else:
        status = "half on"
