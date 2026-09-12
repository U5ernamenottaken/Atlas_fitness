import psycopg2
conn = psycopg2.connect(host='localhost',port=5432,user='postgres'
                        ,password='pa55word',dbname='atlas_fitness')

cur = conn.cursor()

#read operations
#getting all users
def get_users():
    cur.execute("Select * from users")
    users = cur.fetchall()
    return users
see_users=get_users()
#print(see_users)
#getting all members
def get_members():
    cur.execute("select*from members")
    members = cur.fetchall()
    return members

#fetching expired memberships
def get_expired_memberships():
    cur.execute("select*from memberships where end_date>current_date")
    expired_memberships = cur.fetchall()
    return expired_memberships

#fetching active memberships
def get_active_memberships():
    cur.execute("select*from memberships where end_date>=current_date")
    active_memberships = cur.fetchall()
    return active_memberships

#fetching today's payments
def get_payments_today():
    cur.execute("select*from payments where created_at >= current_date and created_at< current_date + interval '1 day'")
    payments_today = cur.fetchall()
    return payments_today

#fetching today's check_ins 
def get_check_in_today():
    cur.execute("select* from attendance where check_in >=current_date and check_in <current_date")
    check_ins_today = cur.fetchall()
    return check_ins_today

#fetching today's check_outs
def get_check_outs_today():
    cur.execute("select*from attendance where check_out >= current_date and check_out < current_date")
    check_outs_today = cur.fetchall()
    return check_outs_today

#fetch member by ID
def get_member_by_userid(userid):
    cur.execute("select * from members where userid=%s",(userid,))
    member_by_id = cur.fetchone()
    return member_by_id
member_info = get_member_by_userid(7)
#print(member_info)
#fetch member's trainer
def get_member_trainer(memberid):
    cur.execute("select trainerid, memberid from trainer_assignments where memberid=%s",(memberid,))
    member_trainer = cur.fetchone()
    return member_trainer

#fetch all payments
def get_payments():
    cur.execute("select*from payments")
    payments = cur.fetchall()
    return payments

pays=get_payments()
#print(pays)
#fetch payments for a user
def get_payments_by_userid(userid):
    cur.execute("select*from payments where userid=%s",(userid,))
    payments_by_userid = cur.fetchone()
    return payments_by_userid
user_pay = get_payments_by_userid(3)
#print(user_pay[1])
#fetch trainers
def get_trainers():
     cur.execute("select *from trainers join users on trainers.userid=users.user_id")
     trainers=cur.fetchall()
     return trainers
trainer_lst = get_trainers()
#print(trainer_lst)
#fetch today's revenue
def get_revenue_today():
    cur.execute("select sum(amount) from payments where created_at=current_date")
    revenue_today = cur.fetchall()
    return revenue_today

#fetch month's revenue
def get_revenue_by_month():
    cur.execute("select sum(amount),date_trunc('month',created_at) as month from payments group by month order by month")
    revenue_month= cur.fetchall()
    return revenue_month

#fetch member's check_ins
def get_member_check_ins(memberid):
        cur.execute("select*from attendance where check_in >= current_date and check_in < current_date and memberid=%s",(memberid,))
        member_check_ins = cur.fetchall()
        return member_check_ins

#fetch member's check_outs
def get_member_check_outs(memberid):
        cur.execute("select*from attendance where check_out >= current_date and check_out < current_date and memberid=%s",(memberid))
        member_check_outs = cur.fetchall()
        return member_check_outs

#fetch attendance per date
def get_attendance_per_date():
     cur.execute("select count(*),date_trunc('day',check_out) from attendance group by date_trunc('day',check_out) ")
     attendance_per_day = cur.fetchall()
     return attendance_per_day

#fetch member progress
def get_member_progress(memberid):
     cur.execute("select*from progress where memberid=%s",(memberid))
     member_progress=cur.fetchone()
     return member_progress

#fetch member program 
def get_member_program(memberid):
     cur.execute("select program_title,program_description from programs where memberid=%s",(memberid,))
     member_program=cur.fetchone()
     return member_program


#write operations

#create user
def insert_user(user_details):
     cur.execute("insert into users(first_name,last_name,email,password,phone_number)values(%s,%s,%s,%s,%s)",user_details)
     conn.commit()
user1=('User','One','userone@gmail.com','subject1','0712345678')
user2=('User','Two','usertwo@gmail.com','subject2','0709876543')
user3=('user','three','userthree@gmail.com','subject3','0711234567')
#insert_user(user1)
#insert_user(user2)
#insert_user(user3)
users=get_users()
#print(users)

       
#create member
def insert_member(member_details):
     cur.execute("insert into members(userid,height,weight,gender,dob,goal)values(%s,%s,%s,%s,%s,%s)",member_details)
     conn.commit()

member_details=(3,170,65,'Male','2005-12-10','Building muscle and increasing mobility')
#insert_member(member_details)
members=get_members()
#print(members)
#update member
def update_member(details_update):
     cur.execute("update members set height=%s,weight=%s,gender=%s,dob=%s,goal=%s where userid=%s",details_update)
     conn.commit()

