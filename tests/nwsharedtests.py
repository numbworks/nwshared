# GLOBAL MODULES
import copy
import os
import pandas as pd
import requests
import sys
import unittest
from contextlib import redirect_stdout
from datetime import date, datetime
from io import StringIO
from numpy import float64
from pandas import DataFrame, Index
from pandas.io.formats.style import Styler
from pandas.testing import assert_frame_equal
from parameterized import parameterized
from typing import Any, Callable, Optional, Tuple, Union, cast
from unittest import mock
from unittest.mock import Mock, call, mock_open, patch

# LOCAL MODULES
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from nwshared import OutlierManager, FilePathManager, FileManager, PageManager
from nwshared import PlotManager, PlotKind, DataFrameReverser, Formatter
from nwshared import Converter, LambdaProvider, Displayer, MarkdownHelper

# SUPPORT METHODS
class ObjectMother():

    '''Collects all the DTOs required by the unit tests.'''

    @staticmethod
    def create_remaining_days_dataframe(return_empty : bool = False) -> DataFrame:

        df_data : dict = {
            "remaining_days": [1234, 30, 7, 6, 6, 6, 2, 2, 2, 1, 1, 1, 1, -13]
            }
        df_index : list[int] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        df : DataFrame = pd.DataFrame(data = df_data, index=df_index)

        if return_empty:
            return df.drop(df.index)

        return df

# TEST CLASSES
class OutlierManagerTestCase(unittest.TestCase):

    def test_tryremovelowerboundoutliers_shouldremoveoutlier_whencolumnvaluesmatchcriteria(self):
        
        # Arrange
        df : DataFrame = ObjectMother.create_remaining_days_dataframe()
        expected_df : DataFrame = df.drop(df.index[-1])     # delete last row (-13)
        cn_remaining_days : str = "remaining_days"

        # Act
        actual_df : DataFrame = OutlierManager().try_remove_lower_bound_outliers(df = df, column_name = cn_remaining_days)

        # Assert
        assert_frame_equal(expected_df , actual_df)
    def test_tryremovelowerboundoutliers_shoulddonothing_whendataframeisempty(self):
        
        # Arrange
        df : DataFrame = ObjectMother.create_remaining_days_dataframe(return_empty = True)
        expected_df : DataFrame = df.copy(deep=True)
        cn_remaining_days : str = "remaining_days"

        # Act
        actual_df : DataFrame = OutlierManager().try_remove_lower_bound_outliers(df = df, column_name = cn_remaining_days)

        # Assert
        assert_frame_equal(expected_df , actual_df)   
    def test_tryremoveupperboundoutliers_shouldremoveoutlier_whencolumnvaluesmatchcriteria(self):
        
        # Arrange
        df : DataFrame = ObjectMother.create_remaining_days_dataframe()
        expected_df : DataFrame = df.drop(df.index[0])      # delete first row (1234)
        cn_remaining_days : str = "remaining_days"

        # Act
        actual_df : DataFrame = OutlierManager().try_remove_upper_bound_outliers(df = df, column_name = cn_remaining_days)

        # Assert
        assert_frame_equal(expected_df , actual_df)
    def test_tryremoveupperboundoutliers_shoulddonothing_whendataframeisempty(self):
        
        # Arrange
        df : DataFrame = ObjectMother.create_remaining_days_dataframe(return_empty = True)
        expected_df : DataFrame = df.copy(deep=True)
        cn_remaining_days : str = "remaining_days"

        # Act
        actual_df : DataFrame = OutlierManager().try_remove_upper_bound_outliers(df = df, column_name = cn_remaining_days)

        # Assert
        assert_frame_equal(expected_df , actual_df) 
    def test_tryremovelowerboundoutliers_shouldraiseanexception_whencolumndoesnotexist(self):
        
		# Arrange
        df : DataFrame = pd.DataFrame({"A" : [1, 2, 3]})
        column_name : str = "B"
        outlier_manager : OutlierManager = OutlierManager()

        # Act
        actual : DataFrame = outlier_manager.try_remove_lower_bound_outliers(df = df, column_name = column_name)

        # Assert
        self.assertTrue(actual.equals(df))
    def test_tryremoveupperboundoutliers_shouldraiseanexception_whencolumndoesnotexist(self):
        
		# Arrange
        df : DataFrame = pd.DataFrame({"A" : [1, 2, 3]})
        column_name : str = "B"
        outlier_manager : OutlierManager = OutlierManager()

        # Act
        actual : DataFrame = outlier_manager.try_remove_upper_bound_outliers(df = df, column_name = column_name)

        # Assert
        self.assertTrue(actual.equals(df))
