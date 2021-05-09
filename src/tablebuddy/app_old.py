import toga
from toga.constants import COLUMN, ROW
from toga.sources import Source
from toga.style import Pack
from string import ascii_lowercase, ascii_uppercase, digits



bee_movies = [
    ('Mike','Johnson','Male','18'),('Ann','Bird','Female','34'),('John','Smith','Male','27')
]

#this would be athlete
class Movie:
    def __init__(self, first_name,last_name, sex, age):
            self.first_name = first_name
            self.last_name = last_name
            self.age = int(age)
            self.sex = sex


    


#maybe we need an athlete source
class MovieSource(Source):
    def __init__(self):
        super().__init__()
        self._movies = []
#e.g. docs say every list source must have this:
    def __len__(self):
        return len(self._movies)
#e.g. docs say every list source must have this:
    def __getitem__(self, index):
        return self._movies[index]

    def index(self, entry):
        return self._movies.index(entry)
 #EG adding info       
    def add(self, entry):
        movie = Movie(*entry)
        self._movies.append(movie)
        self._movies.sort(key=lambda m: m.first_name)
        self._notify('insert', index=self._movies.index(movie), item=movie)    

    def remove(self, item):
        index = self.index(item)
        self._notify('pre_remove', index=index, item=item)
        del self._movies[index]
        self._notify('remove', index=index, item=item)

    def clear(self):
        self._movies = []
        self._notify('clear')

class ExampleTableSourceApp(toga.App):

    # Table callback functions
    def on_select_handler(self, widget, row, **kwargs):
        self.label.text = 'You selected row: {}'.format(row.title) if row is not None else 'No row selected'

    # Button callback functions
    # EG looks like this is how we insert data into the table
    def insert_handler(self, widget, **kwargs):
        #self.table1.data.add(choice(bee_movies))
        # EG I modified this to set the index number of the movie list manually
        self.table1.data.add(bee_movies[0])
    def delete_handler(self, widget, **kwargs):
        if self.table1.selection:
            self.table1.data.remove(self.table1.selection)
        elif len(self.table1.data) > 0:
            self.table1.data.remove(self.table1.data[0])
        else:
            print('Table is empty!')

    def clear_handler(self, widget, **kwargs):
        self.table1.data.clear()

    def startup(self):
        self.main_window = toga.MainWindow(title=self.name, size=(640, 400))

                # set up common styles
        label_style = Pack(flex=1, padding_right=24)
        box_style_1 = Pack(direction=ROW, padding=10)
        box_style_2 = Pack(direction=COLUMN, padding=10)

        # Label to show which row is currently selected.
        self.label = toga.Label('Ready.')
        self.table1 = toga.Table(
            #headings=['Year', 'Title', 'Rating', 'Genre'],
            headings=['First Name', 'Last Name', 'Sex', 'Age'],
            data=MovieSource(),
            style=Pack(flex=1),
            on_select=self.on_select_handler
        )

        # Populate the table
        for entry in bee_movies:
            self.table1.data.add(entry)

        #adding the on change stuff
        self.first_name_input = toga.TextInput(
                            on_change=self.first_name_select,

                        )
        self.last_name_input = toga.TextInput(
                            on_change=self.last_name_select,

                        )   

        self.sexinput = toga.Selection(
                            on_select=self.sex_select,
                            items=["Select", "Female", "Male"],
                        )   
        self.ageinput = toga.NumberInput(
                            min_value = 1,
                            max_value = 110,
                            on_change = self.age_select
                        )

        #tablebox = toga.Box(children=[self.table1, self.table2], style=Pack(flex=1))
        self.box = toga.Box(
            children=[
                #Welcome message
                toga.Box(
                    style=box_style_1,
                    children=[
                        toga.Label(
                            "Hello! Welcome to the Calorie Counter",
                            style=label_style,
                        ),
                        toga.Divider(style=Pack(direction=COLUMN, flex=1, padding=20)),
                    ],
                ),
                #athlete information
                toga.Box(
                    style=box_style_2,
                    children=[
                        toga.Label(
                            "Athlete's first name:",
                            style=label_style,
                        ),
                        self.first_name_input
                    ],
                ),
                toga.Box(
                    style=box_style_1,
                    children=[
                        toga.Label(
                            "Athlete's last name:",
                            style=label_style,
                        ),
                        self.last_name_input
                    ],
                ),

                toga.Box(
                    style=box_style_1,
                    children=[
                        toga.Label(
                            "Athlete's sex:",
                            style=label_style,
                        ),
                        self.sexinput  
                    ],
                ),
                toga.Box(
                    style=box_style_1,
                    children=[
                        toga.Label(
                            "Athlete's age:",
                            style = label_style,
                            
                        ),
                        self.ageinput

                    ],
                ),
            ],
            style=Pack(direction=COLUMN, padding=24),
        )

    #Functions to get the users selections and assign to variables.        
    def first_name_select(self, selection):
        first_name = selection.value   

    def last_name_select(self, selection):
        last_name = selection.value

    def sex_select(self, selection):
        sex = selection.value   

    def age_select(self, selection):
        age = selection.value

    
        tablebox = toga.Box(children=[self.table1], style=Pack(flex=1))
        # Buttons
        # EG these buttons call handler functions
        btn_style = Pack(flex=1)
        btn_insert = toga.Button('Insert Row', on_press=self.insert_handler, style=btn_style)
        btn_delete = toga.Button('Delete Row', on_press=self.delete_handler, style=btn_style)
        btn_clear = toga.Button('Clear Table', on_press=self.clear_handler, style=btn_style)
        btn_box = toga.Box(children=[btn_insert, btn_delete, btn_clear], style=Pack(direction=ROW))

        # Most outer box
        outer_box = toga.Box(
            children=[ self.box, btn_box, tablebox, self.label],
            style=Pack(
                flex=1,
                direction=COLUMN,
                padding=10,
            )
        )
        scroller = toga.ScrollContainer(horizontal=False)
        scroller.content = outer_box
        self.main_window.content = scroller
        self.main_window.show()


def main():
    return ExampleTableSourceApp('Table Source', 'org.beeware.widgets.table_source')


if __name__ == '__main__':
    app = main()
    app.main_loop()
    