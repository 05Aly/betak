from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

def validate_video_size(value):
    # Limit size to 10MB (10 * 1024 * 1024 bytes)
    filesize = value.size
    if filesize > 10 * 1024 * 1024:
        raise ValidationError("حجم الفيديو لا يمكن أن يتجاوز 10 ميجابايت.")

class CustomUser(AbstractUser):
    ACCOUNT_CHOICES = [
        ('seller', 'بائع (صاحب عقار)'),
        ('buyer', 'مشتري (باحث عن عقار)'),
    ]
    
    full_name = models.CharField(max_length=150, verbose_name="الاسم رباعي")
    phone_numbers = models.CharField(max_length=100, verbose_name="أرقام الهواتف")
    account_type = models.CharField(
        max_length=10, 
        choices=ACCOUNT_CHOICES, 
        default='buyer', 
        verbose_name="نوع الحساب"
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        verbose_name="الصورة الشخصية الإجبارية"
    )
    is_approved = models.BooleanField(default=False, verbose_name="موافق عليه من الإدارة")
    rejection_notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات الرفض من الإدارة")

    def __str__(self):
        return f"{self.full_name} ({self.get_account_type_display()})"

class Property(models.Model):
    owner = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='properties', 
        limit_choices_to={'account_type': 'seller'},
        verbose_name="صاحب العقار"
    )
    title = models.CharField(max_length=200, verbose_name="عنوان العقار (مثال: شقة للبيع بالهضبة الوسطى)")
    price = models.PositiveIntegerField(verbose_name="السعر (جنيه مصري)")
    address = models.CharField(max_length=300, verbose_name="العنوان بالتفصيل (المقطم - الهضبة)")
    description = models.TextField(verbose_name="الوصف التفصيلي للعقار")
    image = models.ImageField(upload_to='properties/', verbose_name="الصورة الرئيسية للعقار")
    video = models.FileField(
        upload_to='properties_videos/', 
        blank=True, 
        null=True, 
        validators=[validate_video_size], 
        verbose_name="فيديو للعقار (اختياري - بحد أقصى 10MB)"
    )
    waiting_list = models.BooleanField(default=True, verbose_name="في قائمة الانتظار (غير معتمد)")
    rejection_notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات الرفض من الإدارة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    class Meta:
        verbose_name = "عقار"
        verbose_name_plural = "العقارات"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.price} ج.م"