class FilePathManagerTestCase(unittest.TestCase):

    def test_createfilepath_shouldreturnexpectedfilepath_whenproperarguments(self):
        
        '''"C:/", "somefile.txt" => "C:/somefile.txt"'''

        # Arrange
        # Act
        actual : str = FilePathManager().create_file_path(folder_path = "C:/", file_name = "somefile.txt")
        
        # Assert
        self.assertEqual("C:/somefile.txt", actual)
    def test_createnumberedfilepath_shouldreturnexpectedfilepath_whenproperarguments(self):

        '''"C:/", "html" => "C:/1.html"'''        
        
        # Arrange
        
        # Act
        actual : str = FilePathManager().create_numbered_file_path(folder_path = "C:/", number = 1, extension = "html")
        
        # Assert
        self.assertEqual("C:/1.html", actual)
    def test_createnumberedfilepaths_shouldreturnexpectedfilepaths_whenproperarguments(self):

        '''
            "C:/", 1, 3 => [ "C:/1.html", "C:/2.html" ]
        ''' 

        # Arrange
        expected : list[str] = ["C:/1.html", "C:/2.html"]

        # Act
        actual : list[str] = FilePathManager().create_numbered_file_paths(folder_path = "C:/", range_start = 1, range_end = 3, extension = "html")
        
        # Assert
        self.assertEqual(expected, actual)
