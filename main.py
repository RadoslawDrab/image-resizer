import os
import re
from pathlib import Path
from PIL import Image

from args import Arguments


def init():
    args = Arguments()
    files_count: int = 0
    while args.size is None:
        try:
            # Asks for input if there's no size provided
            args.size = int(input('Enter new size: '))
        except Exception as error:
            print('ERROR:', error)

    for directory in args.directories:
        # Files which are in specified directory and don't contain suffix keyword
        files: list[Path] = [f for f in sorted(Path.glob(Path(directory), '**/*' if args.recursive else '*')) if not re.search(f'.{args.suffix}{f.suffix}', f.name)]
        for file in files:
            # Includes only specific file types
            if not any([file.suffix.lower().endswith(t.lower()) for t in args.file_types]):
                continue

            [*file_names, _] = file.name.split('.')
            # Checks if user allows replacement. If so then removes suffix from file name. Otherwise, just appends suffix at the end
            file_name = ".".join([name for name in file_names if name != args.suffix] if args.replace else file_names)
            # Combines new file name
            new_file_name = f'{file_name}.{args.suffix}{file.suffix}'
            try:
                im = Image.open(file)

                # Resize ratio depending on user preference
                ratio = args.size / float(im.size[1 if args.compute_height else 0])

                # Image's size is smaller or equal to specified size
                if ratio >= 1:
                    print(f'File "{file}" not modified')
                    continue

                # New size of other dimension
                size = round(float(im.size[0 if args.compute_height else 1]) * float(ratio))
                # New whole size
                new_size = (size, args.size) if args.compute_height else (args.size, size)

                im.thumbnail(new_size, Image.Resampling.LANCZOS)

                im.save(Path(file.absolute().parent, new_file_name))
                files_count += 1
            except IOError:
                print(f"Cannot resize '{file}'")

    print('-' * min(40, os.get_terminal_size()[0]))
    input(f'Files {files_count} resized to {args.size}px along {'height' if args.compute_height else 'width'}. ')

if __name__ == '__main__':
    init()

