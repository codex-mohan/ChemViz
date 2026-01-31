# Views module
from .dashboard import DashboardView
from .upload import UploadView
from .data_table import DataTableView
from .charts import ChartsView
from .history import HistoryView
from .report import ReportView
from .auth import AuthView

__all__ = [
    'DashboardView', 
    'UploadView', 
    'DataTableView', 
    'ChartsView',
    'HistoryView',
    'ReportView',
    'AuthView'
]