#create membership
def insert_membership(paymentid):
     cur.execute("insert into memberships(payment_id)values(%s)",paymentid)
     conn.commit()
payment_one=(1,)
#insert_membership(payment_one)
memberships=get_active_memberships()
#print(memberships)
#update membership
def update_membership(paymentid,membershipid):
     cur.execute("update memberships set paymentid=%s where membershipid=%s",(paymentid,membershipid))
     conn.commit()

#create payment
def insert_payment(payment_details):
     cur.execute("insert into payments(userid,means,amount)values(%s,%s,%s)returning paymentid",payment_details)
     paymentid=cur.fetchone()[0]
     conn.commit()
     return paymentid

payment1=(3,'Mpesa',7000)
#insert_payment(payment1)
payments=get_payments()
#print(payments)

#create attendance check_in
def insert_attendance_in(memberid):
     cur.execute("insert into(memberid)values(%s)",memberid)
     conn.commit()

#update attendance check out
def update_attendance_check_out(memberid):
     cur.execute("update attendance set check_out=current_timestamp where memberid=%s",(memberid,))
     conn.commit()

#insert trainer
def insert_trainer(trainer_details):
     cur.execute("insert into trainers(userid,specialization,bio,years_of_experience)values(%s,%s,%s,%s)",trainer_details)
     conn.commit()

trainer_one=(2,'Bodybuilding and mobility','Two is an experienced trainer who believes in building muscle while maintaining flexibility and long term joint health',15)
#insert_trainer(trainer_one)
trainers=get_trainers()
#print(trainers)

#assign trainer
def assign_trainer(assignment_details):
     cur.execute("insert into trainer_assignments(trainer_id,memberid)values(%s,%s)",assignment_details)
     conn.commit()

assignment_one=(1,1)
#assign_trainer(assignment_one)


#insert progress
def insert_progress(memberid,chest,arms,body_fat_percentage,thighs,waist):
     cur.execute("insert into progress(memberid,chest,arms,body_fat_percentage,thighs,waist)values(%s,%s,%s,%s,%s,%s,%s)",(memberid,chest,arms,body_fat_percentage,thighs,waist))
     conn.commit()

#create programs
def create_program(program_details):
     cur.execute("insert into programs(trainer_id,memberid,program_title,program_description)values(%s,%s,%s,%s)",program_details)
     conn.commit()

program_details=(1,1,'Mobility & Muscle Builder','A balanced training program combining resistance exercises for muscle growth with mobility work to improve range of motion, flexibility, and movement control.')
#create_program(program_details)
program=get_member_program(1)
#print(program)

#update program
def update_program(memberid,program_title,program_description):
     cur.execute("update programs set program_title=%s,program_description=%s where memberid=%s",(program_title,program_description,memberid))
     conn.commit()

def check_user_email(email):
     cur.execute("select*from users where email=%s",(email,))
     user=cur.fetchone()
     return user

def check_user_membership(userid):
     cur.execute("select*from memberships inner join payments on memberships.payment_id=payments.paymentid where end_date>=current_date and userid=%s",(userid,))
     status=cur.fetchone()
     return status

state=check_user_membership(3)
#print(state)

def check_member(userid):
     cur.execute("select *from members where userid=%s",(userid,))
     member=cur.fetchone()
     return member

#state_member=check_member(3)
#print(state_member)

def check_trainer(userid):
     cur.execute("select*from trainers where userid=%s",(userid,))
     trainer = cur.fetchone()
     return trainer

chck=check_trainer(10)
#print(chck)

def check_member_trainer(memberid):
     cur.execute("""select*from members left join trainer_assignments on members.memberid=trainer_assignments.memberid 
     where members.memberid=%s 
     order by assignmentid desc limit 1""",(memberid,))
     member_trainer= cur.fetchone()
     return member_trainer

def check_assigned_members(trainerid):
     cur.execute("select count(*) from trainer_assignments where trainer_id=%s",(trainerid,))
     client_count = cur.fetchall()
     return client_count

def get_trainer_info(trainerid):
     cur.execute("select*from trainers join users on trainers.userid=users.user_id join trainer_assignments on trainers.trainerid = trainer_assignments.trainer_id where trainerid=%s",(trainerid,))
     trainer_info=cur.fetchone()
     return trainer_info

def get_trainer_clients(trainer_id):
     cur.execute("""
     select*from trainer_assignments 
     left join members on members.memberid=trainer_assignments.memberid 
     join users on users.user_id=members.userid
     where trainer_id=%s 
     row nmbe()(
     partion by memberid
     order by assignment_date desc 
     )
                     """,(trainer_id))
     trainer_clients = cur.fetchall()
     return trainer_clients

def get_trainer_by_userid(userid):
     cur.execute("""
     select trainerid from trainers where userid=%s
               """,(userid,))
     trainerid= cur.fetchone()
     return trainerid



