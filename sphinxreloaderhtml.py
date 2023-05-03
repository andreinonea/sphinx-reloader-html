#!/usr/bin/env python3

import sys

__version__ = '1.0'
usage = 'usage: sphinx-reloader [-h] [-v] [-m MAKEFILEDIR] [-b BUILDDIR] [SOURCEDIR]'
__doc__ = f'''
{usage}

sphinx-reloader v{__version__}
Live reloads given Sphinx SOURCEDIR using files generated in BUILDDIR by running 'make html' in MAKEFILEDIR.
Defaults to current working directory, with BUILDDIR in CWD/build.
'''.strip()


def echoerror(msg: str) -> None:
	print(usage, file=sys.stderr)
	print(f'error: {msg}', file=sys.stderr)


def do_main() -> int:
	from pathlib import Path

	sourcedir = Path.cwd()
	builddir = sourcedir / 'build'
	makefiledir = sourcedir

	args = iter(sys.argv[1:])
	for arg in args:
		if arg == '-h':
			print(__doc__)
			return 0
		if arg == '-v':
			print(__version__)
			return 0
		if arg == '-m':
			try:
				makefiledir = next(args)  # throws StopIteration if no item left.
				if makefiledir[0] == '-':
					raise StopIteration
			except StopIteration:
				echoerror('missing MAKEFILEDIR argument for -m option')
				return 1
			if not Path(makefiledir).is_dir():
				echoerror(f'invalid MAKEFILEDIR: {makefiledir}')
				return 2
			makefiledir = Path(makefiledir)
			continue
		if arg == '-b':
			try:
				builddir = next(args)
			except StopIteration:
				echoerror(f'missing BUILDDIR argument for -b option')
				return 3
			builddir = Path(builddir)
			continue
		if arg[0] == '-':
			echoerror(f'unrecognized option: {arg}')
			return 4
		sourcedir = Path(arg)
		break

	print(
		f'''Starting livereload server with arguments
Makefile dir: {makefiledir}
Build dir   : {builddir}
Source dir  : {sourcedir}'''
	)
	from livereload import Server, shell

	server = Server()
	server.watch(sourcedir.as_posix(), shell('make html', cwd=makefiledir.as_posix()))
	server.serve(root=(builddir / 'html').as_posix(), open_url_delay=None)
	return 0


if __name__ == '__main__':
	sys.exit(do_main())
