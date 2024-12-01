'''
A collection of shared components.

Alias: nwsh
'''

# GLOBAL MODULES
import base64
import os
import re
import requests
from datetime import datetime
from datetime import date
from io import BytesIO
from IPython.core.display import display
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from numpy import float64
from pandas import DataFrame, Index, Series
from pandas.io.formats.style import Styler
from typing import Any, Callable, Tuple, Optional

# CONSTANTS
# STATIC CLASSES
# CLASSES
class OutlierManager():
    
    '''Collects all the logic related to the outlier management.'''

    def try_remove_lower_bound_outliers(self, df : DataFrame, column_name : str) -> DataFrame:

        '''Removes all the values > quantile(0.01) or df if an exception is raised.'''

        try:

            lower_bound : float = df[column_name].quantile(0.01)
            condition : Series = (df[column_name] > lower_bound)
            filtered_df : DataFrame = df[condition]

            return filtered_df    
        except:

            return df
    def try_remove_upper_bound_outliers(self, df : DataFrame, column_name : str) -> DataFrame:

        '''Removes all the values < quantile(0.99) or df if an exception is raised.'''

        try:

            upper_bound : float = df[column_name].quantile(0.99)
            condition : Series = (df[column_name] < upper_bound)
            filtered_df : DataFrame = df[condition]

            return filtered_df
        except:

            return df
class FilePathManager():
    
    '''Collects all the logic related to the file path management.'''

    def create_file_path(self, folder_path : str, file_name : str) -> str:

        '''Creates a file path.'''

        return os.path.join(folder_path, file_name) 
    def create_numbered_file_path(self, folder_path : str, number : int, extension : str) -> str:

        r'''Creates a numbered file path. Example: ("C:\\", 1, "html") => "C:\\1.html"'''

        file_name : str = f"{number}.{extension}"
        file_path : str = self.create_file_path(folder_path = folder_path, file_name = file_name)    

        return file_path
    def create_numbered_file_paths(self, folder_path : str, range_start : int, range_end : int, extension : str) -> list[str]:

        '''
            Creates a collection of numbered file paths.

            If range_start = 1 and range_end = 3, only two items will be created (range_end is excluded).
        '''

        file_paths : list[str] = []
        for i in range(range_start, range_end):
            file_path : str = self.create_numbered_file_path(folder_path = folder_path, number = i, extension = extension)
            file_paths.append(file_path)

        return file_paths
class FileManager():
    
    '''Collects all the logic related to the file management.'''

    __file_path_manager : FilePathManager

    def __init__(self, file_path_manager : FilePathManager) -> None:
        
        self.__file_path_manager = file_path_manager
    def __create_file_paths(self, working_folder_path : str, extension : str) -> list[str]:

        '''Creates file paths.'''

        if not extension.startswith("."):
            extension = f".{extension}"

        file_paths : list[str] = []
        for file_name in os.listdir(path = working_folder_path):
            if file_name.endswith(extension):
                file_path : str = self.__file_path_manager.create_file_path(folder_path = working_folder_path, file_name = file_name)   
                file_paths.append(file_path)

        return file_paths
    def __convert_contents_to_lines(self, contents : list[str]) -> list[str]:

        '''Converts contents to lines.'''

        lines : list[str] = []
        for i in range(len(contents)):
            lines.append(contents[i])
            lines.append('\n')

        return lines

    def remove_files(self, extensions : list[str], working_folder_path : str) -> None:

        '''Delete all the files of the provided extensions from the provided folder.'''    

        for file_name in os.listdir(path = working_folder_path):
            for extension in extensions:
                if file_name.endswith(extension):
                    os.remove(os.path.join(working_folder_path, file_name))
    def load_content(self, file_path : str) -> str:
        
        '''Reads the content of the provided text file and returns it as string.'''

        content : str = ""
        with open(file_path, 'r', encoding = 'utf-8') as file:
            content = file.read()

        return content
    def load_contents(self, working_folder_path : str, extension : str) -> list[str]:

        '''Reads the contents of all the text files in the provided folder and returns them as a collection of strings.'''

        file_paths : list[str] = self.__create_file_paths(working_folder_path = working_folder_path, extension = extension)

        contents : list[str] = []
        for file_path in file_paths:
            content : str = self.load_content(file_path = file_path)
            contents.append(content)

        return contents
    def save_content(self, content : str, file_path : str) -> None:    

        '''Writes the provided content to the provided file path.'''

        with open(file_path, 'w', encoding = 'utf-8') as new_file:
            new_file.write(content)
    def save_contents(self, contents : list[str], file_paths : list[str]) -> None: 

        '''Writes the provided contents to the provided file paths.'''

        for i in range(len(contents)):
            self.save_content(content = str(contents[i]), file_path = file_paths[i]) # without str() it returns 'bytes' (?)
    def save_log(self, contents : list[str], working_folder_path : str, file_name : str) -> None:

        '''Writes the provided collection of strings as newline-separated lines into the provided file.'''

        file_path : str = self.__file_path_manager.create_file_path(folder_path = working_folder_path, file_name  = file_name)
        lines : list[str] = self.__convert_contents_to_lines(contents = contents)

        with open(file_path, 'w', encoding = 'utf-8') as new_file:
            new_file.writelines(lines)
