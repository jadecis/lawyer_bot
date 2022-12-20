from loader import db 


filtres={
    'special' : 9, 
    'counrty' : ["'USA'", "'RUS'"]}

print(db.get_emigrants_by(
    filtres
))