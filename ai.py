import g4f

def ai(text):
    r = g4f.ChatCompletion.create(
    model=g4f.models.default,
    messages=[{"role": "user", 
               "content": text}],
    provider=g4f.Provider.ChatgptNext,
    )
    return r