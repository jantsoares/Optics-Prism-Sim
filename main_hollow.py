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
def plot_prism_and_rays(ax, n1, n2, n3, l, theta1):
    ax.clear()

    # Prism vertices
    prism_out_x = [0, 0, np.sqrt(3) / 2, 0]
    prism_out_y = [-0.5, 0.5, 0, -0.5]
    prism_in_x = [l, l, np.sqrt(3) / 2-2*l, l]
    prism_in_y = [-0.5+np.sqrt(3)*l, 0.5-np.sqrt(3)*l, 0, -0.5+np.sqrt(3)*l]

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
        x_r2, y_r2 = [], []
    else:
        theta2_rad = np.radians(theta2)
        x_r2 = np.linspace(0, l, 100)
        y_r2 = np.tan(theta2_rad) * x_r2
    # Calculate refraction at the second surface
        theta3 = snell_law(n2, n3, theta2)
        if theta3 is None:
            x_r3, y_r3 = [], []
        else:
            theta3_rad = np.radians(theta3)
    #      x_refract2 = np.linspace(-0.5, 1, 100)
            x_r3 = np.linspace(l,(np.sqrt(3)-4*l+2*l*np.sqrt(3)*(np.tan(theta3_rad)-np.tan(theta2_rad))) / (2*np.sqrt(3)*np.tan(theta3_rad)+2), 100)
            y_r3 =l*np.tan(theta2_rad)+np.tan(theta3_rad) * (x_r3 - l)
    # Calculate refraction at the third surface
            theta4 = snell_law(n3,n2,60-theta3)
            if theta4 is None:
                x_r4, y_r4 = [], []
            else:
                theta4_rad = np.radians(theta4)
                x_r4 = np.linspace(x_r3[99],np.sqrt(3)/(1+np.sqrt(3)*np.tan(np.pi/3-theta4_rad))*(0.5-y_r3[99]+x_r3[99]*(np.tan(np.pi/3-theta4_rad))), 100)
                y_r4 = y_r3[99]+np.tan(np.pi/3-theta4_rad) * (x_r4-x_r3[99])
    # Calculate refraction at the fourth surface
                theta5 = snell_law(n2, n1, theta4)
                if theta5 is None:
                    x_r5, y_r5 = [], []
                else:
                    theta5_rad = np.radians(theta5)
                    x_r5 = np.linspace(x_r4[99],1.2, 100)
                    y_r5 = y_r4[99]+np.tan(np.pi/3-theta5_rad) * (x_r5-x_r4[99])
                    if y_r5[99]>1.0:
                        y_r5 = np.linspace(y_r4[99],1.0,100)
                        x_r5 = (y_r5 - y_r4[99])/np.tan(np.pi/3-theta5_rad) + x_r4[99]

    # Plot the prism
    ax.plot(prism_out_x, prism_out_y, 'k-', linewidth=2, label='Prism')
    ax.plot(prism_in_x, prism_in_y, 'k-', linewidth=2, label='')

    # Plot rays
    ax.plot(x_in, y_in, 'r-', label=f'Incident Ray: {theta1:.1f}°')
    if theta2 is not None:
        ax.plot(x_r2, y_r2, 'b-', label=f'1st Refracted Ray: {theta2:.1f}°')
        if theta3 is not None:
            ax.plot(x_r3, y_r3, 'g-', label=f'2nd Refracted Ray: {theta3:.1f}°')
            if theta4 is not None:
                ax.plot(x_r4, y_r4, 'mediumseagreen', label=f'3rd Refracted Ray: {theta4:.1f}°')
                if theta5 is not None:
                    ax.plot(x_r5, y_r5, 'k-', label=f'4th Refracted Ray: {theta5:.1f}°')

    # Labels and legend
    ax.text(-0.75, 0.5, f"Incident ray: {theta1:.1f}°", color='red')
    if theta5 is not None:
        ax.text(-.75, 0.4, f"Refracted ray: {60-theta5:.1f}°", color='black')
    ax.legend()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Light Refraction through a hollow Prism')
    ax.axis('equal')
    ax.grid(True)


# Initial parameters
initial_n1 = 1.0
initial_n2 = 1.5
initial_n3 = 1.33
initial_theta1 = 45.0
l=0.1

# Create the figure and axes
fig, ax = plt.subplots(figsize=(8, 6))
plt.subplots_adjust(left=0.1, bottom=0.35)

# Initial plot
plot_prism_and_rays(ax, initial_n1, initial_n2,initial_n3,l, initial_theta1)

# Axes for sliders
ax_n1 = plt.axes([0.1, 0.25, 0.65, 0.03])
ax_n2 = plt.axes([0.1, 0.2, 0.65, 0.03])
ax_n3 = plt.axes([0.1, 0.15, 0.65, 0.03])
ax_l = plt.axes([0.1, 0.1, 0.65, 0.03])
ax_theta1 = plt.axes([0.1, 0.05, 0.65, 0.03])

slider_n1 = Slider(ax_n1, 'n1', 1.0, 3.0, valinit=initial_n1)
slider_n2 = Slider(ax_n2, 'n2', 1.0, 3.0, valinit=initial_n2)
slider_n3 = Slider(ax_n3, 'n3', 0.5, 3.0, valinit=initial_n3)
slider_l = Slider(ax_l, 'l', 0.01, 0.2, valinit=l)
slider_theta1 = Slider(ax_theta1, '\u03b81', 0.1, 89.99, valinit=initial_theta1)


# Update function for sliders
def update(val):
    n1 = slider_n1.val
    n2 = slider_n2.val
    n3 = slider_n3.val
    l = slider_l.val
    theta1 = slider_theta1.val
    plot_prism_and_rays(ax, n1, n2, n3, l, theta1)
    fig.canvas.draw_idle()


slider_n1.on_changed(update)
slider_n2.on_changed(update)
slider_n3.on_changed(update)
slider_l.on_changed(update)
slider_theta1.on_changed(update)

# Reset button
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset')


def reset(event):
    slider_n1.reset()
    slider_n2.reset()
    slider_n3.reset()
    slider_l.reset()
    slider_theta1.reset()


button.on_clicked(reset)

plt.show()
