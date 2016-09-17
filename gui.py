import kivy
kivy.require('1.9.1')

#importing necessary kivy files
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.widget import Widget

#make it search upon user hitting enter
def on_enter(instance, value):
  print('User pressed enter in', instance)

#make search window
class searchScreen(GridLayout):
  def __init__(self, **kwargs):
    super(searchScreen, self).__init__(**kwargs)
    self.cols = 1
    self.row_force_default=True
    self.row_default_height=50
    #self.add_widget(Label(text='Search:'))
    self.searchQuery = TextInput(multiline=False, label='search', font_size=32)
    self.add_widget(self.searchQuery)


class MyApp(App):
  def build(self):
#    return Label(text='Hello World')
    return searchScreen()

if __name__ == '__main__':
  MyApp().run()
