import toga
from toga.constants import COLUMN, ROW
from toga.sources import Source
from toga.style import Pack

athletes = []
class Athlete:
    def __init__(self, first_name, last_name, sex, exercise_level, age, height, weight):
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.exercise_level = exercise_level
        self.age = age
        self.height = height
        self.weight = weight

    @property
    def exercisefactor(self):
        if self.exercise_level=="Little-to-None":
            return 1.2
        elif self.exercise_level=="Light":
            return 1.375
        elif self.exercise_level=="Moderate":
            return 1.55
        elif self.exercise_level=="Heavy":
            return 1.725
        else:
            return 1.725

    @property
    def BMR(self):
        if self.sex=="Male":
            return (10.0 * float(self.weight)) + (6.25 * float(self.height)) - (5.0 * float(self.age)) + 5.0
        elif self.sex == "Female":
            return (10.0 * float(self.weight)) + (6.25 * float(self.height)) - (5.0 * float(self.age)) - 161
        else:
            return "error"
            
    @property
    def daily_cal_target(self):
        return self.BMR * self.exercisefactor

class AthleteSource(Source):
    def __init__(self):
        super().__init__()
        self._athletes = []
#e.g. docs say every list source must have this:
    def __len__(self):
        return len(self._athletes)
#e.g. docs say every list source must have this:
    def __getitem__(self, index):
        return self._athletes[index]

    def index(self, entry):
        return self._athletes.index(entry)
 #EG adding info       
    def add(self, entry):
        athlete = Athlete(*entry)
        self._athletes.append(athlete)
        self._athletes.sort(key=lambda m: m.first_name)
        self._notify('insert', index=self._athletes.index(athlete), item=athlete)    

class ExampleTableSourceApp(toga.App):
    # Button callback functions
    def on_select_handler(self, widget, row, **kwargs):
        self.label.text = 'You selected row: {}'.format(row.title) if row is not None else 'No row selected'
    def first_name_select(self, selection):
        first_name = selection.value
    def last_name_select(self, selection):
        last_name = selection.value
    def sex_select(self, selection):
        sex = selection.value
    def exercise_level_select(self, selection):
        exercise_level = selection.value
    def age_select(self, selection):
        age = selection.value
    def height_select(self, selection):
        height = selection.value
    def weight_select(self, selection):
        weight = selection.value
    
    # EG looks like this is how we insert data into the table

    def insert_handler(self, widget, **kwargs):
        ath = Athlete(self.first_name_input.value,self.last_name_input.value,self.sexinput.value,self.exercise_level_input.value,self.ageinput.value, self.heightinput.value, self.weightinput.value)

        print(ath.daily_cal_target)
        
    
        self.table1.data.add((self.first_name_input.value,self.last_name_input.value,self.sexinput.value,self.exercise_level_input.value,self.ageinput.value, self.heightinput.value, self.weightinput.value))

    def startup(self):
        
        self.main_window = toga.MainWindow(title=self.name)
# set up common styles
        label_style = Pack(flex=1, padding_right=24)
        box_style_1 = Pack(direction=ROW, padding=10)
        box_style_2 = Pack(direction=COLUMN, padding=10)
        # Label to show which row is currently selected.
        self.label = toga.Label('Ready.')
        self.table1 = toga.Table(
        
            headings = ['First Name', 'Last Name', 'Sex','Exercise Level', 'Age', 'Height', 'Weight'],
            accessors = ['first_name', 'last_name', 'sex', 'exercise_level', 'age', 'height', 'weight'], 
            data=AthleteSource(),
            style=Pack(flex=1),
            on_select=self.on_select_handler
        )
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
        self.exercise_level_input = toga.Selection(
                            on_select=self.exercise_level_select,
                            items=["Select", "Little-to-None","Light","Moderate","Heavy","Very Heavy"],
                        )
        self.ageinput = toga.NumberInput(
                            min_value = 1,
                            max_value = 110,
                            on_change = self.age_select
                        )
        self.heightinput = toga.NumberInput(
                            min_value = 10,
                            max_value = 500,
                            on_change = self.height_select,
                        )
        self.weightinput = toga.NumberInput(
                            min_value = 10,
                            max_value = 500,
                            on_change = self.weight_select,
                        )
        

        # Populate the table
        for entry in athletes:
            self.table1.data.add(entry)
        
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
                    style=box_style_1,
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
                            "Athlete's exercise level:",
                            style=label_style,
                        ),
                        self.exercise_level_input
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
                toga.Box(
                    style=box_style_1,
                    children=[
                        toga.Label(
                            "Athlete's height(cm):",
                            style = label_style,
                            
                        ),
                        self.heightinput
                    ],
                ),
                toga.Box(
                    style=box_style_1,
                    children=[
                        toga.Label(
                            "Athlete's weight(kg):",
                            style = label_style,
                            
                        ),
                        self.weightinput

                    ],
                ),

                
            ],
            style=Pack(direction=COLUMN, padding=24),

        )

        # Buttons
        btn_style = Pack(flex=1)
        btn_insert = toga.Button('Add Athlete', on_press=self.insert_handler, style=btn_style)
        btn_box = toga.Box(children=[btn_insert], style=Pack(direction=ROW))

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