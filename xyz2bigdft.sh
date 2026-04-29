#!/bin/bash

input="$1"

# controlla che il file esista
if [ ! -f "$input" ]; then
    echo "Error: file '$input' not found"
    exit 1
fi

# file temporaneo
tmpfile=$(mktemp)

# prima riga modificata
head -n 1 "$input" | awk '{print $1, "angstroemd0"}' > "$tmpfile"

# seconda riga
echo "free" >> "$tmpfile"

# resto del file
tail -n +3 "$input" >> "$tmpfile"

# sovrascrive il file originale
mv "$tmpfile" "$input"

echo "$input is converted "
