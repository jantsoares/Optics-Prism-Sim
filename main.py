import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


# Function to calculate Snell's law
def snell_law(n1, n2, theta1):
    theta1_rad = np.radians(theta1)
    sin_theta2 = (n1 / n2) * np.sin(theta1_rad)
    if abs(sin_theta2) > 1:
        return None  # Total internal reflection
    theta2_rad = np.arcsin(sin_theta2)
    return np.degrees(theta2_rad)


# Function to plot the prism and rays
def plot_prism_and_rays(ax, n1, n2, theta1):
    ax.clear()

    # Prism vertices
    prism_x = [0, 0, np.sqrt(3) / 2, 0]
    prism_y = [-0.5, 0.5, 0, -0.5]

    # Initial ray
    theta1_rad = np.radians(theta1)
    x_in = np.linspace(-0.5, 0, 100)
    y_in = np.tan(theta1_rad) * x_in 
    if y_in[0] < -0.6:
        y_in = np.linspace(-0.6, 0, 100)
        x_in = y_in/ np.tan(theta1_rad)
    # Calculate refraction at the first surface
    theta2 = snell_law(n1, n2, theta1)
    if theta2 is None:
        x_refract, y_refract = [], []
    else:
        theta2_rad = np.radians(theta2)
        x_refract = np.linspace(0, 0.5, 100)
        y_refract = np.tan(theta2_rad) * x_refract

    # Plot the prism
    ax.plot(prism_x, prism_y, 'k-', linewidth=2, label='Prism')

    # Plot rays
    ax.plot(x_in, y_in, 'r-', label='Incident Ray')
    if theta2 is not None:
        ax.plot(x_refract, y_refract, 'b-', label='Refracted Ray')

    # Labels and legend
    ax.text(-0.4, 0.6, f"Incident: {theta1:.1f}°", color='red')
    if theta2 is not None:
        ax.text(0.2, 0.1, f"Refracted: {theta2:.1f}°", color='blue')
    ax.legend()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Light Refraction in a Prism')
    ax.axis('equal')
    ax.grid(True)


# Initial parameters
initial_n1 = 1.0
initial_n2 = 1.5
initial_theta1 = 45

# Create the figure and axes
fig, ax = plt.subplots(figsize=(8, 6))
plt.subplots_adjust(left=0.1, bottom=0.35)

# Initial plot
plot_prism_and_rays(ax, initial_n1, initial_n2, initial_theta1)

# Axes for sliders
ax_n1 = plt.axes([0.1, 0.25, 0.65, 0.03])
ax_n2 = plt.axes([0.1, 0.2, 0.65, 0.03])
ax_theta1 = plt.axes([0.1, 0.15, 0.65, 0.03])

slider_n1 = Slider(ax_n1, 'n1', 1.0, 2.0, valinit=initial_n1)
slider_n2 = Slider(ax_n2, 'n2', 1.0, 2.0, valinit=initial_n2)
slider_theta1 = Slider(ax_theta1, '\u03b81', 0, 89.99, valinit=initial_theta1)


# Update function for sliders
def update(val):
    n1 = slider_n1.val
    n2 = slider_n2.val
    theta1 = slider_theta1.val
    plot_prism_and_rays(ax, n1, n2, theta1)
    fig.canvas.draw_idle()


slider_n1.on_changed(update)
slider_n2.on_changed(update)
slider_theta1.on_changed(update)

# Reset button
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset')


def reset(event):
    slider_n1.reset()
    slider_n2.reset()
    slider_theta1.reset()


button.on_clicked(reset)

plt.show()
