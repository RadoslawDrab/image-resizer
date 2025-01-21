from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

class Arguments:
    file_types: list[str] = ['jpg', 'jpeg', 'png']
    suffix: str = 'mod'
    recursive: bool = True
    directories: list[str] = ['./']
    size: int | None = None
    compute_height: bool = False
    replace: bool = True

    def __init__(self):
        parser = ArgumentParser('Image resizer', formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument('--dir', '-d', help='Directories to check', action='store', nargs='*', dest='directories', default=self.directories)
        parser.add_argument('--not-recursive', help='Don\'t search recursively', action='store_true', dest='recursive', default=self.recursive)
        parser.add_argument('--types', '-t',help='File types to modify', action='store', nargs='*', dest='file_types', default=self.file_types)
        parser.add_argument('--suffix', help='Suffix', action='store', dest='suffix', default=self.suffix)
        parser.add_argument('--size', '-s', help='Size in pixels', action='store', dest='size', type=int)
        parser.add_argument('--height', help='Resize height instead of width', action='store_true', dest='compute_height')
        parser.add_argument('--replace', '-r', help='Replace modified images', action='store_false', dest='replace')

        args = parser.parse_args()
        for (key, value) in args._get_kwargs():
            if value is None:
                continue
            setattr(self, key, value)