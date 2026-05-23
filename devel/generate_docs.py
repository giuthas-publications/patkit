#
# Copyright (c) 2019-2026
# Pertti Palo, Scott Moisik, Matthew Faytak, and Motoki Saito.
#
# This file is part of the Phonetic Analysis ToolKIT
# (see https://github.com/giuthas/patkit/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# The example data packaged with this program is licensed under the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International (CC BY-NC-SA 4.0) License. You should have received a
# copy of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International (CC BY-NC-SA 4.0) License along with the data. If not,
# see <https://creativecommons.org/licenses/by-nc-sa/4.0/> for details.
#
# When using the toolkit for scientific publications, please cite the
# articles listed in README.md. They can also be found in
# citations.bib in BibTeX format.
#
"""
PATKIT doc generator.
"""
from pathlib import Path
import pkgutil
import sys
import warnings

import pdoc

# Suppress the annoying duplicate module warnings from pdoc
warnings.filterwarnings(
    "ignore",
    message="The module specification.*adds a module named.*has already been added"
)


def main():
    """
    Generate the docs for PATKIT.

    Run with `uv run devel/generate_docs.py` at project root.
    """
    src_path = Path("src").resolve()
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    # Import patkit dynamically to inspect its contents
    import patkit

    # 2. Programmatically crawl and collect the package and all submodules
    modules_to_document = ["patkit"]
    for module_info in pkgutil.walk_packages(
        patkit.__path__, patkit.__name__ + "."
    ):
        modules_to_document.append(module_info.name)

    pdoc.render.configure(docformat="numpy", )

    pdoc.pdoc(*modules_to_document, output_directory=Path("docs/api"))


if __name__ == "__main__":
    main()
