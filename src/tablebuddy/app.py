import toga
from toga.constants import COLUMN, ROW
from toga.sources import Source
from toga.style import Pack


bee_movies = [
    ('Mike','17','Male'),('Ann','34','Female'),('John','27','Male')
]

#this would be athlete
class Movie:
    def __init__(self, first_name, age, sex):
            self.first_name = first_name
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
        
        self.main_window = toga.MainWindow(title=self.name)
# set up common styles
        label_style = Pack(flex=1, padding_right=24)
        box_style_1 = Pack(direction=ROW, padding=10)
        box_style_2 = Pack(direction=COLUMN, padding=10)
        # Label to show which row is currently selected.
        self.label = toga.Label('Ready.')
        self.table1 = toga.Table(
            #headings=['Year', 'Title', 'Rating', 'Genre'],
            headings=['First Name', 'Age', 'Sex'],
            data=MovieSource(),
            style=Pack(flex=1),
            on_select=self.on_select_handler
        )

        # Populate the table
        for entry in bee_movies:
            self.table1.data.add(entry)
        # EG trying to get some UserInput
#            self.first_name_input = toga.TextInput(
#                            on_change=self.first_name_select,
#
#                        )
        #tablebox = toga.Box(children=[self.table1, self.table2], style=Pack(flex=1))
        
        tablebox = toga.Box(children=[self.table1], style=Pack(flex=1))
        
        self.box = toga.Box(
            children=[
                #Welcome message
                toga.Box(
                    style=box_style_2,
                    children=[
                        toga.Label(
                            "Hello! Welcome to the Calorie Counter",
                            style=label_style,
                        ),
                        toga.Divider(style=Pack(direction=COLUMN, flex=1, padding=20)),
                    ],
                ),
                toga.Box(
                    style=box_style_2,
                    children=[
                        toga.Label(
                            "Hello! Welcome to the Calorie Counter",
                            style=label_style,
                        ),
                        toga.Divider(style=Pack(direction=COLUMN, flex=1, padding=20)),
                    ],
                ),
#                toga.Box(
#                    style=box_style_1,
#                    children=[
#                        toga.Label(
#                            "Athlete's first name:",
#                            style=label_style,
#                        ),
#                        self.first_name_input
#                    ],
#               ),   
            ],
            style=Pack(direction=COLUMN, padding=24),
        )
#Functions to get the users selections and assign to variables.  
# EG when I try to pull the first_name to atleast try to get one value I get this error. 

# File "/Users/ellie/beeware-tutorial/beeware-venv/lib/python3.8/site-packages/toga_cocoa/app.py", line 55, in applicationOpenUntitledFile_
    #self.impl.select_file()
#AttributeError: 'App' object has no attribute 'select_file

    #def first_name_select(self, selection):
        #first_name = selection.value


        # Buttons
        # EG these buttons call handler functions
        btn_style = Pack(flex=1)
        btn_insert = toga.Button('Insert Row', on_press=self.insert_handler, style=btn_style)
        btn_delete = toga.Button('Delete Row', on_press=self.delete_handler, style=btn_style)
        btn_clear = toga.Button('Clear Table', on_press=self.clear_handler, style=btn_style)
        btn_box = toga.Box(children=[btn_insert, btn_delete, btn_clear], style=Pack(direction=ROW))

        # Most outer box
        outer_box = toga.Box(
            children=[self.box, btn_box, tablebox, self.label],
            style=Pack(
                flex=1,
                direction=COLUMN,
                padding=10,
            )
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return ExampleTableSourceApp('Table Source', 'org.beeware.widgets.table_source')


if __name__ == '__main__':
    app = main()
    app.main_loop()