import importlib.metadata
from pathlib import Path

__version__ = importlib.metadata.version(__package__ or __name__)


# TODO: get directory from command line arg or iterate all directories
# TODO: check config file for available versions etc.
def inject():
    for f in Path('pages/0.1.0').rglob('*.html'):
        remainder = f.read_text()
        chunks = []
        while remainder:
            prefix, sep, remainder = remainder.partition(
                '<!--version-injector-injects-')
            chunks.append(prefix)
            if sep == '':
                # no more markers found
                assert remainder == ''
                break
            chunks.append(sep)
            category, sep, remainder = remainder.partition('-below-->')
            if sep == '':
                # TODO: somehow continue?
                raise RuntimeError(
                    'error! malformed marker? missing opening marker?')
            chunks.append(category)
            chunks.append(sep)
            discard, sep, remainder = remainder.partition(
                f'<!--version-injector-injects-{category}-above-->')
            if sep == '':
                raise RuntimeError(
                    f'error/warning? no closing marker for {category!r}')
            chunks.append('\n')
            if category == 'VERSIONS':
                chunks.append('<li>generated content!</li>\n')
                chunks.append('<li>more generated content!</li>\n')
            elif category == 'WARNING':
                chunks.append('<p><b>warning!</b></p>\n')
                chunks.append('<p><b>another warning!</b></p>\n')
            else:
                raise RuntimeError(f'Unknown category: {category!r}')
            chunks.append(sep)
        f.write_text(''.join(chunks))


if __name__ == '__main__':
    inject()