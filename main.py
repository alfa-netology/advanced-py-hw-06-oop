from habr_parser import HabrParser

SOURCE_URL = 'https://habr.com/ru/all/'
KEYWORDS = ['дизайн', 'фото', 'web', 'python']


if __name__ == "__main__":
    habr_parser = HabrParser(SOURCE_URL, KEYWORDS)
    find_in_preview, find_in_full_text = habr_parser.find_articles_by_keywords()

    print(f'\nНайдено статей по ключевым словам в превью [{len(find_in_preview)}]:')
    print(*find_in_preview, sep='\n')

    print(f'\nНайдено статей по ключевым словам в тексте статьи [{len(find_in_full_text)}]:')
    print(*find_in_full_text, sep='\n')
