from app import app, db, Question

with app.app_context():
    # Crea il database e le tabelle
    db.create_all()

    # Domande iniziali
    domande = [
        Question(text="colore preferito?", options="rosso;rosa;blu;viola", answer="rosa"),
        Question(text="città preferita?", options="boston;new york;barcellona;mykonos", answer="barcellona"),
        Question(text="cibo preferito?", options="pizza;spaghetti alle vongole;patatine fritte;wurstel", answer="patatine fritte"),
        Question(text="chi ascolterei 24/7?", options="bad bunny;rauw alejandro;feid;ozuna", answer="bad bunny"),
    ]

    # Inserisce solo se il database è vuoto
    if Question.query.count() == 0:
        db.session.add_all(domande)
        db.session.commit()
        print("✅ Database inizializzato con domande")
    else:
        print("⚠️ Il database contiene già domande")