class FileManagerTestCase(unittest.TestCase):

    def test_removefiles_shouldremoveallfileswithprovidedextensions_whenfilesareinworkingfolder(self):
        
        # Arrange
        file_names : list[str] = [
            "0.html",
            "1.html",
            "0.json",
            "dataframe.csv",
            "log.txt"
        ]
        extensions : list[str] = ["html"]
        working_folder_path : str = "C:/nwshared/"

        # Act
        file_manager : FileManager = FileManager(file_path_manager = FilePathManager())
        with patch.object(os, 'listdir', return_value = file_names) as mocked_listdir:
            with patch.object(os, 'remove', return_value = None) as mocked_remove:
                file_manager.remove_files(extensions = extensions, working_folder_path = working_folder_path)

        # Assert
        self.assertEqual(2, mocked_remove.call_count)
        mocked_remove.assert_has_calls([ 
            call(os.path.join(working_folder_path, file_names[0])),
            call(os.path.join(working_folder_path, file_names[1]))
        ])
    def test_removefiles_shoulddonothing_whenfilesarenotinworkingfolder(self):
        
        # Arrange
        file_names : list[str] = [
            "0.json",
            "dataframe.csv",
            "log.txt"
        ]
        extensions : list[str] = ["html"]
        working_folder_path : str = "C:/nwshared/"

        # Act
        file_manager : FileManager = FileManager(file_path_manager = FilePathManager())
        with patch.object(os, 'listdir', return_value = file_names) as mocked_listdir:
            with patch.object(os, 'remove', return_value = None) as mocked_remove:
                file_manager.remove_files(extensions = extensions, working_folder_path = working_folder_path)

        # Assert
        self.assertEqual(0, mocked_remove.call_count)
    def test_loadcontent_shouldreadfilecontent_whenproperarguments(self):

        # Arrange
        file_path : str = "C:/0.html"
        content : str = "Some content."

        # Act
        file_manager : FileManager = FileManager(file_path_manager = FilePathManager())        
        with patch("builtins.open", mock_open(read_data = content)) as mocked_open:
            actual : str = file_manager.load_content(file_path = file_path)

        # Assert
        mocked_open.assert_has_calls([ 
            call(file_path, 'r', encoding='utf-8'),
            call().__enter__(),
            call().read(),
            call().__exit__(None, None, None)
        ])
    def test_loadcontents_shouldreadfilecontents_whenproperarguments(self):
        
        # Arrange
        file_names : list[str] = [
            "0.html",
            "1.html",
            "0.json",
            "dataframe.csv",
            "log.txt"
        ]
        extension : str = "html"
        working_folder_path : str = "C:/nwshared/"
        content : str = "Some content."        

        # Act
        file_manager : FileManager = FileManager(file_path_manager = FilePathManager())
        with patch.object(os, 'listdir', return_value = file_names) as mocked_listdir:
            with patch("builtins.open", mock_open(read_data = content)) as mocked_open:
                actual : list[str] = file_manager.load_contents(working_folder_path = working_folder_path, extension = extension)

        # Assert
        self.assertEqual(2, mocked_open.call_count)
        mocked_open.assert_has_calls([ 
            call(os.path.join(working_folder_path, file_names[0]), 'r', encoding='utf-8'),
            call().__enter__(),
            call().read(),
            call().__exit__(None, None, None),            
            call(os.path.join(working_folder_path, file_names[1]), 'r', encoding='utf-8'),
            call().__enter__(),
            call().read(),
            call().__exit__(None, None, None)
        ])
    def test_savecontent_shouldwritecontenttofile_whenproperarguments(self):

        # Arrange
        file_path : str = "C:/0.html"
        content : str = "Some content."

        # Act
        file_manager : FileManager = FileManager(file_path_manager = FilePathManager())        
        with patch("builtins.open", mock_open()) as mocked_open:
            file_manager.save_content(content = content, file_path = file_path)

        # Assert
        mocked_open.assert_has_calls([ 
            call(file_path, 'w', encoding='utf-8'),
            call().__enter__(),
            call().write(content),
            call().__exit__(None, None, None)
        ])
    def test_savecontents_shouldwritecontentstofiles_whenproperarguments(self):

        # Arrange
        file_paths : list[str] = [ 
            "C:/0.html", 
            "C:/1.html" 
        ]
        contents : list[str] = [ 
            "Some content.", 
            "Some content."
        ]

        # Act
        file_manager : FileManager = FileManager(file_path_manager = FilePathManager())        
        with patch("builtins.open", mock_open()) as mocked_open:
            file_manager.save_contents(contents = contents, file_paths = file_paths)

        # Assert
        self.assertEqual(2, mocked_open.call_count)            
        mocked_open.assert_has_calls([ 
            call(file_paths[0], 'w', encoding='utf-8'),
            call().__enter__(),
            call().write(contents[0]),
            call().__exit__(None, None, None),            
            call(file_paths[1], 'w', encoding='utf-8'),
            call().__enter__(),
            call().write(contents[1]),
            call().__exit__(None, None, None)
        ])
    def test_savelog_shouldwritecontentsasloglinestofile_whenproperarguments(self):

        # Arrange
        working_folder_path : str = "C:/nwshared/"
        file_name : str = "log.txt"
        contents : list[str] = [
            "[2024-03-16 23:13:19] Analysis session started.",
            "[2024-03-16 23:13:19] The dataframe has been successfully created.",
            "[2024-03-16 23:13:19] Analysis session completed."
        ]
        file_path : str = "C:/nwshared/log.txt"
        lines : list[str] = [
            "[2024-03-16 23:13:19] Analysis session started.",
            "\n",
            "[2024-03-16 23:13:19] The dataframe has been successfully created.",
            "\n",            
            "[2024-03-16 23:13:19] Analysis session completed.",
            "\n"            
        ]

        # Act
        file_manager : FileManager = FileManager(file_path_manager = FilePathManager())        
        with patch("builtins.open", mock_open()) as mocked_open:
            file_manager.save_log(contents = contents, working_folder_path = working_folder_path, file_name = file_name)

        # Assert
        mocked_open.assert_has_calls([ 
            call(file_path, 'w', encoding='utf-8'),
            call().__enter__(),
            call().writelines(lines),
            call().__exit__(None, None, None)
        ])