class PageManager():
    
    '''Collects all the logic related to the page management.'''

    def get_page_content(self, page_url : str) -> str:

        '''
            Performs a GET request against the provided url and returns its content as string.
            
            Use req.text instead of req.content to ensure that you get Unicode.
        '''

        page_response = requests.get(page_url)
        page_content = page_response.text

        return page_content
    def get_page_contents(self, page_urls : list[str]) -> list[str]:

        '''Performs a GET request against the provided urls and returns their contents as a collection of strings.'''

        page_contents : list[str] = []
        for page_url in page_urls:
            page_content = self.get_page_content(page_url = page_url)
            page_contents.append(page_content)

        return page_contents
    def decode_unicode_characters(self, string : str) -> str:
        
        r'''Example: "Antikt \u0026 Design" => "Antikt & Design"'''

        return string.encode('utf_8').decode('unicode_escape')
class PlotManager():
    
    '''Collects all the logic related to the plot management.'''

    def show_bar_plot(self, df : DataFrame, x_name : str, y_name : str, figsize : Tuple[int, int] = (5, 5)) -> None:

        '''Shows a bar plot.'''

        title = f"{y_name} by {x_name}"
        df.plot(x = x_name, y = y_name, legend = True, kind = "bar", title = title, figsize = figsize)
    def show_box_plot(self, df : DataFrame, x_name : str, figsize : Tuple[int, int] = (5, 5)) -> None:

        '''Shows a box plot.'''
    
        plt.figure(figsize = figsize)
        plt.boxplot(x = df[x_name], vert = False, tick_labels = [x_name])
        plt.show()

    def create_bar_plot_function(self, df : DataFrame, x_name : str, y_name : str = "items", figsize : Tuple[int, int] = (5, 5)) -> Callable[[], None]:

        '''
            Returns a function that visualizes a bar plot.

            Example:
            >>> func = PlotManager().create_bar_plot_function(df = df , x_name = "seller_alias")
            >>> func()
        '''

        func : Callable[[], None] = lambda : self.show_bar_plot(df = df, x_name = x_name, y_name = y_name, figsize = figsize)

        return func    
    def create_bar_plot_as_base64(self, df : DataFrame, x_name : str, y_name : str = "items", figsize : Tuple[int, int] = (5, 5)) -> Optional[str]:

        '''
            Returns a bar plot as a base64 string or None.

            Example:            
            >>> plot_manager : PlotManager = PlotManager()
            >>> image_string : str = plot_manager.create_bar_plot_as_base64(df = df, x_name = "seller_alias")
            >>> image_string = plot_manager.create_html_image_tag(image_string = image_string)
            >>> HTML(image_string)
        '''

        buffer : BytesIO = BytesIO()

        title = f"{y_name} by {x_name}"
        fig : Optional[Figure] = df.plot(x = x_name, y = y_name, legend = True, kind = "bar", title = title, figsize = figsize).get_figure()
        
        image_string : Optional[str] = None

        if fig:
            fig.savefig(buffer, format = "png", bbox_inches = 'tight')
            plt.close(fig)
            image_string = base64.b64encode(buffer.getbuffer()).decode("ascii")
            
        return image_string

    def create_box_plot_function(self, df : DataFrame, x_name : str, figsize : Tuple[int, int] = (5, 5)) -> Callable[[], None]:

        '''
            Returns a function that visualizes a box plot.

            Example:
            >>> func = PlotManager().create_box_plot_function(df = df , x_name = "seller_alias")
            >>> func()
        '''

        func : Callable[[], None] = lambda : self.show_box_plot(df = df, x_name = x_name, figsize = figsize)

        return func
    def create_box_plot_as_base64(self, df : DataFrame, x_name : str, figsize : Tuple[int, int] = (5, 5)) -> str:

        '''
            Returns a box plot as a base64 string.

            Example:            
            >>> plot_manager : PlotManager = PlotManager()
            >>> image_string : str = plot_manager.create_box_plot_as_base64(df = df, x_name = "seller_alias")
            >>> image_string = plot_manager.create_html_image_tag(image_string = image_string)
            >>> HTML(image_string)
        '''

        buffer : BytesIO = BytesIO()

        plt.figure(figsize = figsize)
        plt.boxplot(x = df[x_name], vert = False, tick_labels = [x_name])
        plt.savefig(buffer, format = "png", bbox_inches = 'tight')
        plt.close()

        image_string : str = base64.b64encode(buffer.getbuffer()).decode("ascii")

        return image_string

    def create_html_image_tag(self, image_string : str) -> str:

        '''Creates a <img /> HTML tag to display an image from the provided base64 string.'''

        return f'<img src="data:image/png;base64,{image_string}" />'
    def describe_dataframe(self, df : DataFrame, column_names : list[str]) -> DataFrame:
        
        '''Describes the provided dataframe according to the provided column names.'''

        describe_df = df[column_names].describe().apply(lambda s: s.apply(lambda x: format(x, 'g')))

        return describe_df
