from flask import Flask,redirect,render_template,request,url_for,flash,session
from database_atlas import check_user_email,insert_user,get_payments_by_userid,check_user_membership,insert_payment,insert_membership,check_member,insert_member,get_member_by_userid,update_member
from flask_bcrypt import Bcrypt
atlas=Flask(__name__)
bcrypt = Bcrypt(atlas)
atlas.secret_key = "ulijkadhvkyuQHD89Q2EUWO0QIERW7UE8YQ92398URFH"

@atlas.route("/")
def home():
    return render_template('home.html')


@atlas.route("/dashboard")
def dashboard():
  user_id = session['user_id']
  member_info = get_member_by_userid(user_id)

  return render_template('dashboard.html',member_info=member_info)

@atlas.route("/trainers")
def trainers():
   return render_template('trainers.html')

@atlas.route("/register",methods=['GET','POST'])
def register():
   if request.method == 'POST':
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email_address']
    password = request.form['password']
    phone_number = request.form['phone_number']

    existing_user=check_user_email(email)
    if not existing_user:
       hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
       new_user = (first_name,last_name,email,hashed_password,phone_number)
       insert_user(new_user)
       flash('User account registered successfully','success')
       return redirect(url_for('login'))

    else:
       flash('User already exists login instead','danger')
  
   return render_template('register.html')

@atlas.route("/login",methods=['POST','GET'])
def login():
   if request.method=='POST':
      email=request.form['email_address']
      password=request.form['password']

      user_exist=check_user_email(email)
      if user_exist:
         if bcrypt.check_password_hash(user_exist[4],password):
            session['email']=email
            session['user_id']=user_exist[0]
            session['first_name'] = user_exist[1]
            flash(f'Login successful,{user_exist[1]} ','success')
            return redirect(url_for('dashboard'))
         else:
            flash('Incorrect details','danger')       
      else:
        flash('User not registered','warning')
   return render_template('login.html')

@atlas.route("/logout")
def logout():
   first_name = session['first_name']
   session.pop('user_id',None)
   flash(f'{first_name} successfully logged out','success')
   return redirect(url_for('login'))



@atlas.route("/create_membership",methods=['POST','GET'])
def create_membership():
 if request.method == 'POST':
    userid = session['user_id']
    amount = request.form['amount']
    means = request.form['means']
    paymentid = get_payments_by_userid(userid)
    existing_membership = check_user_membership(userid)

    if not existing_membership:
       payment_details=(userid,means,amount)
       new_payment = insert_payment(payment_details)
       membership_details = (new_payment,)
       new_membership=insert_membership(membership_details)
       flash('New membership obtained successfully','success')
       return redirect(url_for('dashboard'))
    else:
       flash('Membership already exists','danger')
       return redirect(url_for('dashboard'))


@atlas.route('/member_profile',methods=['POST','GET'])
def member_profile():
   if request.method == 'POST':
     userid = session['user_id']
     height = request.form['height']
     weight = request.form['weight']
     gender = request.form['gender']
     dob = request.form['date_of_birth']
     goal = request.form['goal']

     

     member_exist = check_member(userid)
     if not member_exist:
        member_details = (userid,height,weight,gender,dob,goal)
        insert_member(member_details)
        flash("Member profile created successfully",'success')
        return redirect(url_for('dashboard'))
     else:
        flash("Member already exists",'danger')

   return render_template('member_profile.html',height=height)



@atlas.route('/edit_profile',methods=['POST','GET'])
def edit_profile():
   if request.method == 'POST':
      userid = session['user_id']
      height = request.form['height']
      weight = request.form['weight']
      gender = request.form['gender']
      dob = request.form['date_of_birth']
      goal = request.form['goal']

      member_info = get_member_by_userid(userid)
      details_update = (height,weight,gender,dob,goal,userid)
      update_member(details_update)
      flash('Member profile updated successfully','success')
      
      return redirect(url_for('dashboard'))




@atlas.route("/test-id")
def test_id():
    user_id = session["user_id"]
    return render_template('test.html',user_id=user_id)

atlas.run(debug=True)