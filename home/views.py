from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'home/index.html')


#for showing signup/login button for customer
def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'home/customerclick.html')

#for showing signup/login button for supervisor
def supervisorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'home/supervisorclick.html')


#for showing signup/login button for ADMIN(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


def customer_signup_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request,'home/customersignup.html',context=mydict)


def supervisor_signup_view(request):
    userForm=forms.supervisorUserForm()
    supervisorForm=forms.supervisorForm()
    mydict={'userForm':userForm,'supervisorForm':supervisorForm}
    if request.method=='POST':
        userForm=forms.supervisorUserForm(request.POST)
        supervisorForm=forms.supervisorForm(request.POST,request.FILES)
        if userForm.is_valid() and supervisorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            supervisor=supervisorForm.save(commit=False)
            supervisor.user=user
            supervisor.save()
            my_supervisor_group = Group.objects.get_or_create(name='supervisor')
            my_supervisor_group[0].user_set.add(user)
        return HttpResponseRedirect('supervisorlogin')
    return render(request,'home/supervisorignup.html',context=mydict)


#for checking user customer, supervisor or admin(by sumit)
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()
def is_supervisor(user):
    return user.groups.filter(name='supervisor').exists()


def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('customer-dashboard')
    elif is_supervisor(request.user):
        accountapproval=models.supervisor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('supervisor-dashboard')
        else:
            return render(request,'home/supervisor_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')



#============================================================================================
# ADMIN RELATED views start
#============================================================================================

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    dict={
    'total_customer':models.Customer.objects.all().count(),
    'total_supervisor':models.supervisor.objects.all().count(),
    'total_request':models.Request.objects.all().count(),
    'total_feedback':models.Feedback.objects.all().count(),
    'data':zip(customers,enquiry),
    }
    return render(request,'home/admin_dashboard.html',context=dict)


@login_required(login_url='adminlogin')
def admin_customer_view(request):
    return render(request,'home/admin_customer.html')

@login_required(login_url='adminlogin')
def admin_view_customer_view(request):
    customers=models.Customer.objects.all()
    return render(request,'home/admin_view_customer.html',{'customers':customers})


@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('admin-view-customer')


