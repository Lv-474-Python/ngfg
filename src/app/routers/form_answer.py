from flask import request, jsonify
from flask_restx import Resource, fields
from flask_login import current_user
from app import API
from app.services import FieldService, FormService

name_space = API.namespace('form/<int:form_id>/answer', description='NgFg APIs')


@name_space.route("")
class AnswerAPI(Resource):

    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid Argument',
            500: 'Mapping Key Error'
        },
        params={'form_id': 'Specify the form_id'})
    def get(self, form_id):
        if current_user.is_anonymous:
            return jsonify('You are not logged in!')
        form = FormService.get_by_id(form_id)
        print(current_user.id)
        answers = ['blank']
        if form.owner_id == current_user.id:
            print("i'm here")
            answers = ["perfect"]
            #answers = [{'answers': str(res.answers),
            #                'user_id': res.user_id,
            #                'created': str(res.created)} for res in form.form_results]
        return {
            "title": form.title,
            "answers": answers
        }


    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid Argument',
            500: 'Mapping Key Error'},
        params={'id': 'Specify the Id associated with the person'})
#    @API.expect(model)
    def post(self):
        try:
            return {
                "status": "New person added",
            }
        except KeyError as e:
            name_space.abort(500,
                             e.__doc__,
                             status="Could not retrieve information",
                             statusCode="500")
        except Exception as e:
            name_space.abort(400,
                             e.__doc__,
                             status="Could not retrieve information",
                             statusCode="400")


@name_space.route("/<int:id>")
class AnswerSingleAPI(Resource):

    @API.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' },
             params={ 'id': 'Specify the Id associated with the person' })
    def get(self, id):
        try:
            return {
                "status": "Person retrieved"
            }
        except KeyError as e:
            name_space.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")

    @API.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' },
                params={ 'id': 'Specify the Id associated with the person'})
#    @API.expect(model)
    def post(self, id):
        try:
            return {
                "status": "New person added",
            }
        except KeyError as e:
            name_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")