class PageManagerTestCase(unittest.TestCase):

    def test_getpagecontent_shouldperformonegetrequest_whenpageurl(self):
        
        # Arrange
        fake_response = mock.MagicMock()
        fake_response.return_value.text = "<html><body>Some content</body></html>"
        page_url : str = "http://www.somewebsite.com/somepage"

        # Act
        with patch.object(requests, "get", fake_response) as mocked_get:
            actual : str = PageManager().get_page_content(page_url = page_url)

        # Assert
        mocked_get.assert_called_once()
    def test_getpagecontents_shouldperformtwogetrequests_whentwopageurl(self):
        
        # Arrange
        fake_response = mock.MagicMock()
        fake_response.return_value.text = "<html><body>Some content</body></html>"
        page_urls : list[str] = [ 
            "http://www.somewebsite.com/somepage",
            "http://www.somewebsite.com/someotherpage"
        ]

        # Act
        with patch.object(requests, "get", fake_response) as mocked_get:
            actual : list[str] = PageManager().get_page_contents(page_urls = page_urls)

        # Assert
        self.assertEqual(2, mocked_get.call_count)
    def test_decodeunicodecharacters_shouldreturnexpectedstring_wheninvoked(self):

        # Arrange
        # Act
        actual : str = PageManager().decode_unicode_characters(string = "Antikt \u0026 Design")     
        
        # Assert
        self.assertEqual("Antikt & Design", actual)          
