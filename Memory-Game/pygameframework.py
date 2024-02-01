from pygame import init, quit, Color, Surface, Rect, KEYUP, K_SPACE, K_RETURN, K_z, K_LSHIFT, K_RSHIFT, K_CAPSLOCK, K_BACKSPACE
from pygame.display import set_caption, set_mode, update
from pygame.font import SysFont, Font
from pygame.event import poll
from pygame.key import get_pressed, name

class Window:
    def __init__(self, title, width, height):
        init()
        self.__surface__ = set_mode((width, height), 0, 0)
        set_caption(title)
        self.__font_name__ = ''
        self.__font_size__ = 18
        self.__font__ = SysFont(self.__font_name__, self.__font_size__, True)
        self.__font_color__ = 'white'
        self.__bg_color__ = 'black'
        self.__auto_update__ = True

    def close(self):
        quit()

    def set_font_name(self, name):
        self.__font_name__ = name
        self.__font__ = SysFont(self.__font_name__, self.__font_size__, True)

    def set_font_size(self, point_size):
        self.__font_size__ = point_size
        self.__font__ = SysFont(self.__font_name__, self.__font_size__, True)

    def set_font_color(self, color_string):
        self.__font_color__ = color_string
    
    def set_bg_color(self, color_string):
        self.__bg_color__ = color_string
        
    def set_auto_update(self, true_false):
        self.__auto_update__ = true_false
    
    def get_font_height(self):
        return self.__font__.size('')[1]

    def get_font_color(self):
        return self.__font_color__

    def get_bg_color(self):
        return self.__bg_color__

    def get_width(self):
        return self.__surface__.get_width()

    def get_height(self):
        return self.__surface__.get_height()

    def clear(self):
        self.__surface__.fill(Color(self.__bg_color__))
        if self.__auto_update__:
            update()
     
    def get_surface(self):
        return self.__surface__

    def draw_string(self, string, x, y):
        text_image = self.__font__.render(string, True, Color(self.__font_color__), Color(self.__bg_color__))
        self.__surface__.blit(text_image, (x, y))
        if self.__auto_update__:
            text_rect = Rect((x, y), text_image.get_size())
            update(text_rect)

    def input_string(self, prompt, x, y):
        key = K_SPACE
        answer = ''
        while key != K_RETURN:
            self.draw_string(prompt + answer + '    ', x, y)
            if not self.__auto_update__:
                update()
            key = self._get_key()
            key_state = get_pressed()
            if (K_SPACE <= key <= K_z):
                if key == K_SPACE:
                    letter = ' '
                else:
                    letter = name(key)
                if key_state[K_LSHIFT] or key_state[K_RSHIFT] or key_state[K_CAPSLOCK]:
                    letter = letter.upper()
                answer = answer + letter
            if key == K_BACKSPACE:
                answer = answer[0:len(answer)-1]
        return answer

    def get_string_width(self, string):
        return self.__font__.size(string)[0]
     
    def update(self):
        update()

    def _get_key(self):
        event = poll()
        while event.type != KEYUP:
            event = poll()
        return event.key
        
def _test():
    # To test the code in this module remove the # from
    # the #_test line below. Don't forget to put the #
    # back before saving the module for production use.
    # When testing try the backspace key.

    window_width = 500
    window_height = 400
    title = 'Window Title'
    window = Window(title, window_width, window_height)
    string = window.input_string('Enter text >', 0, 0)
    window.clear()
    surface = window.get_surface()
    width = window.get_width()
    height = window.get_height()
    s_width = surface.get_width()
    s_height = surface.get_height()
    if width == s_width == window_width:
        window.draw_string(str(width), 0, 0)
    else:
        window.draw_string('width error', 0, 0)
    if height == s_height == window_height:
        window.draw_string(str(height), width // 2, height // 2)
    else:
        window.draw_string('height error', width // 2, height // 2)   
    height = window.get_font_height()
    width = window.get_string_width(string)
    window.draw_string(string, 0, height)
    window.draw_string(string, width, height)
    window.update()
    window.set_font_name('couriernew')
    window.set_font_size(24)
    window.set_font_color('yellow')
    window.set_bg_color('blue')
    font_color = window.get_font_color()
    bg_color = window.get_bg_color()
    window.draw_string(font_color, 200, 200)       
    window.draw_string(bg_color, 300, 300)
    height = window.get_font_height()
    window.input_string('press any key to close window', 0, window_height - height)
    window.close()
    
#_test()

