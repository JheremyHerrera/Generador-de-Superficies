import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from mpl_toolkits.mplot3d import Axes3D
import io
import base64

st.title("Generador de Superficies")

def create_surface(f_str, x_min, x_max, y_min, y_max):
    x = np.linspace(x_min, x_max, 100)
    y = np.linspace(y_min, y_max, 100)
    X, Y = np.meshgrid(x, y)

    try:
        x_sym, y_sym = sp.symbols('x y')
        z_expr = sp.sympify(f_str)
        Z = np.array([[float(z_expr.subs({x_sym: x_val, y_sym: y_val})) for x_val in x] for y_val in y])

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close(fig)  # Cerrar la figura después de guardarla
        return plot_url
    except Exception as e:
        st.error(f"Error creating surface: {e}")
        return None

with st.form(key='surface_form'):
    function_input = st.text_input("Función z = f(x, y):", "sin(x) + cos(y)")
    x_min = st.number_input("x_min:", value=-4.0)
    x_max = st.number_input("x_max:", value=4.0)
    y_min = st.number_input("y_min:", value=-4.0)
    y_max = st.number_input("y_max:", value=4.0)
    submit_button = st.form_submit_button(label='Generar Superficie')

if submit_button:
    plot_url = create_surface(function_input, x_min, x_max, y_min, y_max)
    if plot_url:
        img_data = base64.b64decode(plot_url)
        st.image(img_data, caption='Gráfico de Superficie', use_column_width=True)
