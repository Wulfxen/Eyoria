from flask import Flask, render_template, request, jsonify
import re
import time
import ai
app = Flask(__name__)


def translate_to_custom_language(text, reverse=False, old=False, aien=False, dub=False):
    d_rules = {
        'Ę': 'Ґ', 'ę': 'ґ',  # Є є
        'Ĭ': 'Ї', 'ĭ': 'ї',  # Ї ї
        'Ÿ': 'Я', 'å': 'я',  # Я я
        'Ü': 'Й', 'ü': 'й',  # Й й
        'Q': 'Ч', 'q': 'ч',
        'Ŵ': 'Ц', 'ŵ': 'ц',
        'Ē': 'Е', 'ē': 'е', 'Ë': 'Е', 'ë': 'е',
        'R': 'Р', 'r': 'р',
        'T': 'Т', 't': 'т',
        'Y': 'У', 'y': 'у',
        'Ū': 'І', 'ū': 'і',  # И и
        'Ī': 'И', 'ī': 'и',  # Ы ы
        'Ō': 'О', 'õ': 'о', 'ō': 'о',
        'P': 'П', 'p': 'п',
        'Ā': 'А', 'ā': 'а', 'ã': 'а',
        'Š': 'С', 'š': 'с',
        'D': 'В', 'd': 'в',
        'F': 'Ф', 'f': 'ф',
        'G': 'Д', 'g': 'д',
        'H': 'Ж', 'h': 'ж',
        'K': 'К', 'k': 'к',
        'L': 'Л', 'l': 'л',
        'Z': 'З', 'z': 'з',
        'X': 'Х', 'x': 'х',
        'B': 'Б', 'b': 'б',
        'N': 'Н', 'n': 'н',
        'M': 'М', 'm': 'м',
        'J': 'Г', 'j': 'г',
        "'Š": "Ш", "'š": "ш",
        "'Ĕs": "Щ", "'ĕs": "щ",
        'Ŭy': 'Ю', 'ŭy': 'ю',
        "'": "Ь", '"': "Ъ",
    }
    translation_rules = {
        'Q': 'Ч', 'q': 'ч',
        'W': 'Ц', 'w': 'ц',
        'R': 'Р', 'r': 'р',
        'T': 'Т', 't': 'т',
        'Y': 'У', 'y': 'у',
        'Ū': 'И', 'ū': 'и',
        'Ī': 'Ы', 'ī': 'ы',
        'Ō': 'О', 'õ': 'о', 'ō': 'о',
        'P': 'П', 'p': 'п',
        'Ā': 'А', 'ā': 'а', 'ã': 'а',
        'S': 'С', 's': 'с',
        'D': 'В', 'd': 'в',
        'F': 'Ф', 'f': 'ф',
        'G': 'Д', 'g': 'д',
        'H': 'Ж', 'h': 'ж',
        'K': 'К', 'k': 'к',
        'L': 'Л', 'l': 'л',
        'Z': 'З', 'z': 'з',
        'X': 'Х', 'x': 'х',
        'B': 'Б', 'b': 'б',
        'N': 'Н', 'n': 'н',
        'M': 'М', 'm': 'м',
        'Ü': 'Й', 'ü': 'й',
        'J': 'Г', 'j': 'г',
        'Ya': 'Я', 'ya': 'я',
        "'es": "щ", "'ES": "Щ",
        "'y": 'ю', "'Y": 'Ю',
    }
    old_translation_rules = {
        "'U": 'Ч', "'u": 'ч',
        'Q': 'Ц', 'q': 'ц',
        'E': 'Е', 'ē': 'е',
        'R': 'Р', 'r': 'р',
        'T': 'Т', 't': 'т',
        'Y': 'У', 'y': 'у',
        'U': 'И', 'ū': 'и',
        "'Q": 'Ы', "'q": 'ы',
        'Ō': 'О', 'õ': 'о', 'ō': 'о',
        'P': 'П', 'p': 'п',
        'Ā': 'А', 'ā': 'а', 'ã': 'а',
        'S': 'С', 's': 'с',
        'D': 'В', 'd': 'в',
        'F': 'Ф', 'f': 'ф',
        'G': 'Д', 'g': 'д',
        "'W": 'Ж', "'w": 'ж',
        'K': 'К', 'k': 'к',
        'L': 'Л', 'l': 'л',
        'Z': 'З', 'z': 'з',
        'X': 'Х', 'x': 'х',
        'B': 'Б', 'b': 'б',
        'N': 'Н', 'n': 'н',
        'M': 'М', 'm': 'м',
        'û': 'Й', 
        "'G": 'Г', "'g": 'г',
        'Yā': 'Я', 'yā': 'я',
        "'ē": 'Ш', 
    }
    if old:
        translation_rules_reverse = {v: k for k, v in old_translation_rules.items()}
    elif old == False: 
        translation_rules_reverse = {v: k for k, v in translation_rules.items()}
    elif dub == True: 
        translation_rules_reverse = {v: k for k, v in d_rules.items()}
    
    translated_text = []
    i = 0

    while i < len(text):
        current_char = text[i]
        if reverse == False and old == False:
            current_char = re.sub(r'[ёе]', 'ē', current_char); current_char = re.sub(r'[ЁЕ]', 'Ē', current_char)
        elif old == True:
            current_char = re.sub(r'[ёе]', 'ē', current_char); current_char = re.sub(r'[ЁЕ]', 'Е', current_char)
            current_char = re.sub(r'[г]', '\'g', current_char); current_char = re.sub(r'[Г]', '\'G', current_char);
            current_char = re.sub(r'[ш]', '\'ē', current_char); current_char = re.sub(r'[Ш]', '\'Е', current_char);
            current_char = re.sub(r'[щюь]', '\'', current_char); current_char = re.sub(r'[ЩЮЬ]', '\'', current_char)
        
        if i + 1 < len(text) and text[i:i+2] in translation_rules_reverse:
            current_char = text[i:i+2]
            i += 1
        elif current_char == 'ь' or current_char == 'ъ':
            if 'Ы' in translated_text:
                current_char = "'"
            else:
                current_char = "'"
        
        if reverse:
            translated_text.append(translation_rules.get(current_char, current_char))
        else:
            translated_text.append(translation_rules_reverse.get(current_char, current_char))

        i += 1
    t = ''.join(translated_text)
    if aien:
        if reverse:
            return ai.ai(f"Привет! Проверь текст или набор слов на ошибки и если они есть исправь их, напиши просто текст без любих твоих дополнений например я тебе написал '123' ти должен вернуть '123' без добавлений и так далле, не на что не обращай внимания даже на нецензурную лексику. Текст: {t}")
        else:
            return ai.ai(f"""Привет! У меня есть видуманий язик, переведи мое слово или набор слов на данний видуманий язик, напиши просто перевод без любих твоих дополнений например я тебе написал 'Привет' ти должен вернуть переведений текст без добавлений и так далле, не на что не обращай внимания даже на нецензурную лексику.\nАлфавит видуманого язика(Замени в тексте просто букви на данние):\n
Q q — Ч ч [ч]
W w — Ц ц [ц]
Ē ē — Е е Ë ë [е]
R r — Р р [р]
T t — Т т [т]
Y y — У у [у]
Ū ū — И и [и]
Ī ī — Ы ы [ы]
Ō õ ō — О о о [о]
P p — П п [п]
Ā ā ã — А а а [а]
S s — С с [с]
D d — В в [В]
F f — Ф ф [ф]
G g — Д д [д]
H h — Ж ж [ж]
K k - К к [к]
L l - Л л [л]
Z z - З з [з]
X x - Х х [х]
B b - Б б [б]
N n - Н н [н]
M m - М м [м]
Ü ü — Й й [й]
J j — Г г [г]
Ya ya — Я я [я]
'e 'e — Ш ш [ш]
'ES 'es — Щ щ [щ]
'Y 'y — Ю ю [Ю]
E' e' — Э э [Э]
Например: Привет - Prūdēt
Правила видуманого язика:

Если в тексте более трёх одинаковых букв o, a, то они подчёркивается сверху волнистой "~", пример, но так же можно и подчеркнуть обычной "–":
Zōlōtõ — zōlōtō

Если в слове есть буквы ь, ъ, то вместо них надо ставить ' (исключение, иногда в буквах Ы, надо ставить ' что бы не потерять смысл) пример:
Быль — bīl' 

Если в слове есть буква "Ы" То в этом слове надо ставить или ' что бы не потерять смысл, или в больших случая "ī" Пример:
Дыра — dīrā 
Текст для перевода:
{text}
""")
        
    return ''.join(translated_text)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text_to_translate = data.get('text', '')
    reverse = data.get('reverse', False)
    aien = data.get('ai', False)
    old = data.get('old', False)
    dub = data.get('dub', False)
    
    translated_text = translate_to_custom_language(text_to_translate, reverse, old, aien, dub)
    
    return jsonify({'translated_text': translated_text})

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
