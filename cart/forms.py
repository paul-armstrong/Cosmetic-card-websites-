from django import forms
from .models import Order
class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['first_name','last_name','company','email','phone','postal_code','address_line_1','address_line_2','country','state','city']
      
      



    def __init__(self,*args,**kwargs):
        super(OrderForm,self).__init__(*args,**kwargs)
        self.fields ['first_name'].widget.attrs['placeholder']='Enter first name'      
        self.fields ['last_name'].widget.attrs['placeholder']='Enter last name'      
        # self.fields ['email'].widget.attrs['placeholder']='Enter email Address'      
        self.fields ['phone'].widget.attrs['placeholder']='Enter phone number'      
        self.fields ['address_line_1'].widget.attrs['placeholder']='Enter address_line_1'      
        self.fields ['address_line_2'].widget.attrs['placeholder']='Enter address_line_2(optional) '      
        self.fields ['country'].widget.attrs['placeholder']='Enter country name'      
        self.fields ['state'].widget.attrs['placeholder']='Enter state'      
        self.fields ['city'].widget.attrs['placeholder']='Enter city'      
        # self.fields ['order_note'].widget.attrs['placeholder']='Enter order note'      
        
        for field in self.fields:
            self.fields [field].widget.attrs['class']='form-control'
      