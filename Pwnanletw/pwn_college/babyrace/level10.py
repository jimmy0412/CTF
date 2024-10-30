# the same as level 9

## format of flag : REDACTED: \x00pwn.college{YEo2fOyvZSbBezRKzqeMNfo-kCn.QXwIDNsIDMwQzW}\n
## think race condition at local variable (len)
# 
## sequence : send_message ->  send_redacted_flag -> receive_message(before next send)