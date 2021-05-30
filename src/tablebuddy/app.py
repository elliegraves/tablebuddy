#we're able to import different libraries of code for use in my program
import toga
from toga.constants import COLUMN, ROW
from toga.sources import Source
from toga.style import Pack

#Classes provide a means of bundling data and functionality together
#In this program we need an athlete and food class
class Athlete:
#ex of class data
    def __init__(self, first_name, last_name, sex, exercise_level, age, height, weight):
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.exercise_level = exercise_level
        self.age = age
        self.height = height
        self.weight = weight
#ex of class functionality
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
#creating an empty list to start the table
athletes = []

#this class is useful for toga table construction and management
class AthleteSource(Source):
    def __init__(self):
        super().__init__()
        self._athletes = []

    def __len__(self):
        return len(self._athletes)

    def __getitem__(self, index):
        return self._athletes[index]
    def index(self, entry):
        return self._athletes.index(entry)
 ##F
    def add(self, athlete):
        self._athletes.append(athlete)
        self._athletes.sort(key=lambda m: m.first_name)
        self._notify('insert', index=self._athletes.index(athlete), item=athlete)    

#start
class Food:
#ex of class data
    def __init__(self, food_name, food_category, cal_per_gram ):
        self.food_name = food_name
        self.food_category = food_category
        self.cal_per_gram = cal_per_gram
    
#creating an empty list to start the table
foods = []
#start
class FoodSource(Source):
    def __init__(self):
        super().__init__()
        self._foods = []

    def __len__(self):
        return len(self._foods)

    def __getitem__(self, index):
        return self._foods[index]
    def index(self, entry):
        return self._foods.index(entry)
 ##F
    def add(self, food):
        self._foods.append(food)
        self._foods.sort(key=lambda m: m.food_name)
        self._notify('insert', index=self._foods.index(food), item=food)  
#end
#end
#this is the main application
class ExampleTableSourceApp(toga.App):
    # Button callback functions
        #food stuff

         #athlete 
#takes user selection and assigns to a variable, these fire on_change or on_select
#These variables are used later to create the athlete
##C
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

#Food Info
    def food_name_select(self, selection):
        food_name = selection.value
    def food_category_select(self, selection):
        food_category = selection.value
    def cal_per_gram_select(self, selection):
        cal_per_gram = selection.value
    
    # EG looks like this is how we insert data into the table
    #food
    ##E


    def athlete_insert_handler(self, widget, **kwargs):
        # creating a new instance of the athlete classe called ath 
        ath = Athlete(self.first_name_input.value,self.last_name_input.value,self.sexinput.value,self.exercise_level_input.value,self.ageinput.value, self.heightinput.value, self.weightinput.value)
    #now that we have an athlete we can do whatever we want, for example 
    #print(ath.BMR)
    # the ath data is inserted into the table using the add function
        self.athlete_table1.data.add(ath)
    def food_insert_handler(self, widget, **kwargs):
        # creating a new instance of the athlete classe called ath 
        food = Food(self.food_name_input.value,self.food_category_input.value,self.cal_per_gram_input.value)
    #now that we have an athlete we can do whatever we want, for example 
    #print(ath.BMR)
    # the ath data is inserted into the table using the add function
        self.food_table1.data.add(food)

    def startup(self):
        
        self.main_window = toga.MainWindow(title=self.name)
# set up common styles
        label_style = Pack(flex=1, padding_right=24)
        box_style_1 = Pack(direction=ROW, padding=10)
        box_style_2 = Pack(direction=COLUMN, padding=10)
        # Label to show which row is currently selected.
        self.label = toga.Label('Ready.')
        self.athlete_table1 = toga.Table(
        
            headings = ['First Name', 'Last Name', 'Sex','Exercise Level', 'Age', 'Height', 'Weight', 'BMR' ,'daily calorie target'],
            accessors = ['first_name', 'last_name', 'sex', 'exercise_level', 'age', 'height', 'weight', 'BMR', 'daily_cal_target'], 
            data=AthleteSource(),
            style=Pack(flex=1),
        )
    #start
            # Label to show which row is currently selected.
        self.label = toga.Label('Ready.')
        self.food_table1 = toga.Table(
        
            headings = ['Food Name', 'Food Category', 'Cal Per Gram'],
            accessors = ['food_name', 'food_category', 'cal_per_gram'], 
            data=FoodSource(),
            style=Pack(flex=1),
        )
    #end
        #here are input values and we can set them equal to toga.(TextInput)since we imported toga in the beggining of the code
        #these are functions called from our toga boxes that define the type of input, and what should happen on input
        ##B
        #this gives the ability to define each box as a togga class 
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
        #food info
        self.food_name_input = toga.TextInput(
                            on_change=self.food_name_select,

                        )
        self.food_category_input = toga.Selection(
                            on_select=self.food_category_select,
                            items=["Select", "Fruit", "Grains","Proteins","Vegetables","Dairy"],
                        )
        self.cal_per_gram_input = toga.NumberInput(
                            on_change = self.cal_per_gram_select
                        )

#creating togaboxes to accept the user input
#athlete related
        athlete_tablebox = toga.Box(children=[self.athlete_table1], style=Pack(flex=1))
        food_tablebox = toga.Box(children=[self.food_table1], style=Pack(flex=1))
        #General info box 
        ##A
        self.welcome_box = toga.Box(
            children=[
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
                
            ],
            style=Pack(direction=COLUMN, padding=24),

        )

        self.athlete_box = toga.Box(
            children=[


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
        self.food_box = toga.Box(
            children=[
                toga.Box(
                    style=box_style_2,
                    children=[
                        toga.Label(
                            "Food",
                            style=label_style,
                        ),
                        toga.Divider(style=Pack(direction=COLUMN, flex=1, padding=20)),
                    ],
                ),                
                toga.Box(
                    style=box_style_1,
                    children=[
                        toga.Label(
                            "Food Name:",
                            style=label_style,
                        ),
                        self.food_name_input
                    ],
                ),
                toga.Box(
                    style=box_style_1,
                    children=[
                        toga.Label(
                            "Food Category:",
                            style=label_style,
                        ),
                        self.food_category_input  
                    ],
                ),
                toga.Box(
                    style=box_style_1,
                    children=[
                        toga.Label(
                            "Calories per gram:",
                            style = label_style,
                            
                        ),
                        self.cal_per_gram_input

                    ],
                ),
            ],
            style=Pack(direction=COLUMN, padding=24),

        )
#will put a food box here:
        # Buttons
        btn_style = Pack(flex=1)
        #once we've got user data stored we're now ready to add an athlete which we do by firing insert_handler
        ##D
        athlete_btn_insert = toga.Button('Add athlete', on_press=self.athlete_insert_handler, style=btn_style)
        athlete_btn_box = toga.Box(children=[athlete_btn_insert], style=Pack(direction=ROW))
        food_btn_insert = toga.Button('Add food', on_press=self.food_insert_handler, style=btn_style)
        food_btn_box = toga.Box(children=[food_btn_insert], style=Pack(direction=ROW))
        # Most outer box
  
        #new food section end
        #new food section start
        outer_box = toga.Box(
            children=[self.welcome_box, self.athlete_box, athlete_btn_box, athlete_tablebox, self.label, self.food_box,food_btn_box, food_tablebox],
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