class PlotManagerTestCase(unittest.TestCase):

    @patch("pandas.DataFrame.plot")
    def test_showplot_shouldbecalledwithprovidedarguments_wheninvoked(self, mock_plot) -> None:

        # Arrange
        df : DataFrame = DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        plot_kind : PlotKind = PlotKind.BAR
        x_name : str = "A"
        y_name : str = "B"
        figsize : Tuple[int, int] = (5, 5)

        # Act
        PlotManager().show_plot(df = df, plot_kind = plot_kind, x_name = x_name, y_name = y_name, figsize = figsize)

        # Assert
        mock_plot.assert_called_once_with(
            x = x_name, 
            y = y_name, 
            legend = True, 
            kind = plot_kind.value, 
            title = f"{y_name} by {x_name}", 
            figsize=figsize
            )
    def test_createplotfunction_shouldreturnacallableobjectthatrunsasexpected_wheninvoked(self) -> None:

        # Arrange
        df : DataFrame = DataFrame({"seller_alias": ["A", "B", "C"], "items": [10, 20, 30]})
        plot_kind : PlotKind = PlotKind.BAR
        x_name : str = "seller_alias"
        y_name : str = "items"
        figsize : Tuple[int, int] = (5, 5)

        # Act
        func : Callable[[], None] = PlotManager().create_plot_function(df = df, plot_kind = plot_kind, x_name = x_name, y_name = y_name, figsize = figsize)

        # Assert
        self.assertTrue(callable(func))
        func() # Ensures that the function runs without error.
    def test_createplotasbase64_shouldreturnexpectedstring_wheninvoked(self) -> None:
        
        # Arrange
        df : DataFrame = DataFrame({"seller_alias": ["A", "B", "C"], "items": [10, 20, 30]})
        plot_kind : PlotKind = PlotKind.BAR
        x_name : str = "seller_alias"
        y_name : str = "items"
        figsize : Tuple[int, int] = (5, 5)

        # Act
        actual : Optional[str] = PlotManager().create_plot_as_base64(df = df, plot_kind = plot_kind, x_name = x_name, y_name = y_name, figsize = figsize)
        actual_str : str = cast(str, actual)

        # Assert
        self.assertTrue(actual_str.startswith("iVBORw0KGgo"))

    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.figure')
    @patch('matplotlib.pyplot.boxplot')
    def test_showboxplot_shouldbecalledwithprovidedarguments_wheninvoked(self, mock_boxplot, mock_figure, mock_show) -> None:

        # Arrange
        df : DataFrame = DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        x_name : str = "A"
        figsize : Tuple[int, int] = (5, 5)

        # Act
        PlotManager().show_box_plot(df = df, x_name = x_name)

        # Assert
        mock_figure.assert_called_once_with(figsize = figsize)
        mock_boxplot.assert_called_once_with(x = df[x_name], vert = False, tick_labels = [x_name])
        mock_show.assert_called_once()
    def test_createboxplotfunction_shouldreturnacallableobjectthatrunsasexpected_wheninvoked(self) -> None:
        
        # Arrange
        df : DataFrame = pd.DataFrame({"seller_alias": [1, 2, 3, 4, 5]})
        x_name : str = "seller_alias"
        figsize : Tuple[int, int] = (5, 5)

        # Act
        func : Callable[..., Any] = PlotManager().create_box_plot_function(df = df, x_name = x_name, figsize = figsize)

        # Assert
        self.assertTrue(callable(func))
        func() # Ensures that the function runs without error.
    def test_createboxplotasbase64_shouldreturnexpectedstring_wheninvoked(self) -> None:
        
        # Arrange
        df : DataFrame = pd.DataFrame({"seller_alias": [1, 2, 3, 4, 5]})
        x_name : str = "seller_alias"
        figsize : Tuple[int, int] = (5, 5)

        # Act
        actual : str = PlotManager().create_box_plot_as_base64(df = df, x_name = x_name, figsize = figsize)

        # Assert
        self.assertTrue(actual.startswith("iVBORw0KGgo"))

    def test_createhtmlimagetag_shouldreturnexpectedstring_wheninvoked(self):
        
        # Arrange
        image_string : str = "c29tZWltYWdlc3RyaW5n"
        expected : str = f'<img src="data:image/png;base64,{image_string}" />'

        # Act
        actual : str = PlotManager().create_html_image_tag(image_string = image_string)
        
        # Assert
        self.assertEqual(expected, actual)
    def test_describedataframe_shouldreturnexpecteddataframe_wheninvoked(self) -> None:

        # Arrange
        df : DataFrame = pd.DataFrame({
                    "A": [1, 2, 3, 4, 5],
                    "B": [5, 4, 3, 2, 1]
                })
        column_names : list[str] = ["A", "B"]
        expected_df : DataFrame = pd.DataFrame({
            "A": ["5", "3", "1.58114", "1", "2", "3", "4", "5"],
            "B": ["5", "3", "1.58114", "1", "2", "3", "4", "5"]
        }, index=["count", "mean", "std", "min", "25%", "50%", "75%", "max"])
        
        # Act
        actual_df : DataFrame = PlotManager().describe_dataframe(df = df, column_names = column_names)
        
        # Assert
        assert_frame_equal(actual_df, expected_df)
class DataFrameReverserTestCase(unittest.TestCase):

    def test_convertdataframetosource_code_shouldreturnexpectedstring_wheninvoked(self):
        
        # Arrange
        df : DataFrame = ObjectMother.create_remaining_days_dataframe()
        expected : str = "pd.DataFrame({\n\t'remaining_days': np.array([1234, 30, 7, 6, 6, 6, 2, 2, 2, 1, 1, 1, 1, -13], dtype= np.int64),\n}, index=pd.Index([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], dtype='int64'))"
               
        # Act
        actual : str = DataFrameReverser().convert_dataframe_to_source_code(df = df)

        # Assert
        self.assertEqual(expected, actual)
