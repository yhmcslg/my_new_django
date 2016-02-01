forms.py
#用户注册
class RegistrationForm(forms.Form):
    username = forms.CharField(label="用户名",max_length=30)
    email = forms.EmailField(label='电子邮件')
    password1 = forms.CharField(label='密码',widget=forms.PasswordInput())
    password2 = forms.CharField(label='确认密码',widget=forms.PasswordInput())
    pic = forms.ImageField(label="头像上传")
    def clean_username(self):
        '''验证用户输入的用户名的合法性'''
        username = self.cleaned_data['username']    
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('用户名中只能包含字母、数字和下划线')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('用户名已存在！')
    
    def clean_email(self):
        '''验证输入的电子邮件是否合法'''
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('该邮箱已注册！')
    
    def clean_password2(self):
        '''验证用户两次输入的密码一致性'''
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError('密码不匹配')