class DataFrameReverser():

    '''
        Encapsulates the logic to convert a dataframe object to some source code usable for creating it. 

        Based upon:
        https://stackoverflow.com/questions/41769882/pandas-dataframe-to-code
    '''

    def __convert_values_to_source_code(self, values : Any) -> str:

        '''Converts values to source code.'''

        values_str : str = str(values)
        values_str = re.sub(r" nan(?<![,\]])", " np.nan", values_str)
        
        return values_str
    def __convert_dtype_to_source_code(self, dtype : Any) -> str:

        '''Converts dtype to source code.'''

        dtype_str : str = str(dtype)
        dtype_str = re.sub(r"float64", " np.float64", dtype_str)
        dtype_str = re.sub(r"int64", " np.int64", dtype_str)

        return dtype_str
    def __clean_dataframe_string(self, df_str : str) -> str:

        '''Performs a sequence of cleaning procedures.'''

        # To fix: "TypeError: descriptor 'date' for 'datetime.datetime' objects doesn't apply to a 'int' object"
        df_str = df_str.replace("datetime.date(", "date(")

        return df_str        

    def convert_dataframe_to_source_code(self, df : DataFrame) -> str:

        '''Converts dataframe to source code.'''

        df_str : str = "pd.DataFrame({"

        for column in df.columns:
            values_str : str = self.__convert_values_to_source_code(df[column].values.tolist())
            dtype_str : Any = self.__convert_dtype_to_source_code(df.dtypes[column])
            df_str += f'\n\t\'{column}\': np.array({values_str}, dtype={dtype_str}),'

        df_str += "\n}"

        values_str = self.__convert_values_to_source_code(df.index)
        dtype_str = self.__convert_dtype_to_source_code(df.index.dtype)

        df_str += f', index=pd.{values_str}'
        df_str += ')'

        df_str = self.__clean_dataframe_string(df_str = df_str)

        return df_str
class Formatter():

    '''Collects all the logic related to formatting tasks.'''

    def format_to_iso_8601(self, dt : datetime, include_time : bool = False) -> str:

        '''
            "2023-08-03"
            "2023-08-03 17:22:15"
        '''

        if include_time == False:
            return dt.strftime(format = "%Y-%m-%d")
        else:
            return dt.strftime(format = "%Y-%m-%d %H:%M:%S")
    def format_usd_amount(self, amount : float64, rounding_digits : int) -> str:

        '''
            748.7 => 748.70 => "$748.70"
        '''

        rounded : float64 = amount.round(decimals = rounding_digits)
        formatted : str = f"${rounded:.2f}"

        return formatted
    def format_rating(self, rating : int) -> str:

        '''"★★★★★", "★★★★☆", ...'''

        black_star : str = "★"
        white_star : str = "☆"

        if rating == 1:
            return f"{black_star}{white_star*4}"
        elif rating == 2:
            return f"{black_star*2}{white_star*3}"
        elif rating == 3:
            return f"{black_star*3}{white_star*2}"
        elif rating == 4:
            return f"{black_star*4}{white_star*1}"
        elif rating == 5:
            return f"{black_star*5}"            
        else:
            return str(rating)
