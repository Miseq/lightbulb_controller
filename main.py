import time
from flask import Flask, make_response, jsonify
from controller_mqtt_client import ControllerMQTT
from flask import request
from flask.views import MethodView

app = Flask(__name__)
controller = ControllerMQTT("Krzysiek", 'lightbulbs', True)


class AllLighbutlbs(MethodView):
    @staticmethod
    def get():
        output = controller.show_lightbulbs("")
        return make_response(jsonify(output), 200)

    @staticmethod
    def post():
        data = request.get_json()
        condition = data.get("condition")
        controller.change_lightbulbs_status(condition)
        time.sleep(0.5)
        output = controller.show_lightbulbs("")
        return make_response(jsonify(output), 200)

    @staticmethod
    def delete():
        controller.sql_client.delete_table()
        controller.sql_client.create_table_if_dosent_exists(controller.sql_client.table_name)
        return make_response(jsonify("Usunieto wszystkie rekordy"), 200)


class OnOnlyLightbulbs(MethodView):
    @staticmethod
    def get():
        output = dict(controller.show_lightbulbs("ON"))
        return output


class OffOnlyLightbulbs(MethodView):
    @staticmethod
    def get():
        output = dict(controller.show_lightbulbs("OFF"))
        return output


class SingleLightbulb(MethodView):
    @staticmethod
    def get(lightbulb_id):
        try:
            output = dict(controller.show_lightbulbs(lightbulb_id))
            return make_response(jsonify(output), 200)
        except TypeError:
            return make_response(jsonify("Nie znaleziono urzadzenia o takim lightbulb_id"), 404)

    @staticmethod
    def post(lightbulb_id):
        try:
            data = request.get_json()
            condition = data.get("condition")
            controller.change_lightbulbs_status(condition, lightbulb_id)
            time.sleep(0.5)
            output = dict(controller.show_lightbulbs(lightbulb_id))
            return make_response(jsonify(output), 200)
        except TypeError:
            return make_response(jsonify("Nie znaleziono urzadzenia o takim lightbulb_id"), 404)

    @staticmethod
    def delete(lightbulb_id):
        try:
            output = controller.delete_lightbulb_from_db(lightbulb_id)
            return make_response(jsonify(output), 200)
        except TypeError:
            return make_response(jsonify("Nie znaleziono urzadzenia o takim lightbulb_id"), 404)


class Conection(MethodView):
    @staticmethod
    def get():
        return make_response(jsonify(controller.is_connected()), 200)

    @staticmethod
    def delete():
        controller.disconnect()
        return make_response(jsonify(f"Polaczenie z brokerem zakonczone"))


app.add_url_rule("/api/lightbulbs/on", view_func=OnOnlyLightbulbs.as_view("on_only"))
app.add_url_rule("/api/lightbulbs/off", view_func=OffOnlyLightbulbs.as_view("off_only"))
app.add_url_rule("/api/connection", view_func=Conection.as_view("connection"))
app.add_url_rule("/api/lightbulbs/all", view_func=AllLighbutlbs.as_view("lightbulbs_all"))
app.add_url_rule("/api/lightbulbs/<lightbulb_id>", view_func=SingleLightbulb.as_view("single_lightbulb"))

if __name__ == '__main__':
    controller.connect('broker.hivemq.com')
    controller.loop_start()
    app.run('127.0.0.1', 5000, debug=False)
    controller.loop_stop()
    controller.disconnect()