class FormatterTestCase(unittest.TestCase):

    def test_formattoiso8601_shouldreturnexpectedstring_whenincludetimeisfalse(self):
        
        # Arrange
        dt : datetime = datetime(year = 2023, month = 8, day = 3)
        expected : str = "2023-08-03"

        # Act
        actual : str = Formatter().format_to_iso_8601(dt = dt, include_time = False)

        # Assert
        self.assertEqual(expected, actual)
    def test_formattoiso8601_shouldreturnexpectedstring_whenincludetimeistrue(self):
        
        # Arrange
        dt : datetime = datetime(year = 2023, month = 8, day = 3, hour = 17, minute = 22, second = 15)
        expected : str = "2023-08-03 17:22:15"

        # Act
        actual : str = Formatter().format_to_iso_8601(dt = dt, include_time = True)

        # Assert
        self.assertEqual(expected, actual)
    def test_formatusdamount_shouldreturnexpectedstring_wheninvoked(self):
        
        # Arrange
        amount : float64 = float64(748.7)
        rounding_digits : int = 2
        expected : str = "$748.70"

        # Act
        actual : str = Formatter().format_usd_amount(amount = amount, rounding_digits = rounding_digits)

        # Assert
        self.assertEqual(expected, actual)

    @parameterized.expand([
        [5, "★★★★★"],
        [4, "★★★★☆"],
        [3, "★★★☆☆"],
        [2, "★★☆☆☆"],
        [1, "★☆☆☆☆"],
        [0, "0"]
    ])
    def test_formatrating_shouldreturnexpectedstring_wheninvoked(self, rating : int, expected : str):
        
        # Arrange
        # Act
        actual : str = Formatter().format_rating(rating = rating)

        # Assert
        self.assertEqual(expected, actual)
class ConverterTestCase(unittest.TestCase):

    @parameterized.expand([
        [0, 0],
        [12, 1],
        [499, 1],
        [500, 2],
        [999, 2],
        [1000, 3],        
    ])
    def test_convertwordcounttoA4sheets_shouldreturnexpectedint_wheninvoked(self, word_count : int, expected : int):
        
        # Arrange
        # Act
        actual : int = Converter().convert_word_count_to_A4_sheets(word_count = word_count)

        # Assert
        self.assertEqual(expected, actual)

    def test_convertindextoblanks_shouldreturnexpectedindex_wheninvoked(self):

        # Arrange
        df: DataFrame = DataFrame({'A': [1, 2, 3]})
        expected: list[str] = [''] * len(df)

        # Act
        actual_df: DataFrame = Converter().convert_index_to_blanks(df = df)

        # Assert
        self.assertEqual(list(actual_df.index), expected)
    def test_convertindextoonebased_shouldreturnexpectedindex_wheninvoked(self):
        
        # Arrange
        df: DataFrame = DataFrame({'A': [1, 2, 3]})
        df.index = Index([0, 1, 2])
        expected: list[int] = [1, 2, 3]

        # Act
        actual_df: DataFrame = Converter().convert_index_to_one_based(df = df)

        # Assert
        self.assertEqual(list(actual_df.index), expected)
    def test_convertdatetodatetime_shouldreturnexpecteddate_wheninvoked(self):

        # Arrange
        dt : date = date(2023, 1, 1)
        expected: datetime = datetime(2023, 1, 1)

        # Act
        actual : datetime = Converter().convert_date_to_datetime(dt)

        # Assert
        self.assertEqual(actual, expected)
class LambdaProviderTestCase(unittest.TestCase):

    @parameterized.expand([
        ["Some message", "Some message"]      
    ])
    def test_getdefaultloggingfunction_shouldreturnexpectedmessage_wheninvoked(self, msg : str, expected : str):
        
        # Arrange
        lambda_provider : LambdaProvider = LambdaProvider()
        logging_function : Callable[[str], None] = lambda_provider.get_default_logging_function() 

        # Act
        # Assert                
        with StringIO() as buf, redirect_stdout(buf):
          
            logging_function(msg)
            actual : str = buf.getvalue().replace("\n", "")

            self.assertEqual(expected, actual)

    def test_gettimestampedloggingfunction_shouldreturnexpectedmessage_wheninvoked(self):
        
        # Arrange
        dt : datetime = datetime(year = 2023, month = 8, day = 3, hour = 17, minute = 22, second = 15)
        now_function : Callable[[], datetime] = lambda : dt

        lambda_provider : LambdaProvider = LambdaProvider()
        logging_function : Callable[[str], None] = lambda_provider.get_timestamped_logging_function(now_function = now_function) 

        msg : str = "Some message"        
        expected : str = "[2023-08-03 17:22:15] Some message"

        # Act
        # Assert                
        with StringIO() as buf, redirect_stdout(buf):
          
            logging_function(msg)
            actual : str = buf.getvalue().replace("\n", "")

            self.assertEqual(expected, actual)
