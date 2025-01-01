import svgutils.compose as sc
import nextera_utils.utils as utils


class PanningPathPlotter:
    def __init__(self, image_original_size, image_display_size, images, label_height):
        self._image_original_size = image_original_size
        self._image_display_size = image_display_size
        self._images = images
        self._label_height = label_height

    def plot(self, out_fn):
        img_width=str(self._image_display_size) + 'px'
        img_height = (len(self._images) * self._image_display_size) \
                     + (len(self._images) * self._label_height)
        img_height = str(img_height) + 'px'
        panels=[]
        for key, image in self._images.items():
            panel = self._create_panel(key, image)
            panels.append(panel)
        n = len(panels)
        if n == 1:
            fig = sc.Figure(img_width, img_height, panels[0])
        elif n == 2:
            fig = sc.Figure(img_width, img_height, panels[0], panels[1])
        elif n == 3:
            fig = sc.Figure(img_width, img_height, panels[0], panels[1], panels[2])
        elif n == 4:
            fig = sc.Figure(img_width, img_height, panels[0], panels[1], panels[2], panels[3])
        elif n == 5:
            fig = sc.Figure(img_width, img_height, panels[0], panels[1], panels[2], panels[3], panels[4])
        elif n == 6:
            fig = sc.Figure(img_width, img_height, panels[0], panels[1], panels[2], panels[3], panels[4], panels[5])
        else:
            raise ValueError('Max no of panels == 6, exceeded!')
        fig=fig.tile(1,n)
        fig.save(out_fn)

    def _create_panel(self, image_title, image_fn):
        image_scale = self._image_display_size / self._image_original_size
        label_x = '1px'
        label_y = str(self._label_height) + 'px'
        label_size = str(self._label_height) + 'px'
        out = sc.Panel(sc.Text(image_title, label_x, label_y, size=label_size),
                        sc.SVG(image_fn).scale(image_scale).move(0, self._label_height))
        return out
