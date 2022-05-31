from datetime import date, timedelta

NUM_EMOJIS = {0: f"{0}\N{COMBINING ENCLOSING KEYCAP}",
              1: f"{1}\N{COMBINING ENCLOSING KEYCAP}",
              2: f"{2}\N{COMBINING ENCLOSING KEYCAP}",
              3: f"{3}\N{COMBINING ENCLOSING KEYCAP}",
              4: f"{4}\N{COMBINING ENCLOSING KEYCAP}",
              5: f"{5}\N{COMBINING ENCLOSING KEYCAP}",
              6: f"{6}\N{COMBINING ENCLOSING KEYCAP}",
              7: f"{7}\N{COMBINING ENCLOSING KEYCAP}",
              8: f"{8}\N{COMBINING ENCLOSING KEYCAP}",
              9: f"{9}\N{COMBINING ENCLOSING KEYCAP}",
              10: "\U0001F51F",
              }

TODAY = date.today()
TODAY_PLUS_THREE = TODAY + timedelta(days=3)

ROOMS = {
        107: 128080,
        108: 128209,
        110: 128210, 
        111: 128212,
        112: 128213,
        113: 128211,
        123: 128214,
        210: 128215 
        }