class MarkdownHelperTestCase(unittest.TestCase):

    def test_getmarkdownheader_shouldreturnexpectedstring_wheninvoked(self):
        
        # Arrange
        last_update : datetime = datetime(2023, 4, 28)
        paragraph_title : str = "Reading List By Month"
        
        lines : list[str] = [
            "## Revision History",
            "",
            "|Date|Author|Description|",
            "|---|---|---|",
            "|2020-12-22|numbworks|Created.|",
            "|2023-04-28|numbworks|Last update.|",
            "",
            "## Reading List By Month",
            ""
        ]
        expected : str = "\n".join(lines)
        markdown_helper : MarkdownHelper = MarkdownHelper(formatter = Formatter())

        # Act
        actual : str = markdown_helper.get_markdown_header(last_update = last_update, paragraph_title = paragraph_title)

        # Assert
        self.assertEqual(expected, actual)

    @parameterized.expand([
        ["49.99", "<sub>49.99</sub>"]
    ])
    def test_addsubscripttagstovalue_shouldreturnexpectedstring_wheninvoked(self, value : str, expected : str):
        
        # Arrange
        markdown_helper : MarkdownHelper = MarkdownHelper(formatter = Formatter())

        # Act
        actual : str = markdown_helper.add_subscript_tags_to_value(value = value)

        # Assert
        self.assertEqual(expected, actual)

    def test_addsubscripttagstodataframe_shouldreturnexpecteddataframe_wheninvoked(self):

        # Arrange
        df : DataFrame = pd.DataFrame({
            'A': ['1', '2'],
            'B': ['3', '4']
        })
        expected_df : DataFrame = pd.DataFrame({
            '<sub>A</sub>': ['<sub>1</sub>', '<sub>2</sub>'],
            '<sub>B</sub>': ['<sub>3</sub>', '<sub>4</sub>']
        })        
        markdown_helper : MarkdownHelper = MarkdownHelper(formatter = Formatter())

        # Act
        actual_df : DataFrame = markdown_helper.add_subscript_tags_to_dataframe(df = df)

        # Assert
        assert_frame_equal(actual_df, expected_df)
    def test_formatfilenameascontent_shouldreturnexpectedstring_wheninvoked(self):

        # Arrange
        file_name : str = "example.txt"
        expected : str = "example.txt\n"
        markdown_helper : MarkdownHelper = MarkdownHelper(formatter = Formatter())

        # Act
        actual : str = markdown_helper.format_file_name_as_content(file_name = file_name)
        
        # Assert
        self.assertEqual(actual, expected)