@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,request.FILES,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('admin-view-customer')
    return render(request,'home/update_customer.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_add_customer_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('/admin-view-customer')
    return render(request,'home/admin_add_customer.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_view_customer_enquiry_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    return render(request,'home/admin_view_customer_enquiry.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminlogin')
def admin_view_customer_invoice_view(request):
    enquiry=models.Request.objects.values('customer_id').annotate(Sum('cost'))
    print(enquiry)
    customers=[]
    for enq in enquiry:
        print(enq)
        customer=models.Customer.objects.get(id=enq['customer_id'])
        customers.append(customer)
    return render(request,'home/admin_view_customer_invoice.html',{'data':zip(customers,enquiry)})

@login_required(login_url='adminlogin')
def admin_supervisor_view(request):
    return render(request,'home/admin_supervisor.html')


@login_required(login_url='adminlogin')
def admin_approve_supervisor_view(request):
    supervisor=models.supervisor.objects.all().filter(status=False)
    return render(request,'home/admin_approve_supervisor.html',{'supervisor':supervisor})

@login_required(login_url='adminlogin')
def approve_supervisor_view(request,pk):
    supervisoralary=forms.supervisoralaryForm()
    if request.method=='POST':
        supervisoralary=forms.supervisoralaryForm(request.POST)
        if supervisoralary.is_valid():
            supervisor=models.supervisor.objects.get(id=pk)
            supervisor.salary=supervisoralary.cleaned_data['salary']
            supervisor.status=True
            supervisor.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-approve-supervisor')
    return render(request,'home/admin_approve_supervisor_details.html',{'supervisoralary':supervisoralary})


@login_required(login_url='adminlogin')
def delete_supervisor_view(request,pk):
    supervisor=models.supervisor.objects.get(id=pk)
    user=models.User.objects.get(id=supervisor.user_id)
    user.delete()
    supervisor.delete()
    return redirect('admin-approve-supervisor')


@login_required(login_url='adminlogin')
def admin_add_supervisor_view(request):
    userForm=forms.supervisorUserForm()
    supervisorForm=forms.supervisorForm()
    supervisoralary=forms.supervisoralaryForm()
    mydict={'userForm':userForm,'supervisorForm':supervisorForm,'supervisoralary':supervisoralary}
    if request.method=='POST':
        userForm=forms.supervisorUserForm(request.POST)
        supervisorForm=forms.supervisorForm(request.POST,request.FILES)
        supervisoralary=forms.supervisoralaryForm(request.POST)
        if userForm.is_valid() and supervisorForm.is_valid() and supervisoralary.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            supervisor=supervisorForm.save(commit=False)
            supervisor.user=user
            supervisor.status=True
            supervisor.salary=supervisoralary.cleaned_data['salary']
            supervisor.save()
            my_supervisor_group = Group.objects.get_or_create(name='supervisor')
            my_supervisor_group[0].user_set.add(user)
            return HttpResponseRedirect('admin-view-supervisor')
        else:
            print('problem in form')
    return render(request,'home/admin_add_supervisor.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_view_supervisor_view(request):
    supervisor=models.supervisor.objects.all()
    return render(request,'home/admin_view_supervisor.html',{'supervisor':supervisor})

"""
@login_required(login_url='adminlogin')
def delete_supervisor_view(request,pk):
    supervisor=models.supervisor.objects.get(id=pk)
    user=models.User.objects.get(id=supervisor.user_id)
    user.delete()
    supervisor.delete()
    return redirect('admin-view-supervisor') """


@login_required(login_url='adminlogin')
def update_supervisor_view(request,pk):
    supervisor=models.supervisor.objects.get(id=pk)
    user=models.User.objects.get(id=supervisor.user_id)
    userForm=forms.supervisorUserForm(instance=user)
    supervisorForm=forms.supervisorForm(request.FILES,instance=supervisor)
    mydict={'userForm':userForm,'supervisorForm':supervisorForm}
    if request.method=='POST':
        userForm=forms.supervisorUserForm(request.POST,instance=user)
        supervisorForm=forms.supervisorForm(request.POST,request.FILES,instance=supervisor)
        if userForm.is_valid() and supervisorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            supervisorForm.save()
            return redirect('admin-view-supervisor')
    return render(request,'home/update_supervisor.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_view_supervisor_salary_view(request):
    supervisor=models.supervisor.objects.all()
    return render(request,'home/admin_view_supervisor_salary.html',{'supervisor':supervisor})

@login_required(login_url='adminlogin')
def update_salary_view(request,pk):
    supervisoralary=forms.supervisoralaryForm()
    if request.method=='POST':
        supervisoralary=forms.supervisoralaryForm(request.POST)
        if supervisoralary.is_valid():
            supervisor=models.supervisor.objects.get(id=pk)
            supervisor.salary=supervisoralary.cleaned_data['salary']
            supervisor.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-supervisor-salary')
    return render(request,'home/admin_approve_supervisor_details.html',{'supervisoralary':supervisoralary})


@login_required(login_url='adminlogin')
def admin_request_view(request):
    return render(request,'home/admin_request.html')

@login_required(login_url='adminlogin')
def admin_view_request_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    return render(request,'home/admin_view_request.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminlogin')
def change_status_view(request,pk):
    adminenquiry=forms.AdminApproveRequestForm()
    if request.method=='POST':
        adminenquiry=forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.supervisor=adminenquiry.cleaned_data['supervisor']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status=adminenquiry.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-request')
    return render(request,'home/admin_approve_request_details.html',{'adminenquiry':adminenquiry})


@login_required(login_url='adminlogin')
def admin_delete_request_view(request,pk):
    requests=models.Request.objects.get(id=pk)
    requests.delete()
    return redirect('admin-view-request')



@login_required(login_url='adminlogin')
def admin_add_request_view(request):
    enquiry=forms.RequestForm()
    adminenquiry=forms.AdminRequestForm()
    mydict={'enquiry':enquiry,'adminenquiry':adminenquiry}
    if request.method=='POST':
        enquiry=forms.RequestForm(request.POST)
        adminenquiry=forms.AdminRequestForm(request.POST)
        if enquiry.is_valid() and adminenquiry.is_valid():
            enquiry_x=enquiry.save(commit=False)
            enquiry_x.customer=adminenquiry.cleaned_data['customer']
            enquiry_x.supervisor=adminenquiry.cleaned_data['supervisor']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status='Approved'
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('admin-view-request')
    return render(request,'home/admin_add_request.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_approve_request_view(request):
    enquiry=models.Request.objects.all().filter(status='Pending')
    return render(request,'home/admin_approve_request.html',{'enquiry':enquiry})

@login_required(login_url='adminlogin')
def approve_request_view(request,pk):
    adminenquiry=forms.AdminApproveRequestForm()
    if request.method=='POST':
        adminenquiry=forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.supervisor=adminenquiry.cleaned_data['supervisor']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status=adminenquiry.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-approve-request')
    return render(request,'home/admin_approve_request_details.html',{'adminenquiry':adminenquiry})




@login_required(login_url='adminlogin')
def admin_view_service_cost_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    print(customers)
    return render(request,'home/admin_view_service_cost.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminlogin')
def update_cost_view(request,pk):
    updateCostForm=forms.UpdateCostForm()
    if request.method=='POST':
        updateCostForm=forms.UpdateCostForm(request.POST)
        if updateCostForm.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.cost=updateCostForm.cleaned_data['cost']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-service-cost')
    return render(request,'home/update_cost.html',{'updateCostForm':updateCostForm})



@login_required(login_url='adminlogin')
def admin_supervisor_attendance_view(request):
    return render(request,'home/admin_supervisor_attendance.html')


@login_required(login_url='adminlogin')
def admin_take_attendance_view(request):
    supervisor=models.supervisor.objects.all().filter(status=True)
    aform=forms.AttendanceForm()
    if request.method=='POST':
        form=forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel=models.Attendance()
                
                AttendanceModel.date=date
                AttendanceModel.present_status=Attendances[i]
                print(supervisor[i].id)
                print(int(supervisor[i].id))
                supervisor=models.supervisor.objects.get(id=int(supervisor[i].id))
                AttendanceModel.supervisor=supervisor
                AttendanceModel.save()
            return redirect('admin-view-attendance')
        else:
            print('form invalid')
    return render(request,'home/admin_take_attendance.html',{'supervisor':supervisor,'aform':aform})

@login_required(login_url='adminlogin')
def admin_view_attendance_view(request):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            attendancedata=models.Attendance.objects.all().filter(date=date)
            supervisordata=models.supervisor.objects.all().filter(status=True)
            mylist=zip(attendancedata,supervisordata)
            return render(request,'home/admin_view_attendance_page.html',{'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'home/admin_view_attendance_ask_date.html',{'form':form})

@login_required(login_url='adminlogin')
def admin_report_view(request):
    reports=models.Request.objects.all().filter(Q(status="Repairing Done") | Q(status="Released"))
    dict={
        'reports':reports,
    }
    return render(request,'home/admin_report.html',context=dict)


@login_required(login_url='adminlogin')
def admin_feedback_view(request):
    feedback=models.Feedback.objects.all().order_by('-id')
    return render(request,'home/admin_feedback.html',{'feedback':feedback})

#============================================================================================
# ADMIN RELATED views END
#============================================================================================


#============================================================================================
# CUSTOMER RELATED views start
#============================================================================================

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_dashboard_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    work_in_progress=models.Request.objects.all().filter(customer_id=customer.id,status='Repairing').count()
    work_completed=models.Request.objects.all().filter(customer_id=customer.id).filter(Q(status="Repairing Done") | Q(status="Released")).count()
    new_request_made=models.Request.objects.all().filter(customer_id=customer.id).filter(Q(status="Pending") | Q(status="Approved")).count()
    bill=models.Request.objects.all().filter(customer_id=customer.id).filter(Q(status="Repairing Done") | Q(status="Released")).aggregate(Sum('cost'))
    print(bill)
    dict={
    'work_in_progress':work_in_progress,
    'work_completed':work_completed,
    'new_request_made':new_request_made,
    'bill':bill['cost__sum'],
    'customer':customer,
    }
    return render(request,'home/customer_dashboard.html',context=dict)


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'home/customer_request.html',{'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id , status="Pending")
    return render(request,'home/customer_view_request.html',{'customer':customer,'enquiries':enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_delete_request_view(request,pk):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiry=models.Request.objects.get(id=pk)
    enquiry.delete()
    return redirect('customer-view-request')

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_approved_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'home/customer_view_approved_request.html',{'customer':customer,'enquiries':enquiries})

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_approved_request_invoice_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'home/customer_view_approved_request_invoice.html',{'customer':customer,'enquiries':enquiries})



@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_add_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiry=forms.RequestForm()
    if request.method=='POST':
        enquiry=forms.RequestForm(request.POST)
        if enquiry.is_valid():
            customer=models.Customer.objects.get(user_id=request.user.id)
            enquiry_x=enquiry.save(commit=False)
            enquiry_x.customer=customer
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('customer-dashboard')
    return render(request,'home/customer_add_request.html',{'enquiry':enquiry,'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'home/customer_profile.html',{'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def edit_customer_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm,'customer':customer}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('customer-profile')
    return render(request,'home/edit_customer_profile.html',context=mydict)


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_invoice_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'home/customer_invoice.html',{'customer':customer,'enquiries':enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_feedback_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    feedback=forms.FeedbackForm()
    if request.method=='POST':
        feedback=forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request,'home/feedback_sent_by_customer.html',{'customer':customer})
    return render(request,'home/customer_feedback.html',{'feedback':feedback,'customer':customer})
#============================================================================================
# CUSTOMER RELATED views END
#============================================================================================






#============================================================================================
# supervisor RELATED views start
#============================================================================================


@login_required(login_url='supervisorlogin')
@user_passes_test(is_supervisor)
def supervisor_dashboard_view(request):
    supervisor=models.supervisor.objects.get(user_id=request.user.id)
    work_in_progress=models.Request.objects.all().filter(supervisor_id=supervisor.id,status='Repairing').count()
    work_completed=models.Request.objects.all().filter(supervisor_id=supervisor.id,status='Repairing Done').count()
    new_work_assigned=models.Request.objects.all().filter(supervisor_id=supervisor.id,status='Approved').count()
    dict={
    'work_in_progress':work_in_progress,
    'work_completed':work_completed,
    'new_work_assigned':new_work_assigned,
    'salary':supervisor.salary,
    'supervisor':supervisor,
    }
    return render(request,'home/supervisor_dashboard.html',context=dict)

@login_required(login_url='supervisorlogin')
@user_passes_test(is_supervisor)
def supervisor_work_assigned_view(request):
    supervisor=models.supervisor.objects.get(user_id=request.user.id)
    works=models.Request.objects.all().filter(supervisor_id=supervisor.id)
    return render(request,'home/supervisor_work_assigned.html',{'works':works,'supervisor':supervisor})


@login_required(login_url='supervisorlogin')
@user_passes_test(is_supervisor)
def supervisor_update_status_view(request,pk):
    supervisor=models.supervisor.objects.get(user_id=request.user.id)
    updateStatus=forms.supervisorUpdateStatusForm()
    if request.method=='POST':
        updateStatus=forms.supervisorUpdateStatusForm(request.POST)
        if updateStatus.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.status=updateStatus.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/supervisor-work-assigned')
    return render(request,'home/supervisor_update_status.html',{'updateStatus':updateStatus,'supervisor':supervisor})

@login_required(login_url='supervisorlogin')
@user_passes_test(is_supervisor)
def supervisor_attendance_view(request):
    supervisor=models.supervisor.objects.get(user_id=request.user.id)
    attendaces=models.Attendance.objects.all().filter(supervisor=supervisor)
    return render(request,'home/supervisor_view_attendance.html',{'attendaces':attendaces,'supervisor':supervisor})





@login_required(login_url='supervisorlogin')
@user_passes_test(is_supervisor)
def supervisor_feedback_view(request):
    supervisor=models.supervisor.objects.get(user_id=request.user.id)
    feedback=forms.FeedbackForm()
    if request.method=='POST':
        feedback=forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request,'home/feedback_sent.html',{'supervisor':supervisor})
    return render(request,'home/supervisor_feedback.html',{'feedback':feedback,'supervisor':supervisor})

@login_required(login_url='supervisorlogin')
@user_passes_test(is_supervisor)
def supervisor_salary_view(request):
    supervisor=models.supervisor.objects.get(user_id=request.user.id)
    workdone=models.Request.objects.all().filter(supervisor_id=supervisor.id).filter(Q(status="Repairing Done") | Q(status="Released"))
    return render(request,'home/supervisor_salary.html',{'workdone':workdone,'supervisor':supervisor})

@login_required(login_url='supervisorlogin')
@user_passes_test(is_supervisor)
def supervisor_profile_view(request):
    supervisor=models.supervisor.objects.get(user_id=request.user.id)
    return render(request,'home/supervisor_profile.html',{'supervisor':supervisor})

@login_required(login_url='supervisorlogin')
@user_passes_test(is_supervisor)
def edit_supervisor_profile_view(request):
    supervisor=models.supervisor.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=supervisor.user_id)
    userForm=forms.supervisorUserForm(instance=user)
    supervisorForm=forms.supervisorForm(request.FILES,instance=supervisor)
    mydict={'userForm':userForm,'supervisorForm':supervisorForm,'supervisor':supervisor}
    if request.method=='POST':
        userForm=forms.supervisorUserForm(request.POST,instance=user)
        supervisorForm=forms.supervisorForm(request.POST,request.FILES,instance=supervisor)
        if userForm.is_valid() and supervisorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            supervisorForm.save()
            return redirect('supervisor-profile')
    return render(request,'home/edit_supervisor_profile.html',context=mydict)






#============================================================================================
# supervisor RELATED views start
#============================================================================================




# for aboutus and contact
def aboutus_view(request):
    return render(request,'home/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'home/contactussuccess.html')
    return render(request, 'home/contactus.html', {'form':sub})