class Converter():

    '''Collects all the logic related to converting tasks.'''

    def convert_index_to_blanks(self, df : DataFrame) -> DataFrame:

        '''Converts the index of the provided DataFrame to blanks.'''

        blank_idx : list[str] = [''] * len(df)
        df.index = Index(blank_idx)

        return df
    def convert_index_to_one_based(self, df : DataFrame) -> DataFrame:

        '''Converts the index of the provided DataFrame from zero-based to one-based.'''

        df.index += 1

        return df
    def convert_date_to_datetime(self, dt : date) -> datetime:

        '''Converts provided date to datetime.'''

        return datetime(year = dt.year, month = dt.month, day = dt.day)
    def convert_word_count_to_A4_sheets(self, word_count : int) -> int:

        '''
            "[...], a typical page which has 1-inch margines and is typed with a 12-point font 
            with standard spacing elements will be approximately 500 words when typed single spaced."
        '''

        if word_count == 0:
            return 0

        A4_sheets : int = int(word_count / 500)
        A4_sheets += 1

        return A4_sheets
class LambdaProvider():

    '''Provides useful lambda functions.'''

    def get_default_logging_function(self) -> Callable[[str], None]:

        '''
            An adapter around print().
            Prints something like: "Some message"
        '''

        return lambda msg : print(msg)
    def get_timestamped_logging_function(self, now_function : Callable[[], datetime] = lambda : datetime.now()) -> Callable[[str], None]:

        '''
            An adapter around print(). 
            Prints something like: "[2023-08-03 17:22:15] Some message"
        '''

        dt_str : str = Formatter().format_to_iso_8601(dt = now_function(), include_time = True)

        return lambda msg : print(f"[{dt_str}] {msg}")
class MarkdownHelper():

    '''Collects a bunch of helper functions related to Markdown.'''

    __formatter : Formatter

    def __init__(self, formatter : Formatter) -> None:

        self.__formatter = formatter

    def get_markdown_header(self, last_update : datetime, paragraph_title : str) -> str:
        
        '''
            ## Revision History

            |Date|Author|Description|
            |---|---|---|
            |2020-12-22|numbworks|Created.|
            |2023-04-28|numbworks|Last update.|

            ## Reading List By Month
        '''

        lines : list[str] = [
            "## Revision History", 
            "", 
            "|Date|Author|Description|", 
            "|---|---|---|",
            "|2020-12-22|numbworks|Created.|",
            f"|{self.__formatter.format_to_iso_8601(dt = last_update)}|numbworks|Last update.|",
            "",
            f"## {paragraph_title}",
            ""
            ]

        markdown_header : str = "\n".join(lines)

        return markdown_header
    def add_subscript_tags_to_value(self, value : str) -> str:

        '''
        "49.99" => "<sub>49.99</sub>"
        '''

        tagged : str = f"<sub>{value}</sub>"

        return tagged
    def add_subscript_tags_to_dataframe(self, df : DataFrame) -> DataFrame:

        '''Adds subscript tags to every cell and column name of the provided DataFrame.'''

        tagged_df = df.copy(deep=True)
        
        tagged_df = tagged_df.map(func = self.add_subscript_tags_to_value)
        tagged_df = tagged_df.rename(columns = lambda column_name : self.add_subscript_tags_to_value(value = column_name))

        return tagged_df
    def format_file_name_as_content(self, file_name : str) -> str:

        '''Formats the provided file_name so that it can be displayed on the screen before the Markdown content.'''

        md_content : str = file_name
        md_content += "\n"
        md_content += ""

        return md_content
class Displayer():

    '''Adapter around IPython.core.display.display().'''

    def display(self, df : DataFrame, hide_index : bool = True, formatters : Optional[dict] = None) -> None:

        '''
            Displays df in Jupyter Notebook according to provided arguments.

            Example for 'formatters':

                formatters : dict = { "Price" : "{:.2f}" }
        '''

        styler : Styler = df.style.format()

        if formatters:
            styler = df.style.format(formatters)

        if hide_index:
            styler.hide()

        display(styler)

# MAIN
if __name__ == "__main__":
    pass