class DisplayerTestCase(unittest.TestCase):

    def setUp(self) -> None:

        self.df : DataFrame = DataFrame({"A": [1.123456, 2.654321], "B": [3.987654, 4.123456]})
        self.formatters : Optional[dict] = {"A" : "{:.2f}"}

        self.styled_df : DataFrame = DataFrame('', index = self.df.index, columns = self.df.columns)
        self.styled_df.iloc[0, 0] = f"background-color: lightgreen"
        self.styler : Styler = self.df.style.apply(lambda _ : self.styled_df, axis = None)

    def test_displaydf_shouldcallstyle_whenhideindexisfalseandformattersisnone(self):
        
        # Arrange
        hide_index : bool = False

        # Act, Assert
        with redirect_stdout(None):
            with patch.object(DataFrame, "style") as style:
    
                # Act
                Displayer()._Displayer__display_df(df = self.df, hide_index = hide_index, formatters = None) # type: ignore

                # Assert
                style.format.assert_has_calls([call()])
    def test_displaydf_shouldcallstyle_whenhideindexisfalseandformattersisnotnone(self):
        
        # Arrange
        hide_index : bool = False

        # Act, Assert
        with redirect_stdout(None):
            with patch.object(DataFrame, "style") as style:
    
                # Act
                Displayer()._Displayer__display_df(df = self.df, hide_index = hide_index, formatters = self.formatters) # type: ignore

                # Assert
                style.format.assert_has_calls([call(), call(self.formatters)])
    def test_displaydf_shouldcallhide_whenhideindexistrue(self):
        
        # Arrange
        hide_index : bool = True

        # Act, Assert
        with redirect_stdout(None):
            with patch.object(Styler, "hide") as hide:
    
                # Act
                Displayer()._Displayer__display_df(df = self.df, hide_index = hide_index) # type: ignore

                # Assert
                self.assertTrue(hide.called)
    def test_displaydf_shouldnotcallhide_whenhideindexisfalse(self):
        
        # Arrange
        hide_index : bool = False

        # Act, Assert
        with redirect_stdout(None):
            with patch.object(Styler, "hide") as hide:
    
                # Act
                Displayer()._Displayer__display_df(df = self.df, hide_index = hide_index) # type: ignore

                # Assert
                self.assertFalse(hide.called)

    def test_displaystyler_shouldcalldeepcopy_wheninvoked(self):
        
        # Arrange
        # Act, Assert
        with patch.object(copy, "deepcopy") as deepcopy:

            # Act
            Displayer()._Displayer__display_styler(styler = self.styler, hide_index = False, formatters = None) # type: ignore

            # Assert
            deepcopy.assert_called_once()
    def test_displaystyler_shouldcallformat_whenhideindexisfalseandformattersisnotnone(self):
        
        # Arrange
        # Act, Assert
        with redirect_stdout(None):
            with patch.object(Styler, "format") as format:        
        
                # Act
                Displayer()._Displayer__display_styler(styler = self.styler, hide_index = False, formatters = self.formatters) # type: ignore

                # Assert
                format.assert_called_with(self.formatters)
    def test_displaystyler_shouldcallhide_whenhideindexistrue(self):
        
        # Arrange
        hide_index : bool = True

        # Act, Assert
        with redirect_stdout(None):
            with patch.object(Styler, "hide") as hide:        
        
                # Act
                Displayer()._Displayer__display_styler(styler = self.styler, hide_index = hide_index) # type: ignore

                # Assert
                hide.assert_called()
    def test_displaystyler_shouldnotcallhide_whenhideindexisfalse(self):
        
        # Arrange
        hide_index : bool = False

        # Act, Assert
        with redirect_stdout(None):
            with patch.object(Styler, "hide") as hide:        
        
                # Act
                Displayer()._Displayer__display_styler(styler = self.styler, hide_index = hide_index) # type: ignore

                # Assert
                self.assertFalse(hide.called)

    def test_display_shouldcalldisplaydf_whenobjisdataframe(self):

        # Arrange
        hide_index : bool = True

        # Act, Assert
        with patch.object(Displayer, "_Displayer__display_df") as display_df:

            # Act
            Displayer().display(obj = self.df, hide_index = hide_index, formatters = self.formatters)

            # Assert
            display_df.assert_called_once_with(df = self.df, hide_index = hide_index, formatters = self.formatters)
    def test_display_shouldcalldisplaystyler_whenobjisstyler(self):

        # Arrange
        hide_index : bool = True

        # Act, Assert
        with patch.object(Displayer, "_Displayer__display_styler") as display_styler:

            # Act
            Displayer().display(obj = self.styler, hide_index = hide_index, formatters = None)

            # Assert
            display_styler.assert_called_once_with(styler = self.styler, hide_index = hide_index, formatters = None)

    def test_displaycascade_shouldcalldisplayforeachobject_whenobjsislist(self):

        # Arrange
        hide_index : bool = True
        objs : list[Union[DataFrame, Styler]] = [self.df, self.styler]
        
        with patch.object(Displayer, "display") as display:

            # Act
            Displayer().display_cascade(objs = objs, hide_index = hide_index, formatters = self.formatters)

            # Assert
            self.assertEqual(display.call_count, len(objs))

# Main
if __name__ == "__main__":
    result = unittest.main(argv=[''], verbosity=3, exit=False)