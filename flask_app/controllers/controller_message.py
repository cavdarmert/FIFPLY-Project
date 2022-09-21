from flask_app import app, bcrypt
from flask import render_template, redirect, request, session, flash
from flask_app.models.model_post import Post
#MAY NOT NEED BELOW, WILL CHECK LATER !!!
from flask_app.models.model_user import User

from flask_app.models.model_message import Message

@app.route("/messages/new/<int:receiver_id>")
def new_message(receiver_id):
    if 'id' not in session:
        flash('Plesae login before trying to go to send a message')
        return redirect('/')
    user = User.get_one_by_id(int(session['id']))
    return render_template("new_message.html", user=user, rec_id = receiver_id)

@app.route('/messages/create', methods=['POST'])
def create_message():
    if not Message.is_valid(request.form):
        return redirect('/messages/new')
    #CREATING A MESSAGE BELOW
    data = {
        **request.form,
        'sender_id': session['id']
    }
    Message.save_message(data)
    return redirect('/dashboard')

@app.route('/inbox')
def inbox():
    if 'id' not in session:
        flash('Please login before going to inbox!')
        return redirect ('/')
    data = {
        **request.form,
        'sender_id': session['id']
    }
    user = User.get_one_by_id(int(session['id'])) 
    ##FRI 11:50AM, BELOW message will change there will be for loop
    # receiver_messages = []
    # messages = Message.get_all_messages()
    # for i in messages:
    #     if i.receiver_id not in receiver_messages:
    #         receiver_messages.append(i)





    
    ##FRI 11:50AM, BELOW message will change
    return render_template('inbox.html', user=user, messages = Message.get_all_messages())

@app.route('/messages/<int:id>/view')
def show_one_message(id):
    if 'id' not in session:
        flash('Please login first!')
        return redirect('/')
    data = {'id':id}
    message = Message.get_one_message_by_id(data)
    user = Message.get_one_message_by_id({'id': session['id']})
    return render_template("show_message.html", message=message, user=user)

@app.route('/messages/chatbox/<int:sender_id>')
def show_chatbox(sender_id):
    messages = User.get_user_with_messages_recived({'id': session['id']})
    connected_messages = []
    for message in messages:
        if sender_id ==  message.sender.id:
            connected_messages.append(message)
        
    return render_template("chat_window.html", messages = connected_messages, user = User.get_one_by_id(int(session['id']))
)
