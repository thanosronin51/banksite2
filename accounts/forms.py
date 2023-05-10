import datetime
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, AccountDetails, UserAddress


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "contact_no",
        ]


class AccountDetailsForm(forms.ModelForm):

    class Meta:
        model = AccountDetails
        fields = [

            'gender',
            'account_type',
            'picture'
 
            
        ]
        widgets = {
            'picture': forms.ClearableFileInput(attrs={'multiple': True}),
        }


class UserAddressForm(forms.ModelForm):
    COUNTRY_CHOICES = [
        ('', 'Select Country'),
        ('AF', 'Afghanistan'),
        ('AM', 'Armenia'),
        ('AZ', 'Azerbaijan'),
        ('BH', 'Bahrain'),
        ('BD', 'Bangladesh'),
        ('BT', 'Bhutan'),
        ('BN', 'Brunei'),
        ('KH', 'Cambodia'),
        ('CN', 'China'),
        ('CY', 'Cyprus'),
        ('TL', 'East Timor'),
        ('EG', 'Egypt'),
        ('GE', 'Georgia'),
        ('IN', 'India'),
        ('ID', 'Indonesia'),
        ('IR', 'Iran'),
        ('IQ', 'Iraq'),
        ('IL', 'Israel'),
        ('JP', 'Japan'),
        ('JO', 'Jordan'),
        ('KZ', 'Kazakhstan'),
        ('KW', 'Kuwait'),
        ('KG', 'Kyrgyzstan'),
        ('LA', 'Laos'),
        ('LB', 'Lebanon'),
        ('MY', 'Malaysia'),
        ('MV', 'Maldives'),
        ('MN', 'Mongolia'),
        ('MM', 'Myanmar'),
        ('NP', 'Nepal'),
        ('KP', 'North Korea'),
        ('OM', 'Oman'),
        ('PK', 'Pakistan'),
        ('PS', 'Palestine'),
        ('PH', 'Philippines'),
        ('QA', 'Qatar'),
        ('RU', 'Russia'),
        ('SA', 'Saudi Arabia'),
        ('SG', 'Singapore'),
        ('KR', 'South Korea'),
        ('LK', 'Sri Lanka'),
        ('SY', 'Syria'),
        ('TW', 'Taiwan'),
        ('TJ', 'Tajikistan'),
        ('TH', 'Thailand'),
        ('TR', 'Turkey'),
        ('TM', 'Turkmenistan'),
        ('AE', 'United Arab Emirates'),
        ('UZ', 'Uzbekistan'),
        ('VN', 'Vietnam'),
        ('YE', 'Yemen'),
        ('AG', 'Antigua and Barbuda'),
        ('AR', 'Argentina'),
        ('BS', 'Bahamas'),
        ('BB', 'Barbados'),
        ('BZ', 'Belize'),
        ('BO', 'Bolivia'),
        ('BR', 'Brazil'),
        ('CA', 'Canada'),
        ('CL', 'Chile'),
        ('CO', 'Colombia'),
        ('CR', 'Costa Rica'),
        ('CU', 'Cuba'),
        ('DM', 'Dominica'),
        ('DO', 'Dominican Republic'),
        ('EC', 'Ecuador'),
        ('SV', 'El Salvador'),
        ('GD', 'Grenada'),
        ('GT', 'Guatemala'),
        ('GY', 'Guyana'),
        ('HT', 'Haiti'),
        ('HN', 'Honduras'),
        ('JM', 'Jamaica'),
        ('MX', 'Mexico'),
        ('NI', 'Nicaragua'),
        ('PA', 'Panama'),
        ('PY', 'Paraguay'),
        ('PE', 'Peru'),
        ('KN', 'Saint Kitts and Nevis'),
        ('LC', 'Saint Lucia'),
        ('VC', 'Saint Vincent and the Grenadines'),
        ('SR', 'Suriname'),
        ('TT', 'Trinidad and Tobago'),
        ('US', 'United States'),
        ('UY', 'Uruguay'),
        ('VE', 'Venezuela'),
        ('AL', 'Albania'),
        ('DZ', 'Algeria'),
        ('AD', 'Andorra'),
        ('AO', 'Angola'),
        ('AM', 'Armenia'),
        ('AT', 'Austria'),
        ('AZ', 'Azerbaijan'),
        ('BH', 'Bahrain'),
        ('BY', 'Belarus'),
        ('BE', 'Belgium'),
        ('BJ', 'Benin'),
        ('BA', 'Bosnia and Herzegovina'),
        ('BW', 'Botswana'),
        ('BG', 'Bulgaria'),
        ('BF', 'Burkina Faso'),
        ('BI', 'Burundi'),
        ('CM', 'Cameroon'),
        ('CV', 'Cape Verde'),
        ('CF', 'Central African Republic'),
        ('TD', 'Chad'),
        ('KM', 'Comoros'),
        ('HR', 'Croatia'),
        ('CY', 'Cyprus'),
        ('CZ', 'Czech Republic'),
        ('DK', 'Denmark'),
        ('DJ', 'Djibouti'),
        ('EG', 'Egypt'),
        ('GQ', 'Equatorial Guinea'),
        ('ER', 'Eritrea'),
        ('EE', 'Estonia'),
        ('ET', 'Ethiopia'),
        ('FI', 'Finland'),
        ('FR', 'France'),
        ('GA', 'Gabon'),
        ('GM', 'Gambia'),
        ('GE', 'Georgia'),
        ('DE', 'Germany'),
        ('GH', 'Ghana'),
        ('GR', 'Greece'),
        ('GN', 'Guinea'),
        ('GW', 'Guinea-Bissau'),
        ('HU', 'Hungary'),
        ('IS', 'Iceland'),
        ('IE', 'Ireland'),
        ('IL', 'Israel'),
        ('IT', 'Italy'),
        ('CI', 'Ivory Coast'),
        ('JO', 'Jordan'),
        ('KZ', 'Kazakhstan'),
        ('KE', 'Kenya'),
        ('KW', 'Kuwait'),
        ('KG', 'Kyrgyzstan'),
        ('LV', 'Latvia'),
        ('LB', 'Lebanon'),
        ('LS', 'Lesotho'),
        ('LR', 'Liberia'),
        ('LY', 'Libya'),
        ('LI', 'Liechtenstein'),
        ('LT', 'Lithuania'),
        ('LU', 'Luxembourg'),
        ('MK', 'Macedonia'),
        ('MG', 'Madagascar'),
        ('MW', 'Malawi'),
        ('ML', 'Mali'),
        ('MT', 'Malta'),
        ('MR', 'Mauritania'),
        ('MU', 'Mauritius'),
        ('MD', 'Moldova'),
        ('MC', 'Monaco'),
        ('ME', 'Montenegro'),
        ('MA', 'Morocco'),
        ('MZ', 'Mozambique'),
        ('NA', 'Namibia'),
        ('NL', 'Netherlands'),
        ('NE', 'Niger'),
        ('NG', 'Nigeria'),
        ('NO', 'Norway'),
        ('OM', 'Oman'),
        ('PK', 'Pakistan'),
        ('PS', 'Palestinian Territory'),
        ('PL', 'Poland'),
        ('PT', 'Portugal'),
        ('QA', 'Qatar'),
        ('RO', 'Romania'),
    ]

    
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, label='Country', widget=forms.Select(attrs={'class': 'form-control'}))


    class Meta:
        model = UserAddress
        fields = [

            'postal_code',
            'country',
            'state',
            'street_address',
            'country',
            'religion',
        ]






class UserLoginForm(forms.Form):
    username = forms.CharField(label="Username/Email")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid login credentials")
            if not user.is_active:
                raise forms.ValidationError("This account is inactive.")

        return super(UserLoginForm, self).clean(*args, **kwargs)