#!/bin/env python2
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.scatterlayout import ScatterLayout

import define
import threading

class VocabListScreen(ScatterLayout):
    def __init__(self,**kwargs):
        super(VocabListScreen, self).__init__(**kwargs)

    def build_screen(self):
        self.clear_widgets()
        fab=PanelButton(size_hint=(None,None),
                   text='+',
                   font_size="34dp",
                   height="39dp",
                   width="39dp",
                   pos_hint={'center_x':0.9,'center_y':0.1},
                   on_release=app.side_panel.pressed,
                   screen='addnewwordscreen')
        scroll_layout=ScrollView(do_scroll_x=False)
        grid_layout=GridLayout(cols=3,
                          spacing="10dp",
                          size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        with open('lexicon.txt','r') as vlist:
            for line in vlist:
                line=line.split('"')
                word=Label(text=line[1],
                        markup=True,
                        size_hint= (0.3,None),
                        height="90dp")
                wtype=Label(text=line[3],
                            markup=True,
                            size_hint_x=0.04)
                meaning=TextInput(text=line[5],
                                hint_text="List Empty",
                                allow_copy=False,
                                focus=False,
                                hint_text_color=(0.7,0.7,0.7,1),
                                background_color=(0,0,0.228,0.8),
                                foreground_color=(1,1,1,1),
                                readonly=True,
                                cursor_color=(0,0,0,1),
                                markup=True,
                                font_size="15dp",
                                size_hint_x=0.6)
                grid_layout.add_widget(word)
                grid_layout.add_widget(wtype)
                grid_layout.add_widget(meaning)
        scroll_layout.add_widget(grid_layout)
        self.add_widget(scroll_layout)
        self.add_widget(fab)

class AddWordButton(Button):
    def __init__(self,**kwargs):
        super(AddWordButton, self).__init__(**kwargs)
        self.field=kwargs['field']


class AddNewWordScreen(BoxLayout):
    def build_screen(self):
        self.orientation='vertical'
        self.box=BoxLayout(orientation='vertical',
                      spacing='10dp')

        in_field=TextInput(hint_text='Enter word here',
                        text='',
                        allow_copy=False,
                        background_color=(1,1,1,1),
                        font_size='20sp',
                        multiline=False,
                        hint_text_color=(0.7,0.7,0.7,1),
                        write_tab=False,
                        size_hint=(0.8,0.2),
                        height="30dp",
                        width="500dp",
                        pos_hint={'center_x':0.5,'center_y':0.5})

        ok_button=AddWordButton(text='Add Word',
                        size_hint=(0.5,0.1),
                        height='30dp',
                        width='300dp',
                        field=in_field,
                        on_release=self.add_word_pressed,
                        pos_hint={'center_x':0.5,'center_y':0.5})

        self.empty_label=Label(size_hint_y=0.7)
        self.add_widget(self.box)
        self.box.add_widget(Label(size_hint_y=None, height='10dp'))
        self.box.add_widget(in_field)
        self.box.add_widget(ok_button)
        self.box.add_widget(self.empty_label)

        self.loading_screen=Label(text='Adding Word...\nPlease Wait',
                             font_size="16sp",
                             valign='top',
                             background_color=(1,1,1,0.9),
                             size_hint=(1.,0.7),
                             pos_hint={'center_x':0.5,'center_y':0.5})
        self.loading_screen.text_size=self.loading_screen.size

        self.load_state=False

    def add_word(self,instance):
        if(instance.field.text):
            word=instance.field.text
            print 'word is '+ word
            instance.field.text=''
            meaning=define.define(word)
            if(meaning!='Enter proper word!'):
                with open('lexicon.txt','a') as vlist:
                    vlist.write('"[b]'+word+'[/b]"'+ meaning +'\n')
                instance.field.hint_text="'"+ word+"'" +' is added to your lexicon!'
                Screens['vocablistscreen'].build_screen()
                self.loading_screen.text='"' +  word + '"\n' + " added to your lexicon"
            else:
                instance.field.hint_text="Enter proper word!"
                self.loading_screen.text="Enter proper word!"
    def add_word_pressed(self,instance):
        if(self.load_state==False):
            self.box.remove_widget(self.empty_label)
            self.box.add_widget(self.loading_screen)
            self.load_state=True
        if(self.load_state==True):
            self.loading_screen.text="Adding Word...\nPlease Wait"
        adding_word=threading.Thread(target=self.add_word,args=(instance,))
        adding_word.start()

class FlashcardScreen(Widget):
    pass


class SettingsScreen(Widget):
    pass

class AboutScreen(BoxLayout):
    def build_screen(self):
        self.about_label=Label(text='Vocabulary List\nBy Himanshu\nv0.1alpha',
                               font_size='16sp',
                               halign='center',
                               pos_hint={'center_x':0.5,'center_y':0.5})
        self.add_widget(self.about_label)




class PanelButton(Button):
    def __init__(self,**kwargs):
        super(PanelButton,self).__init__(**kwargs)
        self.screen=kwargs['screen']

class SidePanel(BoxLayout):
    def __init__(self,**kwargs):
        super(SidePanel,self).__init__(**kwargs)
        self.navdrawer=kwargs['navdrawer']


    def build_sidepanel(self):
        self.orientation='vertical'

        vocab_list_button=PanelButton(
        text="Vocabulary List",
        screen="vocablistscreen",
        size_hint=(1.,None),
        height='45dp',
        on_release=self.pressed)

        new_word_button=PanelButton(
        text="Add New Word",
        screen="addnewwordscreen",
        size_hint=(1.,None),
        height='45dp',
        on_release=self.pressed)

        flashcard_button=PanelButton(
        text="Flashcards",
        screen="flashcardscreen",
        size_hint=(1.,None),
        height='45dp',
        on_release=self.pressed)

        settings_button=PanelButton(
        text="Settings",
        screen="settingsscreen",
        size_hint=(1.,None),
        height='45dp',
        on_release=self.pressed)

        about_button=PanelButton(
        text="About",
        screen="aboutscreen",
        size_hint=(1.,None),
        height='45dp',
        on_release=self.pressed)

        blank_label=Label()


        self.add_widget(vocab_list_button)
        self.add_widget(new_word_button)
        self.add_widget(flashcard_button)
        self.add_widget(settings_button)
        self.add_widget(about_button)
        self.add_widget(blank_label)

    def pressed(self, button_name):
        print("Going to " + button_name.screen)
        self.navdrawer.change_main_panel(Screens[button_name.screen])



class NavDrawer(NavigationDrawer):
    def change_main_panel(self, to_screen):
        self.remove_widget(self.main_panel)
        self.set_main_panel(to_screen)
        if (self.state == 'open'):
            self.anim_to_state('closed')
        else:
            self.state = 'closed'

#List of all screens
Screens={'vocablistscreen': VocabListScreen(),
         'addnewwordscreen': AddNewWordScreen(),
         'flashcardscreen': FlashcardScreen(),
         'settingsscreen' : SettingsScreen(),
         'aboutscreen' : AboutScreen()}
app=NavDrawer()


class VocabApp(App):
    def build(self):

        sidepanel=SidePanel(navdrawer=app)
        sidepanel.build_sidepanel()
        app.set_side_panel(sidepanel)
        Screens['vocablistscreen'].build_screen()
        Screens['addnewwordscreen'].build_screen()
        Screens['aboutscreen'].build_screen()
        app.set_main_panel(Screens['vocablistscreen'])
        return app

if __name__ == '__main__':
    VocabApp().run()
