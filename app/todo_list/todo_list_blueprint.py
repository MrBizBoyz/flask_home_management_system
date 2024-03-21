from flask import redirect
from flask import url_for
from flask import render_template
from flask import request
from ..models import Item
import datetime

from flask import Blueprint

todo_list_blueprint = Blueprint('todo_list_blueprint', __name__, template_folder='templates', static_folder='static')




@todo_list_blueprint.route('/')
def index():
    # return "<h1>Todo List</h1>"
    return render_template('show_items.html', items=Item.query.order_by(Item.item_priority).all())



@todo_list_blueprint.route('/add-new-item-form', methods = ['GET', 'POST'])
def add_new_item_form():

    id = request.args.get('_id')
    if id:
        return render_template('add_new_item_form.html', item=Item.query.get(id))
    else:
        return render_template('add_new_item_form.html')


@todo_list_blueprint.route('/add-new-item', methods = ['GET', 'POST'])
def add_new_item():
    form_data = request.form.to_dict(flat=False)
    item = None
    if "_id" in form_data.keys():
        item = Item.query.get(form_data["_id"][0])

        item.item_name = form_data["item_name"][0]
        item.item_notes = form_data["item_notes"][0]
    else:
        form_data.pop('_id', None)
        item = Item(form_data)

    db.session.add(item)
    db.session.commit()
    return redirect("/")


@todo_list_blueprint.route('/delete-item', methods = ['GET'])
def delete_item():
    args = request.args
    Item.query.filter_by(_id=args.get("_id")).delete()
    db.session.commit()
    return redirect("/")


@todo_list_blueprint.route('/toggle-completed', methods = ['GET'])
def toggle_completed():
    id = request.args.get('_id')
    item=Item.query.get(id)
    checked = request.args.get('checked')

    if checked == "true":
        item.item_completed = True
    else:
        item.item_completed = False
    db.session.commit()
    return redirect("/")



@todo_list_blueprint.route('/change-item-priority-up', methods = ['GET'])
def change_item_priority_up():
    item_id = request.args.get('_id', type=int)

    item_to_move = Item.query.get(item_id)
    item_to_swap = Item.query.get(item_id - 1)
    if item_to_move and item_to_swap:
        item_to_move.item_priority, item_to_swap.item_priority = item_to_swap.item_priority, item_to_move.item_priority
        db.session.commit()
    return redirect(url_for('index'))


@todo_list_blueprint.route('/change-item-priority-down', methods = ['GET'])
def change_item_priority_down():
    item_id = request.args.get('_id', type=int)

    item_to_move = Item.query.get(item_id)
    item_to_swap = Item.query.get(item_id + 1)
    if item_to_move and item_to_swap:
        item_to_move.item_priority, item_to_swap.item_priority = item_to_swap.item_priority, item_to_move.item_priority
        db.session.commit()
    return redirect(url_for('index'))
