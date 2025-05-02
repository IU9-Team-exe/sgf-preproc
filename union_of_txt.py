import os

# Путь к директории
source_dir = 'doc/_sources'
# Имя итогового файла
output_file = 'doc/merged_output.txt'

with open(output_file, 'w', encoding='utf-8') as outfile:
    for filename in sorted(os.listdir(source_dir)):
        if filename.endswith('.txt'):
            filepath = os.path.join(source_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as infile:
                outfile.write(f'--- {filename} ---\n')  # можно убрать, если не нужно название файла
                outfile.write(infile.read())
                outfile.write('\n\n')  # разделитель между файлами

print(f'Все файлы объединены в {output_file}')
