import kivy
import sys
import assistant
kivy.require('1.9.1')

from kivy.config import Config

if sys.platform == "linux" or sys.platform == "linux2":
  Config.set('graphics', 'height', '0')
elif sys.platform == "darwin":
  Config.set('graphics', 'height', '50')
  Config.set('graphics', 'fullscreen', 'fake')
  Config.set('graphics', 'position', 'custom')
  Config.set('graphics', 'left', 400)
  Config.set('graphics', 'top', 300)
#importing necessary kivy files


#unfortunately setting fullscreen to fake is deprecated, preferred method is setting Window.borderless to True
#from kivy.config import Config
Config.set('graphics', 'width', '850')
#when fullscreen is true, set height to 50. With fullscreen off and borderless true, set height to 0.
#Config.set('graphics', 'height', '50')
#Config.set('graphics', 'fullscreen', 'fake')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.widget import Widget

from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp

#make it search upon user hitting enter
def on_enter(value):
  print('have:', str(value.text))
  if str(value.text)==('exit' or 'quit'):
    sys.exit(0)
  
  assistant.getintents(value.text)
  assistant.runaction()
  return resultScreen()

#expand once we get results
class resultScreen(GridLayout):
  def __init__(self, **kwargs):
    super(resultScreen, self).__init__(**kwargs)
    print "works"
    self.cols = 1
    #self.row_force_default=True
    self.row_default_height=80
    self.clear_widgets()
    self.add_widget(Label(text="hello", size_hint_x=None, width=100)) 
    for pod in assistant.pods:
      if pod.imgurl=='':
        self.add_widget(Label(text=pod.text, size_hint_x=None, width=100))
      else:
        self.add_widget(Image(source=imgurl))



#make search window
class searchScreen(GridLayout):
  def __init__(self, **kwargs):
    super(searchScreen, self).__init__(**kwargs)
    self.cols = 1
    self.row_force_default=True
    self.row_default_height=50
    #self.add_widget(Label(text='Search:'))
    self.searchQuery = TextInput(multiline=False, label='search', font_size=32, cursor_blink=True, hint_text='Type question to ask or "exit" to quit and press Enter key.')
    self.add_widget(self.searchQuery)
    self.searchQuery.bind(on_text_validate=on_enter)
    
    #Window.size = (500, 50)

class MyApp(App):
  def build(self):
    Window.borderless = True
    #layout = GridLayout(cols=2)
    #layout.add_widget(Button(text='hello1'))
    #layout.add_widget(Button(text='hello2'))
    #return layout
    #Window.clearcolor = (1, 1, 1, .2)
    #return Label(text='Hello World')
    return searchScreen()

if __name__ == '__main__':
  MyApp().run()

