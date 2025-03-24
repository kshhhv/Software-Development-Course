import numpy as np
import matplotlib.pyplot as plt


def find_translate(hrsc_image, simulated_image, shifts = [0,0]):
    """
    Manually translates two images by shifting the simulated_image over the hrsc_image.
    
    Uses Matplotlib for interactive adjustment.

    Parameters:
        hrsc_image (np.ndarray): Reference HRSC image (grayscale).
        simulated_image (np.ndarray): Simulated image to be aligned (grayscale).

    Returns:
        tuple: (yshift, xshift) representing the required translation.
    """
    if hrsc_image.shape != simulated_image.shape:
        raise ValueError("Both images must have the same dimensions.")

    display_mode = 'both'  # Modes: 'both', 'first', 'second'

    fig, ax = plt.subplots(figsize=(16, 16))
    plt.subplots_adjust(bottom=0.2)

    def update_image():
        """Updates the displayed image with the current shift values."""
        dx, dy = shifts
        shifted_img2 = np.roll(simulated_image, shift=(dy, dx), axis=(0, 1))
        ax.clear()
        
        if display_mode == 'both':
            ax.imshow(hrsc_image, cmap='gray', alpha=0.6)
            ax.imshow(shifted_img2, cmap='jet', alpha=0.2)  # Overlay for visibility

        elif display_mode == 'first':
            cmap = plt.cm.gray.copy()
            cmap.set_bad(color='black')
            ax.imshow(hrsc_image, cmap=cmap)

        elif display_mode == 'second':
            cmap = plt.cm.jet.copy()
            cmap.set_bad(color='black')
            ax.imshow(shifted_img2, cmap=cmap)

        plt.draw()

    def move_image(event):
        """Adjust shift values based on button presses."""
        nonlocal display_mode

        if event.key == '8':  # Move up
            shifts[1] -= 1
        elif event.key == '5':  # Move down
            shifts[1] += 1
        elif event.key == '4':  # Move left
            shifts[0] -= 1
        elif event.key == '6':  # Move right
            shifts[0] += 1
        elif event.key == '7':  # Show only first image
            display_mode = 'first'
        elif event.key == '9':  # Show only second image
            display_mode = 'second'
        elif event.key == '2':  # Reset to overlay
            display_mode = 'both'
        elif event.key == '0':  # Quit and return values
            plt.close()
            print(f"Final Translation: (yshift={shifts[1]}, xshift={shifts[0]})")
            return shifts[1], shifts[0]
        
        update_image()

    fig.canvas.mpl_connect('key_press_event', move_image)
    update_image()
    plt.show()

    return (shifts[0], shifts[1])