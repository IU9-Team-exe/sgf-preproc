import json
import sgfmill.sgf
import sgfmill.sgf_moves
from deep_translator import GoogleTranslator

# Форматирование хода в читаемый вид (например, "D4")
def format_move(color, move):
    if move is None:
        return "pass"
    row, col = move
    letters = "ABCDEFGHJKLMNOPQRST"  # Пропускаем 'I' в соответствии со стандартом Го
    return f"{letters[col]}{19 - row}"

# Получение последовательности ходов до текущего узла, исключая корневой узел
def get_move_sequence(node):
    sequence = []
    current = node
    while current.parent and current.parent.parent:  # Исключаем корень
        color, move = current.get_move()
        if color:
            sequence.append(format_move(color, move))
        current = current.parent
    return sequence[::-1]  # Хронологический порядок

# Получение следующих ходов (до 3-х)
def get_next_moves(node, limit=3):
    next_moves = []
    current = node
    for _ in range(limit):
        if not current:
            break
        color, move = current.get_move()
        if color:
            next_moves.append(format_move(color, move))
        current = current[0] if current else None  # Основная ветка
    return next_moves

# Получение вариантов ответвлений
def get_variations(node):
    variations = []
    for child in node[1:]:  # Пропускаем основную ветку
        color, move = child.get_move()
        if color:
            variations.append(format_move(color, move))
    return variations

# Перевод текста на английский язык
def translate_to_english(text):
    translator = GoogleTranslator(source='auto', target='en')
    return translator.translate(text)

# Обработка одного SGF-файла
def process_sgf(sgf_content):
    try:
        game = sgfmill.sgf.Sgf_game.from_string(sgf_content)
    except ValueError as e:
        print(f"Ошибка парсинга SGF: {e}")
        return []

    examples = []
    for node in game.get_main_sequence():
        if node.has_property("C"):  # Проверяем наличие комментария
            comment = node.get("C")
            translated_comment = translate_to_english(comment)  # Переводим комментарий
            color, move = node.get_move()
            if not color:
                continue  # Пропускаем узлы без ходов

            # Собираем данные для промпта
            move_sequence = get_move_sequence(node)
            current_move = format_move(color, move)
            next_moves = get_next_moves(node[0] if node else None)
            variations = get_variations(node)

            # Формируем промпт на английском языке
            prompt = f"Sequence of moves: {' '.join(move_sequence)}\n"
            prompt += f"Current move: {current_move}\n"
            if next_moves:
                prompt += f"Next moves: {' '.join(next_moves)}\n"
            if variations:
                prompt += f"Variations: {' '.join(variations)}"

            # Создаем обучающий пример
            example = {
                "messages": [
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": translated_comment}
                ]
            }
            examples.append(example)
    return examples

# Преобразование SGF в JSONL
def sgf_to_jsonl(sgf_file, jsonl_file):
    with open(sgf_file, "r", encoding="utf-8") as f:
        sgf_content = f.read()

    examples = process_sgf(sgf_content)

    with open(jsonl_file, "w", encoding="utf-8") as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + "\n")

# Пример использования
if __name__ == "__main__":
    sgf_file = "./test/pro_1.sgf"  # Укажите путь к вашему SGF-файлу
    jsonl_file = "output.jsonl" # Укажите путь для выходного файла
    sgf_to_jsonl(sgf_file, jsonl_file)
    print(f"Обработка завершена. Результат сохранен в {jsonl_file}")