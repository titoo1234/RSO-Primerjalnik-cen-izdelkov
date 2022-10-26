"""Code for the flask app."""
#import sys
#sys.path.append("./")
from flask import Flask
from flask_restful import Api#, Resource, reqparse

#import logging

#resources
#from catalog import catalog
# from Presentation.Resources.ScriptCalculationResource import ScriptCalculationResource
# from Presentation.Resources.ScriptMultipleCalculationResource import ScriptMultipleCalculationResource
# from Presentation.Resources.PickleCalculationResource import PickleCalculationResource
# from Presentation.Resources.TestCalculationResource import TestCalculationResource
# from Presentation.Resources.FileCalculationResource import FileCalculationResource
# from Presentation.Resources.UserResource import UserResource
# from Presentation.Resources.CheckScriptResources import CheckScriptResource
# from Presentation.Resources.DBCalculationResource import DBCalculationResource
# from Presentation.Resources.GeneralPickleCalculationResource import GeneralPickleCalculationResource
# from Presentation.Resources.GetMethodsPickleResource import GetMethodsPickleResource

def create_app():
    app = Flask(__name__)
    api = Api(app)
#     api.add_resource(ScriptCalculationResource, '/do_work_script')
#     api.add_resource(ScriptMultipleCalculationResource, '/do_work_script_m')
#     api.add_resource(PickleCalculationResource, '/do_work_pkl')
#     api.add_resource(TestCalculationResource, '/test')
#     api.add_resource(FileCalculationResource, '/do_work_script_file')
#     api.add_resource(UserResource, '/login')
#     api.add_resource(CheckScriptResource, '/check_script')
#     api.add_resource(DBCalculationResource, '/database')
#     api.add_resource(GeneralPickleCalculationResource, '/do_work_pkl_general')
#     api.add_resource(GetMethodsPickleResource, '/methods_pkl')
    return app

#logging.basicConfig(filename='record.log', level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = create_app()
if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)