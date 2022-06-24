import pandas as pd
import sympy as sp
import numpy as np
import os as os
import matplotlib.pyplot as plt
from pylatex import Document, Section, Subsection, Tabular, Math, Figure, Alignat
import webbrowser
import cmath
import dataframe_image as dfi

pd.set_option("display.precision", 2)


def remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)


def export_table(data_frame, file_name):
    remove_file(f"{file_name}.csv")
    remove_file(f"{file_name}.html")
    data_frame.to_csv(f"{file_name}.csv")
    data_frame.to_html(f"{file_name}.html")


def create_dictionary(columns):
    dictionary = {}

    for c in columns:
        dictionary[c] = []
    return dictionary


def add_info(dictionary, columns, data):
    i = 0
    for c in columns:
        dictionary[c].append(data[i])
        i += 1


def validate_newton_method(df, z0):
    if df(z0) == 0:
        return False, 0


root = 0


def newton_method(f, fprime, z0, tol):
    i = 0
    n_max = 500

    columns = ("n", "z_n", "f(z_n)", "f'(z_n)", "z_(n+1)", "Error")
    table = create_dictionary(columns)

    if not validate_newton_method(fprime, z0):
        while True:

            z = z0 - f(z0) / fprime(z0)
            error = abs(z - z0)

            row = ((i + 1).real, z0, f(z0), fprime(z0), z, error)

            add_info(table, columns, row)

            if error < tol or i + 1 == n_max or validate_newton_method(fprime, z):
                break

            z0 = z
            i += 1
            global root
            root = z
        return z, i + 1, table


def newton_fractal(z0, f, fprime, tol):
    z = z0
    for i in range(500):
        dz = f(z) / fprime(z)
        if abs(dz) < tol:
            return z
        z -= dz
    return False


dom = 10


def plot_newton_fractal(f, fprime, n, tol, filename, domain=(-dom, dom, -dom, dom)):
    roots = []
    m = np.zeros((n, n))

    def get_root_index(roots, r):

        try:
            return np.where(np.isclose(roots, r, atol=tol))[0][0]
        except IndexError:
            roots.append(r)
            return len(roots) - 1

    xmin, xmax, ymin, ymax = domain
    for ix, x in enumerate(np.linspace(xmin, xmax, n)):
        for iy, y in enumerate(np.linspace(ymin, ymax, n)):
            z0 = x + y * 1j
            r = newton_fractal(z0, f, fprime, tol)
            if r:
                ir = get_root_index(roots, r)
                m[iy, ix] = ir
    plt.imshow(m, cmap="viridis", origin='lower')
    plt.axis('off')
    plt.savefig(f"{filename}_graph.png", bbox_inches='tight')


def plot_polar(root_p, filename):
    magnitude, angle = cmath.polar(root_p)
    plt.figure()
    plt.polar([0, angle], [0, magnitude], marker='o', color='r')
    plt.savefig(f"{filename}_polar.png", bbox_inches='tight')


def write_math(doc, text):
    with doc.create(Alignat(numbering=False, escape=False)) as math:
        math.append(text)


def write(doc, text):
    doc.append(text)


def write_pdf(f, f_sym, df, df_sym, z0, tol, filename, df_table, n=None):
    geometry_options = {"tmargin": "1.5in", "lmargin": "1.5in"}
    doc = Document(geometry_options=geometry_options)
    image_filename = f"{filename}_graph.png"
    polar_filename = f"{filename}_polar.png"
    table_filename = f"{filename}_table.png"

    with doc.create(Section("Newton's Method")):
        with doc.create(Subsection("Function")):
            write_math(doc, f"f(x) = {sp.latex(f_sym)}")
        with doc.create(Subsection("Derivative")):
            write_math(doc, f"f'(x) = {sp.latex(df_sym)}")
        with doc.create(Subsection("Initial Point")):
            write_math(doc, z0)
        with doc.create(Subsection("Tolerance")):
            write_math(doc, tol)
        with doc.create(Subsection("Root")):
            write_math(doc, root)

        if not df_table.empty:
            with doc.create(Subsection("Iterations")):
                with doc.create(Figure(position='h!')) as plot:
                    plot.add_image(table_filename, width='400px')

        with doc.create(Subsection("Number of Iterations")):
            write_math(doc, n)
        with doc.create(Subsection("Fractal")):
            with doc.create(Figure(position="h!")) as graph:
                graph.add_image(image_filename, width="250px")

        with doc.create(Subsection("Polar")):
            with doc.create(Figure(position="h!")) as graph:
                graph.add_image(polar_filename, width="250px")

    doc.generate_pdf(filename, clean_tex=False, compiler="pdflatex")
    doc.generate_tex()


def solve(function, z0, tol, filename):
    z = sp.Symbol("z")

    f_sym = function
    f = sp.lambdify(z, f_sym)

    df_sym = sp.diff(f_sym, z)
    fprime = sp.lambdify(z, df_sym)

    validation = validate_newton_method(fprime, z0)

    if not validation:
        z, n, table = newton_method(f, fprime, z0, tol)
        df_table = pd.DataFrame(table)
        export_table(df_table, filename)
        dfi.export(df_table, f"{filename}_table.png")
        plot_newton_fractal(f, fprime, 1000, tol, filename)
        plot_polar(z, filename)
        write_pdf(f, f_sym, fprime, df_sym, z0, tol, filename, df_table, n)

    webbrowser.open(f"{filename}.pdf")
