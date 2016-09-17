import kivy
kivy.require('1.9.1')

#importing necessary kivy files


#unfortunately setting fullscreen to fake is deprecated, preferred method is setting Window.borderless to True
from kivy.config import Config
Config.set('graphics', 'width', '800')
#when fullscreen is true, set height to 50. With fullscreen off and borderless true, set height to 0.
Config.set('graphics', 'height', '0')
#Config.set('graphics', 'fullscreen', 'fake')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.widget import Widget


#make it search upon user hitting enter
def on_enter(instance, value):
  print('User pressed enter in', instance)
  
  textinput = TextInput()
  textinput.bind(text=on_text)

#make search window
class searchScreen(GridLayout):
  def __init__(self, **kwargs):
    super(searchScreen, self).__init__(**kwargs)
    self.cols = 1
    self.row_force_default=True
    self.row_default_height=50
    #self.add_widget(Label(text='Search:'))
    self.searchQuery = TextInput(multiline=False, label='search', font_size=32, cursor_blink=True, hint_text='Type question and press Enter key to continue')
    self.add_widget(self.searchQuery)
    #Window.size = (500, 50)

class MyApp(App):
  def build(self):
    Window.borderless = True
    #Window.clearcolor = (1, 1, 1, .2)
#    return Label(text='Hello World')
    return searchScreen()

if __name__ == '__main__':
  MyApp().run()
