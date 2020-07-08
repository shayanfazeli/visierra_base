from flask import Blueprint
from application import admin
bp = Blueprint('vis', __name__)
from application.blueprints.visualizations.views import VisualizationsPortfolio, VisualizationPalette, TableBoard
admin.add_view(VisualizationsPortfolio(name="Portfolio", endpoint='portfolio', menu_icon_type='fa', menu_icon_value='fa-book',))
admin.add_view(VisualizationPalette(name="Palette", endpoint='palette', menu_icon_type='fa', menu_icon_value='fa-area-chart',))
admin.add_view(TableBoard(name="Sample Table", endpoint='table_board', menu_icon_type='fa', menu_icon_value='fa-address-book',))
