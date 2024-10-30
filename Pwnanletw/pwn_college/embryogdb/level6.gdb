start
break *main+577
commands
    silent
    set $local_variable = *(unsigned long long*)($rbp-0x18)
    printf "Current value: %llx\n", $local_variable
    
continue
end
break *main+686
commands
    silent
    set $rdx = $local_variable
    continue
end
continue